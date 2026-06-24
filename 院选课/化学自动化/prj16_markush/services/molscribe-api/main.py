import os
import platform
import socket
import tempfile
import time

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware


MODEL_NAME = "MolScribe"
model = None
model_error = None


def runtime_info():
    return {"hostname": socket.gethostname(), "platform": platform.platform()}


def elapsed_ms(start):
    return int((time.perf_counter() - start) * 1000)

try:
    from huggingface_hub import hf_hub_download
    import torch
    from molscribe import MolScribe

    checkpoint = hf_hub_download(repo_id="yujieq/MolScribe", filename="swin_base_char_aux_1m.pth")
    model = MolScribe(checkpoint, device=torch.device("cpu"))
except Exception as exc:  # Keep the service inspectable if model startup fails.
    model_error = str(exc)


app = FastAPI(title="MolScribe API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    start = time.perf_counter()
    temp_path = None
    try:
        if model is None:
            raise RuntimeError(model_error or "MolScribe model is not loaded")

        suffix = os.path.splitext(file.filename or "image.png")[1] or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        result = model.predict_image_file(temp_path)
        return {
            "smiles": result.get("smiles") if isinstance(result, dict) else None,
            "confidence": result.get("confidence") if isinstance(result, dict) else None,
            "error": None,
            "model": MODEL_NAME,
            "duration_ms": elapsed_ms(start),
            "runtime": runtime_info(),
        }
    except Exception as exc:
        return {
            "smiles": None,
            "confidence": None,
            "error": str(exc),
            "model": MODEL_NAME,
            "duration_ms": elapsed_ms(start),
            "runtime": runtime_info(),
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
