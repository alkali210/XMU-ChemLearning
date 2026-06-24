const APIS = {
  molscribe: 'http://localhost:8001',
  decimer: 'http://localhost:8002',
}

export const MODEL_KEYS = Object.keys(APIS)

export async function predictAll(imageFile) {
  const startedAt = new Map()
  const call = async ([name, base]) => {
    const started = performance.now()
    startedAt.set(name, started)
    const form = new FormData()
    form.append('file', imageFile)
    const res = await fetch(`${base}/predict`, { method: 'POST', body: form })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    return { ...data, model: name, duration_ms: data.duration_ms ?? Math.round(performance.now() - started) }
  }

  const settled = await Promise.allSettled(Object.entries(APIS).map(call))
  return settled.map((result, index) =>
    result.status === 'fulfilled'
      ? result.value
      : {
          model: MODEL_KEYS[index],
          smiles: null,
          error: result.reason.message,
          confidence: null,
          duration_ms: Math.round(performance.now() - (startedAt.get(MODEL_KEYS[index]) ?? performance.now())),
          runtime: null,
        },
  )
}
