'use client'

import { useMemo, useState } from 'react'
import { ArrowDownLeft, ArrowUpRight, Bell, CalendarDays, ChevronDown, CircleHelp, Download, FileUp, LayoutDashboard, Menu, Plus, Search, Settings2, Wallet, X } from 'lucide-react'

type Tx = { name: string; detail: string; category: string; date: string; amount: number; icon: string; color: string }
const initial: Tx[] = [
  { name: 'Whole Foods Market', detail: 'Groceries ·•• 4821', category: 'Groceries', date: 'Today, 10:42 AM', amount: -68.42, icon: 'W', color: 'mint' },
  { name: 'Monthly salary', detail: 'Income · Direct deposit', category: 'Income', date: 'Today, 8:15 AM', amount: 4250, icon: '↗', color: 'blue' },
  { name: 'Blue Bottle Coffee', detail: 'Food & dining ·•• 4821', category: 'Food & dining', date: 'Yesterday', amount: -8.75, icon: 'B', color: 'peach' },
  { name: 'City Transit', detail: 'Transport ·•• 2104', category: 'Transport', date: 'Nov 18, 2026', amount: -24, icon: '↔', color: 'lavender' },
  { name: 'Netflix', detail: 'Entertainment ·•• 4821', category: 'Entertainment', date: 'Nov 17, 2026', amount: -17.99, icon: 'N', color: 'rose' },
]
const categories = [ ['Housing', 1450, 1800, '#c2d944'], ['Food & dining', 482, 650, '#ff9c6a'], ['Transport', 216, 300, '#a898ef'], ['Shopping', 348, 400, '#6bb9c4'] ] as const
const months = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
const spend = [2450, 2180, 2780, 2320, 2610, 2542]
const money = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 }).format(n)

export function ExpenseDashboard() {
  const [transactions, setTransactions] = useState(initial)
  const [query, setQuery] = useState('')
  const [showAdd, setShowAdd] = useState(false)
  const [toast, setToast] = useState('')
  const [name, setName] = useState('')
  const [amount, setAmount] = useState('')
  const [mobileNav, setMobileNav] = useState(false)
  const filtered = useMemo(() => transactions.filter(t => `${t.name} ${t.category}`.toLowerCase().includes(query.toLowerCase())), [transactions, query])
  function addTransaction(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const value = Number(amount)
    if (!name.trim() || !Number.isFinite(value) || value <= 0) return
    setTransactions([{ name: name.trim(), detail: 'Uncategorized · Manual entry', category: 'Other', date: 'Just now', amount: -value, icon: name.trim()[0].toUpperCase(), color: 'mint' }, ...transactions])
    setName(''); setAmount(''); setShowAdd(false); setToast('Expense added to your activity')
    window.setTimeout(() => setToast(''), 2800)
  }
  function exportReport() {
    const rows = [['Name','Category','Date','Amount'], ...transactions.map(t => [t.name,t.category,t.date,t.amount.toFixed(2)])]
    const csv = rows.map(r => r.map(v => `"${String(v).replaceAll('"','""')}"`).join(',')).join('\n')
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
    const a = document.createElement('a'); a.href = url; a.download = 'november-expense-report.csv'; a.click(); URL.revokeObjectURL(url)
  }
  return <div className="app-shell">
    <aside className={`sidebar ${mobileNav ? 'sidebar-open' : ''}`}>
      <div className="brand"><span className="brand-mark"><Wallet size={19}/></span><span>pennywise<span className="brand-dot">.</span></span><button className="icon-button mobile-close" aria-label="Close navigation" onClick={() => setMobileNav(false)}><X size={18}/></button></div>
      <div className="workspace-label">WORKSPACE</div>
      <nav className="side-nav" aria-label="Main navigation"><a className="nav-link active" href="#overview"><LayoutDashboard size={17}/>Overview</a><a className="nav-link" href="#transactions"><ArrowDownLeft size={17}/>Transactions<span className="nav-count">12</span></a><a className="nav-link" href="#budgets"><Wallet size={17}/>Budgets</a></nav>
      <div className="workspace-label tools-label">TOOLS</div><nav className="side-nav" aria-label="Tools"><a className="nav-link" href="#reports"><CalendarDays size={17}/>Reports</a><a className="nav-link" href="#settings"><Settings2 size={17}/>Settings</a></nav>
      <div className="sidebar-bottom"><div className="budget-mini"><div className="budget-mini-head"><span>This month</span><span className="mini-dots">•••</span></div><strong>$2,542<span>.80</span></strong><div className="meter"><i style={{width:'72%'}}/></div><small><b>$957</b> left of $3,500</small></div><button className="profile"><span className="avatar">JD</span><span className="profile-copy"><b>Jamie Davis</b><small>Personal account</small></span><ChevronDown size={15}/></button></div>
    </aside>
    {mobileNav && <button className="scrim" aria-label="Close navigation" onClick={() => setMobileNav(false)}/>}
    <main className="main-content" id="overview">
      <header className="topbar"><button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setMobileNav(true)}><Menu size={20}/></button><div className="crumb">My finances <span>/</span> <b>Overview</b></div><div className="top-actions"><button className="icon-button" aria-label="Help"><CircleHelp size={18}/></button><button className="icon-button notification" aria-label="Notifications"><Bell size={18}/><i/></button><span className="top-avatar">JD</span></div></header>
      <div className="content-wrap"><section className="page-heading"><div><div className="eyebrow"><span className="live-dot"/>YOUR FINANCIAL SNAPSHOT</div><h1>Good morning, Jamie <span>✳</span></h1><p>Here&apos;s what&apos;s happening with your money this month.</p></div><div className="heading-actions"><button className="button secondary" onClick={exportReport}><Download size={16}/>Export report</button><button className="button primary" onClick={() => setShowAdd(true)}><Plus size={17}/>Add expense</button></div></section>
      <section className="stats-grid" aria-label="Monthly financial summary"><article className="stat-card primary-stat"><div className="stat-top"><span>Total spending</span><span className="stat-icon"><ArrowUpRight size={17}/></span></div><strong>$2,542<span>.80</span></strong><div className="stat-foot"><span className="trend down"><ArrowDownLeft size={13}/> 8.2%</span><span>vs. last month</span><div className="sparkline"><i/><i/><i/><i/><i/><i/><i/></div></div></article><article className="stat-card"><div className="stat-top"><span>Monthly income</span><span className="stat-icon green"><ArrowDownLeft size={17}/></span></div><strong>$4,250<span>.00</span></strong><div className="stat-foot"><span className="trend up"><ArrowUpRight size={13}/> 4.5%</span><span>vs. last month</span></div></article><article className="stat-card"><div className="stat-top"><span>Available to save</span><span className="stat-icon peach-icon"><Wallet size={17}/></span></div><strong>$1,707<span>.20</span></strong><div className="stat-foot"><span className="saving-label"><span/>40.2% savings rate</span></div></article></section>
      <section className="insights-grid"><article className="panel spending-panel"><div className="panel-heading"><div><h2>Spending overview</h2><p>Your spending over the last 6 months</p></div><button className="select-button">Last 6 months <ChevronDown size={14}/></button></div><div className="chart-legend"><span><i className="legend-spend"/> Spending</span><span><i className="legend-income"/> Income</span></div><div className="chart-area"><div className="y-labels"><span>$5k</span><span>$3k</span><span>$1k</span><span>$0</span></div><div className="chart-plot"><div className="grid-line line-one"/><div className="grid-line line-two"/><div className="grid-line line-three"/><div className="bar-groups">{months.map((m,i)=><div className="bar-group" key={m}><div className="bars"><span className="income-bar" style={{height:`${[78,68,86,77,90,84][i]}%`}}/><span className="spend-bar" style={{height:`${spend[i]/35}%`}}/></div><small>{m}</small></div>)}</div></div></div></article>
      <article className="panel categories-panel" id="budgets"><div className="panel-heading"><div><h2>Budget status</h2><p>Category limits for November</p></div><button className="more-button" aria-label="More budget options">•••</button></div><div className="category-list">{categories.map(([label,val,max,color])=><div className="category-row" key={label}><div className="category-line"><span className="category-name"><i style={{background:color}}/>{label}</span><span className="category-value">{money(val)} <small>/ {money(max)}</small></span></div><div className="category-meter"><span style={{width:`${val/max*100}%`,background:color}}/></div></div>)}</div><button className="text-link" onClick={()=>setToast('Budget editor is available in the Python dashboard')}>Manage budgets <span>→</span></button></article></section>
      <section className="panel transactions-panel" id="transactions"><div className="panel-heading transaction-heading"><div><h2>Recent transactions</h2><p>Your latest income and expenses</p></div><div className="transaction-tools"><label className="search-box"><Search size={15}/><input aria-label="Search transactions" placeholder="Search" value={query} onChange={e=>setQuery(e.target.value)}/></label><button className="select-button date-select"><CalendarDays size={15}/> November <ChevronDown size={14}/></button><button className="button secondary upload-button" onClick={()=>setToast('CSV import is available in the Python dashboard')}><FileUp size={15}/>Import CSV</button></div></div><div className="table-wrap"><table><thead><tr><th>TRANSACTION</th><th>CATEGORY</th><th>DATE</th><th className="amount-col">AMOUNT</th></tr></thead><tbody>{filtered.map((t,i)=><tr key={`${t.name}-${i}`}><td><div className="transaction-name"><span className={`merchant-icon ${t.color}`}>{t.icon}</span><span><b>{t.name}</b><small>{t.detail}</small></span></div></td><td><span className={`pill ${t.category==='Income'?'income-pill':''}`}>{t.category}</span></td><td className="date-cell">{t.date}</td><td className={`amount-cell ${t.amount>0?'positive':''}`}>{t.amount>0?'+':'−'}{money(Math.abs(t.amount))}</td></tr>)}</tbody></table>{filtered.length===0&&<div className="empty-state">No transactions match “{query}”.</div>}</div><button className="view-all" onClick={()=>setToast('You’re viewing all recent transactions')}>View all transactions <span>→</span></button></section>
      <footer className="footer-note">Built for better money habits <span>·</span> Demo data for portfolio use only</footer></div>
    </main>
    {showAdd&&<div className="modal-backdrop" role="presentation" onMouseDown={e=>{if(e.target===e.currentTarget)setShowAdd(false)}}><section className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title"><div className="modal-head"><div><div className="eyebrow">QUICK ENTRY</div><h2 id="modal-title">Add an expense</h2></div><button className="icon-button" aria-label="Close dialog" onClick={()=>setShowAdd(false)}><X size={18}/></button></div><form onSubmit={addTransaction}><label>Description<input autoFocus value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Lunch with friends" required/></label><label>Amount <span className="input-prefix"><span>$</span><input type="number" min="0.01" step="0.01" value={amount} onChange={e=>setAmount(e.target.value)} placeholder="0.00" required/></span></label><div className="modal-actions"><button type="button" className="button secondary" onClick={()=>setShowAdd(false)}>Cancel</button><button type="submit" className="button primary"><Plus size={16}/>Save expense</button></div></form></section></div>}
    {toast&&<div role="status" className="toast">{toast}<button aria-label="Dismiss notification" onClick={()=>setToast('')}><X size={14}/></button></div>}
  </div>
}
