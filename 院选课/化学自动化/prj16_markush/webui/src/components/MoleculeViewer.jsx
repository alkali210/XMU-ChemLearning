import { useEffect, useRef, useState } from 'react'
import SmilesDrawer from 'smiles-drawer'

export default function MoleculeViewer({ smiles }) {
  const canvasRef = useRef(null)
  const [renderError, setRenderError] = useState(false)

  useEffect(() => {
    setRenderError(false)
    const canvas = canvasRef.current
    if (!canvas) return

    const context = canvas.getContext('2d')
    context.clearRect(0, 0, canvas.width, canvas.height)

    SmilesDrawer.parse(
      smiles,
      (tree) => {
        try {
          const drawer = new SmilesDrawer.Drawer({ width: 250, height: 200 })
          drawer.draw(tree, canvas, 'light')
        } catch {
          setRenderError(true)
        }
      },
      () => setRenderError(true),
    )
  }, [smiles])

  if (renderError) return <p className="render-error">Cannot render structure</p>
  return <canvas ref={canvasRef} width="250" height="200" aria-label="Rendered molecule" />
}
