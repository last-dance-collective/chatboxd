export type MovieCardData = {
  title: string
  url: string
  image_url: string
  plot: string
  ratings: { Source?: string; Value?: string }[]
}

export type ChatEvent =
  | { type: 'token'; text: string }
  | { type: 'status'; message: string }
  | { type: 'movie_card'; movie: MovieCardData }
  | { type: 'graph'; data: number[] }
  | { type: 'error'; message: string }
  | { type: 'done' }

export type ProviderInfo = {
  id: string
  available: boolean
  models: string[]
}

export type ModelChoice = {
  provider: string
  model: string
}

export function firstAvailable(providers: ProviderInfo[]): ModelChoice | null {
  const provider = providers.find((item) => item.available && item.models.length > 0)
  const model = provider?.models[0]
  if (!provider || !model) return null
  return { provider: provider.id, model }
}

export type Bootstrap = {
  db_exists: boolean
  default_language: string
  languages: Record<string, string>
  providers: ProviderInfo[]
  translations: Record<string, Record<string, unknown>>
  provider_help: Record<string, Record<string, string>>
  no_db_text: string
}

export type ChatRequest = {
  session_id: string
  message: string
  language: string
  provider: string
  model: string
}

export type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  content: string
  status?: string
  movie?: MovieCardData
  graph?: number[]
  error?: string
}

export type Texts = {
  select_language: string
  select_model: string
  available_provider: string
  not_available_provider: string
  reset_chat: string
  configure_app: string
  chat_placeholder: string
  header_caption: string
  chat_loading: string
  continue: string
  start_page_markdown: string
  keys_not_set: string
  suggestions_label: string
  suggestions_list: string[]
}

export function textsOf(
  translations: Record<string, Record<string, unknown>>,
  language: string,
): Texts {
  const raw = translations[language] ?? translations.EN ?? {}
  const list = raw.suggestions_list
  return {
    select_language: String(raw.select_language ?? 'Select language'),
    select_model: String(raw.select_model ?? 'Choose a model'),
    available_provider: String(raw.available_provider ?? '{provider} available'),
    not_available_provider: String(raw.not_available_provider ?? '{provider} unavailable'),
    reset_chat: String(raw.reset_chat ?? 'Reset'),
    configure_app: String(raw.configure_app ?? 'Settings'),
    chat_placeholder: String(raw.chat_placeholder ?? 'Type a message'),
    header_caption: String(raw.header_caption ?? ''),
    chat_loading: String(raw.chat_loading ?? 'Generating...'),
    continue: String(raw.continue ?? 'Continue'),
    start_page_markdown: String(raw.start_page_markdown ?? ''),
    keys_not_set: String(raw.keys_not_set ?? 'Agent keys are missing'),
    suggestions_list: Array.isArray(list) ? list.map(String) : [],
    suggestions_label: String(raw.suggestions_label ?? ''),
  }
}
