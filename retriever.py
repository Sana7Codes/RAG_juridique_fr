"""
retriever.py — Chargement de l'index FAISS et recherche par similarité.

Expose :
    load_retriever()   → objet LegalRetriever
    LegalRetriever.get_relevant_chunks(query, k=5) → list[RetrievedChunk]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

# ── Configuration ─────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "dangvantuan/sentence-camembert-large"
INDEX_DIR = Path(__file__).parent / "faiss_index"
DEFAULT_K = 5


# ── Types ─────────────────────────────────────────────────────────────────────


@dataclass
class RetrievedChunk:
    """Un chunk récupéré depuis l'index avec son score de similarité."""

    article_number: str
    title: str
    source: str
    content: str
    score: float  # distance L2 normalisée (plus bas = plus similaire)

    def format_for_context(self) -> str:
        """Formate le chunk pour l'injection dans le prompt Claude."""
        return (
            f"[{self.source} — Article {self.article_number}] "
            f"{self.title}\n{self.content}"
        )

    def display_label(self) -> str:
        """Étiquette courte pour l'affichage dans l'UI."""
        return f"Article {self.article_number} ({self.source})"


# ── Classe principale ─────────────────────────────────────────────────────────


class LegalRetriever:
    """
    Encapsule le vectorstore FAISS et fournit une interface de recherche.

    Usage :
        retriever = LegalRetriever()
        chunks = retriever.get_relevant_chunks("durée légale travail", k=5)
    """

    def __init__(self, index_dir: Path | None = None) -> None:
        self._index_dir = index_dir or INDEX_DIR
        self._vectorstore: FAISS | None = None
        self._embeddings: HuggingFaceEmbeddings | None = None

    def _ensure_loaded(self) -> None:
        """Charge l'index et le modèle d'embedding si ce n'est pas déjà fait."""
        if self._vectorstore is not None:
            return

        index_file = self._index_dir / "index.faiss"
        if not index_file.exists():
            raise FileNotFoundError(
                f"Index FAISS introuvable dans '{self._index_dir}'. "
                "Veuillez exécuter : python ingest.py"
            )

        logger.info("Chargement du modèle d'embedding depuis le cache HuggingFace...")
        self._embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        logger.info("Chargement de l'index FAISS depuis '%s'...", self._index_dir)
        self._vectorstore = FAISS.load_local(
            str(self._index_dir),
            self._embeddings,
            allow_dangerous_deserialization=True,
        )
        logger.info("Index FAISS chargé avec succès.")

    def get_relevant_chunks(
        self,
        query: str,
        k: int = DEFAULT_K,
    ) -> list[RetrievedChunk]:
        """
        Recherche les k chunks les plus pertinents pour la requête.

        Args:
            query: Question de l'utilisateur (en français).
            k:     Nombre de chunks à retourner.

        Returns:
            Liste de RetrievedChunk triés par pertinence décroissante.

        Raises:
            FileNotFoundError: Si l'index FAISS n'existe pas.
        """
        self._ensure_loaded()

        results = self._vectorstore.similarity_search_with_score(query, k=k)  # type: ignore[union-attr]

        chunks = []
        for doc, score in results:
            meta = doc.metadata
            chunks.append(
                RetrievedChunk(
                    article_number=meta.get("article_number", "N/A"),
                    title=meta.get("title", "Sans titre"),
                    source=meta.get("source", "Source inconnue"),
                    content=doc.page_content,
                    score=float(score),
                )
            )

        return chunks

    def get_indexed_documents(self) -> list[dict]:
        """
        Retourne la liste des documents indexés (pour l'affichage dans la sidebar).

        Returns:
            Liste de dicts {article_number, title, source}.
        """
        self._ensure_loaded()

        docs = []
        docstore = self._vectorstore.docstore  # type: ignore[union-attr]
        for doc_id in self._vectorstore.index_to_docstore_id.values():  # type: ignore[union-attr]
            doc = docstore.search(doc_id)
            if doc:
                docs.append(
                    {
                        "article_number": doc.metadata.get("article_number", "N/A"),
                        "title": doc.metadata.get("title", "Sans titre"),
                        "source": doc.metadata.get("source", "Source inconnue"),
                    }
                )

        # Trier par source puis par numéro d'article
        docs.sort(key=lambda d: (d["source"], d["article_number"]))
        return docs


# ── Singleton helper ──────────────────────────────────────────────────────────

_retriever_instance: LegalRetriever | None = None


def load_retriever() -> LegalRetriever:
    """
    Retourne une instance singleton de LegalRetriever.
    L'index est chargé paresseusement lors du premier appel.
    """
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = LegalRetriever()
    return _retriever_instance
