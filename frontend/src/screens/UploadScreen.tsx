import { useEffect, useState, type DragEvent } from 'react'
import { CircleNotch, FileArchive, FileZip } from '@phosphor-icons/react'
import { ingestExport } from '../api'
import { RichText } from '../components/RichText'
import type { Texts } from '../types'

type Props = {
  intro: string
  texts: Texts
  onUploaded: () => Promise<void>
  onCancel?: () => void
}

function headingFromMarkdown(markdown: string): { title: string; body: string } {
  const lines = markdown.trim().split('\n')
  const first = lines[0] ?? ''
  if (first.startsWith('# ')) {
    return { title: first.slice(2).trim(), body: lines.slice(1).join('\n').trim() }
  }
  return { title: first.replace(/^#+ /, ''), body: lines.slice(1).join('\n').trim() }
}

function zipFromList(files: FileList | File[] | null): File | null {
  if (!files) return null
  return [...files].find((file) => file.name.toLowerCase().endsWith('.zip')) ?? null
}

export function UploadScreen({ intro, texts, onUploaded, onCancel }: Props) {
  const { title, body } = headingFromMarkdown(intro)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [fileName, setFileName] = useState<string | null>(null)
  const [dragging, setDragging] = useState(false)

  useEffect(() => {
    if (!onCancel) return
    const cancel = onCancel
    function onKey(event: KeyboardEvent) {
      if (event.key === 'Escape' && !busy) cancel()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [busy, onCancel])

  async function upload(file: File | null) {
    if (!file) {
      setError(texts.upload_need_zip)
      return
    }
    setFileName(file.name)
    setBusy(true)
    setError(null)
    try {
      await ingestExport(file)
      await onUploaded()
    } catch (err) {
      setError(err instanceof Error ? err.message : texts.upload_need_zip)
    } finally {
      setBusy(false)
    }
  }

  function onDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault()
    setDragging(false)
    if (!busy) void upload(zipFromList(event.dataTransfer.files))
  }

  return (
    <div className="upload-panel">
      <h1>{title}</h1>
      {body ? (
        <div className="lede">
          <RichText text={body} />
        </div>
      ) : null}
      <div className="upload-form">
        <label
          className="file-drop"
          data-dragging={dragging}
          data-busy={busy}
          onDragOver={(event) => {
            event.preventDefault()
            if (!busy) setDragging(true)
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
        >
          {busy ? (
            <CircleNotch size={34} weight="bold" className="file-drop-icon spin" aria-hidden />
          ) : (
            <FileArchive size={34} weight="duotone" className="file-drop-icon" aria-hidden />
          )}
          <span className="file-drop-title">{busy ? texts.upload_busy : texts.upload_drop_title}</span>
          <span className="file-drop-hint">{texts.upload_drop_hint}</span>
          <input
            className="visually-hidden"
            type="file"
            accept=".zip,application/zip"
            disabled={busy}
            onChange={(event) => {
              void upload(zipFromList(event.currentTarget.files))
              event.currentTarget.value = ''
            }}
          />
        </label>
        {fileName ? (
          <ul className="file-list">
            <li>
              <FileZip size={15} aria-hidden />
              {fileName}
            </li>
          </ul>
        ) : null}
        {error ? <p className="error">{error}</p> : null}
        {onCancel ? (
          <button className="btn-ghost" type="button" disabled={busy} onClick={onCancel}>
            {texts.upload_cancel}
          </button>
        ) : null}
      </div>
    </div>
  )
}
