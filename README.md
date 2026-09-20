\# 🛠️ DevOps \& Cloud Infrastructure RAG Assistant



An end-to-end, production-grade Retrieval-Augmented Generation (RAG) assistant designed to answer complex technical queries regarding Docker containerization, Kubernetes orchestration, and Linux infrastructure configurations with deterministic grounding and source citations.



\---



\## 📌 Architecture Overview



The system ingests official technical documentation, splits it into semantic chunks, computes vector embeddings, and persists them into a local vector store. When a query is submitted via the web UI or REST API, the most relevant passages are retrieved and injected into a tailored system prompt served by a local Ollama LLM instance.



```text

+-------------------+      HTTP POST      +------------------------+

|                   |  ---------------->  |                        |

|  Streamlit UI     |                     |    FastAPI Backend     |

|  (Chat Interface) |  <----------------  |  (Lifespan Management) |

+-------------------+     JSON Response   +-----------+------------+

&#x20;                                                     |

&#x20;                        +----------------------------+----------------------------+

&#x20;                        |                                                         |

&#x20;                        v                                                         v

&#x20;         +-----------------------------+                           +-----------------------------+

&#x20;         |         ChromaDB            |                           |         Ollama LLM          |

&#x20;         |  (all-MiniLM-L6-v2 Embeds)  |                           |     (Llama 3.2 Engine)      |

&#x20;         +-----------------------------+                           +-----------------------------+

```



\---



\## 💻 Tech Stack



\- \*\*Large Language Model (LLM):\*\* Llama 3.2 (via local Ollama server)

\- \*\*Embedding Model:\*\* `sentence-transformers/all-MiniLM-L6-v2`

\- \*\*Vector Database:\*\* ChromaDB (persistent local storage)

\- \*\*Backend Framework:\*\* FastAPI, Uvicorn, Pydantic v2

\- \*\*Frontend Framework:\*\* Streamlit

\- \*\*Document Processing:\*\* PyPDF



\---



\## 📂 Project Structure



```text

rag-assistant-project/

├── data/

│   └── raw\_docs/             # Source technical PDFs (Docker, K8s, Linux)

│   └── vector\_store/         # Persisted ChromaDB vector embeddings

├── notebooks/

│   └── rag\_pipeline.ipynb    # Data loading, chunking, retrieval \& evaluation

├── backend/

│   ├── app/

│   │   ├── api/

│   │   │   └── routes/

│   │   │       └── query.py  # Endpoints: GET /health, POST /query

│   │   ├── core/

│   │   │   └── config.py     # Pydantic environment configuration

│   │   ├── schemas/

│   │   │   └── query.py      # QueryRequest \& QueryResponse Pydantic models

│   │   ├── services/

│   │   │   ├── retrieval.py  # ChromaDB query \& similarity search

│   │   └── main.py           # FastAPI entrypoint, lifespan startup \& CORS

│   ├── tests/

│   │   └── test\_query.py     # Automated pytest test cases (200 OK \& 422 Unprocessable)

│   ├── requirements.txt      # Backend pinned dependencies

│   └── .env.example          # Environment variables template

├── frontend/

│   ├── app.py                # Streamlit chat interface with source inspection

│   ├── api\_client.py         # HTTP client communicating with backend

│   ├── requirements.txt      # Frontend pinned dependencies

│   └── .env.example          # Frontend configuration template

├── .gitignore                # Production ignore patterns (caches, venvs, secrets)

└── README.md                 # Complete system documentation

```



\---



\## ⚙️ Environment Variables



\### Backend Configuration (`backend/.env`)

| Variable | Type | Default | Description |

| :--- | :--- | :--- | :--- |

| `OLLAMA\_BASE\_URL` | string | `http://localhost:11434` | Base endpoint of running Ollama service |

| `OLLAMA\_MODEL` | string | `llama3.2` | Local model name loaded in Ollama |

| `CHROMA\_PERSIST\_DIR` | string | `../data/vector\_store` | Path to persistent vector database directory |

| `EMBEDDING\_MODEL\_NAME` | string | `all-MiniLM-L6-v2` | SentenceTransformer model checkpoint |



\### Frontend Configuration (`frontend/.env`)

| Variable | Type | Default | Description |

| :--- | :--- | :--- | :--- |

| `API\_BASE\_URL` | string | `http://localhost:8000` | Target FastAPI backend URL |



\---



\## 🚀 Setup \& Execution Guide



\### 1. Prerequisites

\- Python 3.10 or 3.11 installed.

\- Ollama installed with the model pulled:

&#x20; ```bash

&#x20; ollama serve

&#x20; ollama run llama3.2

&#x20; ```



\### 2. Environment Activation \& Dependencies

```bash

\# Clone the repository

git clone \[https://github.com/MohamedElNoby/rag-assistant-app.git](https://github.com/MohamedElNoby/rag-assistant-app.git)

cd rag-assistant-app



\# Setup virtual environment (Miniconda or venv)

conda activate rag\_env



\# Install backend dependencies

pip install -r backend/requirements.txt

```



\### 3. Running the Backend Server

```bash

cd backend

uvicorn app.main:app --reload --port 8000

```

\- Interactive API Docs (Swagger UI): `http://localhost:8000/docs`

\- Health check status: `http://localhost:8000/health`



\### 4. Running the Frontend Interface

In a separate terminal window:

```bash

cd frontend

streamlit run app.py

```

\- Open your browser at `http://localhost:8501` to use the interactive assistant.



\---



\## 📡 API Reference \& cURL Example



\### `POST /query`

Submits a natural language technical question and returns a grounded answer with citations.



\#### Example Request:

```bash

curl -X POST "http://localhost:8000/query" \\

&#x20;    -H "Content-Type: application/json" \\

&#x20;    -d '{"question": "How do I list all running containers in Docker?"}'

```



\#### Example Response:

```json

{

&#x20; "answer": "To list all active containers, use the command `docker ps`. If you want to include stopped containers as well, pass the `-a` flag: `docker ps -a`.",

&#x20; "sources": \[

&#x20;   "docker\_overview.pdf (Page 1)"

&#x20; ]

}

```



\---



\## 📊 RAG Pipeline Evaluation (10 Sample Test Cases)



| # | Question | Retrieved Source | Answer Grounded? | Verdict |

| :--- | :--- | :--- | :---: | :---: |

| 1 | How to create a detached container in Docker? | `docker\_overview.pdf (Page 2)` | Yes | ✅ Correct |

| 2 | What command checks running containers? | `docker\_overview.pdf (Page 1)` | Yes | ✅ Correct |

| 3 | What is the core purpose of Docker Engine? | `docker\_overview.pdf (Page 1)` | Yes | ✅ Correct |

| 4 | How does Docker isolate applications? | `docker\_overview.pdf (Page 3)` | Yes | ✅ Correct |

| 5 | What is a Docker image? | `docker\_overview.pdf (Page 2)` | Yes | ✅ Correct |

| 6 | How do you run an interactive container? | `docker\_overview.pdf (Page 2)` | Yes | ✅ Correct |

| 7 | What is the role of Docker daemon? | `docker\_overview.pdf (Page 1)` | Yes | ✅ Correct |

| 8 | How do containers share host resources? | `docker\_overview.pdf (Page 3)` | Yes | ✅ Correct |

| 9 | How to expose container ports? | `docker\_overview.pdf (Page 2)` | Yes | ✅ Correct |

| 10 | What is Docker Hub used for? | `docker\_overview.pdf (Page 1)` | Yes | ✅ Correct |



\### Observed Failure Modes \& Mitigations:

\- \*\*Retrieval of generalized terms:\*\* Broad queries initially retrieved introductory paragraphs. \*\*Mitigation:\*\* Applied context filtering and top-4 retrieval with overlap.

\- \*\*Out-of-Scope Queries:\*\* Instructed the prompt explicitly: \*"State clearly that the information is not found in the context rather than generating speculative answers."\*

