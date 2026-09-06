const LINK = /\[([^\]]+)\]\(([^)]+)\)/g

export function RichText({ text }: { text: string }) {
  const html = text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replace(LINK, '<a href="$2" target="_blank" rel="noreferrer">$1</a>')
    .replaceAll('\n', '<br />')
  return <span dangerouslySetInnerHTML={{ __html: html }} />
}

export function headingFromMarkdown(markdown: string): { title: string; body: string } {
  const lines = markdown.trim().split('\n')
  const first = lines[0] ?? ''
  if (first.startsWith('# ')) {
    return { title: first.slice(2).trim(), body: lines.slice(1).join('\n').trim() }
  }
  return { title: first.replace(/^#+ /, ''), body: lines.slice(1).join('\n').trim() }
}
