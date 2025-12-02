# Telegram Bingo Bot - Railway Template

Push this repo to GitHub, then create two Railway services in the same project:
- web: `gunicorn web.server:app --bind 0.0.0.0:$PORT --workers 2`
- worker: `python3 bot/main.py`

Set environment variables in Railway Project Variables (see `.env.example`).

This template contains:
- `bot/main.py` — aiogram polling worker (handles Telegram messages)
- `web/server.py` — Flask web server for health, tasker-deposit, and admin stubs
- `database/` — SQLAlchemy models and helper setup

After pushing:
1. Add Railway Postgres (optional) or set `DATABASE_URL`
2. Create services and set start commands
3. Add environment variables (BOT_TOKEN, TASKER_SECRET_KEY, DATABASE_URL, etc)
4. Deploy and check logs
