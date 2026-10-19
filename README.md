<div align="center">

# 🛠️ Intelligent IT Support Agent

**An AI-assisted help-desk demo that classifies IT tickets, retrieves troubleshooting evidence, and recommends next steps, with a full audit trail.**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-workflow-1C3C3C)
![scikit-learn](https://img.shields.io/badge/scikit--learn-classifier-F7931E?logo=scikitlearn&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-vector%20search-0467DF)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-learning%20%2F%20demo-blue)

</div>

> **In one sentence:** someone writes *"My VPN is not connecting"*, and the app guesses the problem category, searches a small library of troubleshooting notes, and suggests what to try next, or asks for more information when it is not sure.
>
> ⚠️ This is a **learning/demo project**, not a production support system. The training data is small and synthetic, and the diagnostics are simulated.

---

## Table of contents

- [Features](#-features)
- [Quick start](#-quick-start-windows)
- [How it works](#-how-it-works)
- [Architecture](#-architecture)
- [Tech stack](#-tech-stack)
- [Project structure](#-project-structure)
- [Detailed setup](#-detailed-setup-windows)
- [Using the app](#-using-the-app)
- [API reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Limitations](#-limitations)
- [Improving the project](#-improving-the-project)
- [Evaluation](#-evaluation)
- [Safety and privacy](#-safety-and-privacy)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 🏷️ | **Ticket classification** | TF-IDF + Logistic Regression predicts a category (`access_account`, `application`, `hardware`, `software`, `vpn_network`) with a confidence score |
| 🔎 | **Semantic search (RAG)** | Sentence Transformers + FAISS retrieve the most relevant troubleshooting passages from local Markdown articles |
| 🧭 | **Workflow orchestration** | LangGraph coordinates classification, retrieval, diagnostics and the final decision |
| 🧪 | **Safe simulated diagnostics** | Placeholder tools return example output and never touch real systems |
| 🙋 | **Asks when unsure** | Weak confidence or weak evidence leads to a request for more detail rather than a guess |
| 📜 | **Audit trail** | Every workflow step is listed so you can see how the answer was produced |
| 🌐 | **API + web UI** | FastAPI backend with interactive docs, and a Streamlit front end |

It helps organize and suggest. It does **not** replace an IT support engineer.

---

## 🚀 Quick start (Windows)

Requires **Python 3.11** and an internet connection (the embedding model is downloaded on first run).

```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. Train the classifier and build the knowledge index
python -m scripts.train_classifier
python -m scripts.build_knowledge_index

# 4. Start the backend (Terminal 1)
python -m uvicorn app.main:app --reload
```

Then, in a **second** terminal (with the venv activated):

```powershell
python -m streamlit run ui/streamlit_app.py
```

Open **http://localhost:8501**, enter a ticket, and click **Analyze ticket**.

> 💡 Seeing a PyTorch `c10.dll` / `WinError 1114` error? Jump to [PyTorch DLL error](#pytorch-c10dll--winerror-1114).

---

## 🧠 How it works

Think of the app as a junior helper with a small textbook:

1. **You describe the problem**, e.g. *"The VPN fails after I changed my password."*
2. **The classifier guesses** the likely category and reports a confidence score.
3. **The retriever opens the textbook.** Troubleshooting documents are turned into embeddings (lists of numbers that capture meaning) and searched for similar passages.
4. **The workflow combines everything.** LangGraph runs classification, retrieval and simulated diagnostics, then decides what to say next.
5. **You see the result:** predicted category, suggested priority, response, retrieved evidence, simulated diagnostics, and an audit trail.

> A confidence score is **not** a guarantee of correctness. If confidence or evidence is weak, the app may ask for more information.

---

## 🏗️ Architecture

```text
                 YOU / SUPPORT ENGINEER
                           |
                           v
                 Streamlit Web Interface
                    (ui/streamlit_app.py)
                           |
                           | HTTP request
                           v
                    FastAPI Backend
                     (app/main.py)
                           |
                           v
                    LangGraph Workflow
                    (app/agent/graph.py)
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
   ML Classifier      RAG Retriever    Simulated Tools
   TF-IDF +            Sentence         Safe placeholder
   Logistic            Transformers     diagnostics only
   Regression          + FAISS
          |                |
          +----------------+----------------+
                           |
                           v
               Decision and Response Builder
                           |
                           v
           Response + Evidence + Audit Trail
                           |
                           v
                 Streamlit Web Interface
```

<details>
<summary><b>What each component means</b></summary>

- **Streamlit:** the web page you interact with.
- **FastAPI:** receives the ticket from the page and returns the result.
- **ML classifier:** predicts a category using TF-IDF features and Logistic Regression.
- **RAG (Retrieval-Augmented Generation):** searches local troubleshooting documents and supplies relevant passages as evidence. In this starter the response can be a deterministic template, so RAG does not automatically mean an LLM is called.
- **Sentence Transformers:** turns text into embeddings so meaning can be compared.
- **FAISS:** efficiently finds similar embeddings (document chunks).
- **LangGraph:** organizes workflow steps and decisions.
- **Simulated diagnostics:** return example messages only. They do not inspect any real laptop, account, network or company system.
- **Audit trail:** lists the steps the workflow took.

</details>

---

## 🧰 Tech stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Main language |
| scikit-learn | TF-IDF and Logistic Regression classifier |
| pandas | Reads and handles the ticket CSV |
| Sentence Transformers | Text embeddings for semantic search |
| FAISS | Fast similarity search over document chunks |
| LangGraph | Ticket-analysis workflow |
| FastAPI + Uvicorn | Backend API and local server |
| Streamlit | Browser-based UI |
| pytest | Automated tests |

---

## 📁 Project structure

```text
intelligent-it-support-agent/
├── app/
│   ├── agent/                     # LangGraph workflow and optional LLM helper
│   ├── ml/                        # Ticket classifier and evaluation
│   ├── rag/                       # Chunking, embeddings and FAISS index
│   ├── tools/                     # Simulated diagnostic tools
│   ├── main.py                    # FastAPI routes
│   └── schemas.py                 # Request/response data models
├── data/
│   ├── tickets.csv                # Small synthetic labelled dataset
│   └── knowledge/                 # Markdown troubleshooting articles
├── scripts/
│   ├── train_classifier.py        # Train and evaluate the classifier
│   └── build_knowledge_index.py   # Build the searchable knowledge index
├── tests/                         # Starter automated tests
├── ui/
│   └── streamlit_app.py           # Web interface
├── .env.example                   # Example environment settings
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT License
└── README.md                      # This guide
```

Generated model and index files may be created when you run the scripts (their locations are defined in the code). Do not delete them while the app is running.

---

## ⚙️ Detailed setup (Windows)

### Requirements

- Windows 10 or 11
- **Python 3.11** (recommended for this setup)
- VS Code (recommended editor)
- Internet access for installing packages and the first-time model download
- A few GB of free disk space (ML packages and models can be large)

Check your Python version:

```powershell
python --version
```

It should show `3.11.x`. If `python` is not recognized, try `py -3.11 --version` and install Python 3.11 if needed.

### Step 1: Open the project

1. Download and extract the project ZIP (or clone the repository).
2. In VS Code choose **File → Open Folder** and select `intelligent-it-support-agent`.
3. Open **Terminal → New Terminal**. The prompt should end with the project folder, e.g. `PS D:\intelligent-it-support-agent>`.

### Step 2: Create and activate a virtual environment

A virtual environment keeps this project's packages separate from your other projects.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

The prompt should now start with `(.venv)`. In VS Code, press `Ctrl + Shift + P`, run **Python: Select Interpreter**, and choose the one ending in `.venv\Scripts\python.exe`.

<details>
<summary>PowerShell blocks activation?</summary>

Run this in that terminal only, then activate again. It does not permanently change your policy.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

</details>

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 4: Install CPU-only PyTorch (only if needed)

On the machine used to prepare these instructions, the default PyTorch install failed with a `c10.dll` / `WinError 1114` error, and the CPU-only PyTorch 2.8.0 build fixed it. If `import torch` already works for you, skip this step.

```powershell
python -m pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu
```

Verify:

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

Expected: a version like `2.8.0+cpu` and `False` (CUDA is not required for this demo).

> If you change dependency versions, re-run the tests and verify the application. Package compatibility changes over time.

### Step 5: Train the classifier

Run from the project root with `(.venv)` active:

```powershell
python -m scripts.train_classifier
```

Use the `-m` form. Running `python scripts/train_classifier.py` can cause `ModuleNotFoundError: No module named 'app'` because Python's import path differs.

The script prints metrics such as accuracy and macro-F1. With a small starter dataset, treat them as a basic sanity check, not real-world performance.

### Step 6: Build the knowledge index

```powershell
python -m scripts.build_knowledge_index
```

A successful run prints something similar to:

```text
Built FAISS index with 15 chunks.
```

The first run downloads a public Sentence Transformers model from Hugging Face, which may take a few minutes. A warning about unauthenticated requests is normally harmless, and no token is needed for the basic demo.

---

## 🖥️ Using the app

You need **two terminals** (use **Terminal → New Terminal** in VS Code) and must keep both open.

### Terminal 1: FastAPI backend

```powershell
python -m uvicorn app.main:app --reload
```

(`uvicorn app.main:app --reload` also works if the `uvicorn` command is on your path.)

Wait for `Application startup complete.` and `Uvicorn running on http://127.0.0.1:8000`.

| Page | URL |
|---|---|
| Interactive API docs | http://127.0.0.1:8000/docs |
| Health check | http://127.0.0.1:8000/health |

`http://127.0.0.1:8000/` may show `404 Not Found`. That is expected because no homepage route is defined, and it does not mean the backend failed.

### Terminal 2: Streamlit frontend

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run ui/streamlit_app.py
```

Open **http://localhost:8501**, enter a title and description, and select **Analyze ticket**.

### Try an example

| Field | Value |
|---|---|
| **Title** | VPN connection fails |
| **Description** | I cannot connect to the company VPN. It keeps timing out, and I cannot access internal applications. |

Also try a locked account or an overheating laptop. Predictions and confidence can vary because the starter dataset is small.

To stop either server, focus its terminal and press `Ctrl + C`.

---

## 🔌 API reference

With the backend running, open http://127.0.0.1:8000/docs for interactive documentation.

| Method | Route | Description |
|---|---|---|
| `POST` | `/tickets/analyze` | Analyze a ticket and return category, evidence, response and audit trail |
| `GET` | `/health` | Basic health check |
| `GET` | `/classifier/evaluate` | Run the classifier's holdout evaluation (if evaluation code and data are available) |

**Example request body for `POST /tickets/analyze`:**

```json
{
  "title": "VPN connection fails",
  "description": "I cannot connect to the company VPN. It keeps timing out after I changed my password."
}
```

**Call it from PowerShell:**

```powershell
$body = @{
  title       = "VPN connection fails"
  description = "I cannot connect to the company VPN. It keeps timing out."
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/tickets/analyze `
  -Method Post -ContentType "application/json" -Body $body
```

**Run the tests:**

```powershell
python -m pytest
```

---

## 🩹 Troubleshooting

### PyTorch `c10.dll` / `WinError 1114`

1. Confirm the project `.venv` interpreter is the one in use.
2. If Conda `(base)` is also active, run `conda deactivate` until `(base)` disappears, keeping `.venv` active.
3. Test with `python -c "import torch; print(torch.__version__)"`.
4. Install the CPU build from [Step 4](#step-4-install-cpu-only-pytorch-only-if-needed).
5. Install or repair the [Microsoft Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe), restart VS Code, and test again.

Avoid repeatedly reinstalling packages without checking the error message.

<details>
<summary><code>ModuleNotFoundError: No module named 'app'</code></summary>

Run scripts as modules from the project root:

```powershell
python -m scripts.train_classifier
python -m scripts.build_knowledge_index
```

Also confirm VS Code opened the root project folder, not just the `scripts` subfolder.

</details>

<details>
<summary><code>No module named scripts.build_index</code></summary>

The script is named `build_knowledge_index`:

```powershell
python -m scripts.build_knowledge_index
```

</details>

<details>
<summary><code>404 Not Found</code> at <code>http://127.0.0.1:8000/</code></summary>

Expected when no `/` route exists. Use `/docs` or `/health` instead.

</details>

<details>
<summary>Port 8000 or 8501 already in use</summary>

Stop the older server with `Ctrl + C` in its terminal. If necessary, start Uvicorn on another port:

```powershell
uvicorn app.main:app --reload --port 8001
```

Then update any frontend API URL setting that expects port 8000.

</details>

<details>
<summary>Streamlit page does not update</summary>

Save the file, wait for Streamlit to rerun, then hard-refresh the browser with `Ctrl + Shift + R`. If needed, stop Streamlit with `Ctrl + C` and start it again.

</details>

<details>
<summary>Hugging Face unauthenticated warning</summary>

Normally not fatal for public model downloads. Check that the download completes. Configure a token only if you need higher rate limits or a restricted model.

</details>

---

## 🚧 Limitations

- The CSV is a small **synthetic** starter dataset, not representative of real enterprise tickets.
- Model confidence can be low, and confidence is not accuracy.
- The classifier has **not** been shown to be reliable for production decisions.
- The knowledge base contains only a few example Markdown documents.
- Several retrieved chunks can come from one document, so the UI may show the same filename more than once.
- Diagnostics are **simulated**. They do not inspect devices, query identity systems, connect to a VPN, change infrastructure, or close tickets.
- The default response path can use deterministic templates. An LLM API is optional and not required.
- No production authentication, authorization, ticket database, role management, enterprise integrations, monitoring or deployment hardening is included.
- A human should review recommendations before they are used in a real support process.

---

## 📈 Improving the project

Better data is the most valuable improvement. Collect representative examples and label them consistently rather than adding many random sentences.

### A. Ticket-classification data (`data/tickets.csv`)

Inspect the existing column names and follow the same format when adding rows.

1. Collect many varied examples for every category: short and detailed messages, typos, and common technical wording.
2. Have a knowledgeable reviewer assign each label.
3. Keep categories reasonably balanced, or use an evaluation plan that accounts for imbalance.
4. Remove duplicates, personal information, passwords, MFA codes, tokens and confidential company data.
5. Split into training, validation and test sets **before** tuning. Keep related or duplicate tickets in the same split to avoid data leakage.
6. Retrain and compare metrics on a test set never used for training or tuning.

Current categories: `access_account`, `application`, `hardware`, `software`, `vpn_network`. Changing labels may require code updates.

**Suggested starting target:** a few hundred reviewed examples per category, then keep growing and diversifying. Quality and coverage matter more than raw row count.

### B. Knowledge base (`data/knowledge/`)

Add reviewed articles on topics such as password reset and lockouts, VPN issues, Wi-Fi and connectivity, laptop hardware problems, software installs and crashes, printers and peripherals, and approved escalation paths.

Suggested article template:

```markdown
# Article title

## Symptoms
What the user may observe.

## Safe checks
Checks a user is allowed to perform.

## Information to collect
Non-secret details useful for diagnosis.

## When to escalate
When support should take over.

## Source and review date
Authoritative source and when it was last reviewed.
```

Use accurate, authorized documentation. Never copy confidential internal material into a public repository. After changes, rebuild the index:

```powershell
python -m scripts.build_knowledge_index
```

### C. Retrieval quality

- Check whether the correct article appears in the top 3 or top 5 results for each test question.
- Track `Recall@k` / `Hit@k`.
- Tune chunk size and overlap per content type.
- Deduplicate chunks or show unique source filenames while keeping the separate chunks as evidence.
- Compare embedding models using the same fixed test questions.
- Consider metadata such as category, product, article version and review date.

### D. Confidence and decision-making

- Calibrate category probabilities on held-out data where appropriate.
- Choose confidence thresholds from measured validation results, not guesswork.
- Ask for more details when a ticket is ambiguous or retrieval is weak.
- Escalate uncertain or high-impact cases to a human.
- Test priority rules against explicit scenarios. The current priority is a heuristic, not a company SLA decision.

### E. Data quality and privacy

If you use real ticket data, get permission and follow company policy. Remove identifiers and secrets, store data securely, restrict access, and never upload confidential tickets to a public Git repository or an external model without approval.

---

## 📊 Evaluation

Do not judge the project on two or three hand-picked tickets. Build a repeatable test set with expected categories and expected knowledge sources, record a baseline, and re-run the same tests after every change.

| Area | What to measure |
|---|---|
| **Classification** | Accuracy; per-category precision, recall and F1; macro-F1; confusion matrix; performance on an untouched test set |
| **Retrieval** | Expected article in top 3 / top 5; whether the passage truly supports the recommendation; whether the source is current and authoritative |
| **Workflow** | Clear tickets; ambiguous tickets (should ask for info); low-confidence predictions; no relevant knowledge found; urgent cases (should escalate); the rule that **no real diagnostic or remediation action is executed** |

Never claim a metric you have not measured.

---

## 🔒 Safety and privacy

- Use synthetic examples while learning.
- Never enter real passwords, MFA codes, API keys, tokens or confidential company information.
- Diagnostics are simulated and must not be described as real system checks.
- Recommendations are suggestions, not guaranteed fixes.
- Do not connect real infrastructure or automate changes without authorization, testing, access controls, logging and a rollback plan.
- If you enable an optional LLM provider, review its data-handling policy and your organization's rules before sending ticket content.

---

## 🗺️ Roadmap

- [ ] **Data and evaluation:** improve labelled examples and create a fixed test set
- [ ] **Retrieval:** better articles, chunking, deduplication and source citations
- [ ] **Workflow:** explicit branches for missing information, low confidence and escalation
- [ ] **Testing:** API responses, workflow branches, retrieval quality and safety behavior
- [ ] **Persistence:** store demo tickets and outcomes in a database with privacy controls
- [ ] **Feedback loop:** reviewers mark predictions correct/incorrect; approved feedback improves future training data
- [ ] **Observability:** structured logs, latency tracking, error reporting, model/version metadata
- [ ] **Security:** authentication, authorization, input validation, rate limiting, secrets management
- [ ] **Integrations:** approved ticketing systems or read-only diagnostics first, with human approval for any change
- [ ] **Optional LLM responses:** grounded answers with visible citations, and measured unsupported-claim rates

---

## 📄 License

This project is released under the [MIT License](LICENSE).