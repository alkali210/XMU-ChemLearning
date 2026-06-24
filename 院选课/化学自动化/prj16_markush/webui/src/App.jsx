import { useEffect, useState } from 'react'
import { MODEL_KEYS, predictAll } from './api/client.js'
import ImageUploader from './components/ImageUploader.jsx'
import ModelCard from './components/ModelCard.jsx'

const DISPLAY_NAMES = {
  molscribe: 'MolScribe',
  decimer: 'DECIMER',
}

export default function App() {
  const [imageFile, setImageFile] = useState(null)
  const [imageUrl, setImageUrl] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    return () => {
      if (imageUrl) URL.revokeObjectURL(imageUrl)
    }
  }, [imageUrl])

  const handleSelect = (file) => {
    if (imageUrl) URL.revokeObjectURL(imageUrl)
    setImageFile(file)
    setImageUrl(URL.createObjectURL(file))
    setResults([])
  }

  const handleAnalyze = async () => {
    if (!imageFile) return
    setLoading(true)
    try {
      setResults(await predictAll(imageFile))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">Markush Recognition Benchmark</p>
        <h1>Compare molecular OCR models on generic atom symbols.</h1>
        <p className="intro">
          Upload a molecule image and inspect whether MolScribe and DECIMER preserve Markush labels such as R, A, X, and Z.
        </p>
      </section>

      <ImageUploader imageUrl={imageUrl} loading={loading} onAnalyze={handleAnalyze} onSelect={handleSelect} />

      <section className="results-grid" aria-label="Model results">
        {MODEL_KEYS.map((key) => (
          <ModelCard
            key={key}
            modelName={DISPLAY_NAMES[key]}
            result={results.find((result) => result.model === key || result.model === DISPLAY_NAMES[key])}
            loading={loading}
          />
        ))}
      </section>
    </main>
  )
}
