# ⚖️ Droit du Travail RAG

> **FR** | [EN below](#english-version)

Assistant juridique conversationnel spécialisé dans le **Code du travail français** et le **RGPD**, alimenté par Claude (Anthropic) et une architecture RAG (Retrieval-Augmented Generation).

---

## Table des matières

- [Ce que fait le projet](#ce-que-fait-le-projet)
- [Architecture](#architecture)
- [Installation et démarrage rapide](#installation-et-démarrage-rapide)
- [Déploiement sur Hugging Face Spaces](#déploiement-sur-hugging-face-spaces)
- [Passer en mode Production (données Legifrance)](#passer-en-mode-production)
- [Structure du projet](#structure-du-projet)
- [English Version](#english-version)


---

## Ce que fait le projet

L'utilisateur pose une question en français sur ses droits au travail ou les obligations RGPD. Le système :

1. **Encode** la question avec `dangvantuan/sentence-camembert-large` (embeddings optimisés pour le français)
2. **Récupère** les 5 articles les plus pertinents depuis un index FAISS
3. **Génère** une réponse via Claude, en citant explicitement les articles utilisés
4. **Affiche** la réponse + un expander « Voir les sources » avec les chunks bruts

### Exemples de questions

- _« Quelle est la durée légale du travail en France ? »_
- _« Comment fonctionne la rupture conventionnelle ? »_
- _« Quels sont mes droits en matière de congés payés ? »_
- _« Quelles sont les sanctions RGPD pour une fuite de données ? »_

---

## Architecture

```
Utilisateur
    │  question (fr)
    ▼
┌─────────────────────────────────────────────────────────┐
│  app.py  (Streamlit)                                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │  chain.py  (RAGChain)                            │   │
│  │                                                  │   │
│  │  retriever.py ──► FAISS index                   │   │
│  │       │           (faiss_index/)                │   │
│  │       │ top-5 chunks                            │   │
│  │       ▼                                         │   │
│  │  ChatAnthropic (Claude)                         │   │
│  │       │ réponse + citations                     │   │
│  └───────┼──────────────────────────────────────────┘   │
└──────────┼──────────────────────────────────────────────┘
           │
           ▼
     Réponse affichée
     + Expander sources
```

**Stack technique :**

| Composant | Technologie |
|-----------|-------------|
| LLM | Claude (claude-sonnet-4-5) via `langchain-anthropic` |
| Embeddings | `dangvantuan/sentence-camembert-large` via `sentence-transformers` |
| Vector store | FAISS (`faiss-cpu`) |
| Orchestration | LangChain LCEL |
| Interface | Streamlit 1.41 |
| Données démo | 30 articles fictifs mais réalistes (Code du travail + RGPD) |

---

## Installation et démarrage rapide

### Prérequis

- Python 3.11+
- Une clé API Anthropic ([console.anthropic.com](https://console.anthropic.com))

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/Sana7Codes/RAG_juridique_fr.git
cd droit-travail-rag

# 2. Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la clé API
cp .env.example .env
# Éditer .env et renseigner ANTHROPIC_API_KEY=sk-ant-...

# 5. Créer l'index FAISS (mode démo, ~2 minutes au premier lancement)
python ingest.py

# 6. Lancer l'application
streamlit run app.py
```

L'application est disponible sur **http://localhost:8501**.

### Options d'`ingest.py`

```bash
python ingest.py           # idempotent : skip si index existant
python ingest.py --force   # recrée l'index même s'il existe
```

### Avec Docker

```bash
# Build (télécharge le modèle d'embedding + crée l'index FAISS)
docker build -t droit-travail-rag .

# Run (passer la clé API)
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=sk-ant-... droit-travail-rag
```


### Instructions

Dans `ingest.py`, décommenter le bloc **PRODUCTION MODE** (lignes ~30–80). Ce bloc contient :

1. Les URLs de téléchargement des PDFs Legifrance
2. La fonction `load_legifrance_pdfs()` qui parse les PDFs avec PyMuPDF
3. Le découpage automatique par article via regex sur les patterns `Article L\d+-\d+`

Puis remplacer dans `build_index()` :

```python
# AVANT (démo)
articles = get_sample_articles()

# APRÈS (production)
articles = load_legifrance_pdfs(LEGIFRANCE_PDFS)
```

Reconstruire l'index :

```bash
python ingest.py --force
```

> **Note :** Les URLs Legifrance peuvent nécessiter une mise à jour. Consulter [legifrance.gouv.fr](https://www.legifrance.gouv.fr) pour les liens actuels. L'API DILA (data.gouv.fr) fournit également un accès structuré au Code du travail au format JSON.

---

## Structure du projet

```
rag_droit_fr/
├── data/
│   └── sample_articles.py  # 30 articles fictifs pour le mode démo
├── faiss_index/            # Créé par ingest.py (ignoré par Git)
│   ├── index.faiss
│   └── index.pkl
├── ingest.py               # Chunking + embedding + sauvegarde FAISS
├── retriever.py            # Chargement index + similarité search
├── chain.py                # Chaîne RAG LangChain + Claude
├── app.py                  # Interface Streamlit
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

---

# English Version

## ⚖️ Droit du Travail RAG

A conversational legal assistant specialized in **French Labour Law** (Code du travail) and **GDPR**, powered by Claude (Anthropic) and a RAG (Retrieval-Augmented Generation) architecture.

## What it does

Users ask questions in French about their employment rights or GDPR obligations. The system:

1. **Encodes** the question using `dangvantuan/sentence-camembert-large` (French-optimized embeddings)
2. **Retrieves** the 5 most relevant article chunks from a FAISS vector index
3. **Generates** a formal French answer via Claude, explicitly citing the articles used
4. **Displays** the answer + a collapsible "View sources" panel with raw retrieved chunks

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env: ANTHROPIC_API_KEY=sk-ant-...

# Build FAISS index (demo mode, ~2 min first run)
python ingest.py

# Launch
streamlit run app.py
```


## Production Mode (Real Legifrance Data)

Uncomment the **PRODUCTION MODE** block in `ingest.py` to download and parse real Legifrance PDFs using PyMuPDF. The block includes full parsing code with regex-based article splitting.

---



*Ce projet est un démonstrateur pédagogique. Il ne constitue pas un avis juridique. Consultez un professionnel du droit pour tout conseil officiel.*
# RAG_juridique_fr
