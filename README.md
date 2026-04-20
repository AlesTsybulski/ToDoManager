# TaskHUB

A task management web app built with Django. Create tasks with deadlines, mark them done, and receive Telegram reminders before they're due.

## Features

- Create, edit, and delete tasks with optional deadlines
- Mark tasks as done / pending
- Telegram bot integration — get a reminder when a deadline is approaching
- Dark theme UI

## Tech Stack

- **Backend** — Django 4.2, PostgreSQL
- **Task queue** — Celery + Redis Cloud
- **Notifications** — python-telegram-bot v20
- **Frontend** — vanilla CSS (OKLCH design tokens, mobile-friendly)

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database
- Redis Cloud account (free tier works) — [redis.io/try-free](https://redis.io/try-free/)
- Telegram bot token from [@BotFather](https://t.me/BotFather)

### Installation

1. Clone the repo and create a virtual environment:
   ```bash
   git clone https://github.com/AlesTsybulski/ToDoManager.git
   cd ToDoManager
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```env
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   REDIS_URL=redis://default:<password>@<host>:<port>
   BOT_TOKEN=123456789:AAxxxxx
   ```

4. Apply migrations:
   ```bash
   cd todo
   python manage.py migrate
   ```

### Running

You need 4 terminals, all run from the `todo/` directory:

```bash
# Terminal 1 — Django dev server
python manage.py runserver

# Terminal 2 — Celery worker
celery -A todo worker --loglevel=info --pool=solo

# Terminal 3 — Celery Beat (sends reminders every 10 minutes)
celery -A todo beat --loglevel=info

# Terminal 4 — Telegram bot (links users to their chat)
python bot.py
```

## Telegram Reminders

1. Create a bot via [@BotFather](https://t.me/BotFather) and add the token to `.env`
2. Sign up on the app
3. Open your bot in Telegram, send `/start`, then reply with your account email
4. Create a task with a deadline — you'll get a Telegram message when it's less than an hour away

## Project Structure

```
todo/
├── todo/           # Django project (settings, urls, celery)
├── tasks/          # Task model, views, Celery task
├── users/          # Custom user model, auth views
└── bot.py          # Telegram bot process
```
