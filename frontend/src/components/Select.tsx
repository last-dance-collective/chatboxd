import { useEffect, useId, useRef, useState, type KeyboardEvent } from 'react'
import { CaretUpDown, Check } from '@phosphor-icons/react'

export type SelectOption = {
  value: string
  label: string
  /** Shown in the trigger next to the label, muted. Group headers already cover it in the panel. */
  hint?: string
}

export type SelectGroup = {
  label: string
  options: SelectOption[]
}

type Props = {
  value: string
  onChange: (value: string) => void
  options?: SelectOption[]
  groups?: SelectGroup[]
  placeholder?: string
  ariaLabel: string
  /** The composer's select sits at the bottom of the screen, so it opens upward. */
  placement?: 'up' | 'down'
  disabled?: boolean
}

function flatten(options: SelectOption[] | undefined, groups: SelectGroup[] | undefined): SelectOption[] {
  if (groups) return groups.flatMap((group) => group.options)
  return options ?? []
}

export function Select({
  value,
  onChange,
  options,
  groups,
  placeholder = 'Select…',
  ariaLabel,
  placement = 'down',
  disabled = false,
}: Props) {
  const uid = useId()
  const rootRef = useRef<HTMLDivElement>(null)
  const panelRef = useRef<HTMLDivElement>(null)
  const [open, setOpen] = useState(false)
  const flat = flatten(options, groups)
  const selectedIndex = flat.findIndex((option) => option.value === value)
  const selected = selectedIndex >= 0 ? flat[selectedIndex] : null
  const [activeIndex, setActiveIndex] = useState(selectedIndex >= 0 ? selectedIndex : 0)

  const optionId = (index: number) => `${uid}-option-${index}`

  function openPanel() {
    setActiveIndex(selectedIndex >= 0 ? selectedIndex : 0)
    setOpen(true)
  }

  function choose(index: number) {
    const option = flat[index]
    if (!option) return
    onChange(option.value)
    setOpen(false)
  }

  // Close on outside click.
  useEffect(() => {
    if (!open) return
    function onPointerDown(event: PointerEvent) {
      if (rootRef.current && !rootRef.current.contains(event.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('pointerdown', onPointerDown)
    return () => document.removeEventListener('pointerdown', onPointerDown)
  }, [open])

  // Keep the active option visible while keyboard-navigating.
  useEffect(() => {
    if (!open) return
    document.getElementById(`${uid}-option-${activeIndex}`)?.scrollIntoView({ block: 'nearest' })
  }, [activeIndex, open, uid])

  function onKeyDown(event: KeyboardEvent) {
    if (disabled) return
    switch (event.key) {
      case 'ArrowDown':
      case 'ArrowUp': {
        event.preventDefault()
        if (!open) {
          openPanel()
          return
        }
        const delta = event.key === 'ArrowDown' ? 1 : -1
        setActiveIndex((index) => Math.min(flat.length - 1, Math.max(0, index + delta)))
        return
      }
      case 'Home':
        if (!open) return
        event.preventDefault()
        setActiveIndex(0)
        return
      case 'End':
        if (!open) return
        event.preventDefault()
        setActiveIndex(flat.length - 1)
        return
      case 'Enter':
      case ' ':
        event.preventDefault()
        if (open) choose(activeIndex)
        else openPanel()
        return
      case 'Escape':
        if (open) {
          event.preventDefault()
          setOpen(false)
        }
        return
      case 'Tab':
        setOpen(false)
        return
      default:
        // Native-style typeahead while the panel is open.
        if (open && event.key.length === 1 && /\S/.test(event.key)) {
          const query = event.key.toLowerCase()
          const match = flat.findIndex((option, index) => index > activeIndex && option.label.toLowerCase().startsWith(query))
          const wrap = match >= 0 ? match : flat.findIndex((option) => option.label.toLowerCase().startsWith(query))
          if (wrap >= 0) setActiveIndex(wrap)
        }
    }
  }

  let optionIndex = -1
  const renderOption = (option: SelectOption) => {
    optionIndex += 1
    const index = optionIndex
    const isSelected = option.value === value
    return (
      <div
        key={option.value}
        id={optionId(index)}
        role="option"
        aria-selected={isSelected}
        data-active={index === activeIndex}
        className="select-option"
        onClick={() => choose(index)}
        onMouseEnter={() => setActiveIndex(index)}
      >
        <span className="select-option-label">{option.label}</span>
        <Check size={14} weight="bold" className="select-check" aria-hidden />
      </div>
    )
  }

  return (
    <div className="select" ref={rootRef} onKeyDown={onKeyDown}>
      <button
        type="button"
        className="select-trigger"
        disabled={disabled}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={ariaLabel}
        title={selected ? `${selected.hint ? `${selected.hint} ` : ''}${selected.label}` : placeholder}
        onClick={() => (open ? setOpen(false) : openPanel())}
      >
        <span className="select-value" data-empty={!selected}>
          {selected ? (
            <>
              {selected.hint ? <span className="select-value-hint">{selected.hint}</span> : null}
              {selected.label}
            </>
          ) : (
            placeholder
          )}
        </span>
        <CaretUpDown size={14} weight="bold" className="select-caret" aria-hidden />
      </button>
      {open ? (
        <div
          className={`select-panel select-panel-${placement}`}
          role="listbox"
          aria-label={ariaLabel}
          aria-activedescendant={optionId(activeIndex)}
          ref={panelRef}
        >
          {groups
            ? groups.map((group) => (
                <div className="select-group" key={group.label}>
                  <div className="select-group-label">{group.label}</div>
                  {group.options.map(renderOption)}
                </div>
              ))
            : (options ?? []).map(renderOption)}
        </div>
      ) : null}
    </div>
  )
}
