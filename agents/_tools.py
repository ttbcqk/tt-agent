"""
Agent Tools — 出行决策 Agent 的工具集（私有模块，不映射为路由）

工具：
  1. search_nearby_malls  — 按位置和偏好搜索附近商场（高德地图，失败自动降级为内置示例数据）
  2. get_mall_details     — 查询某个商场详情（品牌、餐饮、适合场景）
  3. plan_trip            — 结合偏好生成出行建议与待用户手动确认的事项

设计说明：
  - 若配置了 AMAP_API_KEY，search_nearby_malls 会调用高德地图 Web 服务 API 获取真实 POI；
  - 若未配置或调用失败，自动使用内置示例数据，保证 Agent 在没有密钥时也能完整演示。
"""

import json
import os
import re
from typing import Annotated

import httpx
from agents import function_tool


# ========== 内置示例数据（无高德 Key 时的兜底，保证可演示） ==========
DEMO_MALLS = [
    {
        "name": "静安嘉里中心",
        "district": "静安区",
        "distance_km": 1.2,
        "brands": ["Gucci", "Dior", "Apple Store", "lululemon", "蓝瓶咖啡"],
        "scenes": ["情侣约会", "轻奢购物", "网红打卡"],
        "dining": ["鼎泰丰", "蓝瓶咖啡", "Bistro", "日料"],
        "highlight": "高端品牌与网红咖啡聚集，环境安静适合约会与拍照",
    },
    {
        "name": "兴业太古汇",
        "district": "静安区",
        "distance_km": 1.8,
        "brands": ["LV", "Dior", "星巴克臻选烘焙工坊", "Supreme", "Apple Store"],
        "scenes": ["情侣约会", "潮流购物", "下午茶"],
        "dining": ["星巴克臻选", "甬府", "Powder", "甜品店"],
        "highlight": "有全球最大星巴克烘焙工坊，潮流与餐饮选择丰富",
    },
    {
        "name": "静安大悦城",
        "district": "静安区",
        "distance_km": 2.4,
        "brands": ["泡泡玛特", "喜茶", "UR", "优衣库", "网红餐饮"],
        "scenes": ["年轻潮流", "情侣约会", "动漫二次元"],
        "dining": ["喜茶", "网红火锅", "甜品", "轻食"],
        "highlight": "年轻潮流地标，摩天轮与网红店多，适合拍照打卡",
    },
    {
        "name": "上海恒隆广场",
        "district": "静安区",
        "distance_km": 2.1,
        "brands": ["Hermès", "Chanel", "Cartier", "LV", "Dior"],
        "scenes": ["高端购物", "奢侈品", "品质约会"],
        "dining": ["米其林餐厅", "法餐", "下午茶"],
        "highlight": "顶级奢侈品商场，适合品质购物与正式约会",
    },
    {
        "name": "芮欧百货",
        "district": "静安区",
        "distance_km": 1.5,
        "brands": ["小众设计师品牌", "买手店", "精品咖啡", "生活方式"],
        "scenes": ["文艺小众", "情侣约会", "生活方式"],
        "dining": ["精品咖啡", "brunch", "西餐"],
        "highlight": "文艺小众路线，买手店与精品咖啡多，适合安静约会",
    },
]

# 常见地标 → 经纬度（无高德 Key 时用于估算距离/展示位置）
LANDMARK_COORDS = {
    "静安寺": "121.445309,31.223402",
    "人民广场": "121.473701,31.230416",
    "外滩": "121.490317,31.240570",
    "南京西路": "121.456800,31.228600",
}

# 品牌/场景关键词 → 商场名的打分权重（演示用简单匹配）
def _score_mall(mall: dict, preference: str) -> int:
    if not preference:
        return 0
    text = json.dumps(mall, ensure_ascii=False)
    score = 0
    for kw in re.findall(r"[\u4e00-\u9fa5A-Za-z]{2,}", preference):
        if kw in text:
            score += 3
    for scene in mall["scenes"]:
        if scene in preference:
            score += 5
    for brand in mall["brands"]:
        if brand.lower() in preference.lower():
            score += 4
    return score


# ========== 工具 1：搜索附近商场 ==========
@function_tool
def search_nearby_malls(
    location: Annotated[str, "用户当前位置或想搜索的地点，如'上海静安寺'"],
    preference: Annotated[str, "用户的品牌或场景偏好，如'情侣约会、有咖啡和轻奢品牌'；没有就传空字符串"],
    radius_meters: Annotated[int, "搜索半径（米），默认3000"] = 3000,
) -> str:
    """搜索指定地点附近的商场。优先用高德地图真实数据；无密钥或失败时用内置示例数据。"""
    amap_key = os.getenv("AMAP_API_KEY", "").strip()
    real_data = None

    if amap_key:
        try:
            # 用高德地理编码把地点转成经纬度
            geo = httpx.get(
                "https://restapi.amap.com/v3/geocode/geo",
                params={"address": location, "key": amap_key},
                timeout=10,
            ).json()
            location_str = ""
            if geo.get("geocodes"):
                location_str = geo["geocodes"][0].get("location", "")

            if location_str:
                poi = httpx.get(
                    "https://restapi.amap.com/v3/place/around",
                    params={
                        "key": amap_key,
                        "location": location_str,
                        "keywords": "商场|购物中心",
                        "radius": radius_meters,
                        "offset": 20,
                        "extensions": "all",
                    },
                    timeout=10,
                ).json()
                pois = poi.get("pois") or []
                real_data = [
                    {
                        "name": p.get("name"),
                        "address": p.get("address"),
                        "distance_meters": p.get("distance"),
                        "biz_type": p.get("biz_type"),
                    }
                    for p in pois[:10]
                ]
        except Exception as e:  # 任何异常都降级到示例数据，保证可用
            real_data = None

    if real_data:
        return json.dumps(
            {"source": "高德地图", "location": location, "malls": real_data},
            ensure_ascii=False,
        )

    # 降级：内置示例数据 + 按偏好打分排序
    ranked = sorted(DEMO_MALLS, key=lambda m: _score_mall(m, preference), reverse=True)
    result = {
        "source": "示例数据（未配置高德 Key）",
        "location": location,
        "hint": "以下为内置示例商场，演示用；配置 AMAP_API_KEY 后自动切换为真实地图数据。",
        "malls": ranked,
    }
    return json.dumps(result, ensure_ascii=False)


# ========== 工具 2：查询商场详情 ==========
@function_tool
def get_mall_details(
    mall_name: Annotated[str, "要查询的商场名称"],
) -> str:
    """查询某个商场的品牌、餐饮、适合场景等详情。"""
    for mall in DEMO_MALLS:
        if mall["name"] in mall_name or mall_name in mall["name"]:
            return json.dumps({"found": True, "mall": mall}, ensure_ascii=False)
    return json.dumps(
        {
            "found": False,
            "message": f"示例数据中没有「{mall_name}」的详情，可让用户提供更具体的商场名称，或用 search_nearby_malls 重新搜索。",
        },
        ensure_ascii=False,
    )


# ========== 工具 3：生成出行建议 ==========
@function_tool
def plan_trip(
    location: Annotated[str, "出发地"],
    destination: Annotated[str, "目的商场名称"],
    preference: Annotated[str, "用户偏好与限制，如'预算200元、2小时内、情侣约会'"],
) -> str:
    """生成出行建议，并列出需要用户手动确认的事项（不代下单/付款/预订）。"""
    return json.dumps(
        {
            "from": location,
            "to": destination,
            "preference": preference,
            "suggestion": (
                f"建议从「{location}」前往「{destination}」。"
                "优先选择地铁或步行，具体路线与耗时请以实时地图为准。"
            ),
            "manual_confirmations": [
                "确认商场当日营业时间与是否临时闭店",
                "确认心仪品牌/餐厅是否排队或需要提前预约",
                "确认交通实时路况与末班车时间",
                "到店后自行完成点单、购买、付款等操作（Agent 不代下单/付款）",
            ],
        },
        ensure_ascii=False,
    )
