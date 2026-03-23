"""
app.py — Interface Streamlit pour le chatbot RAG Droit du Travail.

Lancement : streamlit run app.py
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ── Chargement de l'environnement ─────────────────────────────────────────────
load_dotenv()

# ── Configuration de la page (DOIT être le premier appel Streamlit) ───────────
st.set_page_config(
    page_title="⚖️ Droit du Travail RAG",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "**Droit du Travail RAG** — Assistant juridique alimenté par Claude.\n\n"
            "Ce projet est un démonstrateur pédagogique. "
            "Il ne constitue pas un avis juridique."
        )
    },
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Répertoire de sauvegarde des conversations ────────────────────────────────
CONVERSATIONS_DIR = Path(__file__).parent / "conversations"
CONVERSATIONS_DIR.mkdir(exist_ok=True)


# ── CSS personnalisé ──────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
        :root {
            --primary: #1a3a5c;
            --accent:  #c8a84b;
        }
        .app-header {
            background: linear-gradient(135deg, var(--primary) 0%, #2c5282 100%);
            color: white;
            padding: 1.25rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .app-header h1 { margin: 0; font-size: 1.6rem; }
        .app-header p  { margin: 0.25rem 0 0; opacity: 0.85; font-size: 0.9rem; }
        .source-badge {
            display: inline-block;
            background: #edf2f7;
            color: #2d3748;
            border-radius: 4px;
            padding: 0.15rem 0.5rem;
            font-size: 0.78rem;
            margin: 0.1rem 0.15rem;
        }
        .legal-disclaimer {
            background: #fffbeb;
            border-left: 3px solid var(--accent);
            padding: 0.6rem 0.9rem;
            border-radius: 0 6px 6px 0;
            font-size: 0.82rem;
            color: #744210;
            margin-top: 0.5rem;
        }
        .session-ended {
            text-align: center;
            padding: 3rem 1rem;
            color: #4a5568;
        }
        .session-ended h2 { color: var(--primary); }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Persistance des conversations ─────────────────────────────────────────────


def _conversation_path(conv_id: str) -> Path:
    return CONVERSATIONS_DIR / f"{conv_id}.json"


def save_conversation(conv_id: str, messages: list[dict]) -> None:
    """Sauvegarde la conversation courante dans un fichier JSON."""
    if not messages:
        return
    payload = {
        "id": conv_id,
        "saved_at": datetime.now().isoformat(),
        "messages": messages,
    }
    _conversation_path(conv_id).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_conversation(conv_id: str) -> list[dict]:
    """Charge une conversation depuis le disque. Retourne [] si introuvable."""
    path = _conversation_path(conv_id)
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("messages", [])
    except Exception:
        return []


def list_saved_conversations() -> list[dict]:
    """
    Retourne la liste des conversations sauvegardées, triées par date décroissante.
    Chaque élément : {id, saved_at, preview, message_count}
    """
    convs = []
    for f in sorted(CONVERSATIONS_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            # Extraire la première question utilisateur comme aperçu
            preview = next(
                (m["content"][:60] + "…" for m in data["messages"] if m["role"] == "user"),
                "Conversation vide",
            )
            convs.append(
                {
                    "id": data["id"],
                    "saved_at": data.get("saved_at", ""),
                    "preview": preview,
                    "message_count": len(data["messages"]),
                }
            )
        except Exception:
            continue
    return convs


def delete_conversation(conv_id: str) -> None:
    path = _conversation_path(conv_id)
    if path.exists():
        path.unlink()


# ── Session state helpers ─────────────────────────────────────────────────────


def _init_session() -> None:
    """Initialise toutes les clés de session_state au premier chargement."""
    if "conv_id" not in st.session_state:
        st.session_state.conv_id = datetime.now().strftime("conv_%Y%m%d_%H%M%S")
    if "messages" not in st.session_state:
        # Tentative de reprise de la dernière conversation sauvegardée
        st.session_state.messages = load_conversation(st.session_state.conv_id)
    if "session_ended" not in st.session_state:
        st.session_state.session_ended = False


def _new_conversation() -> None:
    """Sauvegarde la conversation courante et en démarre une nouvelle."""
    save_conversation(st.session_state.conv_id, st.session_state.messages)
    st.session_state.conv_id = datetime.now().strftime("conv_%Y%m%d_%H%M%S")
    st.session_state.messages = []
    st.session_state.session_ended = False


def _end_session() -> None:
    """Sauvegarde et marque la session comme terminée."""
    save_conversation(st.session_state.conv_id, st.session_state.messages)
    st.session_state.session_ended = True


def _load_past_conversation(conv_id: str) -> None:
    """Sauvegarde la conversation courante et charge une ancienne."""
    save_conversation(st.session_state.conv_id, st.session_state.messages)
    st.session_state.conv_id = conv_id
    st.session_state.messages = load_conversation(conv_id)
    st.session_state.session_ended = False


# ── Helpers ───────────────────────────────────────────────────────────────────


def _check_api_key() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _check_index() -> bool:
    return (Path(__file__).parent / "faiss_index" / "index.faiss").exists()


@st.cache_resource(show_spinner=False)
def get_chain():
    """Initialise et met en cache la chaîne RAG (chargée une seule fois)."""
    from chain import build_rag_chain
    return build_rag_chain()


# ── Sidebar ───────────────────────────────────────────────────────────────────


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### ⚖️ Droit du Travail RAG")
        st.caption("Assistant juridique — Démo")

        st.divider()

        # ── Contrôles de conversation ─────────────────────────────────────────
        st.markdown("**Conversation**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "✨ Nouvelle",
                use_container_width=True,
                help="Sauvegarde la conversation actuelle et en démarre une nouvelle",
            ):
                _new_conversation()
                st.rerun()
        with col2:
            if st.button(
                "🚪 Terminer",
                use_container_width=True,
                help="Sauvegarde et termine la session",
            ):
                _end_session()
                st.rerun()

        n_msgs = len(st.session_state.get("messages", []))
        st.caption(f"Session actuelle : {n_msgs // 2} échange(s)")

        st.divider()

        # ── Conversations sauvegardées ────────────────────────────────────────
        st.markdown("**Historique**")
        past = list_saved_conversations()

        # Exclure la conversation courante de la liste
        current_id = st.session_state.get("conv_id", "")
        past = [c for c in past if c["id"] != current_id]

        if not past:
            st.caption("Aucune conversation sauvegardée.")
        else:
            for conv in past[:8]:  # afficher les 8 dernières
                saved_dt = conv["saved_at"][:16].replace("T", " ") if conv["saved_at"] else ""
                label = f"🗂 {saved_dt}"
                with st.expander(label, expanded=False):
                    st.caption(conv["preview"])
                    st.caption(f"{conv['message_count'] // 2} échange(s)")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button(
                            "Charger",
                            key=f"load_{conv['id']}",
                            use_container_width=True,
                        ):
                            _load_past_conversation(conv["id"])
                            st.rerun()
                    with c2:
                        if st.button(
                            "Suppr.",
                            key=f"del_{conv['id']}",
                            use_container_width=True,
                        ):
                            delete_conversation(conv["id"])
                            st.rerun()

        st.divider()

        # ── Informations modèle ───────────────────────────────────────────────
        st.markdown("**Modèle de génération**")
        model_name = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
        st.code(model_name, language=None)

        st.markdown("**Modèle d'embedding**")
        st.code("sentence-camembert-large", language=None)

        st.markdown("**Chunks récupérés**")
        st.code("top-5 par similarité cosine", language=None)

        st.divider()

        # ── Documents indexés ─────────────────────────────────────────────────
        st.markdown("**Documents indexés**")

        if not _check_index():
            st.warning("Index FAISS non trouvé.\n\nExécutez :\n```\npython ingest.py\n```")
        else:
            try:
                chain = get_chain()
                docs = chain.indexed_documents
                sources: dict[str, list] = {}
                for doc in docs:
                    sources.setdefault(doc["source"], []).append(doc)
                for source_name, source_docs in sources.items():
                    with st.expander(f"📚 {source_name} ({len(source_docs)})", expanded=False):
                        for doc in source_docs:
                            st.markdown(
                                f"<span class='source-badge'>Art. {doc['article_number']}</span>",
                                unsafe_allow_html=True,
                            )
            except Exception as exc:
                st.error(f"Impossible de lister les documents : {exc}")

        st.divider()

        st.markdown(
            "<div class='legal-disclaimer'>"
            "⚠️ Démonstrateur pédagogique uniquement.<br>"
            "Ce chatbot ne dispense pas de conseil juridique. "
            "Consultez un avocat ou l'inspection du travail pour "
            "tout avis juridique officiel."
            "</div>",
            unsafe_allow_html=True,
        )


# ── Écran de fin de session ───────────────────────────────────────────────────


def render_session_ended() -> None:
    st.markdown(
        """
        <div class="session-ended">
            <h2>⚖️ Session terminée</h2>
            <p>Votre conversation a été sauvegardée.<br>
            Vous pouvez la retrouver dans l'<strong>Historique</strong> de la barre latérale.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Démarrer une nouvelle conversation", use_container_width=True):
            _new_conversation()
            st.rerun()


# ── Page principale ───────────────────────────────────────────────────────────


def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
            <h1>⚖️ Droit du Travail RAG</h1>
            <p>Posez vos questions sur le Code du travail français et le RGPD</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_history() -> None:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander("🔍 Voir les sources récupérées", expanded=False):
                    for i, chunk in enumerate(msg["sources"], 1):
                        st.markdown(
                            f"**Source {i} — {chunk['display_label']}** "
                            f"*(score : {chunk['score']:.4f})*"
                        )
                        st.text(chunk["content"])
                        if i < len(msg["sources"]):
                            st.divider()


def handle_user_input(user_input: str) -> None:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Recherche des articles pertinents et génération de la réponse..."):
            try:
                chain = get_chain()
                result = chain.invoke(user_input)

                st.markdown(result.answer)

                if result.sources:
                    with st.expander("🔍 Voir les sources récupérées", expanded=False):
                        for i, chunk in enumerate(result.sources, 1):
                            st.markdown(
                                f"**Source {i} — {chunk.display_label()}** "
                                f"*(score : {chunk.score:.4f})*"
                            )
                            st.text(chunk.content)
                            if i < len(result.sources):
                                st.divider()

                serialized_sources = [
                    {
                        "article_number": c.article_number,
                        "title": c.title,
                        "source": c.source,
                        "content": c.content,
                        "score": c.score,
                        "display_label": c.display_label(),
                    }
                    for c in result.sources
                ]
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result.answer,
                        "sources": serialized_sources,
                    }
                )

                # Auto-save après chaque réponse
                save_conversation(st.session_state.conv_id, st.session_state.messages)

            except FileNotFoundError as exc:
                error_msg = (
                    f"**Erreur : Index FAISS introuvable.**\n\n"
                    f"Veuillez exécuter `python ingest.py`.\n\nDétail : `{exc}`"
                )
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg, "sources": []}
                )

            except EnvironmentError as exc:
                error_msg = (
                    f"**Erreur de configuration.**\n\n{exc}\n\n"
                    f"Créez un fichier `.env` avec votre clé `ANTHROPIC_API_KEY`."
                )
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg, "sources": []}
                )

            except Exception as exc:
                error_msg = (
                    f"**Erreur inattendue.**\n\n"
                    f"Type : `{type(exc).__name__}`\n\nMessage : `{exc}`"
                )
                st.error(error_msg)
                logger.error("Erreur lors de la génération", exc_info=True)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg, "sources": []}
                )


def render_example_questions() -> None:
    if st.session_state.messages:
        return

    st.markdown("#### Essayez ces questions :")
    examples = [
        "Quelle est la durée légale du travail en France ?",
        "Comment fonctionne la rupture conventionnelle ?",
        "Quels sont mes droits en matière de congés payés ?",
        "Qu'est-ce que le SMIC et comment est-il calculé ?",
        "Quelles sont les obligations d'un employeur en matière de RGPD ?",
        "Quelle est la durée maximale de travail quotidienne ?",
    ]
    cols = st.columns(2)
    for i, example in enumerate(examples):
        if cols[i % 2].button(f"💬 {example}", key=f"example_{i}", use_container_width=True):
            handle_user_input(example)
            st.rerun()


def render_prereq_warnings() -> bool:
    all_ok = True
    if not _check_api_key():
        st.error(
            "**Clé API Anthropic manquante.**\n\n"
            "Créez un fichier `.env` et définissez :\n"
            "```\nANTHROPIC_API_KEY=sk-ant-...\n```"
        )
        all_ok = False
    if not _check_index():
        st.warning(
            "**Index FAISS non trouvé.**\n\n"
            "```bash\npython ingest.py\n```\nPuis rechargez cette page."
        )
        all_ok = False
    return all_ok


# ── Point d'entrée principal ──────────────────────────────────────────────────


def main() -> None:
    _init_session()
    render_sidebar()

    # Écran de fin de session
    if st.session_state.session_ended:
        render_session_ended()
        return

    render_header()

    if not render_prereq_warnings():
        st.stop()

    render_chat_history()
    render_example_questions()

    if user_input := st.chat_input(
        "Posez votre question sur le droit du travail ou le RGPD...",
        key="chat_input",
    ):
        handle_user_input(user_input)


if __name__ == "__main__":
    main()
