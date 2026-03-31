# COMPASS

**COMPASS** is a personal productivity web application built with Django.  
It helps students manage their daily habits, tasks, and finances in one place.

---

## Features

- 📋 **Tasks** — Create, manage, and track to-do items
- ✅ **Habits** — Build daily habits with streak tracking
- 💰 **Finance** — Log income and expenses, view spending overview
- 📊 **Dashboard** — Unified view of all productivity data
- 🔐 **Accounts** — Register, login, and password reset

---

## Requirements

- Python 3.10+
- Django 4.2+

---

## Setup & Run

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Create a superuser (optional, for admin panel)
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

---

## Running in VS Code

Open the project folder in VS Code, select the `.venv` Python interpreter,  
then press **F5** to launch the Django server using the built-in debugger.

---

## Project Structure

```
compass-2/
├── compass/          # Project settings & URL config
├── accounts/         # Auth: login, register, password reset
├── dashboard/        # Main dashboard view
├── habits/           # Habit tracking
├── tasks/            # Task management
├── finance/          # Income & expense tracking
├── templates/        # HTML templates
├── static/           # CSS & JS assets
├── manage.py
└── requirements.txt
```
