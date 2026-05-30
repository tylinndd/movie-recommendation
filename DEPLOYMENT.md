# Deployment: Vercel (frontend) + Render (backend)

This project is split for production:

| Part | Host | What runs |
|------|------|-----------|
| Frontend | [Vercel](https://vercel.com) | `index.html`, `static/*` (static site) |
| Backend | [Render](https://render.com) | Flask + Gunicorn, ML dataset, PostgreSQL |

**Why not Flask on Vercel?** The API loads ~30MB of CSV data and builds a scikit-learn similarity matrix at startup. That is a poor fit for Vercel serverless (size limits, cold starts). Render runs a long-lived process suited to this workload.

**Simpler alternative:** Deploy only to Render (frontend + API from one Flask app). You already have [filmfanatic.onrender.com](https://filmfanatic.onrender.com) that way—no CORS or cross-site cookies required.

---

## 1. Deploy the backend on Render

1. Push this repo to GitHub.
2. In Render: **New → Blueprint** and connect the repo (uses `render.yaml`), **or** **New → Web Service**:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn main:app --bind 0.0.0.0:$PORT --timeout 120`
   - **Health check path:** `/health`
3. Add a **PostgreSQL** database (free tier). Render sets `DATABASE_URL` automatically when linked.
4. Set environment variables:
   - `SECRET_KEY` — long random string
   - `FRONTEND_URL` — your Vercel URL(s), comma-separated, no trailing slash  
     Example: `https://film-fanatic.vercel.app`  
     Preview deployments are covered if you set `FRONTEND_ORIGIN_REGEX` (included in `render.yaml`).
5. After deploy, note the API URL (e.g. `https://filmfanatic.onrender.com`).

Free Render web services spin down after inactivity; the first request after sleep can take 30–60 seconds.

---

## 2. Deploy the frontend on Vercel

1. Import the same GitHub repo in Vercel.
2. **Framework preset:** Other  
3. **Build command:** `npm run build`  
4. **Output directory:** leave default (project root; `index.html` at root).
5. **Environment variable (Production):**
   - `API_URL` = your Render service URL (no trailing slash), e.g. `https://filmfanatic.onrender.com`
6. Deploy.

`npm run build` writes `static/config.js` so the browser calls the Render API. `.vercelignore` keeps Python and CSV files off Vercel uploads.

---

## 3. Wire frontend → backend

1. In **Render**, set `FRONTEND_URL` to your live Vercel URL (exact scheme + host, no path).
2. Redeploy Render so CORS and session cookies apply.
3. Test on Vercel: sign up, login, search, watchlist.

Cross-origin auth uses `SameSite=None` + `Secure` cookies when `FRONTEND_URL` is set.

---

## Local development

**Full stack (single origin):**

```bash
pip install -r requirements.txt
python main.py
# http://localhost:5000 — API_BASE stays empty in static/config.js
```

**Frontend against remote API:**

```bash
API_URL=https://filmfanatic.onrender.com npm run build
python -m http.server 3000
# Open http://localhost:3000 and set FRONTEND_URL on Render to http://localhost:3000 for CORS
```

---

## Environment reference

| Variable | Where | Purpose |
|----------|--------|---------|
| `API_URL` | Vercel build | Backend base URL injected into `static/config.js` |
| `FRONTEND_URL` | Render | Allowed CORS origin(s) for the Vercel app |
| `SECRET_KEY` | Render | Flask session signing |
| `DATABASE_URL` | Render | PostgreSQL (required for persistent users on Render) |

SQLite on Render’s ephemeral disk is not suitable for production user data.
