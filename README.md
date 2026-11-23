# Lumina - Personal Expense Tracker

Lumina is a personal finance dashboard for exploring spending, income, budgets, and recent transactions. It includes a responsive Next.js interface and a Python Streamlit analytics app backed by SQLite.

**Live app:** https://lumina-webss.vercel.app

## Features

- Monthly spending, income, and savings overview
- Spending breakdown by category and payment method
- Six-month financial trend visualization
- Budget status and remaining balance
- Searchable transaction history
- Manual expense entry
- CSV report export
- CSV transaction import in the Python dashboard
- SQLite-backed transaction storage
- Synthetic demo data; no real banking connection

## Applications

### Next.js web interface

The deployed interface presents the Lumina dashboard with sample portfolio data. It supports expense entry, transaction search, category budget status, and CSV export.

### Python analytics dashboard

The Streamlit application provides a SQLite data pipeline, CSV imports, synthetic data generation, monthly filtering, budget alerts, chart exports, and a downloadable monthly report.

## Tech Stack

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- Lucide React
- Python 3.10+
- Pandas
- SQLite
- Streamlit
- Matplotlib

## Project Structure

```text
lumina/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   └── expense-dashboard.tsx
├── src/
│   └── main.py
├── requirements.txt
├── package.json
└── README.md
```

## Run the Web Interface

Requirements: Node.js 20+ and pnpm.

```bash
pnpm install
pnpm dev
```

Open `http://localhost:3000`.

### Production build

```bash
pnpm build
pnpm start
```

## Run the Python Dashboard

Requirements: Python 3.10 or later.

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start Streamlit:

```bash
python -m pip install -r requirements.txt
streamlit run src/main.py
```

The Streamlit app opens in your browser and creates `db/expenses.db` automatically.

## CSV Import Format

The Python dashboard accepts CSV files with these columns:

```text
date,description,amount,payment_method
2026-11-20,Grocery market,-92.15,Card
2026-11-21,Monthly salary,4250.00,Bank transfer
```

- `date`, `description`, and `amount` are required.
- `payment_method` is optional and defaults to `Card`.
- Negative amounts represent expenses.
- Positive amounts represent income.
- Invalid rows and duplicate transactions are skipped.

## Data and Privacy

Lumina uses clearly labeled synthetic demo records by default. It does not connect to banks or collect real account credentials. Generated SQLite databases and reports should not be committed to Git.

## Possible Improvements

- Persistent category budgets and editing flows
- Authentication and per-user cloud storage
- Real CSV account imports with configurable columns
- Unit tests for cleaning and categorization
- Database migrations
- Multi-currency support
- Automated transaction categorization

## License

No license has been specified for this repository.
