import { useRef, useState } from 'react'

export default function ImageUploader({ imageUrl, loading, onAnalyze, onSelect }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  const selectFile = (file) => {
    if (file && file.type.startsWith('image/')) onSelect(file)
  }

  const handleDrop = (event) => {
    event.preventDefault()
    setDragging(false)
    selectFile(event.dataTransfer.files?.[0])
  }

  return (
    <section className="upload-card">
      <div
        className={`drop-zone ${dragging ? 'is-dragging' : ''}`}
        role="button"
        tabIndex="0"
        onClick={() => inputRef.current?.click()}
        onKeyDown={(event) => {
          if (event.key === 'Enter' || event.key === ' ') inputRef.current?.click()
        }}
        onDragOver={(event) => {
          event.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/png,image/jpeg"
          onChange={(event) => selectFile(event.target.files?.[0])}
        />
        {imageUrl ? (
          <img className="preview" src={imageUrl} alt="Selected molecule" />
        ) : (
          <div>
            <strong>Drop a molecule image here</strong>
            <span>or click to choose a PNG/JPEG file</span>
          </div>
        )}
      </div>
      <button className="analyze-button" type="button" disabled={loading || !imageUrl} onClick={onAnalyze}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
    </section>
  )
}
