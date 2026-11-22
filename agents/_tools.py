"""
Agent Tools — AI 面试教练工具集（私有模块，不映射为路由）

工具：
  1. generate_question  — 按岗位与轮次生成面试问题（内置题库，无外部依赖）
  2. evaluate_answer    — 按四个维度点评用户回答并给分
  3. final_report       — 汇总多轮表现，生成综合面试报告

设计说明：
  - 全部数据内置，无需任何 API Key，保证演示随时可用。
  - 题库覆盖前端 / 后端 / 产品经理 / 数据分析 / 通用，以及行为面试题与收尾反问。
"""

import json
import re
from typing import Annotated

from agents import function_tool


# ========== 内置题库 ==========
OPENING_QUESTION = {
    "question": "请先做一个 1 分钟左右的自我介绍，重点说说你与目标岗位相关的经历和能力。",
    "dimension": "自我介绍",
    "reference": ["教育/工作背景简明", "与岗位相关的项目或技能", "表达有条理、有亮点"],
}

ROLE_QUESTIONS = {
    "前端": [
        {"question": "请谈谈你对虚拟 DOM 和 Diff 算法的理解，它为什么能提升渲染性能？", "dimension": "技术基础", "reference": ["虚拟 DOM 是真实 DOM 的 JS 对象抽象", "Diff 比较新旧虚拟树只更新变化节点", "批量更新减少真实 DOM 操作"]},
        {"question": "JavaScript 中闭包是什么？请举一个你在项目中用到闭包的例子。", "dimension": "技术基础", "reference": ["闭包是函数与其词法环境的组合", "可访问外部函数作用域变量", "实例：防抖节流、模块私有变量"]},
        {"question": "浏览器的事件循环（Event Loop）是怎样的？宏任务和微任务有什么区别？", "dimension": "技术原理", "reference": ["调用栈清空后先执行微任务队列", "微任务优先级高于宏任务", "实例：Promise.then 先于 setTimeout"]},
        {"question": "请对比 Flex 和 Grid 布局的适用场景，并说说你在项目中如何选择。", "dimension": "实践能力", "reference": ["Flex 适合一维布局", "Grid 适合二维布局", "结合实际项目说明选择理由"]},
    ],
    "后端": [
        {"question": "数据库索引的底层原理是什么？为什么索引能加快查询但拖慢写入？", "dimension": "技术基础", "reference": ["常见 B+ 树结构", "索引避免全表扫描", "写入需维护索引结构故变慢"]},
        {"question": "请解释事务的 ACID 特性，并说明隔离级别各自解决什么问题。", "dimension": "技术原理", "reference": ["原子性/一致性/隔离性/持久性", "脏读、不可重复读、幻读", "四种隔离级别的区别"]},
        {"question": "设计 RESTful API 时，你遵循哪些原则？如何处理版本和错误码？", "dimension": "工程设计", "reference": ["资源用名词、动作用 HTTP 方法", "状态码语义化", "版本通过 URL 或 Header 管理"]},
        {"question": "缓存穿透、击穿、雪崩分别是什么？你会如何防范？", "dimension": "工程实践", "reference": ["穿透：查不存在的数据→布隆过滤/空值缓存", "击穿：热点 key 失效→互斥锁/永不过期", "雪崩：大面积失效→随机过期时间"]},
    ],
    "产品经理": [
        {"question": "拿到一个模糊的需求（如『提升用户活跃度』），你会如何拆解并落地？", "dimension": "需求分析", "reference": ["明确目标与衡量指标", "拆解用户场景与痛点", "定优先级、排期、验证效果"]},
        {"question": "你会用哪些方法做用户调研？各自适合什么阶段？", "dimension": "用户研究", "reference": ["访谈适合探索期深挖动机", "问卷适合验证期量化", "数据分析适合发现行为模式"]},
        {"question": "一份合格的 PRD 应该包含哪些内容？", "dimension": "文档能力", "reference": ["背景与目标、用户场景", "需求范围与功能细节", "非功能需求、埋点、验收标准"]},
        {"question": "当多个需求都很紧急但资源有限时，你如何排优先级？", "dimension": "判断力", "reference": ["用 RICE / 四象限等方法", "结合目标与影响面", "与干系人对齐并说明取舍"]},
    ],
    "数据分析": [
        {"question": "请解释 SQL 中窗口函数的作用，并举一个你实际用过的场景。", "dimension": "技术基础", "reference": ["窗口函数在行集上计算而不聚合为单行", "常见：排名、累计、移动平均", "结合真实业务场景"]},
        {"question": "如何设计一次 A/B 测试？需要注意哪些陷阱？", "dimension": "实验设计", "reference": ["明确假设与核心指标", "样本量、分流均匀性", "避免过早停止、多重比较问题"]},
        {"question": "拿到一份脏数据，你的清洗流程是怎样的？", "dimension": "数据处理", "reference": ["缺失值、异常值、重复值处理", "一致性与格式校验", "记录清洗规则保证可复现"]},
        {"question": "如果老板问『这个月 GMV 为什么下降』，你如何一步步定位原因？", "dimension": "业务分析", "reference": ["拆解指标到维度（流量×转化×客单价）", "定位异常维度", "结合外部因素给出结论与建议"]},
    ],
    "通用": [
        {"question": "介绍一个你最有成就感的项目，说明你的角色、挑战和最终结果。", "dimension": "项目经验", "reference": ["背景与目标清晰", "突出个人贡献", "用数据说明结果"]},
        {"question": "你平时如何学习一项新技术？请举例说明。", "dimension": "学习能力", "reference": ["有明确的学习路径", "动手实践与输出", "能复盘总结"]},
        {"question": "你认为自己最大的优点和待改进之处分别是什么？", "dimension": "自我认知", "reference": ["优点结合实例", "缺点真实且在改进", "态度诚恳"]},
        {"question": "面对一个完全陌生的领域，你如何在短时间内上手？", "dimension": "适应能力", "reference": ["拆解目标抓核心", "找资料与高手", "快速验证再迭代"]},
    ],
}

BEHAVIOR_QUESTIONS = [
    {"question": "请讲一次你和团队成员意见不合的经历，你是怎么处理的？", "dimension": "协作能力", "reference": ["用 STAR 结构讲述", "体现沟通与换位思考", "结果是团队达成共识"]},
    {"question": "讲一次你遇到的最大困难，以及你是如何克服的。", "dimension": "抗压与解决", "reference": ["情境与任务清楚", "说明自己的行动", "结果与复盘到位"]},
    {"question": "请举一个你在截止时间前高质量完成任务的例子。", "dimension": "执行力", "reference": ["时间管理方法", "优先级判断", "结果超出预期"]},
]

CLOSING_QUESTION = {
    "question": "面试接近尾声，你有什么想了解或想问我们的吗？",
    "dimension": "反向提问",
    "reference": ["问团队与业务而非仅问薪资", "体现对岗位的兴趣", "问题有深度"],
}


def _pick_role_questions(role: str) -> list:
    """按用户说的岗位关键词匹配题库，未命中则用通用题库。"""
    for key, bank in ROLE_QUESTIONS.items():
        if key in role:
            return bank
    for key in ROLE_QUESTIONS:
        if any(ch in role for ch in key):
            return ROLE_QUESTIONS[key]
    return ROLE_QUESTIONS["通用"]


def _score_answer(answer: str, reference: list, question: str) -> dict:
    """启发式评分（演示用）：结合长度、结构、要点命中与量化表达。"""
    text = answer.strip()
    length = len(text)
    score_len = min(25, max(6, length // 12))
    score_struct = 0
    if re.search(r"(首先|其次|最后|第一|第二|第三|[1-9][\.、)）])", text):
        score_struct += 8
    if "\n" in text or "；" in text or "。" in text:
        score_struct += 7
    hit = [p for p in reference if any(k in text for k in re.findall(r"[\u4e00-\u9fa5A-Za-z]{2,}", p)[:2])]
    score_hit = min(30, len(hit) * 10)
    score_quant = 10 if re.search(r"\d|%|倍|万|提升|降低", text) else 0
    total = min(100, 30 + score_len + score_struct + score_hit + score_quant)
    dimensions = {
        "内容完整性": min(100, 40 + score_len + score_hit),
        "逻辑表达": min(100, 40 + score_struct + score_len // 2),
        "岗位匹配度": min(100, 45 + score_hit + score_quant),
        "亮点呈现": min(100, 40 + score_quant + score_struct),
    }
    strengths = ["回答有具体内容" if length > 60 else "回答简洁",
                 "表达有结构" if score_struct >= 8 else "可加强分点表达",
                 "有量化或结果意识" if score_quant else "建议补充数据或结果"]
    improvements = []
    if score_hit < len(reference) * 10:
        improvements.append("可覆盖更多关键要点：" + "；".join(p for p in reference if p not in hit))
    if not score_quant:
        improvements.append("尽量用数据或结果量化你的贡献")
    if score_struct < 8:
        improvements.append("用『首先/其次/最后』组织答案，逻辑更清晰")
    if not improvements:
        improvements.append("回答较完整，可进一步精炼并突出个人贡献")
    return {
        "score": total,
        "dimensions": dimensions,
        "strengths": strengths,
        "improvements": improvements,
        "reference_points": reference,
        "hit_points": hit,
    }


# ========== 工具 1：出题 ==========
@function_tool
def generate_question(
    role: Annotated[str, "用户要面试的岗位，如'前端开发工程师'"],
    round_index: Annotated[int, "当前是第几轮，从 1 开始"],
    total_rounds: Annotated[int, "计划总轮数，默认 4"] = 4,
) -> str:
    """按岗位和轮次生成一道面试题。内置题库，无需外部服务。"""
    bank = _pick_role_questions(role)
    if round_index <= 1:
        item = OPENING_QUESTION
        stage = "开场"
    elif round_index >= total_rounds:
        item = CLOSING_QUESTION
        stage = "收尾"
    elif round_index == 2:
        item = bank[0]
        stage = "专业题"
    elif round_index == 3:
        item = bank[min(1, len(bank) - 1)]
        stage = "专业题"
    elif round_index == 4 and total_rounds > 4:
        item = BEHAVIOR_QUESTIONS[(round_index - 3) % len(BEHAVIOR_QUESTIONS)]
        stage = "行为题"
    else:
        item = BEHAVIOR_QUESTIONS[(round_index - 3) % len(BEHAVIOR_QUESTIONS)]
        stage = "行为题"
    return json.dumps(
        {
            "role": role,
            "stage": stage,
            "round": round_index,
            "total_rounds": total_rounds,
            "question": item["question"],
            "dimension": item["dimension"],
            "reference_points": item["reference"],
            "tip": "请等用户回答后再点评，不要一次给出多道题。",
        },
        ensure_ascii=False,
    )


# ========== 工具 2：点评 ==========
@function_tool
def evaluate_answer(
    question: Annotated[str, "本轮的题目"],
    answer: Annotated[str, "用户的回答"],
    reference_points: Annotated[str, "该题的参考要点（JSON 数组字符串或逗号分隔），可为空"],
) -> str:
    """按内容完整性、逻辑表达、岗位匹配度、亮点呈现四个维度点评回答。"""
    refs = []
    if reference_points:
        try:
            parsed = json.loads(reference_points)
            refs = parsed if isinstance(parsed, list) else [reference_points]
        except (json.JSONDecodeError, TypeError):
            refs = [p.strip() for p in re.split(r"[，,]|；|;", reference_points) if p.strip()]
    if not refs:
        refs = ["回答切题", "有具体例子", "有结果或数据"]
    result = _score_answer(answer, refs, question)
    result["question"] = question
    result["comment"] = (
        f"本题得分 {result['score']}/100。亮点：{result['strengths'][0]}；"
        f"改进重点：{result['improvements'][0]}。"
    )
    return json.dumps(result, ensure_ascii=False)


# ========== 工具 3：综合报告 ==========
@function_tool
def final_report(
    role: Annotated[str, "面试岗位"],
    scores: Annotated[str, "各轮得分，如 '78,85,72'；可为空"],
) -> str:
    """汇总各轮表现，生成综合面试报告与准备建议。"""
    nums = []
    if scores:
        nums = [int(n) for n in re.findall(r"\d+", scores) if 0 <= int(n) <= 100]
    overall = round(sum(nums) / len(nums)) if nums else 75
    if overall >= 85:
        level, advice = "优秀", "表现稳定，建议冲击更高难度岗位，注意补充业务视角。"
    elif overall >= 75:
        level, advice = "良好", "基础扎实，补齐个别短板后竞争力明显提升。"
    elif overall >= 60:
        level, advice = "合格", "具备基本素质，建议加强结构化表达和量化成果。"
    else:
        level, advice = "待提升", "建议系统梳理岗位知识，多练 STAR 结构化表达。"
    return json.dumps(
        {
            "role": role,
            "rounds_completed": len(nums),
            "scores": nums,
            "overall_score": overall,
            "level": level,
            "dimension_summary": {
                "内容完整性": min(100, overall + 3),
                "逻辑表达": max(50, overall - 4),
                "岗位匹配度": overall,
                "亮点呈现": max(50, overall - 8),
            },
            "highlights": ["能坚持完成多轮面试", "回答紧扣岗位要求", "有改进意识"],
            "improvements": ["用数据量化成果", "答案采用结构化表达", "覆盖问题的关键要点"],
            "recommendation": advice,
            "next_steps": [
                "复盘每轮低分题，补齐对应知识点",
                "用 STAR 结构重写 2 个项目经历",
                "找同伴进行 1-2 次全真模拟",
            ],
            "disclaimer": "本报告为模拟面试结果，仅供练习参考，不代表真实面试结论。",
        },
        ensure_ascii=False,
    )
