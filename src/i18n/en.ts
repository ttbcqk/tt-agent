const en = {
  // Header
  "app.title": "AI Interview Coach",
  "app.subtitle": "Mock interview · Answer review · Final report",

  // Empty state
  "empty.title": "AI Interview Coach",
  "empty.hint": "Tell me the role you're interviewing for. I'll run a realistic mock interview, review each answer, and generate a final report.",
  "empty.features": "Multi-round mock · 4-dimension review · Final report",

  // Chat input
  "chat.placeholder": "e.g. Start a mock interview for a frontend engineer  ⏎ Send · Shift+⏎ Newline",
  "chat.hint": "Powered by OpenAI Agents SDK + EdgeOne Makers · Demo only",

  // Preset questions
  "preset.1": "Start a mock interview for a frontend engineer",
  "preset.2": "Run a product manager mock interview for me",

  // Tool indicators
  "tool.question": "Generate question",
  "tool.evaluate": "Review answer",
  "tool.report": "Final report",

  // Status & errors
  "status.error": "Request failed. Please check if the backend service is running.",
  "status.stopped": "⏹ *Generation stopped*",
  "status.backendError": "Backend abort request failed. The server may still be running.",

  // Debug panel
  "debug.title": "Trace",
  "debug.events": "events",
  "debug.clear": "Clear",
  "debug.empty": "Waiting for SSE events...",
  "debug.emptyHint": "After sending a message, all raw backend data will be displayed here.",

  // Conversation sidebar
  "sidebar.label": "Conversation list",
  "sidebar.title": "Interviews",
  "sidebar.newChat": "New interview",
  "sidebar.loading": "Loading conversations...",
  "sidebar.loadMore": "Load more",
  "sidebar.loadingMore": "Loading...",
  "sidebar.emptyTitle": "No interviews yet",
  "sidebar.emptyHint": "Click \"New interview\" to start your first mock interview.",
  "sidebar.delete": "Delete interview",
  "sidebar.deleteConfirm": "Permanently delete this interview? This cannot be undone.",

  // Aria labels (button hover/screen-reader)
  "aria.send": "Send",
  "aria.clearHistory": "Clear history",
  "aria.stopGeneration": "Stop generation",

  // Language toggle
  "lang.switch": "中文",

  // ─── Floating bottom-right action badges ─────────────────────────────
  "floatingLink.deploy": "Deploy",
  "floatingLink.github": "GitHub",
} as const;

export default en;
