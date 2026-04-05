# 🤖 AI Resume Matcher & Skill Gap Analyzer

A **production-ready SaaS web application** that uses AI to compare resumes against job descriptions and deliver match scores, skill gap analysis, and actionable improvement suggestions.

---

## ✨ Features

- **Secure Auth** — JWT + bcrypt registration & login
- **Resume Upload** — PDF, DOCX, TXT (≤5 MB) with drag-and-drop
- **Hybrid AI Scoring** — TF-IDF keyword matching + semantic sentence embeddings
  ```
  Final Score = 0.4 × keyword_score + 0.6 × semantic_score
  ```
- **Skill Gap Analysis** — matched skills vs. missing skills from 70+ curated skill vocabulary
- **Suggestions Engine** — actionable improvement tips per missing skill
- **Dashboard** — paginated history of past analyses with expandable detail cards

---

## 🗂️ Project Structure

```
RESUMEMATCHER/
├── .devcontainer/
│   └── devcontainer.json         # GitHub Codespaces config
├── backend/
│   ├── app/
│   │   ├── core/                 # Config, DB, Security (JWT)
│   │   ├── models/               # SQLAlchemy User & Result models
│   │   ├── routes/               # auth.py, match.py, results.py
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # file_parser, skill_extractor, matcher, suggestions
│   │   └── main.py               # FastAPI app entrypoint
│   ├── .env                      # Backend env vars (not committed)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                  # Axios client
│   │   ├── context/              # AuthContext
│   │   └── pages/                # Login, Register, Dashboard, Match
│   ├── nginx.conf                # Production nginx config
│   ├── Dockerfile                # Multi-stage build
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Quick Start — GitHub Codespaces (Recommended)

1. **Open in Codespaces** — click the green `Code` button → `Codespaces` → `New codespace`  
   The `.devcontainer` config auto-builds and launches everything.

2. The codespace will auto-run `docker compose up --build -d`

3. Ports `8000` (API) and `5173` (frontend) are forwarded automatically.

---

## 🖥️ Local Development (Docker Compose)

### Prerequisites
- Docker & Docker Compose v2+

### Steps

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd RESUMEMATCHER

# 2. Copy and edit the environment file (optional tweaks)
cp .env.example backend/.env

# 3. Build and start all services
docker compose up --build

# 4. Open the app
open http://localhost:5173
```

**API docs** are available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔧 Running Without Docker (Development)

### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set database URL (PostgreSQL must be running)
export DATABASE_URL=postgresql://resumeuser:resumepass@localhost:5432/resumematcher

# Start backend
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

---

## 📡 API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Register new user |
| POST | `/auth/login` | ❌ | Log in, receive JWT |
| POST | `/match` | ✅ JWT | Upload resume + job desc, get analysis |
| GET | `/results` | ✅ JWT | Paginated list of past results |
| GET | `/health` | ❌ | Health check |

---

## 🔐 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | PostgreSQL connection string |
| `SECRET_KEY` | — | JWT signing secret (min 32 chars) |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 | JWT expiry |
| `MAX_UPLOAD_SIZE_MB` | 5 | Max file upload size |
| `BACKEND_CORS_ORIGINS` | `["http://localhost:5173"]` | Allowed CORS origins |

---

## 🤖 AI / ML Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| TF-IDF Vectorizer | scikit-learn | Keyword-based cosine similarity |
| Sentence Embeddings | sentence-transformers | Semantic similarity (all-MiniLM-L6-v2) |
| Skill Extraction | Custom regex + skill list | Identify matched/missing skills |
| Suggestions | Rule-based | Actionable improvement advice |

---

## 🛡️ Security

- Passwords hashed with **bcrypt** (never stored in plaintext)
- **JWT** Bearer tokens with configurable expiry
- File type **whitelist** enforcement (PDF, DOCX, TXT only)
- **File size limit** (5 MB max)
- Input validation via **Pydantic** throughout

---

## 📜 License

MIT — free to use, modify, and distribute.
