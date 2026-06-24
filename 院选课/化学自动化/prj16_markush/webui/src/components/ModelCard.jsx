import MoleculeViewer from './MoleculeViewer.jsx'

const GENERIC_PATTERN = /\bR\d*\b|\bA\b|\bX\b|\bZ\b/g

function truncateSmiles(smiles) {
  return smiles.length > 80 ? `${smiles.slice(0, 80)}...` : smiles
}

function genericSymbols(smiles) {
  return [...new Set(smiles.match(GENERIC_PATTERN) || [])]
}

function RuntimeMeta({ result }) {
  if (!result) return null

  const duration = Number.isFinite(result.duration_ms) ? `${result.duration_ms} ms` : 'Unknown'
  const hostname = result.runtime?.hostname || 'Unknown'
  const platform = result.runtime?.platform || 'Unknown'

  return (
    <dl className="runtime-meta" aria-label="Runtime metadata">
      <div>
        <dt>Time:</dt>
        <dd>{duration}</dd>
      </div>
      <div>
        <dt>Host:</dt>
        <dd>{hostname}</dd>
      </div>
      <div>
        <dt>Platform:</dt>
        <dd>{platform}</dd>
      </div>
    </dl>
  )
}

export default function ModelCard({ modelName, result, loading }) {
  const symbols = result?.smiles ? genericSymbols(result.smiles) : []

  return (
    <article className="model-card">
      <header>
        <h2>{modelName}</h2>
      </header>

      {loading ? (
        <div className="skeleton" aria-label={`${modelName} loading`} />
      ) : result?.error ? (
        <div className="error-banner">{result.error}</div>
      ) : result?.smiles ? (
        <div className="result-body">
          <code>{truncateSmiles(result.smiles)}</code>
          <MoleculeViewer smiles={result.smiles} />
          {symbols.length > 0 && <div className="generic-pill">Generic atoms detected: {symbols.join(', ')}</div>}
        </div>
      ) : (
        <p className="empty-output">No output</p>
      )}

      {!loading && <RuntimeMeta result={result} />}
    </article>
  )
}
