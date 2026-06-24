FROM python:3.10-slim

RUN apt-get update && apt-get install -y libxrender1 libxext6 libgl1 libglib2.0-0 git curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt constraints.txt .
RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt -f https://download.pytorch.org/whl/torch_stable.html
COPY main.py .

EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
