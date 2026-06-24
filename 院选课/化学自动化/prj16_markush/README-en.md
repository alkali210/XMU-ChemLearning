<p align="center">
  <a href="README.md">中文</a> | <b>English</b>
</p>

# Markush Recognition Benchmark

## Background

Markush structures are patent-style chemical drawings that describe a family of related compounds by combining a fixed core with variable placeholders such as `R`, `R1`, `A`, `X`, and `Z`. WIPO's PATENTSCOPE training material describes these placeholders as a way to represent variations of substituents, functional groups, or parts of a structure in patent searches.[^wipo-markush]

Most open molecular structure recognition models are trained to convert ordinary chemical depictions into fully specified molecular graphs or SMILES strings. That makes Markush drawings a useful stress test: a model may return a syntactically valid molecule while silently deleting or normalizing the generic atom labels that make the patent claim meaningful.

This project is a small, CPU-only benchmark harness for that failure mode. The default WebUI compares MolScribe and DECIMER side by side, shows whether generic labels were preserved, and records simple runtime metadata so repeated tests can be compared under controlled conditions.

## Example Result

<p align="center">
  <img src="docs/images/two-model-b001-success.png" alt="Successful two-model WebUI result for B001 phenyl R-group" width="500"/>
</p>

The screenshot shows `B001_phenyl_R.png`, a phenyl ring with an R-group placeholder. MolScribe returns an ordinary-looking output with a wildcard atom, while DECIMER preserves the generic label as `[R]`. The cards also show timing and system metadata for each model service.

## Project Technical Route

The project is intentionally simple and service-oriented:

1. `data/generate_dataset.py` generates molecule PNGs and metadata, including ordinary molecules and Markush-like placeholders drawn into the image.
2. Each model runs in its own FastAPI container with the same `/health` and `/predict` contract.
3. The React/Vite WebUI uploads one image to each default model service in parallel.
4. Each result card displays the returned SMILES, render attempt, generic-symbol detection, prediction duration, container hostname, and platform string.
5. Docker Compose starts only the stable default services: MolScribe, DECIMER, and WebUI.

The default stack avoids databases, authentication, queues, and GPUs. This keeps the benchmark reproducible on a laptop and makes model-level differences easier to inspect.

## Quick Start

```bash
git clone https://github.com/alkali210/markush-benchmark.git
cd markush-benchmark
docker-compose up --build
# open http://localhost:5173
```

The default Compose stack starts MolScribe, DECIMER, and the Vite WebUI only. Model caches are persisted in the named Docker volume `model-cache`; MolScribe uses the HuggingFace cache path and DECIMER 2.x uses `/root/.data/DECIMER-V2` under the mounted `/root/.data` path.

## First-Run Note

MolScribe and DECIMER model weights are downloaded automatically on first start. The first `docker-compose up --build` may take 20-40 minutes depending on network speed. Subsequent starts are fast because weights are cached in the named `model-cache` volume.

## Generating The Test Dataset

```bash
pip install rdkit-pypi Pillow cairosvg
cd data && python generate_dataset.py
```

On newer Python or NumPy installations, RDKit may need an older NumPy ABI:

```bash
py -3.11 -m pip install "numpy<2" rdkit-pypi Pillow cairosvg
py -3.11 data/generate_dataset.py
```

The script writes PNG files to `data/images/` and updates `data/metadata.json`. The current generator includes baseline A-C records plus generated complex Markush records in category D.

## Default Model

### MolScribe

MolScribe is an image-to-graph molecular structure recognition model. The paper describes it as explicitly predicting atoms, bonds, and geometric layouts from molecular images, rather than treating the task only as image-to-string translation.[^molscribe-paper] This benchmark uses MolScribe as a strong modern OCSR baseline and checks whether its graph-oriented output preserves generic atom symbols in Markush-like drawings.

### DECIMER

DECIMER is an open optical chemical structure recognition platform for extracting chemical structures from images and documents. The DECIMER.ai publication describes a deep-learning platform for automated OCSR workflows, including chemical image classification and structure recognition components.[^decimer-paper] In this benchmark, DECIMER is useful because it often returns a directly comparable SMILES string and can sometimes preserve bracketed generic labels such as `[R]`.

## API Contract

Each default model service exposes the same endpoints:

- `GET /health` returns JSON with service status and whether the model is loaded.
- `POST /predict` accepts `multipart/form-data` field `file` and always returns JSON.

`/predict` returns the model output plus simple runtime telemetry:

```json
{
  "smiles": "CC(=O)Oc1ccccc1C(=O)O",
  "confidence": null,
  "error": null,
  "model": "DECIMER",
  "duration_ms": 1234,
  "runtime": {
    "hostname": "container-hostname",
    "platform": "Linux-..."
  }
}
```

`duration_ms` is the server-side prediction duration for that model request. `runtime.hostname` and `runtime.platform` identify the container host name and operating platform used for the prediction.

## Experimental Optional Model: MarkushGrapher-2

MarkushGrapher-2 is an experimental optional dedicated Markush recognizer and remains useful for future experiments, but it is not loaded by the default Compose stack. Its official repository describes MarkushGrapher-2 as an end-to-end multimodal model for recognizing molecular and Markush structures from chemical document images.[^markushgrapher-repo] The Hugging Face model card similarly presents it as a patent-document model that jointly encodes visual and textual information.[^markushgrapher-hf]

It is not enabled by default because the CPU pipeline is resource-heavy, downloads multiple large model assets, and can block the API process during inference. Keep it isolated from default benchmark runs unless you are explicitly testing that model.

## Extending Other Models

Other OCSR models can be integrated through the same adapter layer: create `services/<model>-api/`, implement `GET /health` and `POST /predict`, return the same JSON fields as the default services, then explicitly add the service to `docker-compose.yml` and `webui/src/api/client.js`. Test new models in a separate branch or temporary Compose override first, then decide whether their startup time, checkpoint handling, and CPU latency are stable enough for the default UI.

Minimal adapter shape:

```python
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    start = time.perf_counter()
    try:
        # 1. Save the uploaded image to tempfile
        # 2. Call the model's inference API
        # 3. Return smiles/confidence/error/model/duration_ms/runtime
        return {"smiles": smiles, "confidence": None, "error": None, "model": "NewModel"}
    except Exception as exc:
        return {"smiles": None, "confidence": None, "error": str(exc), "model": "NewModel"}
```

Compose usually needs an explicit port, cache volume, and longer `start_period`:

```yaml
newmodel-api:
  build: ./services/newmodel-api
  ports: ["8004:8004"]
  volumes:
    - newmodel-cache:/root/.cache/newmodel
  healthcheck:
    test: ["CMD-SHELL", "curl -sf http://localhost:8004/health || exit 1"]
    interval: 30s
    timeout: 10s
    retries: 10
    start_period: 180s
```

### Img2Mol

Img2Mol is a molecular image recognition project released by Bayer.[^img2mol-repo] A typical integration clones the official repository, installs CPU PyTorch, installs the package, and wraps its image-to-SMILES inference call in FastAPI.

Possible issues:

- The upstream dependency and checkpoint distribution path is fragile; the checkpoint may need a manual download or pinned URL.
- Some versions depend on external CDDD or remote resources, which can produce empty responses, closed connections, or long blocking calls inside containers.
- The project is not always maintained like a modern Python package, so `pip install -e .`, import paths, and checkpoint paths may need manual fixes.
- Treat it as a best-effort service: if the checkpoint is missing, `/health` can still return 200, while `/predict` should return a clear JSON error instead of blocking the whole Compose stack.

### OSRA

OSRA is an older rule-based/traditional image-processing OCSR tool.[^osra-site] It is easiest to wrap as a command-line binary: install or compile OSRA in the Dockerfile, save the uploaded image, run `osra <image>`, and parse stdout as SMILES.

Possible issues:

- Installation is system-package heavy and may involve ImageMagick, Ghostscript, OCR, or graphics libraries.
- It may be less robust than modern neural models on noisy or complex images.
- Markush generic labels are likely to be ignored, misread, or converted into ordinary elements, so use it as a historical baseline rather than a Markush-aware model.

### MolNexTR

MolNexTR is a newer end-to-end molecular structure recognition model. A practical integration usually clones the research code, downloads weights, installs the exact PyTorch/dependency versions, and wraps the inference script.[^molnextr-repo]

Possible issues:

- Research code can be sensitive to CUDA assumptions, dependency versions, relative paths, and checkpoint filenames.
- If the project only exposes script-style inference, stabilize the command-line invocation before wrapping it as a FastAPI service.
- The output may not be direct SMILES, so a graph-to-SMILES or post-processing step may be needed.

### MarkushGrapher-2

MarkushGrapher-2 is closer to this benchmark's target because it is intended for Markush and patent-document recognition, but it has a much higher deployment cost. Keep it as an optional experimental service unless you are explicitly testing it.

Possible issues:

- First startup downloads several large model assets, and CPU loading/inference can be slow.
- The model may expect multimodal document context or prompts, not only a cropped molecule image.
- If synchronous inference blocks the Uvicorn worker, host-side `/health` and `/predict` can time out.
- Move inference into a background thread/process or queue before considering WebUI integration.

## Known Issues

See issues as they arise.

- `rdkit-pypi` had no wheel for the local Python 3.14 interpreter used during validation. Python 3.11 worked.
- `rdkit-pypi==2022.9.5` emitted NumPy ABI errors with NumPy 2.x. Installing `numpy<2` resolved the issue.
- `docker compose config` warns that the top-level `version` key is obsolete in modern Compose v2. It is retained to match the project specification.
- `npm install` reports upstream dependency vulnerabilities through transitive packages. They do not block the Vite build for this benchmark UI.
- MolScribe 1.1.1 expects a local checkpoint file. The service downloads `swin_base_char_aux_1m.pth` from `yujieq/MolScribe` with `huggingface_hub` before loading the model.
- DECIMER 2.x stores model files under `/root/.data/DECIMER-V2`; concurrent imports during first download can corrupt the partial zip, so let the service finish startup before manually importing DECIMER inside the same container.
- The most common issues when adding a new model are stale checkpoint URLs, missing cache volume mounts, slow CPU inference, import paths that differ from upstream examples, and forgotten WebUI CORS or port wiring.

## Browser Validation

The WebUI sends one `POST /predict` request to MolScribe and one to DECIMER for each upload. The captured example above was produced through Chrome against the running Docker Compose stack.

[^wipo-markush]: WIPO, "Markush searches in PATENTSCOPE", https://www.wipo.int/documents/d/patentscope/docs-en-markush-searches.pdf

[^molscribe-paper]: Qian et al., "MolScribe: Robust Molecular Structure Recognition with Image-to-Graph Generation", *Journal of Chemical Information and Modeling*, https://pubs.acs.org/doi/10.1021/acs.jcim.2c01480

[^decimer-paper]: Rajan et al., "DECIMER.ai: an open platform for automated optical chemical structure identification, segmentation and recognition in scientific publications", *Nature Communications*, https://www.nature.com/articles/s41467-023-40782-0

[^markushgrapher-repo]: DS4SD, "MarkushGrapher", https://github.com/DS4SD/MarkushGrapher

[^markushgrapher-hf]: docling-project, "MarkushGrapher-2", https://huggingface.co/docling-project/MarkushGrapher-2

[^img2mol-repo]: Bayer Science for a Better Life, "Img2Mol", https://github.com/bayer-science-for-a-better-life/Img2Mol

[^osra-site]: OSRA: Optical Structure Recognition Application, https://cactus.nci.nih.gov/osra/

[^molnextr-repo]: MolNexTR, https://github.com/CYF2000127/MolNexTR
