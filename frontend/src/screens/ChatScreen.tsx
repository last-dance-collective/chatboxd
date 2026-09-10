import { useMemo, useState } from 'react'
import { ArrowCounterClockwise, CalendarBlank, PaperPlaneRight, Sparkle } from '@phosphor-icons/react'
import { MovieCard } from '../components/MovieCard'
import { RatingChart } from '../components/RatingChart'
import { RichText } from '../components/RichText'
import { Select, type SelectGroup, type SelectOption } from '../components/Select'
import { type ChatMessage, type ModelChoice, type ProviderInfo, type Texts } from '../types'

type Props = {
  texts: Texts
  languages: Record<string, string>
  language: string
  onLanguage: (language: string) => void
  providers: ProviderInfo[]
  model: ModelChoice | null
  onModel: (choice: ModelChoice) => void
  dailyMessage: string | null
  messages: ChatMessage[]
  streaming: boolean
  onSend: (text: string) => void
  onReset: () => void
}

function encodeChoice(choice: ModelChoice): string {
  return `${choice.provider}\u001f${choice.model}`
}

function decodeChoice(value: string): ModelChoice | null {
  const sep = value.indexOf('\u001f')
  if (sep <= 0 || sep === value.length - 1) return null
  return { provider: value.slice(0, sep), model: value.slice(sep + 1) }
}

export function ChatScreen({
  texts,
  languages,
  language,
  onLanguage,
  providers,
  model,
  onModel,
  dailyMessage,
  messages,
  streaming,
  onSend,
  onReset,
}: Props) {
  const [draft, setDraft] = useState('')
  const suggestions = useMemo(() => {
    const list = [...texts.suggestions_list]
    for (let i = list.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[list[i], list[j]] = [list[j], list[i]]
    }
    return list.slice(0, 3)
  }, [texts.suggestions_list])
  const languageOptions = useMemo<SelectOption[]>(
    () => Object.entries(languages).map(([code, label]) => ({ value: code, label })),
    [languages],
  )
  const modelGroups = useMemo<SelectGroup[]>(
    () =>
      providers
        .filter((item) => item.available && item.models.length > 0)
        .map((item) => ({
          label: item.id,
          options: item.models.map((name) => ({
            value: encodeChoice({ provider: item.id, model: name }),
            label: name,
            hint: item.id,
          })),
        })),
    [providers],
  )
  const showSuggestions = messages.length === 0 && !streaming
  const canSend = Boolean(model) && !streaming

  function submit(text: string) {
    const trimmed = text.trim()
    if (!trimmed || !canSend) return
    setDraft('')
    onSend(trimmed)
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <img className="sidebar-logo" src="/chatboxd.png" alt="Chatboxd" />
        <div className="field">
          <span className="field-label">{texts.select_language}</span>
          <Select
            ariaLabel={texts.select_language}
            options={languageOptions}
            value={language}
            onChange={onLanguage}
          />
        </div>
        <button type="button" className="btn-ghost sidebar-action" onClick={onReset}>
          <ArrowCounterClockwise size={15} weight="bold" aria-hidden />
          {texts.reset_chat}
        </button>
      </aside>

      <div className="chat-main">
        <div className="chat-scroll">
          {dailyMessage ? (
            <div className="daily">
              <CalendarBlank size={18} className="daily-icon" aria-hidden />
              <div>
                <RichText text={dailyMessage} />
              </div>
            </div>
          ) : null}

          {showSuggestions ? (
            <section className="suggestions">
              <p className="suggestions-label">
                <Sparkle size={15} weight="fill" aria-hidden />
                {texts.suggestions_label}
              </p>
              <div className="suggestion-row">
                {suggestions.map((item) => (
                  <button
                    key={item}
                    type="button"
                    className="pill"
                    disabled={!canSend}
                    onClick={() => submit(item)}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </section>
          ) : null}

          <ol className="transcript">
            {messages.map((message) => (
              <li key={message.id} className={`bubble bubble-${message.role}`}>
                {message.status ? (
                  <div className="status">
                    <RichText text={message.status} />
                  </div>
                ) : null}
                {message.role === 'user' && message.content ? (
                  <p className="bubble-plain">{message.content}</p>
                ) : null}
                {message.role === 'assistant' && message.content ? (
                  <RichText text={message.content} />
                ) : null}
                {message.error ? <p className="error">{message.error}</p> : null}
                {message.movie ? <MovieCard movie={message.movie} /> : null}
                {message.graph ? <RatingChart ratings={message.graph} /> : null}
                {streaming && message.id === messages.at(-1)?.id && !message.content && !message.status ? (
                  <p className="typing">
                    <span className="typing-dots" aria-hidden>
                      <span />
                      <span />
                      <span />
                    </span>
                    {texts.chat_loading}
                  </p>
                ) : null}
              </li>
            ))}
          </ol>
        </div>

        <form
          className="composer"
          onSubmit={(event) => {
            event.preventDefault()
            submit(draft)
          }}
        >
          {model ? null : <p className="error composer-alert">{texts.keys_not_set}</p>}
          <textarea
            className="composer-field"
            value={draft}
            rows={2}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault()
                submit(draft)
              }
            }}
            placeholder={texts.chat_placeholder}
            disabled={streaming || !model}
          />
          <div className="composer-bar">
            <Select
              ariaLabel={texts.select_model}
              placeholder={texts.select_model}
              groups={modelGroups}
              value={model ? encodeChoice(model) : ''}
              disabled={streaming}
              placement="up"
              onChange={(value) => {
                const next = decodeChoice(value)
                if (next) onModel(next)
              }}
            />
            <button className="btn-primary" type="submit" disabled={!canSend || !draft.trim()}>
              Send
              <PaperPlaneRight size={15} weight="bold" aria-hidden />
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
