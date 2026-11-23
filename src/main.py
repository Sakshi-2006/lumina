"""Personal Expense Tracker: SQLite-backed analysis, charts, CSV import and reports."""
from __future__ import annotations
import csv
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
DB = ROOT / "db" / "expenses.db"
CATEGORIES = {
    "Groceries": ("grocery", "market", "whole foods", "trader joe", "supermarket"),
    "Food & dining": ("restaurant", "cafe", "coffee", "lunch", "dinner", "takeout"),
    "Transport": ("uber", "transit", "metro", "gas", "fuel", "bus"),
    "Bills & utilities": ("electric", "water", "internet", "phone", "utility"),
    "Shopping": ("amazon", "target", "clothing", "shop", "store"),
    "Entertainment": ("netflix", "spotify", "movie", "cinema", "concert"),
}


def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    return con


def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
        CREATE TABLE IF NOT EXISTS transactions(
          id INTEGER PRIMARY KEY, tx_date TEXT NOT NULL, description TEXT NOT NULL,
          amount REAL NOT NULL CHECK(amount != 0), payment_method TEXT NOT NULL DEFAULT 'Card',
          category_id INTEGER REFERENCES categories(id), source TEXT DEFAULT 'manual',
          UNIQUE(tx_date, description, amount, payment_method));
        CREATE TABLE IF NOT EXISTS budgets(
          month TEXT NOT NULL, category_name TEXT NOT NULL, limit_amount REAL NOT NULL CHECK(limit_amount > 0),
          PRIMARY KEY(month, category_name));
        """)
        for name in [*CATEGORIES, "Income", "Other"]:
            con.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)", (name,))


def classify(description: str, amount: float) -> str:
    if amount > 0:
        return "Income"
    text = description.casefold()
    for category, words in CATEGORIES.items():
        if any(word in text for word in words):
            return category
    return "Other"


def clean_transactions(frame: pd.DataFrame, date_col="date", desc_col="description", amount_col="amount", payment_col="payment_method") -> pd.DataFrame:
    """Normalize common CSV fields; reject invalid dates, blank descriptions and zero amounts."""
    aliases = {"Date": "date", "Description": "description", "Amount": "amount", "Payment Method": "payment_method"}
    frame = frame.rename(columns=aliases).copy()
    required = {date_col, desc_col, amount_col}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
    result = pd.DataFrame({
        "tx_date": pd.to_datetime(frame[date_col], errors="coerce").dt.strftime("%Y-%m-%d"),
        "description": frame[desc_col].astype("string").str.strip(),
        "amount": pd.to_numeric(frame[amount_col].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce"),
        "payment_method": frame[payment_col].fillna("Card").astype(str).str.strip() if payment_col in frame else "Card",
    })
    result = result.dropna(subset=["tx_date", "amount"])
    result = result[(result.description.notna()) & (result.description.str.len() > 0) & (result.amount != 0)]
    result["category"] = [classify(d, a) for d, a in zip(result.description, result.amount)]
    return result.reset_index(drop=True)


def save_transactions(frame: pd.DataFrame, source="manual") -> int:
    init_db()
    added = 0
    with connect() as con:
        for row in frame.itertuples(index=False):
            con.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)", (row.category,))
            category_id = con.execute("SELECT id FROM categories WHERE name=?", (row.category,)).fetchone()[0]
            cursor = con.execute("INSERT OR IGNORE INTO transactions(tx_date,description,amount,payment_method,category_id,source) VALUES(?,?,?,?,?,?)",
                                 (row.tx_date, row.description, float(row.amount), row.payment_method, category_id, source))
            added += cursor.rowcount
    return added


def load_transactions() -> pd.DataFrame:
    init_db()
    with connect() as con:
        frame = pd.read_sql_query("""SELECT t.tx_date AS date,t.description,t.amount,t.payment_method,c.name AS category
            FROM transactions t LEFT JOIN categories c ON c.id=t.category_id ORDER BY t.tx_date DESC,t.id DESC""", con)
    if not frame.empty:
        frame["date"] = pd.to_datetime(frame.date)
        frame["month"] = frame.date.dt.to_period("M").astype(str)
    return frame


def create_sample_data():
    """Seed deterministic synthetic transactions for a 6-month demonstration."""
    if not load_transactions().empty:
        return
    entries = []
    merchants = [("Whole Foods grocery", -68.42, "Card"), ("Coffee cafe", -8.75, "Card"), ("City Transit", -24, "Transit card"),
                ("Netflix subscription", -17.99, "Card"), ("Amazon shopping", -43.50, "Card"), ("Electric utility bill", -82.10, "Bank transfer"),
                ("Monthly salary", 4250, "Bank transfer"), ("Restaurant dinner", -54.20, "Card"), ("Gas station fuel", -46.30, "Card"), ("Grocery market", -92.15, "Card")]
    today = date.today()
    for offset in range(180):
        day = today - timedelta(days=offset)
        if offset % 30 == 0:
            entries.append((day.isoformat(), "Monthly salary", 4250, "Bank transfer"))
        if offset % 3 == 0:
            name, amount, method = merchants[(offset // 3) % (len(merchants) - 1)]
            entries.append((day.isoformat(), name, amount, method))
    frame = pd.DataFrame(entries, columns=["tx_date", "description", "amount", "payment_method"])
    frame["category"] = [classify(d, a) for d, a in zip(frame.description, frame.amount)]
    save_transactions(frame, "synthetic demo")


def summarize(frame: pd.DataFrame, month: str | None = None) -> dict:
    selected = frame if not month else frame[frame.month == month]
    expenses = selected[selected.amount < 0]
    income = selected[selected.amount > 0]
    spend = -expenses.amount.sum()
    return {"spend": float(spend), "income": float(income.amount.sum()), "savings": float(income.amount.sum() - spend),
            "top_category": (-expenses.groupby("category").amount.sum()).idxmax() if not expenses.empty else "—",
            "average_daily_spend": float((-expenses.groupby(expenses.date.dt.date).amount.sum()).mean()) if not expenses.empty else 0.0,
            "category_spend": -expenses.groupby("category").amount.sum().sort_values(ascending=False),
            "payment_spend": -expenses.groupby("payment_method").amount.sum().sort_values(ascending=False)}


def save_charts(frame: pd.DataFrame, month: str):
    OUTPUTS.mkdir(exist_ok=True)
    selected = frame[(frame.month == month) & (frame.amount < 0)].copy()
    charts = [
        ("category-spend.png", -selected.groupby("category").amount.sum().sort_values(), "Spending by category", "#b8cd3a", "barh"),
        ("daily-spend.png", -selected.groupby(selected.date.dt.day).amount.sum(), "Daily spending trend", "#e9895a", "line"),
        ("payment-method.png", -selected.groupby("payment_method").amount.sum(), "Spending by payment method", "#a898ef", "pie"),
    ]
    monthly = -frame[frame.amount < 0].groupby("month").amount.sum()
    charts.append(("monthly-spend.png", monthly, "Monthly spending trend", "#b8cd3a", "monthly"))
    for filename, values, title, color, kind in charts:
        fig, ax = plt.subplots(figsize=(8, 4), facecolor="#fffefa")
        if kind == "barh": values.plot.barh(ax=ax, color=color)
        elif kind == "line": values.plot(ax=ax, color=color, marker="o", linewidth=2)
        elif kind == "pie": values.plot.pie(ax=ax, autopct="%1.0f%%", colors=["#b8cd3a", "#ff9c6a", "#a898ef", "#6bb9c4", "#e7b4b4"], ylabel="")
        elif kind == "monthly": values.plot(ax=ax, color=color, marker="o", linewidth=2)
        ax.set_title(title, loc="left", fontweight="bold"); ax.set_facecolor("#fffefa"); ax.grid(axis="y", alpha=.18)
        fig.tight_layout(); fig.savefig(OUTPUTS / filename, dpi=150, bbox_inches="tight"); plt.close(fig)


def export_month(frame: pd.DataFrame, month: str) -> Path:
    OUTPUTS.mkdir(exist_ok=True)
    selected = frame[frame.month == month].copy()
    path = OUTPUTS / f"expense-report-{month}.csv"
    selected.drop(columns=["month"], errors="ignore").to_csv(path, index=False, date_format="%Y-%m-%d")
    return path


def main():
    import streamlit as st
    st.set_page_config(page_title="Pennywise · Expense Tracker", page_icon="◈", layout="wide")
    st.title("◈ Pennywise")
    st.caption("A clearer picture of where your money goes.")
    init_db(); create_sample_data()
    uploaded = st.file_uploader("Import transactions from CSV", type="csv", help="Required columns: date, description, amount. Optional: payment_method")
    if uploaded:
        try:
            frame = clean_transactions(pd.read_csv(uploaded))
            count = save_transactions(frame, uploaded.name)
            st.success(f"Imported {count} new transactions; duplicates were safely skipped.")
        except (ValueError, pd.errors.ParserError) as error:
            st.error(str(error))
    with st.form("manual-entry", clear_on_submit=True):
        st.subheader("Add an expense")
        a, b, c, d = st.columns(4)
        tx_date = a.date_input("Date", value=date.today())
        description = b.text_input("Description", placeholder="Coffee shop")
        amount = c.number_input("Amount (expense)", min_value=0.01, step=1.0)
        method = d.selectbox("Payment method", ["Card", "Cash", "Bank transfer", "Transit card"])
        if st.form_submit_button("Save expense") and description.strip():
            data = pd.DataFrame([{"tx_date": tx_date.isoformat(), "description": description.strip(), "amount": -amount, "payment_method": method, "category": classify(description, -amount)}])
            save_transactions(data); st.rerun()
    frame = load_transactions()
    if frame.empty:
        st.info("Add a transaction or import a CSV to get started."); return
    months = sorted(frame.month.unique(), reverse=True)
    month = st.selectbox("Reporting month", months)
    current = frame[frame.month == month]
    kpi = summarize(frame, month)
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total spending", f"${kpi['spend']:,.2f}")
    k2.metric("Income", f"${kpi['income']:,.2f}")
    k3.metric("Savings", f"${kpi['savings']:,.2f}")
    k4.metric("Average daily spend", f"${kpi['average_daily_spend']:,.2f}")
    st.subheader(f"November snapshot · Top category: {kpi['top_category']}")
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown("**Monthly spending**")
        st.line_chart(-frame[frame.amount < 0].groupby("month").amount.sum(), color="#b8cd3a")
    with right:
        st.markdown("**Category breakdown**")
        st.bar_chart(kpi["category_spend"], color="#ff9c6a")
    st.markdown("**Payment method breakdown**")
    st.bar_chart(kpi["payment_spend"], color="#a898ef")
    budget = st.number_input("Monthly budget (all categories)", min_value=0.0, value=3500.0, step=100.0)
    progress = min(kpi["spend"] / budget, 1.0) if budget else 0.0
    st.progress(progress, text=f"${kpi['spend']:,.2f} of ${budget:,.2f} spent")
    if kpi["spend"] > budget:
        st.warning(f"Over budget by ${kpi['spend'] - budget:,.2f}.")
    if st.button("Generate monthly report"):
        save_charts(frame, month); report = export_month(frame, month)
        st.success("Report and charts saved in outputs/.")
        st.download_button("Download monthly CSV", report.read_bytes(), file_name=report.name, mime="text/csv")
    st.subheader("Transactions")
    st.dataframe(current.drop(columns=["month"], errors="ignore"), use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
