import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware


MODEL_NAME = "MarkushGrapher-2"
REPO_DIR = Path("/app/MarkushGrapher")
INFERENCE_SCRIPT = REPO_DIR / "scripts/inference/inference.sh"
MODEL_DIR = REPO_DIR / "models/markushgrapher-2"
OCR_MODEL_DIR = REPO_DIR / "models/chemicalocr"
MOLSCRIBE_CHECKPOINT = REPO_DIR / "external/MolScribe/ckpts/swin_base_char_aux_1m680k.pth"
MODEL_REQUIRED_FILES = ("config.json",)
OCR_REQUIRED_FILES = ("config.json", "preprocessor_config.json")
WEIGHT_FILES = ("model.safetensors", "pytorch_model.bin", "tf_model.h5", "model.ckpt.index", "flax_model.msgpack")
MOLSCRIBE_MIN_BYTES = 100_000_000


def missing_required_files(directory, filenames):
    return [str(directory / filename) for filename in filenames if not (directory / filename).exists()]


def missing_weight_file(directory):
    if any((directory / filename).exists() for filename in WEIGHT_FILES):
        return []
    return [str(directory / ("{" + ",".join(WEIGHT_FILES) + "}"))]


def directory_has_files(directory):
    return directory.exists() and any(path.is_file() for path in directory.rglob("*"))


def should_download_directory(directory):
    return not directory_has_files(directory)


def availability_error():
    missing = []
    if not INFERENCE_SCRIPT.exists():
        missing.append(str(INFERENCE_SCRIPT))
    missing.extend(missing_required_files(MODEL_DIR, MODEL_REQUIRED_FILES))
    missing.extend(missing_weight_file(MODEL_DIR))
    missing.extend(missing_required_files(OCR_MODEL_DIR, OCR_REQUIRED_FILES))
    missing.extend(missing_weight_file(OCR_MODEL_DIR))
    if not MOLSCRIBE_CHECKPOINT.exists() or MOLSCRIBE_CHECKPOINT.stat().st_size < MOLSCRIBE_MIN_BYTES:
        missing.append(str(MOLSCRIBE_CHECKPOINT))
    if missing:
        return "MarkushGrapher-2 is not available: missing " + ", ".join(missing)
    return None


def ensure_runtime_assets():
    MODEL_DIR.parent.mkdir(parents=True, exist_ok=True)
    if should_download_directory(MODEL_DIR):
        subprocess.run(["hf", "download", "docling-project/MarkushGrapher-2", "--local-dir", str(MODEL_DIR)], check=False, timeout=1800)
    if should_download_directory(OCR_MODEL_DIR):
        subprocess.run(["hf", "download", "docling-project/ChemicalOCR", "--local-dir", str(OCR_MODEL_DIR)], check=False, timeout=1800)
    if not MOLSCRIBE_CHECKPOINT.exists() or MOLSCRIBE_CHECKPOINT.stat().st_size < MOLSCRIBE_MIN_BYTES:
        MOLSCRIBE_CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "wget",
                "-O",
                str(MOLSCRIBE_CHECKPOINT),
                "https://huggingface.co/yujieq/MolScribe/resolve/main/swin_base_char_aux_1m680k.pth",
            ],
            check=False,
            timeout=1800,
        )


def newest_prediction_file(before):
    inference_root = REPO_DIR / "data/hf/inference"
    if not inference_root.exists():
        return None
    candidates = [
        path
        for path in inference_root.glob("*/evaluation/predictions*.jsonl")
        if path.stat().st_mtime >= before
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def read_prediction(path):
    if path is None or not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            return data.get("cxsmiles") or data.get("cxsmiles_opt") or data.get("prediction")
    return None


app = FastAPI(title="MarkushGrapher-2 API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": availability_error() is None}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    temp_dir = None
    try:
        unavailable = availability_error()
        if unavailable:
            ensure_runtime_assets()
            unavailable = availability_error()
        if unavailable:
            return {"smiles": None, "confidence": None, "error": unavailable, "model": MODEL_NAME}

        temp_dir = tempfile.mkdtemp(prefix="markushgrapher-")
        image_dir = Path(temp_dir) / "images"
        image_dir.mkdir(parents=True, exist_ok=True)
        suffix = os.path.splitext(file.filename or "image.png")[1] or ".png"
        image_path = image_dir / f"input{suffix}"
        image_path.write_bytes(await file.read())

        before = __import__("time").time()
        result = subprocess.run(
            ["bash", str(INFERENCE_SCRIPT), str(image_dir), "--max_eval_samples", "1"],
            cwd=str(REPO_DIR),
            capture_output=True,
            text=True,
            timeout=1800,
        )
        if result.returncode != 0:
            message = (result.stderr or result.stdout or "MarkushGrapher-2 inference failed").strip()
            return {"smiles": None, "confidence": None, "error": message[-2000:], "model": MODEL_NAME}

        prediction = read_prediction(newest_prediction_file(before))
        if not prediction:
            return {
                "smiles": None,
                "confidence": None,
                "error": "MarkushGrapher-2 inference completed but no predictions were produced.",
                "model": MODEL_NAME,
            }
        return {"smiles": prediction, "confidence": None, "error": None, "model": MODEL_NAME}
    except Exception as exc:
        return {"smiles": None, "confidence": None, "error": str(exc), "model": MODEL_NAME}
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
