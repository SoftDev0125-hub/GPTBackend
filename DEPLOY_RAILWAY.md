# Deploying to Railway

These steps deploy the FastAPI backend to [Railway](https://railway.app), giving you a public HTTPS URL for ChatGPT.

## 1. Prerequisites

- Railway account (free tier is fine)
- GitHub/GitLab repo containing this project
- Python 3.12 locally (already used here)

## 2. Prepare the repo

Already done in this project:

- `requirements.txt` lists dependencies
- `Procfile` defines the start command (`uvicorn main:app ...`)
- `runtime.txt` pins Python version to 3.12.7

Push all files to your Git repository (e.g., `git add .`, `git commit`, `git push`).

## 3. Create Railway project

1. Visit https://railway.app and log in.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Authorize GitHub if prompted and select your repo.
4. Railway auto-detects Python and installs `requirements.txt`.

## 4. Configure variables (if needed)

In Railway project settings → **Variables**:

- `GOOGLE_CREDENTIALS_PATH`: leave default (`credentials.json`)
- `GOOGLE_TOKEN_PATH`: leave default
- Upload your actual `credentials.json` using Railway’s **Files** panel (place in project root). Do **not** commit credentials to Git.

## 5. Deploy

1. Click **Deploy** (or wait for automatic deploy after pushing).
2. Railway builds and runs `Procfile` command:  
   `uvicorn main:app --host 0.0.0.0 --port ${PORT}`
3. When status is “Running”, click the generated **Public URL** (e.g., `https://gpt-backend.up.railway.app`).

## 6. Migrate Gmail tokens (optional)

- Download your local `token.json` (created after Gmail auth).
- Upload it via Railway Files (same directory as app).
- Otherwise, run the `/gmail/auth/url` flow again using the Railway URL.

## 7. Connect to ChatGPT

Use the Railway HTTPS URL when importing the OpenAPI schema:

```
https://your-railway-app.up.railway.app/openapi.json
```

Copy instructions from `assistant_instructions.txt` when creating the assistant.

## 8. Redeploying

Whenever you push new commits:

1. `git push` to your repo.
2. Railway auto-deploys. Watch the build logs.
3. Confirm `/health` via the public URL.

## Troubleshooting

| Issue | Fix |
| --- | --- |
| Build fails | Check Railway logs; ensure `requirements.txt` installs locally |
| 404 on `/` | Remember health endpoint is `/health`; docs at `/docs` |
| Gmail auth fails | Ensure `credentials.json` & `token.json` uploaded; redo OAuth |
| ChatGPT can’t reach API | Verify Railway URL uses HTTPS and is live |

Once deployed, you no longer need ngrok; the Railway URL stays constant.

