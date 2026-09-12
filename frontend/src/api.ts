import type { Bootstrap, ChatEvent, ChatRequest } from './types'

async function parseError(res: Response): Promise<string> {
  try {
    const body = (await res.json()) as { detail?: string }
    if (typeof body.detail === 'string') return body.detail
  } catch {
    /* ignore */
  }
  return res.statusText || 'Request failed'
}

export async function fetchBootstrap(): Promise<Bootstrap> {
  const res = await fetch('/api/bootstrap')
  if (!res.ok) throw new Error(await parseError(res))
  return res.json() as Promise<Bootstrap>
}

export async function fetchDailyMessage(language: string): Promise<string | null> {
  const res = await fetch(`/api/daily-message?language=${encodeURIComponent(language)}`)
  if (!res.ok) throw new Error(await parseError(res))
  const body = (await res.json()) as { message: string | null }
  return body.message
}

export async function ingestExport(file: File): Promise<void> {
  const data = new FormData()
  data.append('export', file)
  const res = await fetch('/api/ingest', { method: 'POST', body: data })
  if (!res.ok) throw new Error(await parseError(res))
}

export async function resetSession(sessionId: string): Promise<void> {
  const res = await fetch('/api/session/reset', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  })
  if (!res.ok) throw new Error(await parseError(res))
}

export async function streamChat(
  request: ChatRequest,
  onEvent: (event: ChatEvent) => void,
): Promise<void> {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  })
  if (!res.ok || !res.body) throw new Error(await parseError(res))

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const chunks = buffer.split('\n\n')
    buffer = chunks.pop() ?? ''
    for (const chunk of chunks) {
      for (const line of chunk.split('\n')) {
        if (!line.startsWith('data: ')) continue
        onEvent(JSON.parse(line.slice(6)) as ChatEvent)
      }
    }
  }
}
