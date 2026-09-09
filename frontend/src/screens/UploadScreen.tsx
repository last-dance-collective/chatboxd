import { useRef, useState, type DragEvent, type FormEvent } from 'react'
import { CircleNotch, FileArrowUp, FileCsv } from '@phosphor-icons/react'
import { ingestFiles } from '../api'
import { RichText } from '../components/RichText'

type Props = {
  intro: string
  onUploaded: () => Promise<void>
}

function headingFromMarkdown(markdown: string): { title: string; body: string } {
  const lines = markdown.trim().split('\n')
  const first = lines[0] ?? ''
  if (first.startsWith('# ')) {
    return { title: first.slice(2).trim(), body: lines.slice(1).join('\n').trim() }
  }
  return { title: first.replace(/^#+ /, ''), body: lines.slice(1).join('\n').trim() }
}

export function UploadScreen({ intro, onUploaded }: Props) {
  const { title, body } = headingFromMarkdown(intro)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [fileNames, setFileNames] = useState<string[]>([])
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  function syncFiles(files: FileList | null) {
    setFileNames(files ? [...files].map((file) => file.name) : [])
  }

  function onDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault()
    setDragging(false)
    const { files } = event.dataTransfer
    if (inputRef.current && files.length > 0) {
      inputRef.current.files = files
      syncFiles(files)
    }
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    const files = [...form.getAll('files')].filter((value): value is File => value instanceof File)
    const diary = files.find((file) => file.name === 'diary.csv')
    const reviews = files.find((file) => file.name === 'reviews.csv')
    if (!diary || !reviews) {
      setError('Upload both diary.csv and reviews.csv.')
      return
    }
    setBusy(true)
    setError(null)
    try {
      await ingestFiles(diary, reviews)
      await onUploaded()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ingestion failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="page page-narrow">
      <img className="banner" src="/banner.png" alt="Chatboxd" />
      <h1>{title}</h1>
      <div className="lede">
        <RichText text={body} />
      </div>
      <form className="upload-form" onSubmit={onSubmit}>
        <label
          className="file-drop"
          data-dragging={dragging}
          onDragOver={(event) => {
            event.preventDefault()
            setDragging(true)
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
        >
          <FileArrowUp size={34} weight="duotone" className="file-drop-icon" aria-hidden />
          <span className="file-drop-title">Drop diary.csv and reviews.csv here</span>
          <span className="file-drop-hint">or click to browse your files</span>
          <input
            ref={inputRef}
            className="visually-hidden"
            name="files"
            type="file"
            accept=".csv"
            multiple
            onChange={(event) => syncFiles(event.currentTarget.files)}
          />
        </label>
        {fileNames.length > 0 ? (
          <ul className="file-list">
            {fileNames.map((name) => (
              <li key={name}>
                <FileCsv size={15} aria-hidden />
                {name}
              </li>
            ))}
          </ul>
        ) : null}
        {error ? <p className="error">{error}</p> : null}
        <button className="btn-primary" type="submit" disabled={busy}>
          {busy ? <CircleNotch size={16} weight="bold" className="spin" aria-hidden /> : null}
          {busy ? 'Loading diary…' : 'Build my database'}
        </button>
      </form>
    </main>
  )
}
