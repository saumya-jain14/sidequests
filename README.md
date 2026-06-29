# Side Quests — Backend API

FastAPI + SQLite backend for the Side Quests app.
Runs locally in seconds, deploys to Railway for free.

---

## Local development

```bash
# 1. Create and activate a virtualenv
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file (SQLite is the default, no changes needed)
cp .env.example .env

# 4. Start the server
uvicorn app.main:app --reload
```

The API is now running at http://localhost:8000
Interactive docs at http://localhost:8000/docs

---

## API reference

### Quests

| Method | Path | Description |
|--------|------|-------------|
| GET | /quests | List all quests. Params: `q` (search), `tags` (comma-separated IDs), `status` |
| GET | /quests/random | Random todo quest. Params: `tags` (comma-separated IDs) |
| GET | /quests/{id} | Get one quest |
| POST | /quests | Create quest. Body: `{title, description?, tag_ids[]}` |
| PATCH | /quests/{id} | Update quest. Body: any subset of `{title, description, status, tag_ids[]}` |
| DELETE | /quests/{id} | Delete quest |

### Tags

| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | List all tags |
| POST | /tags | Create tag. Body: `{name, color}` |
| PATCH | /tags/{id} | Update tag |
| DELETE | /tags/{id} | Delete tag (removes from all quests) |

---

## Deploy to Railway (free)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
gh repo create sidequests-backend --public --push
# or push to an existing repo manually
```

### 2. Create a Railway project

1. Go to https://railway.app and sign in with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Select your repository
4. Railway auto-detects the Procfile and starts the deployment

### 3. Set environment variables (optional — SQLite works without this)

To use Postgres instead of SQLite (recommended for production):

1. In your Railway project, click **New → Database → PostgreSQL**
2. Click the Postgres service → **Variables** → copy `DATABASE_URL`
3. Click your app service → **Variables** → add `DATABASE_URL` = (paste value)

Railway will redeploy automatically. SQLite is fine for a personal app though.

### 4. Get your API URL

In Railway: your service → **Settings → Networking → Public domain**
It looks like: `https://sidequests-backend-production.up.railway.app`

---

## Connect the frontend

In `side_quests.html`, replace the `save()` and `load()` functions with
`fetch()` calls to your Railway URL. For example:

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
  loadQuests()
}
```

---

## Project structure

```
sidequests-backend/
├── app/
│   ├── main.py          # FastAPI app, CORS, router registration
│   ├── database.py      # SQLAlchemy engine + session
│   ├── models.py        # Quest, Tag, quest_tags join table
│   ├── schemas.py       # Pydantic request/response models
│   └── routers/
│       ├── quests.py    # All /quests endpoints
│       └── tags.py      # All /tags endpoints
├── requirements.txt
├── Procfile             # Railway start command
└── .env.example
```
