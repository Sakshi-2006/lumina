# Personal Expense Tracker with Data Visualization

A beginner-friendly, portfolio-ready personal finance analytics project. It imports manual or CSV transactions, cleans inconsistent rows, categorizes transactions with transparent keyword rules, stores records in SQLite, calculates spending and savings metrics, and produces charts and monthly reports. It uses synthetic demo data and does not connect to banks.

> **Portfolio note:** all default records are synthetic. Replace them only with data you have permission to use, and never commit private financial data.

## What problem does it solve?

In everyday terms, expense tracking helps people notice where money goes, plan budgets, avoid overspending, and make savings goals concrete. Students, employees, families, freelancers, and small businesses can all benefit from knowing how much they spend by category and how spending changes over time. Technically, this project is a small ETL and analytics pipeline: heterogeneous input is validated and normalized, persisted in a relational schema, aggregated into KPIs, visualized, and exported.

**Workflow:** entry/import → validation and cleaning → SQLite storage → rule-based category assignment → category/month/payment analysis → dashboard charts → CSV report.

## Features

- Manual transaction entry and CSV upload (required `date`, `description`, `amount`; optional `payment_method`).
- Synthetic transactions generated automatically for a six-month demo.
- SQLite tables for transactions, categories, and budgets, with parameterized queries and duplicate protection.
- Rule-based auto-categorization, monthly spending and income, savings, top category, average daily spend, and payment-method totals.
- Streamlit dashboard with monthly filtering, budget progress/overspend alert, and transaction table.
- CSV export and saved charts: category bars, monthly trend, daily trend, and payment-method pie.

## Stack choices

| Option | Tools | Difficulty | Output |
| --- | --- | --- | --- |
| A — Easy | Python, CSV, `datetime`, Matplotlib | Beginner | Command-line summaries and charts |
| B — Student pick | Python, Pandas, SQLite, Streamlit, Matplotlib | Beginner–intermediate | Interactive local dashboard, durable local database, exports |
| C — Advanced | Option B + SQLAlchemy, Pydantic, tests, ML categorizer, deployment | Intermediate–advanced | Validated, extensible analytics product |

Option B is recommended: it demonstrates practical Python, data cleaning, SQL, visualization, and a usable UI without requiring real banking data or paid services.

## Architecture

```text
Manual form / CSV upload / synthetic generator
                     ↓
           clean_transactions()
                     ↓
   rule categorizer + input validation
                     ↓
       SQLite: transactions/categories/budgets
                     ↓
        Pandas analysis and monthly KPIs
                     ↓
  Streamlit dashboard + Matplotlib chart files
                     ↓
       downloadable CSV monthly report
```

Input fields: date, description, amount (negative = expense, positive = income), payment method. Processing normalizes date and amount, ignores invalid and duplicate rows, applies deterministic category rules, and groups by category, month, and payment method. Outputs include spend, income, savings, top category, average daily spend, budget status, charts, and a monthly CSV.

## Project structure

```text
Personal-Expense-Tracker-Visualization/
├── data/                 # Optional source CSVs; don't commit personal records
├── db/                   # Generated SQLite database (ignored by Git)
├── docs/                 # Project notes and architecture
├── images/               # Screenshots for the portfolio README
├── notebooks/            # Optional exploratory notebooks
├── outputs/              # Generated charts and CSV reports (ignored by Git)
├── reports/              # Optional polished report exports
├── src/main.py           # Streamlit app, data pipeline, database, charts
├── app/                  # Companion browser preview built in Next.js
├── components/           # Dashboard UI component
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## Install and run

Python 3.10+ (3.11 recommended) and Node.js 20+ are useful for the complete portfolio. Python dashboard:

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run src/main.py
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run src/main.py
```

The Python app opens locally in a browser, initializes `db/expenses.db`, seeds clearly synthetic demo transactions, and displays KPIs, charts, budget progress, and activity. CSV columns are `date,description,amount,payment_method`; amount may contain `$` and commas, expenses should be negative, and income positive. The first report export creates `outputs/expense-report-YYYY-MM.csv` plus chart PNGs. Re-running is safe: SQLite ignores duplicate transaction keys.

For the companion Next.js preview in v0, the dashboard is interactive with local sample records; “Add expense” and report export work in that prototype. CSV import and budget management are provided in the Python/Streamlit deliverable.

## Analysis and simulation

1. The app seeds deterministic sample purchase and income records across six months.
2. A keyword map assigns grocery, dining, transport, utility, shopping, or entertainment categories. Income is detected from positive amounts; unmatched expenses are “Other.”
3. `clean_transactions` parses dates and currency-like strings, drops invalid/blank/zero rows, and normalizes methods.
4. SQLite stores normalized transactions, categories, and budget limits; duplicate rows are skipped.
5. Pandas groups spending by month, category, day, and payment method. Savings = income − spend; average daily spending averages the daily totals with transactions.
6. The dashboard compares spend to the selected monthly budget and flags overspending.
7. The report action writes CSV and chart PNGs under `outputs/`.

Expected demo insight: a month shows total spend, income, net savings, highest-spend category, daily average, and budget remaining. Exact totals vary with the calendar month because the synthetic sample is relative to today.

## Implementation phases

| Phase | Work and why | Expected output | Beginner pitfall |
| --- | --- | --- | --- |
| 1 Setup | Install Python and create a venv | Isolated environment | Installing outside activated venv |
| 2 Structure | Create source/data/output folders | Maintainable repo | Mixing generated data with source |
| 3 Sample CSV | Create synthetic, labeled data | Reproducible test input | Including real account details |
| 4 Loading | Read with Pandas | Raw DataFrame | Assuming exact bank headers |
| 5 Cleaning | Parse and validate rows | Consistent dates/amounts | Treating invalid numbers as zero |
| 6 Category analysis | Apply transparent rules | Category totals | Expecting rules to understand every merchant |
| 7 Monthly trends | Group by calendar month | Monthly series | Grouping strings lexically without normalized dates |
| 8 Visualization | Plot category/day/month/payment | PNG charts | Comparing expenses and income as same sign |
| 9 Reporting | Export CSV and charts | Shareable month report | Overwriting source files |
| 10 GitHub | Commit code and synthetic examples | Public proof of work | Committing `.db`, venv, or private CSVs |

## Screenshots and proof plan

Capture: project folder/tree; synthetic dataset preview; terminal showing the app started; dashboard monthly summary; category bar chart; monthly line chart; payment method pie; daily trend; exported monthly report; GitHub repository page. Save image files under `images/` and use descriptive names such as `dashboard-overview.png` and `monthly-spending.png`.

| Day | Deliverable | Example commit |
| --- | --- | --- |
| 1 | Setup, structure, requirements | `chore: scaffold expense tracker` |
| 2 | Synthetic CSV and schema | `feat: add synthetic transaction dataset` |
| 3 | Cleaning, categorization, analysis | `feat: analyze and categorize expenses` |
| 4 | Category and payment visuals | `feat: visualize category spending` |
| 5 | Monthly trend and budgets | `feat: add monthly budget insights` |
| 6 | Report exports, README, screenshots | `docs: document setup and portfolio results` |

Suggested repository name: `personal-expense-tracker-visualization`. Description: “Python + SQLite + Streamlit expense analytics dashboard with synthetic data, category rules, budgets, charts, and monthly CSV reports.” Topics: `python`, `pandas`, `sqlite`, `streamlit`, `data-analysis`, `data-visualization`, `finance`, `portfolio-project`.

## GitHub publishing outline

Create a repository with the suggested name and a concise description. In a local clone, review `.gitignore`, add only source, requirements, synthetic sample data, and selected screenshots, then commit in small descriptive steps and push the working branch. Never upload bank exports, `.env`, database files, or virtual environments. GitHub's web interface can also upload screenshots into `images/`. The v0 project can be published using the Publish button; use GitHub or the shadcn CLI to install/download the code project.

## README screenshot gallery

Add your own captures after running the app:

```md
![Dashboard overview](images/dashboard-overview.png)
![Category spending](images/category-spending.png)
![Monthly spending trend](images/monthly-spending.png)
![Payment method breakdown](images/payment-method.png)
![Monthly report](images/monthly-report.png)
```

## Interview preparation

1. **Explain your project.** I built a Python expense analytics tool that accepts manual or CSV transactions, cleans and categorizes them, stores them in SQLite, summarizes budgets and spending with Pandas, and generates an interactive Streamlit dashboard and monthly reports. Demo records are synthetic; it does not access bank data.
2. **Why SQLite?** It is embedded, requires no server, supports relational constraints and SQL queries, and is ideal for a local course project.
3. **How does categorization work?** Deterministic keyword rules map descriptions to categories; the rules are inspectable and easy to override or extend.
4. **How do you clean the data?** Parse dates with coercion, normalize currency strings, validate required columns, remove invalid/blank/zero rows, and standardize payment methods.
5. **How do you avoid duplicate imports?** A unique transaction key and `INSERT OR IGNORE` make repeated imports idempotent.
6. **How is savings calculated?** Sum positive amounts as income, negate the sum of negative transactions as spending, then subtract spend from income.
7. **What does average daily spending mean?** It is the mean of daily expense totals on days with transactions; for calendar-day averages, include zero-spend dates in the date range.
8. **How would you improve categorization?** Add user corrections and merchant normalization first; then evaluate an ML classifier on labeled examples with a held-out test set.
9. **How would you protect financial data?** Keep database and raw exports out of Git, minimize collected data, validate inputs, restrict access, encrypt backups, and explain that the current app is local/demo only.
10. **What would you build next?** Per-category persisted budgets, edit/delete flows, unit tests, schema migrations, multi-currency support, and optional receipt OCR.

**HR explanation:** “This project shows how I turn messy records into useful, explainable insights. I worked across Python data processing, SQL persistence, visual storytelling, and documentation, and used synthetic data to keep the project safe and reproducible.”

**Technical explanation:** “The pipeline normalizes CSV rows with Pandas, categorizes transactions through deterministic rules, persists them with SQLite constraints and parameterized statements, computes grouped KPIs, then renders Streamlit views and Matplotlib reports. The modules/functions can be tested independently and evolved to support user-labeled rules or a classifier.”

## Limitations and next steps

This local demo is not a banking product and should not be treated as financial advice. The sample implementation includes monthly budget progress in the UI; production-grade per-category budget CRUD, authentication, cloud sync, migration management, and automated tests are future work. A useful next contribution is a test suite for date/amount cleaning, categorization precedence, duplicate import behavior, and empty-month handling.
