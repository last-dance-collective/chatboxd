import { useState, type FormEvent } from 'react'
import { ingestFiles } from '../api'
import { headingFromMarkdown, RichText } from '../components/RichText'

type Props = {
  intro: string
  onUploaded: () => Promise<void>
}

export function UploadScreen({ intro, onUploaded }: Props) {
  const { title, body } = headingFromMarkdown(intro)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

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
      <p className="lede">
        <RichText text={body} />
      </p>
      <form className="upload-form" onSubmit={onSubmit}>
        <label className="file-drop">
          <span>Drop diary.csv and reviews.csv here</span>
          <input name="files" type="file" accept=".csv" multiple required />
        </label>
        {error ? <p className="error">{error}</p> : null}
        <button className="btn-primary" type="submit" disabled={busy}>
          {busy ? 'Loading diary…' : 'Build my database'}
        </button>
      </form>
    </main>
  )
}
