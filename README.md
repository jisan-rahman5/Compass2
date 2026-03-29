# COMPASS — Personal Productivity System

> **C**ommit · **O**rganise · **M**anage · **P**lan · **A**nalyse · **S**tay-focused · **S**ucceed

COMPASS is a personal productivity web application built as a Final Year Project (FYP). It helps individuals manage their daily tasks, track habits, and monitor their personal finances — all in one clean, minimal dashboard.

---

## Features

| Module     | Capabilities |
|------------|-------------|
| **Dashboard** | Year-progress tracker, daily task overview, habit anchors, monthly finance summary |
| **Tasks** | Daily task planner with priorities (High / Medium / Low), date navigation, soft-delete |
| **Habits** | Daily habit checklist with streak tracking, activate/deactivate habits |
| **Finance** | Monthly income & expense tracker, savings calculator, category breakdown, CSV export |
| **Accounts** | User registration, login, logout, password reset |

---

## Tech Stack

- **Backend:** Python 3.x, Django 4.2
- **Database:** SQLite (development)
- **Frontend:** Vanilla HTML, CSS (no external CSS framework)
- **Fonts:** DM Sans, Playfair Display (Google Fonts)
- **Charts:** Chart.js (CDN)

---

## Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd compass-2
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin panel)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/**

---

## Project Structure

```
compass-2/
├── accounts/          # User auth (login, register, password reset)
├── compass/           # Django settings & root URL config
├── dashboard/         # Main overview screen
├── finance/           # Income & expense tracking
├── habits/            # Daily habit tracker with streak counters
├── tasks/             # Date-based task planner
├── templates/         # All HTML templates
├── static/            # CSS & static assets
└── manage.py
```

---

## Running Tests

```bash
python manage.py test
```

---

## License

This project was developed as a Final Year Project (FYP). All rights reserved.
