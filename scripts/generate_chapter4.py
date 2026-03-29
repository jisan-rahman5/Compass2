"""
Generates Chapter 4 as a .docx file using only Python standard library (zipfile + xml).
No external packages required.
"""
import zipfile, os, io

OUTPUT = r"c:\Users\jisan\OneDrive\Desktop\compass-2\Chapter4_System_Design.docx"

# ── helpers ──────────────────────────────────────────────────────────────────
def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def heading(text, level=1):
    style = f"Heading{level}"
    return f'''<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>
  <w:r><w:t>{esc(text)}</w:t></w:r></w:p>'''

def para(text, bold=False, justify=True):
    jc = '<w:jc w:val="both"/>' if justify else ''
    bold_on  = '<w:b/>' if bold else ''
    bold_rpr = f'<w:rPr>{bold_on}</w:rPr>' if bold_on else ''
    # handle inline bold via **text** marker:
    parts = text.split('**')
    runs = ''
    for i, part in enumerate(parts):
        b = '<w:b/>' if i % 2 == 1 else ''
        rpr = f'<w:rPr>{b}</w:rPr>' if b else ''
        if part:
            runs += f'<w:r>{rpr}<w:t xml:space="preserve">{esc(part)}</w:t></w:r>'
    return f'<w:p><w:pPr>{jc}</w:pPr>{runs}</w:p>'

def bullet(text):
    return f'''<w:p>
  <w:pPr><w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
  </w:pPr>
  <w:r><w:t>{esc(text)}</w:t></w:r></w:p>'''

def spacer():
    return '<w:p/>'

def toc_row(title, page):
    return f'''<w:tr>
  <w:tc><w:p><w:r><w:t xml:space="preserve">{esc(title)}</w:t></w:r></w:p></w:tc>
  <w:tc><w:tcPr><w:tcW w:w="800" w:type="dxa"/></w:tcPr>
    <w:p><w:pPr><w:jc w:val="right"/></w:pPr>
    <w:r><w:t>{page}</w:t></w:r></w:p></w:tc>
</w:tr>'''

def table2(r1c1, r1c2, r2c1, r2c2, header=False):
    def cell(t, bold=False):
        b = '<w:b/>' if bold else ''
        rpr = f'<w:rPr>{b}</w:rPr>' if bold else ''
        return f'<w:tc><w:p><w:r>{rpr}<w:t xml:space="preserve">{esc(t)}</w:t></w:r></w:p></w:tc>'
    rows = ''
    if header:
        rows += f'<w:tr>{cell(r1c1,True)}{cell(r1c2,True)}</w:tr>'
        rows += f'<w:tr>{cell(r2c1)}{cell(r2c2)}</w:tr>'
    else:
        rows += f'<w:tr>{cell(r1c1)}{cell(r1c2)}</w:tr>'
        rows += f'<w:tr>{cell(r2c1)}{cell(r2c2)}</w:tr>'
    return f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>{rows}</w:tbl>'

def hw_table(rows):
    """rows = list of (label, value) tuples, first is header"""
    out = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>'
    for i,(a,b) in enumerate(rows):
        bold = (i == 0)
        def cell(t):
            b_tag = '<w:b/>' if bold else ''
            rpr = f'<w:rPr>{b_tag}</w:rPr>' if bold else ''
            return f'<w:tc><w:p><w:r>{rpr}<w:t xml:space="preserve">{esc(t)}</w:t></w:r></w:p></w:tc>'
        out += f'<w:tr>{cell(a)}{cell(b)}</w:tr>'
    out += '</w:tbl>'
    return out

# ── document body ─────────────────────────────────────────────────────────────
body_parts = []
A = body_parts.append

# ── TITLE PAGE ────────────────────────────────────────────────────────────────
A('<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
  '<w:r><w:rPr><w:b/><w:sz w:val="52"/></w:rPr><w:t>CHAPTER 4</w:t></w:r></w:p>')
A('<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
  '<w:r><w:rPr><w:b/><w:sz w:val="40"/></w:rPr><w:t>SYSTEM DESIGN</w:t></w:r></w:p>')
A(spacer())

# ── TABLE OF CONTENTS ─────────────────────────────────────────────────────────
A(heading('Table of Contents', 1))
toc_entries = [
    ('Introduction', '1'),
    ('Overview of System Design', '2'),
    ('Types of Design', '3'),
    ('Process and Data Model Design', '5'),
    ('Context Diagram', '7'),
    ('ER Diagram', '9'),
    ('Data Flow Diagram (DFD)', '11'),
    ('System Development Tools', '13'),
    ('Hardware & Software Requirements', '14'),
    ('Conclusion', '17'),
]
A('<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>')
for title, page in toc_entries:
    A(toc_row(title, page))
A('</w:tbl>')
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.1  INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.1  Introduction', 1))
A(para(
    'The design phase is a critical stage in the software development lifecycle. '
    'It translates the requirements captured in the analysis phase into a concrete '
    'blueprint that guides implementation. This chapter presents the complete system '
    'design of COMPASS — a personal productivity and life-management web application '
    'built on the Django framework. COMPASS integrates four core functional modules: '
    '**Task Management**, **Habit Tracking**, **Personal Finance**, and a **Unified Daily Dashboard**.'
))
A(para(
    'The chapter covers the overall system architecture, different design perspectives '
    'such as input and output design, process and data models, diagrammatic representations '
    'including Context Diagrams, Entity-Relationship (ER) Diagrams, and Data Flow '
    'Diagrams (DFDs), as well as the development tools and the hardware and software '
    'requirements needed to run the system successfully.'
))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.2  OVERVIEW OF SYSTEM DESIGN
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.2  Overview of System Design', 1))
A(para(
    'COMPASS follows the **Model-View-Template (MVT)** architectural pattern, which is '
    'the Django framework\'s variant of the classic Model-View-Controller (MVC) pattern. '
    'In this pattern, the **Model** handles all database schema definitions and data '
    'access logic, the **View** contains the business logic and retrieves data to be '
    'displayed, and the **Template** handles the presentation layer rendered in the '
    'user\'s browser.'
))
A(para(
    'The application is structured into five Django applications, each responsible for '
    'a distinct domain of functionality:'
))
A(bullet('accounts — User registration, authentication, and session management.'))
A(bullet('dashboard — The unified daily overview screen aggregating data from all modules.'))
A(bullet('tasks — Task creation, listing, editing, soft-deletion, priority management, and completion toggling.'))
A(bullet('habits — Daily habit definition, activation/deactivation, and binary daily logging.'))
A(bullet('finance — Monthly income tracking and categorised daily expense recording with savings calculation.'))
A(spacer())
A(para(
    'All five applications share a single SQLite relational database, accessed through '
    'Django\'s built-in Object Relational Mapper (ORM). User authentication and session '
    'management are handled by Django\'s built-in `django.contrib.auth` module, which '
    'provides the `User` model that every application references via a foreign-key '
    'relationship to enforce per-user data isolation.'
))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.3  TYPES OF DESIGN
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.3  Types of Design', 1))

A(heading('4.3.1  Input Design', 2))
A(para(
    'Input design refers to the design of all mechanisms through which users supply '
    'data to the system. In COMPASS, user input is exclusively gathered through '
    'Django form classes and HTML form elements rendered in templates.'
))
A(para('The key input points of the system are described below:'))
A(bullet('Registration Form: Collects a username, email address, and password. The password is validated by Django\'s built-in validators (minimum length, common password check, and numeric-only check) before the account is created.'))
A(bullet('Login Form: Accepts a username and password pair. Django\'s built-in LoginView handles credential verification and session creation.'))
A(bullet('Task Form: Accepts a task title, target date, and priority level (High, Medium, or Low). Default values (today\'s date, medium priority) are pre-populated for convenience.'))
A(bullet('Habit Form: Accepts a habit name and active status. Active habits appear on the dashboard every day.'))
A(bullet('Income Form: Collects the income source description, monetary amount, and the applicable month and year.'))
A(bullet('Expense Form: Collects the expense amount, a descriptive note, date, and a category chosen from nine predefined options (Food & Dining, Transport, Shopping, Bills & Utilities, Health, Education, Entertainment, Personal, Other).'))
A(spacer())
A(para(
    'All forms employ Django\'s CSRF (Cross-Site Request Forgery) middleware token to '
    'prevent unauthorised form submissions. Server-side validation is enforced by '
    'Django\'s form validation framework before any data is persisted to the database.'
))
A(spacer())

A(heading('4.3.2  Output Design', 2))
A(para(
    'Output design concerns how the system presents processed data back to the user. '
    'COMPASS delivers its outputs through HTML templates rendered server-side by Django '
    'and returned as HTTP responses. The primary output screens are:'
))
A(bullet('Dashboard Page (/dashboard/): Displays a personalised greeting, current year progress percentage, the day of the year, monthly income and expense totals, calculated savings, today\'s task list (sorted by completion status and priority), and the list of today\'s active habits with their completion status.'))
A(bullet('Task List Page (/tasks/): Shows all tasks for the current day grouped and ordered by priority (High > Medium > Low) and completion status, with inline controls to toggle, edit, or soft-delete each task.'))
A(bullet('Habit Management Page (/habits/manage/): Lists all user-defined habits with options to activate/deactivate or delete them. A separate view shows the completion log grid by date.'))
A(bullet('Finance Overview Page (/finance/): Displays monthly income and expense totals, a categorised expense breakdown, and the monthly savings figure.'))
A(bullet('Income Page (/finance/income/): Lists all income records for the user, with the ability to add or delete entries.'))
A(spacer())

A(heading('4.3.3  Interface Design', 2))
A(para(
    'COMPASS employs a dark-themed, single-column responsive interface that is consistent '
    'across all pages. A shared base template (`templates/base.html`) provides the navigation '
    'bar, global CSS/JS includes, and semantic HTML5 layout. Each application\'s templates '
    'extend this base template using Django\'s `{% extends %}` and `{% block %}` directives. '
    'Custom CSS stored in the `static/css/` directory applies a unified colour palette, '
    'typography, and interactive hover effects across all pages.'
))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.4  PROCESS AND DATA MODEL DESIGN
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.4  Process and Data Model Design', 1))
A(para(
    'The data model of COMPASS is defined through Django\'s ORM model classes. Each class '
    'maps directly to a database table. The following describes each model and its relationship '
    'to the built-in `User` model:'
))
A(spacer())

A(heading('4.4.1  User (django.contrib.auth)', 2))
A(para(
    'The `User` model is provided by Django\'s authentication framework and is not '
    'redefined. It stores the username, email, hashed password, and account status '
    'flags. Every other model in COMPASS references `User` via a `ForeignKey` with '
    '`on_delete=CASCADE`, ensuring all user data is automatically removed when an '
    'account is deleted.'
))
A(spacer())

A(heading('4.4.2  Task Model', 2))
A(para('The `Task` model (tasks/models.py) represents a single actionable item. Its fields are:'))
A(bullet('user (ForeignKey → User): The owner of the task.'))
A(bullet('title (CharField, max 255): The task description.'))
A(bullet('date (DateField): The date the task is assigned to (defaults to today).'))
A(bullet('priority (CharField): One of "high", "medium", or "low".'))
A(bullet('completed (BooleanField): Whether the task has been marked as done.'))
A(bullet('is_deleted (BooleanField): Soft-delete flag — deleted tasks are hidden rather than erased.'))
A(bullet('created_at (DateTimeField): Auto-set timestamp of creation.'))
A(spacer())

A(heading('4.4.3  Habit and HabitLog Models', 2))
A(para('The `Habit` model (habits/models.py) defines a recurring daily commitment. Its fields are:'))
A(bullet('user (ForeignKey → User)'))
A(bullet('name (CharField, max 255): The habit description.'))
A(bullet('active (BooleanField): Whether the habit is currently being tracked.'))
A(bullet('created_at (DateTimeField): Auto-set on creation.'))
A(spacer())
A(para(
    'The `HabitLog` model records the binary completion state of a habit for a specific '
    'date. Its fields are:'
))
A(bullet('habit (ForeignKey → Habit)'))
A(bullet('date (DateField): The date of the log entry.'))
A(bullet('done (BooleanField): True if the habit was completed on that date.'))
A(para('A unique_together constraint on (habit, date) ensures only one log entry exists per habit per day.'))
A(spacer())

A(heading('4.4.4  Income Model', 2))
A(para('The `Income` model (finance/models.py) stores monthly income entries. Its fields are:'))
A(bullet('user (ForeignKey → User)'))
A(bullet('amount (DecimalField, 12 digits, 2 decimal places): The income value.'))
A(bullet('source (CharField): Description of the income source (e.g., "Salary", "Freelance").'))
A(bullet('month (IntegerField): The month number (1–12).'))
A(bullet('year (IntegerField): The four-digit year.'))
A(spacer())

A(heading('4.4.5  Expense Model', 2))
A(para('The `Expense` model (finance/models.py) stores individual daily expenditures. Its fields are:'))
A(bullet('user (ForeignKey → User)'))
A(bullet('amount (DecimalField, 12 digits, 2 decimal places)'))
A(bullet('category (CharField): One of nine predefined choices (Food & Dining, Transport, Shopping, Bills & Utilities, Health, Education, Entertainment, Personal, Other).'))
A(bullet('date (DateField): The date of the expense (defaults to today).'))
A(bullet('note (CharField, optional): A short description of the expense.'))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.5  CONTEXT DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.5  Context Diagram', 1))
A(para(
    'A Context Diagram (also called a Level-0 DFD) provides the highest-level view of '
    'a system, showing the system as a single process and illustrating how it interacts '
    'with external entities. For COMPASS, there is a single external entity: the **Registered User**.'
))
A(spacer())
A(para(
    'The registered user supplies the system with login credentials, task entries, habit '
    'definitions and daily completion updates, income records, and expense records. '
    'In return, the system outputs the personalised daily dashboard view, task lists '
    'sorted by priority, habit completion progress, and financial summaries including '
    'savings calculations.'
))
A(spacer())
A(para('**Context Diagram — Narrative Description:**', bold=False))
A(para(
    'External Entity: User  ←→  [COMPASS System]  '
    'Inputs flowing in: Registration details, Login credentials, Task data (title, date, priority), '
    'Habit data (name, active status, daily completion toggles), Income data (source, amount, month, year), '
    'Expense data (amount, category, date, note).  '
    'Outputs flowing out: Dashboard summary (greeting, year progress, financial snapshot, tasks, habits), '
    'Task list view, Habit management view, Finance overview, Authentication feedback.'
))
A(spacer())
A(para(
    'Note: A visual Context Diagram figure can be inserted here using any diagramming tool '
    '(e.g., draw.io, Lucidchart). The narrative above provides the complete description of '
    'all data flows at the context level.'
))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.6  ER DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.6  ER Diagram', 1))
A(para(
    'The Entity-Relationship (ER) Diagram models the data entities within COMPASS and '
    'the relationships between them. Each Django model corresponds to one entity, and '
    'each ForeignKey field corresponds to a relationship.'
))
A(spacer())
A(para('**Entities and Attributes:**'))
A(bullet('User: user_id (PK), username, email, password, is_active'))
A(bullet('Task: task_id (PK), user_id (FK), title, date, priority, completed, is_deleted, created_at'))
A(bullet('Habit: habit_id (PK), user_id (FK), name, active, created_at'))
A(bullet('HabitLog: log_id (PK), habit_id (FK), date, done'))
A(bullet('Income: income_id (PK), user_id (FK), amount, source, month, year'))
A(bullet('Expense: expense_id (PK), user_id (FK), amount, category, date, note'))
A(spacer())
A(para('**Relationships:**'))
A(bullet('User — Task: One-to-Many. One user can have many tasks; each task belongs to exactly one user.'))
A(bullet('User — Habit: One-to-Many. One user can define many habits; each habit belongs to exactly one user.'))
A(bullet('Habit — HabitLog: One-to-Many. One habit can have many daily log entries; each log entry belongs to exactly one habit.'))
A(bullet('User — Income: One-to-Many. One user can have many income records; each income record belongs to exactly one user.'))
A(bullet('User — Expense: One-to-Many. One user can have many expense records; each expense record belongs to exactly one user.'))
A(spacer())
A(para(
    'Note: A visual ER Diagram figure should be inserted here. The diagram can be generated '
    'using tools such as dbdiagram.io, draw.io or pgAdmin\'s schema diagram view based on '
    'the entity and relationship definitions above.'
))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.7  DATA FLOW DIAGRAM (DFD)
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.7  Data Flow Diagram (DFD)', 1))
A(para(
    'A Data Flow Diagram (DFD) illustrates how data moves through a system — from '
    'input, through processing steps, to storage and output. The following describes '
    'COMPASS at Level 1, decomposing the system into its five core processes.'
))
A(spacer())

A(heading('4.7.1  Process 1 — User Authentication', 2))
A(para(
    'Data Flows In: Username + Password (from User).  '
    'Process: Django\'s `LoginView` validates credentials against the `auth_user` table. '
    'On success, a session is created. On failure, an error message is returned.  '
    'Data Store: auth_user table (SQLite).  '
    'Data Flows Out: Session cookie (to browser); Redirect to Dashboard or error message.'
))
A(spacer())

A(heading('4.7.2  Process 2 — Task Management', 2))
A(para(
    'Data Flows In: Task title, date, priority (from User via Task Form).  '
    'Process: `task_create` view validates the form and saves a new Task record. '
    '`task_toggle` flips the `completed` flag. `task_delete` sets `is_deleted=True`. '
    'Data Store: tasks_task table.  '
    'Data Flows Out: Rendered task list sorted by priority and completion status.'
))
A(spacer())

A(heading('4.7.3  Process 3 — Habit Tracking', 2))
A(para(
    'Data Flows In: Habit name and active status (habit creation); daily toggle click (log update).  '
    'Process: `habit_create` saves a new Habit record. '
    '`habit_toggle` creates or updates the HabitLog for today\'s date using `get_or_create`.  '
    'Data Store: habits_habit table; habits_habitlog table.  '
    'Data Flows Out: Habit list with per-habit completion status for the current day.'
))
A(spacer())

A(heading('4.7.4  Process 4 — Finance Tracking', 2))
A(para(
    'Data Flows In: Income (source, amount, month, year); Expense (amount, category, date, note).  '
    'Process: `income_add` and `expense_add` views validate and save their respective records. '
    'Aggregation queries using `Sum` calculate monthly totals. Savings = Total Income − Total Expenses.  '
    'Data Store: finance_income table; finance_expense table.  '
    'Data Flows Out: Finance overview (income total, expense total, savings, categorised breakdown).'
))
A(spacer())

A(heading('4.7.5  Process 5 — Dashboard Aggregation', 2))
A(para(
    'Data Flows In: Session user identity (from active session cookie).  '
    'Process: The `dashboard_view` queries all four data stores simultaneously — fetching '
    'today\'s tasks, active habits with completion status, and the current month\'s income '
    'and expense totals. It also computes the year progress percentage.  '
    'Data Store: auth_user, tasks_task, habits_habit, habits_habitlog, finance_income, finance_expense.  '
    'Data Flows Out: Unified dashboard HTML page with all summary information.'
))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.8  SYSTEM DEVELOPMENT TOOLS
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.8  System Development Tools', 1))
A(para(
    'The following tools were used during the analysis, design, development, and testing '
    'phases of the COMPASS project:'
))
A(spacer())
tools = [
    ('Tool', 'Purpose'),
    ('Python 3.11', 'Core programming language. Provides the runtime and standard library for the entire application.'),
    ('Django 4.x', 'High-level Python web framework. Provides the MVT pattern, ORM, authentication, URL routing, and form handling.'),
    ('SQLite', 'Lightweight relational database engine bundled with Python. Stores all application data during development.'),
    ('HTML5 / CSS3', 'Front-end markup and styling technologies. Used to build and style all user-facing templates.'),
    ('JavaScript (Vanilla)', 'Client-side scripting for interactive elements such as habit toggle animations and dynamic UI updates without page reload.'),
    ('Visual Studio Code', 'Primary Integrated Development Environment (IDE) used for writing, debugging, and managing project files.'),
    ('Git', 'Version control system used to track changes across the codebase.'),
    ('pip', 'Python package manager used to install Django and other project dependencies.'),
    ('draw.io / Lucidchart', 'Diagramming tools used to design Context Diagrams, ER Diagrams, and DFDs.'),
    ('Google Chrome DevTools', 'Browser-based debugging tool used to inspect rendered HTML, debug JavaScript, and test responsive layouts.'),
]
A(hw_table(tools))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.9  HARDWARE & SOFTWARE REQUIREMENTS
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.9  Hardware & Software Requirements', 1))

A(heading('4.9.1  Hardware Requirements', 2))
A(para(
    'COMPASS is a lightweight Django web application and has minimal hardware demands. '
    'The following specifications represent the minimum and recommended configurations '
    'for running the system on a local development machine:'
))
A(spacer())
hw_rows = [
    ('Component', 'Minimum Requirement', 'Recommended'),
    ('Processor', 'Intel Core i3 / AMD Ryzen 3 or equivalent', 'Intel Core i5 / AMD Ryzen 5 or higher'),
    ('RAM', '4 GB', '8 GB or more'),
    ('Storage', '500 MB free disk space', '1 GB+ free disk space'),
    ('Display', '1280 × 720 resolution', '1920 × 1080 (Full HD) or higher'),
    ('Internet', 'Required for initial package installation', 'Stable broadband connection recommended'),
]
# render 3-col table manually
out = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>'
for i, row in enumerate(hw_rows):
    bold = (i == 0)
    def cell3(t):
        b_tag = '<w:b/>' if bold else ''
        rpr = f'<w:rPr>{b_tag}</w:rPr>' if bold else ''
        return f'<w:tc><w:p><w:r>{rpr}<w:t xml:space="preserve">{esc(t)}</w:t></w:r></w:p></w:tc>'
    out += f'<w:tr>{cell3(row[0])}{cell3(row[1])}{cell3(row[2])}</w:tr>'
out += '</w:tbl>'
A(out)
A(spacer())

A(heading('4.9.2  Software Requirements', 2))
A(para('The following software must be installed on the host machine to run COMPASS:'))
A(spacer())
sw_rows = [
    ('Software', 'Version', 'Role'),
    ('Python', '3.11 or higher', 'Application runtime'),
    ('Django', '4.2 or higher', 'Web framework'),
    ('SQLite', 'Bundled with Python', 'Development database engine'),
    ('pip', 'Latest stable', 'Dependency management'),
    ('Web Browser', 'Chrome 110+ / Firefox 110+ / Edge 110+', 'User interface rendering'),
    ('Git', '2.x', 'Version control (optional for deployment)'),
    ('Operating System', 'Windows 10/11, macOS 12+, or Ubuntu 20.04+', 'Host operating environment'),
]
out2 = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>'
for i, row in enumerate(sw_rows):
    bold = (i == 0)
    def cell3b(t):
        b_tag = '<w:b/>' if bold else ''
        rpr = f'<w:rPr>{b_tag}</w:rPr>' if bold else ''
        return f'<w:tc><w:p><w:r>{rpr}<w:t xml:space="preserve">{esc(t)}</w:t></w:r></w:p></w:tc>'
    out2 += f'<w:tr>{cell3b(row[0])}{cell3b(row[1])}{cell3b(row[2])}</w:tr>'
out2 += '</w:tbl>'
A(out2)
A(spacer())

A(heading('4.9.3  Running the System', 2))
A(para('The following commands are used to set up and start the COMPASS system locally:'))
A(para('Step 1 — Navigate to the project directory:'))
A(para('    cd compass-2'))
A(para('Step 2 — Install dependencies:'))
A(para('    pip install django'))
A(para('Step 3 — Apply database migrations:'))
A(para('    python manage.py migrate'))
A(para('Step 4 — Create a superuser (optional, for admin access):'))
A(para('    python manage.py createsuperuser'))
A(para('Step 5 — Start the development server:'))
A(para('    python manage.py runserver'))
A(para('Step 6 — Open a web browser and navigate to: http://127.0.0.1:8000/'))
A(spacer())

# ═══════════════════════════════════════════════════════════════════════════════
# 4.10  CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
A(heading('4.10  Conclusion', 1))
A(para(
    'This chapter presented the comprehensive system design of COMPASS. Beginning with '
    'an architectural overview of the Django MVT pattern and the five application modules, '
    'the chapter described the input and output design strategies, the interface design '
    'philosophy, and the complete data model definitions for all six database entities.'
))
A(para(
    'The Context Diagram illustrated the system\'s interaction with its single external '
    'entity — the registered user — identifying all incoming and outgoing data flows. '
    'The Entity-Relationship Diagram formalised the relational structure of the data '
    'model, highlighting the central role of the User entity and the one-to-many '
    'relationships that govern data isolation between accounts.'
))
A(para(
    'The Level-1 Data Flow Diagram decomposed the system into five core processes: '
    'User Authentication, Task Management, Habit Tracking, Finance Tracking, and '
    'Dashboard Aggregation, each with clearly defined data flows to and from their '
    'respective data stores.'
))
A(para(
    'Finally, the development tools and hardware and software requirements were documented '
    'to provide a complete picture of the environment in which COMPASS was built and '
    'is intended to operate. With the system design fully established, the following '
    'chapter will proceed to describe the implementation and testing of the system.'
))

# ── assemble XML ──────────────────────────────────────────────────────────────
body_xml = '\n'.join(body_parts)

document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
  xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex"
  xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
  xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink"
  xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d"
  xmlns:o="urn:schemas-microsoft-com:office:office"
  xmlns:oel="http://schemas.microsoft.com/office/2019/extlst"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
  xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
  xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
  xmlns:w10="urn:schemas-microsoft-com:office:word"
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
  xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
  xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex"
  xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid"
  xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml"
  xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash"
  xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex"
  xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
  xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
  xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
  xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
  mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14">
<w:body>
{body_xml}
<w:sectPr>
  <w:pgSz w:w="12240" w:h="15840"/>
  <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
</w:sectPr>
</w:body>
</w:document>'''

# Numbering XML for bullet lists
numbering_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="bullet"/>
      <w:lvlText w:val="•"/>
      <w:lvlJc w:val="left"/>
      <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
      </w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1">
    <w:abstractNumId w:val="0"/>
  </w:num>
</w:numbering>'''

styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="160" w:line="259" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr>
      <w:spacing w:before="240" w:after="120"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="32"/>
      <w:color w:val="1F3864"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr>
      <w:spacing w:before="200" w:after="80"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="28"/>
      <w:color w:val="2E75B6"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph">
    <w:name w:val="List Paragraph"/>
    <w:pPr>
      <w:ind w:left="720"/>
    </w:pPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
</w:styles>'''

rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''

root_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

# ── write .docx (which is a ZIP file) ────────────────────────────────────────
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('[Content_Types].xml', content_types_xml)
    zf.writestr('_rels/.rels', root_rels_xml)
    zf.writestr('word/document.xml', document_xml)
    zf.writestr('word/styles.xml', styles_xml)
    zf.writestr('word/numbering.xml', numbering_xml)
    zf.writestr('word/_rels/document.xml.rels', rels_xml)

print(f"SUCCESS: Created {OUTPUT}")
