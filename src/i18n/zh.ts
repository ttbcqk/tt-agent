const zh = {
  // Header
  "app.title": "AI 面试教练",
  "app.subtitle": "模拟面试 · 逐题点评 · 生成报告",

  // Empty state
  "empty.title": "AI 面试教练",
  "empty.hint": "告诉我你要面试的岗位，我会模拟真实面试：逐轮出题、点评你的回答，最后生成一份综合面试报告。",
  "empty.features": "多轮模拟面试 · 四维点评 · 综合报告",

  // Chat input
  "chat.placeholder": "例如：我要面试前端开发工程师，开始模拟面试  ⏎ 发送 · Shift+⏎ 换行",
  "chat.hint": "由 OpenAI Agents SDK + EdgeOne Makers 驱动 · 仅供演示",

  // Preset questions
  "preset.1": "我要面试前端开发工程师，开始模拟面试",
  "preset.2": "帮我做一场产品经理的模拟面试",

  // Tool indicators
  "tool.question": "生成面试题",
  "tool.evaluate": "答题点评",
  "tool.report": "综合报告",

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
  "sidebar.newChat": "新建面试",
  "sidebar.loading": "正在加载会话...",
  "sidebar.loadMore": "加载更多",
  "sidebar.loadingMore": "加载中...",
  "sidebar.emptyTitle": "暂无会话",
  "sidebar.emptyHint": "点击「新建面试」开始第一场模拟面试。",
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
