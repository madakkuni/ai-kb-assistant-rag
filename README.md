# KB Assistant

Production-Grade Enterprise Knowledge Base Assistant powered by Hybrid RAG and LangGraph for accurate, citation-backed AI responses.

---

## 🚀 Overview

**KB Assistant RAG** is a **Production-Grade Enterprise Knowledge Base Assistant** designed to help users quickly search, retrieve, and understand enterprise documentation using **Advanced Retrieval-Augmented Generation (RAG)** architecture.

The system leverages **Hybrid Retrieval (BM25 + Vector Search)**, **Cross-Encoder Reranking**, and **LangGraph-based orchestration** to deliver **accurate, citation-backed, and context-aware responses** from enterprise knowledge base documents.

This project capable of ingesting large volumes of documents such as troubleshooting guides, operational runbooks, and knowledge base articles, and converting them into an intelligent conversational assistant.

---

### 🎯 Key Features

* **Hybrid Retrieval:** Combines BM25 and Vector Search (ChromaDB) for maximum context accuracy.
* **Cross-Encoder Reranking:** Ensures the most relevant document chunks are prioritized.
* **Citation Enforcement:** Every answer actively cites the source filename and chunk with clickable document links.
* **LangGraph Workflow:** Agentic and dynamic processing pipeline.
* **Evaluation Pipeline:** Measures Faithfulness, Context Precision, and Answer Relevance.
* **Observability:** Built-in Token Usage and Request Latency Tracking.
* **Stunning Modern UI:** Glassmorphism, smooth animations, dynamic gradients, and Dark/Light modes.
* **Document Upload Support:** End-to-end ingestion pipeline for modern documents (PDF, DOCX, TXT, MD).

---

## 🧠Architecture

<img title="" src="file:///C:/Users/Admin/Pictures/Typedown/5f0244e8-3360-4672-8fc6-8269cace2458.png" alt="5f0244e8-3360-4672-8fc6-8269cace2458" style="zoom:33%;">

##### Supporting Components (Background Services)

<img src="file:///C:/Users/Admin/Pictures/Typedown/a54c26e3-d363-466f-8837-b610a6127a64.png" title="" alt="a54c26e3-d363-466f-8837-b610a6127a64" style="zoom:33%;">

##### Observability & Logging Layer

<img src="file:///C:/Users/Admin/Pictures/Typedown/c4dd228b-03e6-4897-a755-c0be14064978.png" title="" alt="c4dd228b-03e6-4897-a755-c0be14064978" style="zoom:33%;">

---

## 🧠 Core Capabilities

### 🔎 Hybrid Retrieval (BM25 + Vector Search)

AI KB Assistant uses **Hybrid Retrieval** to improve search accuracy by combining:

* **BM25 Keyword Search** — Finds exact keyword matches
* **Vector Semantic Search** — Finds contextually similar content

By merging both approaches, the system ensures:

* Higher retrieval accuracy
* Better context understanding
* Reduced missed results
* Improved answer quality

This approach is widely used in **enterprise-grade RAG systems** where precision and reliability are critical.

---

### 🎯 Cross-Encoder Reranking

After retrieving documents, the system applies **Cross-Encoder Reranking** to identify the most relevant content.

Process:

1. Retrieve top documents using hybrid retrieval
2. Score documents using a cross-encoder model
3. Rank documents by relevance
4. Select top results for answer generation

Benefits:

* Improved response accuracy
* Reduced irrelevant context
* Better reasoning by LLM
* Higher quality responses

This significantly improves **answer precision** in enterprise environments.

---

### 📚 Citation Enforcement

AI KB Assistant enforces **source-backed responses** to ensure reliability and transparency.

Each response includes:

* Document source
* File name
* Page or section reference

Example:

Azure App Service timeout occurs due to request timeout configuration.  

Sources:  

- troubleshoot-azure-app-service.pdf (Page 4)  
- troubleshoot-azure-monitor.pdf (Page 2)

Benefits:

* Increased trust
* Reduced hallucinations
* Better auditability
* Enterprise compliance

---

### ⚡ LangGraph Workflow Orchestration

The system uses **LangGraph** to orchestrate a multi-step AI workflow:

User Query  
→ Hybrid Retrieval  
→ Reranker  
→ Answer Generator  
→ Citation Node  
→ Response

This modular pipeline enables:

* Better scalability
* Easier debugging
* Flexible architecture
* Production-ready workflow management

---

### 📊 Observability & Monitoring

AI KB Assistant includes **production-grade observability** to monitor system performance:

* Token usage tracking
* Query latency tracking
* Retrieval performance monitoring
* Model response time
* Error tracking

Metrics include:

* Token consumption
* Request volume

This enables **continuous optimization and performance tuning**.

---

### 📈 Evaluation Pipeline

The system evaluates response quality using key metrics:

* Faithfulness
* Context Precision
* Answer Relevance

Benefits:

* Measure response quality
* Detect performance regressions
* Improve retrieval accuracy
* Maintain production reliability

---

### 📄 Intelligent Document Ingestion

AI KB Assistant supports automated ingestion of knowledge base documents:

Supported Formats:

* PDF
* DOCX
* TXT
* Markdown

The ingestion pipeline:

* Loads documents
* Splits into chunks
* Generates embeddings
* Indexes into vector database
* Updates hybrid retriever

This allows seamless expansion of the knowledge base.

---

## 📂 Project Structure

```text
ai-kb-assistant-rag/
├── app/
│   ├── api/
│   │   └── endpoints.py         # Defines all API routes (/chat, /upload, /ingest-all, /metrics) 
│   │                            # and connects them to the backend workflow state logic.
│   ├── evaluation/
│   │   └── evaluator.py         # Implements the RAG evaluation pipeline to measure Faithfulness, 
│   │                            # Context Precision, and Answer Relevance.
│   ├── ingestion/
│   │   └── document_loader.py   # Handles parsing, chunking, and preparing incoming documents
│   │                            # (PDF, DOCX, TXT) for vector database ingestion.
│   ├── langgraph/
│   │   ├── nodes.py             # Contains the individual processing steps (retrieval, reranking,
│   │                            # generation, citation) executed within the LangGraph workflow.
│   │   ├── state.py             # Defines the TypedDict schema `RequestState` which dictates 
│   │                            # the data passed between nodes in the LangGraph orchestration.
│   │   └── workflow.py          # Orchestrates the connections between nodes to compile the 
│   │                            # final directed acyclic graph (DAG) for the RAG pipeline.
│   ├── reranker/
│   │   └── cross_encoder.py     # Implements a Cross-Encoder model to re-score and re-rank the 
│   │                            # initially retrieved documents for maximal relevance accuracy.
│   ├── retriever/
│   │   └── hybrid_retriever.py  # Combines sparse BM25 retrieval and dense vector search 
│   │                            # (ChromaDB) to fetch the most semantically relevant contexts.
│   ├── services/
│   │   └── tracking.py          # Manages observability by tracking request latencies, LLM 
│   │                            # token usage, and summarizing system-level metrics.
│   ├── utils/
│   │   ├── config.py            # Loads, types, and validates environment variables, API keys, 
│   │                            # and application configurations.
│   │   └── logger.py            # Configures structured application-wide logging to monitor 
│   │                            # background events and safely trace application errors.
│   └── main.py                  # Single entry point for the FastAPI application. Configures 
│                                # CORS, static file mounting, and registers all API routers.
├── frontend/
│   ├── css/style.css            # Contains custom CSS properties for the modern user interface, 
│   │                            # including dynamic gradients, glassmorphism, and animations.
│   ├── js/main.js               # Manages frontend logic, API communication with the FastAPI 
│   │                            # backend, parsing source citations, and typing animations.
│   └── index.html               # The main layout file for the responsive Chat UI, utilizing 
│                                # HTML5 and Bootstrap components.
├── data/documents/              # Directory where uploaded reference documents are stored.
├── vector_db/                   # Directory where ChromaDB operates its SQLite/persistent storage.
├── logs/                        # Dedicated directory outputting `app.log` and `metrics.json`.
├── README.md                    # Primary project overview, architecture insights, and setup manual.
└── requirements.txt             # Lists all the Python packages required to run the application.
```

---

## 📄 Detailed Module Explanations

### `app/main.py`

This is the **application entry point**. It initializes the FastAPI server, configures CORS middleware to accept cross-origin requests from the frontend, mounts static directories (to serve the UI and uploaded documents), and includes the main API router. It also features a global exception handler to gracefully catch unhandled exceptions and return standardized `500 Internal Server Error` JSON responses.

### `app/api/endpoints.py`

This controller file defines and handles all REST API routes for the application:

- `/chat`: Intercepts user queries, spawns the LangGraph orchestration pipeline (`rag_workflow`), tracks request latency and tokens, and returns the generated answer, source citations, and evaluation metrics.
- `/upload` / `/ingest-all`: Endpoints that trigger the document ingestion pipeline. They accept uploaded files, invoke the `DocumentIngestor`, and dynamically add chunks into the active retriever module.
- `/health` / `/metrics` / `/history`: Informational endpoints returning server status and observability data.

### `app/evaluation/evaluator.py`

Houses the `RAGEvaluator`, an automated metric evaluation class. It uses an LLM to score the system's generated output against the original query and retrieved context. It measures **Faithfulness** (are claims supported by context?), **Context Precision** (was retrieved context relevant?), and **Answer Relevance** (did it address the query?).

### `app/ingestion/document_loader.py`

The `DocumentIngestor` module is responsible for ETL. It supports parsing `.pdf`, `.docx`, `.txt`, and `.md` files. It reads raw text, splits it into smaller semantically robust chunks using LangChain text splitters (handling chunk sizes and overlap), attaches metadata, and prepares documents for ChromaDB.

### `app/langgraph/nodes.py`

Contains the discrete logical functions (nodes) that serve as building blocks for the RAG pipeline graph. Each function modifies the `RequestState`:

- **`hybrid_retrieval_node`**: Fetches initial context based on the query.
- **`reranker_node`**: Reorders contexts using a cross-encoder.
- **`answer_generator_node`**: Formats contexts into a prompt and calls the LLM.
- **`citation_node`**: Compiles a deduplicated list of source files used for the answer.
- **`evaluation_node`**: Triggers the `RAGEvaluator` if `eval_mode` is enabled.

### `app/langgraph/state.py`

Defines the `RequestState` `TypedDict`, which rigorously structures the payload flowing through the LangGraph application, enforcing types for `query`, `retrieved_docs`, `answer`, etc.

### `app/langgraph/workflow.py`

The orchestration engine. Initializes a `StateGraph`, adds all nodes from `nodes.py`, creates logical edges defining execution sequence (Retrieve → Rerank → Generate → Cite → Evaluate), and compiles the final executable `rag_workflow`.

### `app/reranker/cross_encoder.py`

Implements the `DocumentReranker`. To circumvent imprecise bi-encoder matching, this module feeds initial results into a `SentenceTransformer` cross-encoder model. It assesses the question and document simultaneously to output highly-accurate relevance scores, sorting out only the best chunks.

### `app/retriever/hybrid_retriever.py`

The `HybridRetriever` implements a two-path retrieval:

1. **Dense Vector Search:** Uses embeddings in a persistent ChromaDB vector store.
2. **Sparse BM25 Search:** Performs classic BM25 lexical keyword matching.
   It executes both, merges results to overcome solely relying on keywords or semantic similarity, and orchestrates live database updates.

### `app/services/tracking.py`

The `MetricsTracker` offers built-in observability. It intercepts outgoing LLM requests to calculate latency and extract prompt/completion token usage from API callbacks, persisting this data to `metrics.json` on disk to monitor performance anomalies.

### `app/utils/config.py`

Centralized app configuration. Utilizing Pydantic's `BaseSettings`, it strictly validates `.env` variables at runtime, ensuring the server instantly aborts if required parameters like `AZURE_OPENAI_API_KEY` are missing.

### `app/utils/logger.py`

Configures Python's standard library `logging` to output highly-readable, structured logs timestamped directly to the console and to an `app.log` file on disk for persistent auditing.

### `frontend/css/style.css`

A customized, responsive stylesheet. It implements a premium "Glassmorphism" design system utilizing subtle backdrop blurring, animated micro-interactions (floating bubbles, responsive hover-lifts), dynamic text gradients, and cleanly toggles Dark/Light theme palettes.

### `frontend/js/main.js`

The client-side brain. Parses user interactions, securely triggers REST fetch requests to `/api/chat` backend routes, maintains chat history continuity, and contains custom evaluation-mode toggling logic and typing animation simulators.

### `frontend/index.html`

The DOM layout. Structures the page using Bootstrap 5 as a lightweight grid framework, organizing the responsive off-canvas sidebars, metrics pop-ups, dynamically updating suggestion badges, and theme switches.

---

## 🏗️ Tech Stack

**Frontend**

* HTML5, Vanilla JavaScript, CSS3
* Bootstrap 5
* Modern UI (Glassmorphism, Gradient Accents, Hover Animations)

**Backend**

* Python 3.10+
* FastAPI & Uvicorn
* LangGraph & LangChain

**Database & AI Models**

* ChromaDB (Vector DB)
* Sentence Transformers & Cross Encoders
* GenAI LLMs (Azure OpenAI, OpenAI, or Local Support)

---

## 🛠️ End-to-End Setup Guide

Follow these steps to set up, configure, and run the AI KB Assistant locally.

### Step 1: Project Setup

1. **Navigate to the Project Directory:**
   
   ```bash
   cd c:\My_Projects\ai-kb-assistant-rag
   ```

2. **Create and Activate a Virtual Environment:**
   
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configuration

Create a `.env` file in the root directory. Ensure it contains the required keys (Example for Azure OpenAI):

```env
# .env file content example
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_chat_model_deployment
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
MODEL_NAME=azure-openai
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
RERANK_TOP_K=3
VECTOR_DB_PATH=vector_db
LOG_LEVEL=INFO
TEMPERATURE=0.0
```

### Step 3: Preparing Documents

Place your base documents (PDF, DOCX, TXT, Markdown) into the automatically mounted `data/documents/` folder:

```text
ai-kb-assistant-rag/
├── data/
│   └── documents/
│       ├── troubleshoot-azure-app-service.pdf
│       └── example.docx
```

### Step 4: Starting the Backend Server

Execute the following command from the root directory with the virtual environment activated:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 5: Bulk Ingesting the Documents

Once the backend is running, you need to ingest the documents so the RAG pipeline can retrieve them.
Open a **new terminal** (leave the backend running) and execute:

```bash
curl -X POST http://127.0.0.1:8000/api/ingest-all
```

Alternatively, open your browser and utilize the interactive Swagger UI at `http://127.0.0.1:8000/docs`.

### Step 6: Using the Assistant

Open your web browser and navigate to the application frontend: 
**http://127.0.0.1:8000/**

You can now start querying your local knowledge base. The application will fetch the precise answers, stream them beautifully to your screen, and cite the source files with clickable links!

---

**Project Goal:** Build a *Production-Ready Enterprise RAG System* demonstrating modern GenAI architecture, dynamic web presentation, and coding best practices.
