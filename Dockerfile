# ════════════════════════════════════════════════════════════════════════════
# Droit du Travail RAG — Dockerfile
# Base : python:3.11-slim
# Port : 8501 (Streamlit)
#
# Note HuggingFace Spaces :
#   - Sur HF Spaces, l'ANTHROPIC_API_KEY doit être défini dans
#     Settings > Repository secrets (pas dans ce fichier).
#   - Le modèle d'embedding est mis en cache dans /root/.cache/huggingface
#     grâce au layer RUN ci-dessous (évite le re-téléchargement à chaque start).
# ════════════════════════════════════════════════════════════════════════════

FROM python:3.11-slim

# ── Variables d'environnement système ────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Évite les invites interactives apt
    DEBIAN_FRONTEND=noninteractive \
    # Répertoire de cache HuggingFace (persisté dans HF Spaces)
    HF_HOME=/root/.cache/huggingface \
    TRANSFORMERS_CACHE=/root/.cache/huggingface/transformers

# ── Répertoire de travail ─────────────────────────────────────────────────────
WORKDIR /app

# ── Dépendances système ───────────────────────────────────────────────────────
# libgomp1 : requis par faiss-cpu pour OpenMP
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
        git \
    && rm -rf /var/lib/apt/lists/*

# ── Dépendances Python ────────────────────────────────────────────────────────
# Copier requirements.txt en premier pour profiter du cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copie des sources ─────────────────────────────────────────────────────────
COPY . .

# ── Pré-téléchargement du modèle d'embedding (layer mis en cache) ─────────────
# Cela évite un long téléchargement au premier démarrage de l'application.
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
print('Téléchargement du modèle sentence-camembert-large...'); \
SentenceTransformer('dangvantuan/sentence-camembert-large'); \
print('Modèle téléchargé et mis en cache.')"

# ── Création de l'index FAISS (mode DÉMO) ────────────────────────────────────
# ingest.py est idempotent : si l'index existe déjà, cette étape est ignorée.
# La clé ANTHROPIC_API_KEY n'est PAS requise pour l'ingestion.
RUN python ingest.py

# ── Port Streamlit ────────────────────────────────────────────────────────────
EXPOSE 8501

# ── Healthcheck ───────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# ── Démarrage de l'application ────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
