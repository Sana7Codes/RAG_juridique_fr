"""
chain.py — Chaîne RAG LangChain avec Claude comme LLM de génération.

Expose :
    RAGChain          — classe principale
    build_rag_chain() — factory retournant une instance prête à l'emploi
    GenerationResult  — dataclass portant la réponse + les sources
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from retriever import LegalRetriever, RetrievedChunk, load_retriever

logger = logging.getLogger(__name__)

# ── Configuration ─────────────────────────────────────────────────────────────

# Modèle par défaut. Modifier ici ou via la variable d'environnement
# CLAUDE_MODEL pour utiliser une autre version de Claude.
DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
DEFAULT_TOP_K = 5
MAX_TOKENS = 1024

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
Vous êtes un assistant juridique expert en droit du travail français et en RGPD. \
Votre rôle est d'aider les salariés et les employeurs à comprendre leurs droits \
et obligations.

RÈGLES ABSOLUES :
1. Répondez EXCLUSIVEMENT à partir du contexte juridique fourni ci-dessous.
2. Répondez toujours en français formel en vouvoyant l'utilisateur.
3. Citez systématiquement les numéros d'articles utilisés \
   (ex. : « Selon l'article L1221-1… », « En vertu de l'article RGPD - Article 6… »).
4. Si le contexte fourni ne contient pas la réponse, dites-le explicitement : \
   « Je ne dispose pas d'information suffisante dans les articles fournis \
   pour répondre à cette question. »
5. Ne jamais inventer de dispositions légales absentes du contexte.
6. Gardez votre réponse sous 200 mots.
7. Terminez CHAQUE réponse par la ligne : \
   « 📎 Sources : [liste des numéros d'articles effectivement cités] »

CONTEXTE JURIDIQUE :
{context}
"""

HUMAN_TEMPLATE = "Question : {question}"


# ── Types ─────────────────────────────────────────────────────────────────────


@dataclass
class GenerationResult:
    """Résultat d'une génération RAG."""

    answer: str
    sources: list[RetrievedChunk] = field(default_factory=list)
    model_used: str = ""

    @property
    def source_labels(self) -> list[str]:
        """Étiquettes courtes des sources pour l'affichage."""
        return [chunk.display_label() for chunk in self.sources]


# ── Classe principale ─────────────────────────────────────────────────────────


class RAGChain:
    """
    Chaîne RAG combinant :
      - LegalRetriever  : recherche vectorielle FAISS
      - ChatAnthropic   : génération avec Claude
    """

    def __init__(
        self,
        retriever: LegalRetriever | None = None,
        model: str = DEFAULT_MODEL,
        top_k: int = DEFAULT_TOP_K,
    ) -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "La variable d'environnement ANTHROPIC_API_KEY est manquante. "
                "Créez un fichier .env à partir de .env.example et "
                "renseignez votre clé API Anthropic."
            )

        self._retriever = retriever or load_retriever()
        self._model_name = model
        self._top_k = top_k

        self._llm = ChatAnthropic(
            model=model,
            anthropic_api_key=api_key,
            max_tokens=MAX_TOKENS,
            temperature=0.1,  # faible créativité pour un contexte juridique
        )

        logger.info(
            "RAGChain initialisée — modèle : %s, top_k : %d", model, top_k
        )

    # ── Méthode principale ────────────────────────────────────────────────────

    def invoke(self, question: str) -> GenerationResult:
        """
        Exécute le pipeline RAG complet pour une question.

        Pipeline :
            1. Récupère les top_k chunks les plus pertinents depuis FAISS
            2. Formate le contexte pour le system prompt
            3. Appelle Claude avec le contexte + la question
            4. Retourne la réponse + les chunks sources

        Args:
            question: Question de l'utilisateur en français.

        Returns:
            GenerationResult avec la réponse et les sources.

        Raises:
            FileNotFoundError : Index FAISS manquant.
            anthropic.APIError : Erreur côté API Anthropic.
        """
        # ── Étape 1 : Retrieval ───────────────────────────────────────────────
        logger.info("Retrieval pour : %r", question[:80])
        chunks = self._retriever.get_relevant_chunks(question, k=self._top_k)

        if not chunks:
            return GenerationResult(
                answer=(
                    "Je ne dispose d'aucun article juridique indexé pour "
                    "répondre à cette question. Veuillez vérifier que l'ingestion "
                    "a été exécutée correctement (python ingest.py)."
                ),
                sources=[],
                model_used=self._model_name,
            )

        # ── Étape 2 : Formatage du contexte ──────────────────────────────────
        context_parts = [
            f"--- Extrait {i + 1} ---\n{chunk.format_for_context()}"
            for i, chunk in enumerate(chunks)
        ]
        context_text = "\n\n".join(context_parts)

        # ── Étape 3 : Construction des messages ───────────────────────────────
        system_content = SYSTEM_PROMPT.format(context=context_text)
        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=HUMAN_TEMPLATE.format(question=question)),
        ]

        # ── Étape 4 : Génération ──────────────────────────────────────────────
        logger.info("Appel Claude (%s)...", self._model_name)
        response = self._llm.invoke(messages)
        answer = response.content

        if not isinstance(answer, str):
            # Claude retourne parfois une liste de blocs de contenu
            answer = "".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in answer
            )

        logger.info("Génération terminée (%d caractères).", len(answer))

        return GenerationResult(
            answer=answer,
            sources=chunks,
            model_used=self._model_name,
        )

    @property
    def indexed_documents(self) -> list[dict]:
        """Délègue à retriever.get_indexed_documents() pour la sidebar."""
        return self._retriever.get_indexed_documents()


# ── Factory ───────────────────────────────────────────────────────────────────

_chain_instance: RAGChain | None = None


def build_rag_chain(
    model: str = DEFAULT_MODEL,
    top_k: int = DEFAULT_TOP_K,
    force_rebuild: bool = False,
) -> RAGChain:
    """
    Retourne une instance singleton de RAGChain.

    Args:
        model:         Identifiant du modèle Claude à utiliser.
        top_k:         Nombre de chunks à récupérer.
        force_rebuild: Si True, recrée l'instance même si elle existe déjà.
    """
    global _chain_instance
    if _chain_instance is None or force_rebuild:
        _chain_instance = RAGChain(model=model, top_k=top_k)
    return _chain_instance
