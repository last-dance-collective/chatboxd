import { useMemo, useState } from 'react'
import { MovieCard } from '../components/MovieCard'
import { RatingChart } from '../components/RatingChart'
import { RichText } from '../components/RichText'
import type { ChatMessage, ModelChoice, ProviderInfo, Texts } from '../types'

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
        <button type="button" className="btn-ghost sidebar-action" onClick={onReset}>
          {texts.reset_chat}
        </button>
        <select
          className="select"
          aria-label={texts.select_language}
          value={language}
          onChange={(event) => onLanguage(event.target.value)}
        >
          {Object.entries(languages).map(([code, label]) => (
            <option key={code} value={code}>
              {label}
            </option>
          ))}
        </select>
      </aside>

      <div className="chat-main">
        <div className="chat-scroll">
          {dailyMessage ? (
            <div className="daily">
              <RichText text={dailyMessage} />
            </div>
          ) : null}

          {showSuggestions ? (
            <section className="suggestions">
              <p>{texts.suggestions_label}</p>
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
                  <p className="muted">{texts.chat_loading}</p>
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
            <select
              className="composer-model"
              aria-label={texts.select_model}
              value={model ? encodeChoice(model) : ''}
              disabled={streaming}
              onChange={(event) => {
                const next = decodeChoice(event.target.value)
                if (next) onModel(next)
              }}
            >
              {model ? null : <option value="">{texts.select_model}</option>}
              {providers
                .filter((item) => item.available && item.models.length > 0)
                .map((item) => (
                  <optgroup key={item.id} label={item.id}>
                    {item.models.map((name) => {
                      const choice = { provider: item.id, model: name }
                      const value = encodeChoice(choice)
                      return (
                        <option key={value} value={value}>
                          {item.id} {name}
                        </option>
                      )
                    })}
                  </optgroup>
                ))}
            </select>
            <button className="btn-primary" type="submit" disabled={!canSend || !draft.trim()}>
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
