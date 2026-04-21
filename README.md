# FinFraud Investigation Agent

An agentic AI system that autonomously investigates B2B payment fraud, scores risk using machine learning, and generates Suspicious Activity Reports (SARs).

> **Evolved from:** [P2P Anomaly Detection](https://carolinjames-p2p-anomaly-detection-ui.hf.space) — a rule-based fraud detector. This system upgrades that foundation into a full agentic investigation pipeline.

## Why Agentic? The Business Case

Traditional fraud detection systems flag transactions and stop there. A compliance analyst then has to manually pull vendor history, cross-check purchase orders, retrieve similar past cases, and write a report — a process that can take hours per case.

This system replaces that manual workflow with an autonomous agent that makes its own decision on whether to auto-approve, escalate for human review, or deep-investigate based on risk level. It calls specialized tools only when needed, retrieves semantically similar past fraud cases from a vector database to inform its reasoning, and produces a structured SAR report that a compliance officer can act on immediately.

**The business impact:**

| Without Agent | With Agent |
|---|---|
| Analyst reviews every flagged invoice | LOW risk cases are auto-approved without human intervention |
| Manual PO cross-check (15–30 min) | Automated in milliseconds |
| SAR written from scratch | Auto-generated, structured, ready to file |
| No pattern matching against past cases | RAG retrieves top 3 similar confirmed frauds |
| Binary flag: fraud or not | Three-tier risk scoring with explainability |

## LangGraph Decision Flow

```
START
  │
  ▼
validate_invoice
  │
  ▼
detect_anomalies
  │
  ▼
get_ml_score
  │
  ▼
decide_risk_level
  │
  ├── LOW ──────────────► auto_approve
  │
  ├── MEDIUM ───────────► flag_for_human_review
  │
  └── HIGH ────────────► investigate_deep
                              │
                    ┌─────────┼──────────┬─────────────┐
                    ▼         ▼          ▼             ▼
             similar_cases  vendor_   cross_ref_   generate_
                           history       po         sar_report
                    │         │          │             │
                    └─────────┴──────────┴─────────────┘
                                    │
                                   END
```

**Why LangGraph over a simple chain?**

A standard LLM chain runs every step for every invoice. LangGraph gives conditional routing — the deep investigation and tool calls only trigger when the risk level warrants it. This mirrors how a real compliance team operates: not every invoice deserves a full audit.

The `decide_risk_level` node evaluates ML score alongside anomaly type and routes accordingly. Phantom deliveries and duplicate invoices always force HIGH regardless of score because those are binary indicators of fraud, not probabilistic ones.

## Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph |
| LLM | OpenAI GPT-4o |
| ML model | Random Forest (scikit-learn) |
| Vector store | ChromaDB (persistent) |
| Embeddings | sentence-transformers all-MiniLM-L6-v2 |
| Backend | FastAPI |
| Frontend | Streamlit (dark theme) |

## Fraud Detection Coverage

| Anomaly Type | Detection Logic | Risk |
|---|---|---|
| Phantom Delivery | gr_amount equals 0 | Always HIGH |
| Duplicate Invoice | Same vendor and PO within 7 days | Always HIGH |
| Overbilling | invoice_amount exceeds po_amount | ML scored |
| New Vendor Risk | is_new_vendor true with amount above $10,000 | ML scored |

## ML Model

Algorithm: Random Forest trained on 21,500 rows including 800 synthetic borderline MEDIUM cases to prevent binary score cliff.

**Top features by importance:**

| Feature | Importance |
|---|---|
| days_since_last_invoice | 0.374 |
| three_way_match | 0.338 |
| deviation_pct | 0.113 |
| is_new_vendor | 0.085 |
| gr_amount | 0.070 |

## RAG Knowledge Base

When an invoice reaches `investigate_deep`, the agent builds a semantic query from the invoice fields and retrieves grounded context from two sources:

**Case index** — 200 confirmed fraud cases embedded into ChromaDB using sentence-transformers. Each case is stored as a human-readable sentence covering anomaly type, vendor, amounts, deviation, and match status. The top 3 most semantically similar cases are retrieved for every HIGH risk investigation.

**Policy and contract documents** — vendor framework contracts, overbilling policy documents, and dispute logs are embedded and stored separately. The agent retrieves the 2 most relevant reference documents to ground the SAR in actual policy language rather than generic reasoning.

ChromaDB uses `PersistentClient` so all embeddings survive server restarts. The BERT embedding model pre-warms in a background thread on startup so the first investigation request is fast.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| POST | /investigate | Full LangGraph agent pipeline |
| POST | /invoice | Legacy anomaly detection |
| POST | /explain | RAG explanation only |

## Test Scenarios

**HIGH — Phantom Delivery** (ml_score approximately 0.99)
```json
{
  "invoice_id": "INV-TEST-001", "vendor_id": "V-007",
  "vendor_name": "Apex Supplies", "vendor_category": "Logistics",
  "po_reference": "PO-9001", "po_amount": 50000, "invoice_amount": 50000,
  "gr_amount": 0, "deviation_pct": 0.0, "days_since_last_invoice": 3,
  "is_new_vendor": false, "three_way_match": false, "invoice_date": "2024-01-15"
}
```

**MEDIUM — Borderline Overbilling** (ml_score approximately 0.65)
```json
{
  "invoice_id": "INV-TEST-MED", "vendor_id": "V-012",
  "vendor_name": "MidRange Supplies Co", "vendor_category": "Supply Chain",
  "po_reference": "PO-5005", "po_amount": 10000, "invoice_amount": 11800,
  "gr_amount": 11800, "deviation_pct": 0.18, "days_since_last_invoice": 10,
  "is_new_vendor": false, "three_way_match": false, "invoice_date": "2024-01-18"
}
```

**LOW — Clean Invoice** (ml_score approximately 0.04)
```json
{
  "invoice_id": "INV-TEST-002", "vendor_id": "V-008",
  "vendor_name": "TechParts Ltd", "vendor_category": "IT",
  "po_reference": "PO-1002", "po_amount": 5000, "invoice_amount": 4900,
  "gr_amount": 4900, "deviation_pct": -0.02, "days_since_last_invoice": 45,
  "is_new_vendor": false, "three_way_match": true, "invoice_date": "2024-01-20"
}
```

## Running Locally

```bash
git clone https://github.com/YOUR_USERNAME/finfraud-investigation-agent.git
cd finfraud-investigation-agent

pip install -r requirements.txt

cp .env.example .env
# Add your OPENAI_API_KEY to .env

uvicorn api:app --reload

# New terminal
streamlit run app.py
```

## Deploying to Railway

The backend and frontend are deployed as two separate Railway services from the same repository using separate Dockerfiles.

**Step 1 — Create a Railway account and install the CLI**
```bash
npm install -g @railway/cli
railway login
```

**Step 2 — Deploy the backend**

1. Go to [railway.app](https://railway.app) and click New Project
2. Select Deploy from GitHub repo and connect your repository
3. In service settings, set the custom Dockerfile path to `Dockerfile.backend`
4. Add environment variables in the Railway dashboard:
   - `OPENAI_API_KEY` — your OpenAI key
5. Railway will assign a public URL to the backend (e.g. `https://finfraud-api.up.railway.app`)

**Step 3 — Deploy the frontend**

1. In the same Railway project, click New Service
2. Connect the same repository again
3. Set the custom Dockerfile path to `Dockerfile.frontend`
4. Add environment variables:
   - `BACKEND_URL` — paste the backend URL from Step 2
5. Railway will assign a separate public URL for the Streamlit app

**Step 4 — Verify**

Visit the frontend URL, select a scenario, and click Investigate. The backend warms up the BERT model in the background on first start — subsequent requests are fast.

## Project Structure

```
api.py                        FastAPI backend
app.py                        Streamlit UI (dark theme)
agent.py                      LangGraph agent graph
state.py                      AgentState TypedDict
rag.py                        RAGExplainer (ChromaDB and sentence-transformers)
Dockerfile.backend            Backend container
Dockerfile.frontend           Frontend container
nodes/
  validate_node.py
  detect_node.py
  get_ml_score_node.py
  decide_risk_node.py
  auto_approve_node.py
  flag_for_review_node.py
  investigate_deep_node.py
tools/
  retrieve_similar_cases.py
  fetch_vendor_history.py
  cross_reference_po.py
  generate_sar_report.py
detectors/
  overbilling_detector.py
  duplicate_detector.py
  phantom_delivery_detector.py
  new_vendor_risk_detector.py
models/
  random_forest.joblib
  schemas.py
data/
  p2p_invoices.csv            21,500 rows including 800 synthetic MEDIUM cases
documents/                    Policy docs loaded into ChromaDB
```

## Evolution from v1

| | v1 P2P Anomaly Detection | v2 FinFraud Investigation Agent |
|---|---|---|
| Detection | Rule-based only | Rule-based with ML scoring |
| Decision | Binary flag | Three-tier routing (LOW, MEDIUM, HIGH) |
| Investigation | None | Autonomous deep investigation for HIGH risk |
| Output | Anomaly flag with RAG explanation | Full SAR report |
| Orchestration | None | LangGraph multi-node agent |
| Tools | None | 4 LLM-callable tools |

## Environment Variables

| Variable | Local | Production |
|---|---|---|
| `OPENAI_API_KEY` | .env file | Railway secret |
| `BACKEND_URL` | http://localhost:8000 | Railway backend URL |
