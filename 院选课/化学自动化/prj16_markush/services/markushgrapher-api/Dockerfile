FROM python:3.10-slim

RUN apt-get update && apt-get install -y git curl wget libgl1 libglib2.0-0 libxrender1 libxext6 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone https://github.com/DS4SD/MarkushGrapher /app/MarkushGrapher

WORKDIR /app/MarkushGrapher
RUN pip install --no-cache-dir torch==2.2.0+cpu torchvision==0.17.0+cpu torchaudio==2.2.0+cpu --index-url https://download.pytorch.org/whl/cpu
RUN grep -Ev '^(torch|torchvision|torchaudio)==|^rdkit-pypi==' requirements.txt > /tmp/requirements.cpu.txt && \
    pip install --no-cache-dir -r /tmp/requirements.cpu.txt
RUN git clone https://github.com/lucas-morin/transformers.git ./external/transformers && \
    git clone https://github.com/lucas-morin/MolScribe.git ./external/MolScribe && \
    pip install --no-cache-dir -e ./external/MolScribe --no-deps && \
    PIP_USE_PEP517=0 pip install --no-cache-dir -e . --no-deps && \
    pip install --no-cache-dir "markushgenerator @ git+https://github.com/DS4SD/MarkushGenerator.git" && \
    pip install --no-cache-dir "numpy<2" "pyonmttok==1.37.1" "OpenNMT-py==2.2.0" && \
    pip install --no-cache-dir -e ./external/transformers
RUN pip install --no-cache-dir huggingface_hub fastapi "uvicorn[standard]" python-multipart

COPY main.py /app/main.py

WORKDIR /app
EXPOSE 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
