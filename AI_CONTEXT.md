# COMPASS Project: AI Developer Context

> **Note for AI Assistants:** Process this document to immediately understand the architecture, database schema, design rules, and file structure of the **COMPASS** project. 

## 1. Project Overview
**COMPASS** is a full-stack, standalone personal productivity web application built for a Final Year Project (FYP). It provides a unified dashboard that tracks three major aspects of a user's life:
*   **Tasks:** Todo list with date scheduling and priorities.
*   **Habits:** Daily habit tracking with automatically calculated streaks.
*   **Finance:** Income and expense tracking with visual category breakdown.

## 2. Tech Stack & Environment
*   **Backend:** Python 3.x, Django 5.x (or 4.x)
*   **Frontend:** Vanilla HTML5, heavily customized Vanilla CSS (no Bootstrap or Tailwind). JS is only used sparingly (e.g., Chart.js for data visualization).
*   **Database:** SQLite (default `db.sqlite3` for local development).
*   **Deployment Readiness:** Configured with `gunicorn` and `python-dotenv` (via `requirements.txt`).

## 3. Application Structure (Django Apps)
The project is strictly modular, split into the following Django apps:

### A. `dashboard` (`/dashboard/`)
*   **Purpose:** The central hub shown after login. It aggregates snippets of data from the other apps (today's habits, today's tasks, quick finance summary).
*   **Architecture:** Heavily relies on context processors or cross-app database queries in `dashboard/views.py`.

### B. `tasks` (`/tasks/`)
*   **Models:** `Task` (user, title, date, priority [low/medium/high], completed boolean, created_at).
*   **Features:** Basic CRUD. Special logic in template (`templates/tasks/list.html`) to highlight "Overdue" tasks (date < today AND completed = False) with a red badge.
*   **Testing:** Basic QA unit tests exist in `tasks/tests.py`.

### C. `habits` (`/habits/`)
*   **Models:** `Habit` (user, name, description, active boolean) and `HabitLog` (habit FK, date, done boolean).
*   **Features:** The view `habits/views.py` contains a dynamic `_calculate_streak` algorithmic function that walks backward from today to count consecutive `HabitLog` entries where `done=True`. Displayed as "🔥 X day streak" in `templates/habits/daily.html`.

### D. `finance` (`/finance/`)
*   **Models:** `Expense` (user, amount, category, description, date) and `Income` (user, amount, source, date).
*   **Features:** End-of-month and current-month aggregation. `finance/views.py` passes category totals to the template, which is rendered as a doughnut chart using **Chart.js** via a CDN link in `templates/finance/overview.html`.

### E. `accounts` (`/accounts/`)
*   **Authentication:** Uses Django's built-in `User` model.
*   **Views:** Standard login, custom registration form (in `accounts/forms.py` using username/email/password verification), logout (via POST request).
*   **Password Reset:** Fully wired up to Django's built-in password reset views. Templates are located in `templates/accounts/password_reset*.html`.

## 4. Design & UI Philosophy (CRITICAL RULES)
If you are generating new UI or modifying existing UI, you **MUST** follow these rules:
1.  **NO EXTERNAL CSS FRAMEWORKS:** Do not add Tailwind, Bootstrap, or Materialize classes.
2.  **Use `style.css`:** All styling comes from `static/css/style.css` (approx 1,700 lines). It defines a heavily customized, premium, minimalist aesthetic relying heavily on CSS Variables (`:root`).
3.  **Color Palette:** Warm off-white backgrounds (`--bg: #faf9f6`), deep forest green sidebars (`--bg-sidebar: #172d24`), and muted teal/coral accents.
4.  **Components:** Use existing classes like `.card`, `.dash-card`, `.btn-primary`, `.form-group`, `.form-control`, `.badge`, `.message-error`, etc. Do not invent new structure unless absolutely necessary.
5.  **Icons:** The app relies on standard Unicode/Emojis (e.g., 🧭, ⚄, ⎋) rather than an icon library like FontAwesome.

## 5. Security & Best Practices Implemented
*   Data Isolation: All database queries proactively filter by `user=request.user`. Users can never see each other's data.
*   Browser Caching fix applied to `templates/base.html` via meta tags so logged-out users don't see cached dashboard pages.
*   CSRF tokens applied to all forms.
*   Logout uses a `<form method="post">` button to align with Django 4.1+ security requirements for `LogoutView`.

## 6. How to Run Locally
1. `python -m venv .venv`
2. `.venv\Scripts\activate` (Windows)
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`
