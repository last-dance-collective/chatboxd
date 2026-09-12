import { useCallback, useEffect, useState } from 'react'
import { fetchBootstrap, fetchDailyMessage, resetSession, streamChat } from './api'
import { ChatScreen } from './screens/ChatScreen'
import { UploadScreen } from './screens/UploadScreen'
import { firstAvailable, textsOf, type Bootstrap, type ChatMessage, type ModelChoice } from './types'

type Phase = 'boot' | 'empty' | 'chat'

function newSessionId(): string {
  return crypto.randomUUID()
}

export default function App() {
  const [phase, setPhase] = useState<Phase>('boot')
  const [replacing, setReplacing] = useState(false)
  const [bootstrap, setBootstrap] = useState<Bootstrap | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [language, setLanguage] = useState('ES')
  const [modelChoice, setModelChoice] = useState<ModelChoice | null>(null)
  const [sessionId, setSessionId] = useState(newSessionId)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [streaming, setStreaming] = useState(false)
  const [dailyMessage, setDailyMessage] = useState<string | null>(null)
  const [diaryEpoch, setDiaryEpoch] = useState(0)

  const loadBootstrap = useCallback(async (preservePrefs = false) => {
    const data = await fetchBootstrap()
    setBootstrap(data)
    if (!preservePrefs) {
      setLanguage(data.default_language)
      setModelChoice(firstAvailable(data.providers))
    }
    setPhase(data.db_exists ? 'chat' : 'empty')
    setReplacing(false)
  }, [])

  useEffect(() => {
    loadBootstrap().catch((err: unknown) => {
      setError(err instanceof Error ? err.message : 'Failed to reach the API')
    })
  }, [loadBootstrap])

  useEffect(() => {
    if (phase !== 'chat') return
    fetchDailyMessage(language)
      .then(setDailyMessage)
      .catch(() => setDailyMessage(null))
  }, [phase, language, diaryEpoch])

  async function onSend(text: string) {
    if (!modelChoice) return
    const user: ChatMessage = { id: crypto.randomUUID(), role: 'user', content: text }
    const assistantId = crypto.randomUUID()
    const assistant: ChatMessage = { id: assistantId, role: 'assistant', content: '' }
    setMessages((current) => [...current, user, assistant])
    setStreaming(true)
    try {
      await streamChat(
        {
          session_id: sessionId,
          message: text,
          language,
          provider: modelChoice.provider,
          model: modelChoice.model,
        },
        (event) => {
          setMessages((current) =>
            current.map((message) => {
              if (message.id !== assistantId) return message
              if (event.type === 'token') {
                return { ...message, content: message.content + event.text }
              }
              if (event.type === 'status') {
                return { ...message, status: event.message }
              }
              if (event.type === 'movie_card') {
                return { ...message, movie: event.movie }
              }
              if (event.type === 'graph') {
                return { ...message, graph: event.data }
              }
              if (event.type === 'error') {
                return { ...message, error: event.message }
              }
              return message
            }),
          )
        },
      )
    } catch (err) {
      setMessages((current) =>
        current.map((message) =>
          message.id === assistantId
            ? { ...message, error: err instanceof Error ? err.message : 'Chat failed' }
            : message,
        ),
      )
    } finally {
      setStreaming(false)
    }
  }

  async function onReset() {
    await resetSession(sessionId)
    setSessionId(newSessionId())
    setMessages([])
  }

  async function onIngested() {
    await loadBootstrap(true)
    await onReset()
    setDiaryEpoch((n) => n + 1)
  }

  if (error) {
    return (
      <main className="page page-narrow">
        <img className="banner" src="/banner.png" alt="Chatboxd" />
        <p className="error">{error}</p>
        <p className="muted">Start the API from backend/ with `uv run uvicorn api.app:app --app-dir src --reload`</p>
      </main>
    )
  }

  if (phase === 'boot' || !bootstrap) {
    return (
      <main className="page page-narrow">
        <img className="banner" src="/banner.png" alt="Chatboxd" />
        <p className="muted">Loading…</p>
      </main>
    )
  }

  const texts = textsOf(bootstrap.translations, language)

  if (phase === 'empty') {
    return (
      <main className="page page-narrow">
        <img className="banner" src="/banner.png" alt="Chatboxd" />
        <UploadScreen intro={texts.no_db_text || bootstrap.no_db_text} texts={texts} onUploaded={onIngested} />
      </main>
    )
  }

  return (
    <>
      <ChatScreen
        texts={texts}
        languages={bootstrap.languages}
        language={language}
        onLanguage={setLanguage}
        providers={bootstrap.providers}
        model={modelChoice}
        onModel={setModelChoice}
        dailyMessage={dailyMessage}
        messages={messages}
        streaming={streaming}
        onSend={onSend}
        onReset={() => {
          void onReset()
        }}
        onUpdateDiary={() => setReplacing(true)}
      />
      {replacing ? (
        <div
          className="upload-overlay"
          role="dialog"
          aria-modal="true"
          aria-label={texts.update_diary}
        >
          <div className="upload-overlay-card">
            <UploadScreen
              intro={texts.replace_diary_text}
              texts={texts}
              onUploaded={onIngested}
              onCancel={() => setReplacing(false)}
            />
          </div>
        </div>
      ) : null}
    </>
  )
}
