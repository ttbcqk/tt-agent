const zh = {
  // Header
  "app.title": "出行决策助手",
  "app.subtitle": "查附近商场 · 按偏好推荐 · 给出出行建议",

  // Empty state
  "empty.title": "出行决策助手",
  "empty.hint": "告诉我你在哪里、喜欢什么品牌或场景，我会搜索附近商场、结合你的偏好推荐最合适的地方，并给出出行建议。",
  "empty.features": "附近商场搜索 · 偏好匹配 · 出行建议",

  // Chat input
  "chat.placeholder": "例如：我在静安寺，想找个适合情侣约会的商场…  ⏎ 发送 · Shift+⏎ 换行",
  "chat.hint": "由 OpenAI Agents SDK + EdgeOne Makers 驱动 · 仅供演示",

  // Preset questions
  "preset.1": "我在上海静安寺，想找个适合情侣约会的商场",
  "preset.2": "帮我在附近找有咖啡和轻奢品牌的商场，并给出出行建议",

  // Tool indicators
  "tool.search": "搜索商场",
  "tool.details": "商场详情",
  "tool.plan": "出行建议",

  // Status & errors
  "status.error": "⚠️ 请求失败，请检查后端服务是否启动。",
  "status.stopped": "⏹ *已停止生成*",
  "status.backendError": "⚠️ 后端中断请求失败，服务端可能仍在运行。",

  // Debug panel
  "debug.title": "传输流",
  "debug.events": "事件",
  "debug.clear": "清除",
  "debug.empty": "等待 SSE 事件...",
  "debug.emptyHint": "发送消息后，所有原始后端数据将在此处显示。",

  // Conversation sidebar
  "sidebar.label": "会话列表",
  "sidebar.title": "会话",
  "sidebar.newChat": "新建聊天",
  "sidebar.loading": "正在加载会话...",
  "sidebar.loadMore": "加载更多",
  "sidebar.loadingMore": "加载中...",
  "sidebar.emptyTitle": "暂无会话",
  "sidebar.emptyHint": "点击「新建聊天」开始第一段对话。",
  "sidebar.delete": "删除会话",
  "sidebar.deleteConfirm": "确定要永久删除这个会话吗？此操作不可恢复。",

  // Aria labels (button hover/screen-reader)
  "aria.send": "发送",
  "aria.clearHistory": "清除历史",
  "aria.stopGeneration": "停止生成",

  // Language toggle
  "lang.switch": "English",

  // ─── Floating bottom-right action badges ─────────────────────────────
  "floatingLink.deploy": "一键部署",
  "floatingLink.github": "GitHub",
} as const;

export default zh;
