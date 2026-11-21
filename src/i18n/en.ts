const en = {
  // Header
  "app.title": "Trip Decision Assistant",
  "app.subtitle": "Find nearby malls · Match your preferences · Plan your trip",

  // Empty state
  "empty.title": "Trip Decision Assistant",
  "empty.hint": "Tell me where you are and what brands or scenes you like. I'll search nearby malls, recommend the best fits, and give you a trip plan.",
  "empty.features": "Nearby mall search · Preference matching · Trip planning",

  // Chat input
  "chat.placeholder": "e.g. I'm near Jing'an Temple, recommend a mall for a date...  ⏎ Send · Shift+⏎ Newline",
  "chat.hint": "Powered by OpenAI Agents SDK + EdgeOne Makers · Demo only",

  // Preset questions
  "preset.1": "I'm near Jing'an Temple, Shanghai. Recommend a mall for a date.",
  "preset.2": "Find a nearby mall with cafes and luxury brands, and plan my trip.",

  // Tool indicators
  "tool.search": "Search malls",
  "tool.details": "Mall details",
  "tool.plan": "Trip plan",

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
  "sidebar.title": "Chats",
  "sidebar.newChat": "New chat",
  "sidebar.loading": "Loading conversations...",
  "sidebar.loadMore": "Load more",
  "sidebar.loadingMore": "Loading...",
  "sidebar.emptyTitle": "No conversations yet",
  "sidebar.emptyHint": "Click \"New chat\" to start your first conversation.",
  "sidebar.delete": "Delete conversation",
  "sidebar.deleteConfirm": "Permanently delete this conversation? This cannot be undone.",

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
