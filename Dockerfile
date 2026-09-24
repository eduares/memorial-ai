# =========================
# Memorial AI - Streamlit app
# =========================
FROM python:3.11-slim

# Evita prompts interativos e melhora logs do Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instala as dependências primeiro (melhor aproveitamento de cache)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do projeto
COPY . .

# Garante que as pastas de dados existam (são ignoradas pelo git)
RUN mkdir -p data/uploads data/processed

EXPOSE 8501

# Verifica se o Streamlit está respondendo
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=5 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://localhost:8501/_stcore/health').status==200 else sys.exit(1)"

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
