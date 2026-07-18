# 🛡️ CyberRAG

AI-powered Cybersecurity Knowledge Assistant.

CyberRAG is a Retrieval-Augmented Generation (RAG) project that enables users to query cybersecurity knowledge using natural language. The goal of the MVP is to provide grounded answers from trusted cybersecurity datasets with proper citations.

---

## 🚀 Current Project Status

This project is currently under development.

Completed:
- Project initialization
- Python virtual environment
- Project structure
- Configuration system
- FastAPI backend setup
- Streamlit frontend setup

---

## 🎯 MVP Goals

- Query cybersecurity knowledge using natural language
- Retrieve relevant documents from a vector database
- Generate grounded responses using an LLM
- Provide citations for retrieved information

---

## 📂 Project Structure

```
cyber-rag/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── evaluation/
│   ├── ingestion/
│   ├── llm/
│   ├── models/
│   ├── retrieval/
│   └── ui/
│
├── storage/
│   ├── datasets/
│   ├── vectorstore/
│   ├── cache/
│   └── exports/
│
├── docs/
├── scripts/
├── tests/
│
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🛠️ Technology Stack

### Backend
- FastAPI
- Uvicorn

### Frontend
- Streamlit

### Language
- Python 3.13

### LLM
- OpenRouter

### Planned Vector Database
- ChromaDB

### Planned Embedding Model
- Sentence Transformers

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
cd cyber-rag
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Backend

```bash
uvicorn app.api.main:app --reload
```

---

## ▶️ Running the Frontend

```bash
streamlit run app/ui/app.py
```

---

## 📈 Project Roadmap

- ✅ Environment Setup
- ✅ FastAPI Backend
- ✅ Streamlit Frontend
- ⬜ Data Ingestion
- ⬜ Embeddings
- ⬜ Vector Database
- ⬜ Retrieval Pipeline
- ⬜ OpenRouter Integration
- ⬜ Evaluation

---

## 📄 License

For educational and research purposes.
