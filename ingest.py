r"""
ingest.py — Création de l'index vectoriel FAISS à partir des articles juridiques.

Utilisation :
    python ingest.py           # mode idempotent (skip si index existant)
    python ingest.py --force   # re-crée l'index même s'il existe déjà

Modes :
    DEMO (défaut)   : utilise data/sample_articles.py (30 articles fictifs)
    PRODUCTION      : décommenter le bloc ci-dessous pour utiliser les vrais
                      PDFs Legifrance.

════════════════════════════════════════════════════════════════════════
PRODUCTION MODE — Legifrance (décommenter pour activer)
════════════════════════════════════════════════════════════════════════

# 1. Installer les dépendances supplémentaires :
#    pip install pymupdf requests

# 2. URLs de téléchargement direct des PDFs Legifrance
#    (remplacer par les URLs officielles à jour depuis legifrance.gouv.fr) :
#
#    LEGIFRANCE_PDFS = [
#        {
#            "url": "https://www.legifrance.gouv.fr/download/pdf/code?id=LEGITEXT000006072050",
#            "name": "Code du travail — Partie législative",
#        },
#        {
#            "url": "https://www.legifrance.gouv.fr/download/pdf/code?id=LEGITEXT000006069565",
#            "name": "Code civil — extraits pertinents",
#        },
#    ]

# 3. Parsing des PDFs avec PyMuPDF :
#
#    import fitz  # PyMuPDF
#    import requests
#
#    def load_legifrance_pdfs(pdf_configs):
#        documents = []
#        for cfg in pdf_configs:
#            response = requests.get(cfg["url"], timeout=60)
#            with open(f"/tmp/{cfg['name']}.pdf", "wb") as f:
#                f.write(response.content)
#            doc = fitz.open(f"/tmp/{cfg['name']}.pdf")
#            full_text = ""
#            for page in doc:
#                full_text += page.get_text()
#            # Découpage par article (regex sur "Article L\d+-\d+")
#            import re
#            pattern = r"(Article [LRD]\d+-\d+(?:-\d+)?)"
#            parts = re.split(pattern, full_text)
#            for i in range(1, len(parts) - 1, 2):
#                article_num = parts[i].replace("Article ", "")
#                content = parts[i + 1].strip()
#                if len(content) > 50:  # ignorer les articles vides
#                    documents.append({
#                        "article_number": article_num,
#                        "title": f"Article {article_num}",
#                        "source": cfg["name"],
#                        "content": content[:2000],  # cap à 2000 chars
#                    })
#        return documents
#
#    # Remplacer la ligne `articles = get_sample_articles()` ci-dessous par :
#    # articles = load_legifrance_pdfs(LEGIFRANCE_PDFS)

════════════════════════════════════════════════════════════════════════
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# Ajouter le répertoire courant au path pour les imports relatifs
sys.path.insert(0, str(Path(__file__).parent))
from data.sample_articles import get_sample_articles

load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "dangvantuan/sentence-camembert-large"
INDEX_DIR = Path(__file__).parent / "faiss_index"
INDEX_FILE = INDEX_DIR / "index.faiss"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Fonctions ─────────────────────────────────────────────────────────────────


def index_exists() -> bool:
    """Vérifie si l'index FAISS existe déjà sur le disque."""
    return INDEX_FILE.exists()


def articles_to_documents(articles: list[dict]) -> list[Document]:
    """Convertit les dicts d'articles en objets LangChain Document."""
    docs = []
    for art in articles:
        content = (
            f"Article {art['article_number']} — {art['title']}\n\n{art['content']}"
        )
        doc = Document(
            page_content=content,
            metadata={
                "article_number": art["article_number"],
                "title": art["title"],
                "source": art["source"],
            },
        )
        docs.append(doc)
    return docs


def build_index(force: bool = False) -> None:
    """
    Construit et sauvegarde l'index FAISS.

    Args:
        force: Si True, recrée l'index même s'il existe déjà.
    """
    if index_exists() and not force:
        logger.info(
            "Index FAISS déjà présent dans '%s'. "
            "Utilisez --force pour reconstruire.",
            INDEX_DIR,
        )
        return

    if force and index_exists():
        logger.info("--force activé : reconstruction de l'index.")

    # ── 1. Chargement des articles ────────────────────────────────────────────
    logger.info("Chargement des articles juridiques (mode DÉMO)...")
    articles = get_sample_articles()
    logger.info("  %d articles chargés.", len(articles))

    documents = articles_to_documents(articles)

    # ── 2. Initialisation du modèle d'embedding ───────────────────────────────
    logger.info("Chargement du modèle d'embedding : %s", EMBEDDING_MODEL)
    logger.info("  (premier lancement : téléchargement depuis HuggingFace Hub...)")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # ── 3. Création de l'index FAISS ──────────────────────────────────────────
    logger.info("Création de l'index FAISS...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    # ── 4. Sauvegarde sur le disque ───────────────────────────────────────────
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))
    logger.info("Index FAISS sauvegardé dans '%s'.", INDEX_DIR)
    logger.info("Ingestion terminée — %d documents indexés.", len(documents))


# ── Point d'entrée ────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crée l'index FAISS pour le RAG Droit du Travail."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reconstruit l'index même s'il existe déjà.",
    )
    args = parser.parse_args()

    try:
        build_index(force=args.force)
    except Exception as exc:
        logger.error("Erreur lors de l'ingestion : %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
