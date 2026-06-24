import os
import platform
import socket
import tempfile
import time

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware


MODEL_NAME = "DECIMER"
predict_SMILES = None
model_error = None


def runtime_info():
    return {"hostname": socket.gethostname(), "platform": platform.platform()}


def elapsed_ms(start):
    return int((time.perf_counter() - start) * 1000)

try:
    from DECIMER import predict_SMILES as decimer_predict_SMILES

    predict_SMILES = decimer_predict_SMILES
except Exception as exc:
    model_error = str(exc)


app = FastAPI(title="DECIMER API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": predict_SMILES is not None}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    start = time.perf_counter()
    temp_path = None
    try:
        if predict_SMILES is None:
            raise RuntimeError(model_error or "DECIMER model is not loaded")

        suffix = os.path.splitext(file.filename or "image.png")[1] or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        smiles = predict_SMILES(temp_path)
        return {
            "smiles": smiles,
            "confidence": None,
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
