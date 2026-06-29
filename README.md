# 🎲 Side Quests

A personal adventure log for tracking spontaneous things to do — classes, experiences, outings, creative experiments. Filter by tags, search your list, or roll a random quest when you're not sure what to do next.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.11+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## What it does

- **Add side quests** with a title, description, and tags
- **Tag system** — create custom tags with colours (e.g. `paid`, `group`, `solo`, `go out`, `activity`)
- **Filter & search** — by text, tag (AND logic), or status
- **Randomise** — roll a random quest from your current filtered view
- **Status tracking** — mark quests as To do, Done, or Skipped

---

## Project structure

```
side-quests/
├── side_quests.html          # Frontend — single HTML file, runs in any browser
└── backend/
    ├── app/
    │   ├── main.py           # FastAPI app, CORS, router registration
    │   ├── database.py       # SQLAlchemy engine + session (SQLite / Postgres)
    │   ├── models.py         # Quest, Tag, quest_tags join table
    │   ├── schemas.py        # Pydantic request/response models
    │   └── routers/
    │       ├── quests.py     # /quests endpoints incl. /quests/random
    │       └── tags.py       # /tags endpoints
    ├── requirements.txt
    ├── Procfile              # Railway deploy command
    └── .env.example
```

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Vanilla HTML/JS | Zero build step, runs from a file |
| Backend | Python + FastAPI | Fast to write, automatic API docs at `/docs` |
| Database | SQLite (dev) / Postgres (prod) | SQLite locally with no config; same codebase switches via env var |
| Backend hosting | [Railway](https://railway.app) | Free tier, auto-deploys from GitHub, persistent disk |
| Frontend hosting | [Vercel](https://vercel.com) | Free tier, one-click deploy |

---

## Getting started

### Frontend only (no backend)

Open `side_quests.html` directly in a browser. Quests save to `localStorage` — no server needed.

### With the backend

**Requirements:** Python 3.11+

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy the example env file (SQLite is the default — no changes needed)
cp .env.example .env

# Start the API server
uvicorn app.main:app --reload
```

The API is running at **http://localhost:8000**
Interactive API docs at **http://localhost:8000/docs**

---

## API reference

### Quests

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/quests` | List all quests. Query params: `q` (search), `tags` (comma-separated IDs), `status` |
| `GET` | `/quests/random` | Random todo quest. Query param: `tags` |
| `GET` | `/quests/{id}` | Get a single quest |
| `POST` | `/quests` | Create a quest |
| `PATCH` | `/quests/{id}` | Update title, description, status, or tags |
| `DELETE` | `/quests/{id}` | Delete a quest |

**Create quest body:**
```json
{
  "title": "Take a pottery class",
  "description": "Find a drop-in studio session.",
  "tag_ids": ["tag-id-1", "tag-id-2"]
}
```

**Update quest body** (all fields optional):
```json
{
  "status": "done"
}
```

### Tags

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/tags` | List all tags |
| `POST` | `/tags` | Create a tag |
| `PATCH` | `/tags/{id}` | Update a tag |
| `DELETE` | `/tags/{id}` | Delete a tag (removes it from all quests) |

**Create tag body:**
```json
{
  "name": "go out",
  "color": "#3a8a5a"
}
```

---

## Deployment

### Backend → Railway

1. Push the `backend/` folder to a GitHub repo
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
3. Select your repo — Railway reads the `Procfile` and deploys automatically

**Optional: add Postgres** (recommended for production)

In your Railway project: **New → Database → PostgreSQL**. Copy the `DATABASE_URL` from the Postgres service's Variables tab, and add it as an environment variable on your app service. The backend will switch automatically — no code changes needed.

**Get your public URL:** Railway project → your service → **Settings → Networking → Public domain**

### Frontend → Vercel

1. Update `API_URL` in `side_quests.html` to your Railway public URL
2. Push to GitHub
3. Go to [vercel.com](https://vercel.com) → **New Project → Import** your repo
4. Set the root directory to `/` (or wherever `side_quests.html` lives)
5. Deploy — Vercel gives you a live URL instantly

### Connecting frontend to backend

In `side_quests.html`, replace the `load()` and `save()` localStorage functions with API calls:

```js
const API = "https://your-app.up.railway.app"

async function loadQuests() {
  const res = await fetch(`${API}/quests`)
  quests = await res.json()
  render()
}

async function createQuest(data) {
  await fetch(`${API}/quests`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  await loadQuests()
}

async function updateQuest(id, patch) {
  await fetch(`${API}/quests/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(patch)
  })
  await loadQuests()
}

async function deleteQuest(id) {
  await fetch(`${API}/quests/${id}`, { method: "DELETE" })
  await loadQuests()
}
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./sidequests.db` | Database connection string. Set automatically by Railway when using their Postgres add-on. |
| `PORT` | `8000` | Set automatically by Railway. |

---

## Local development tips

- The FastAPI dev server at `/docs` lets you test every endpoint interactively without any HTTP client
- SQLite creates `sidequests.db` in the `backend/` folder automatically on first run — no setup needed
- CORS is set to `allow_origins=["*"]` for development. Before going public, tighten this to your Vercel domain in `app/main.py`

---

## Roadmap ideas

- [ ] Connect frontend to backend API
- [ ] Auth (single-user password or magic link)
- [ ] Due dates / scheduling
- [ ] Quest photos or links
- [ ] Export to CSV
- [ ] Mobile PWA (add to home screen)
