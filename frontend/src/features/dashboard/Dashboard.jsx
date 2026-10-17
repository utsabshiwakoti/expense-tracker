import { useCallback, useEffect, useState } from "react";
import {
  getByCategory, getCategories, getExpenses, getMonthly, getSummary,
} from "../../api/endpoints";
import { useAuth } from "../auth/AuthContext";
import ExpenseForm from "../expenses/ExpenseForm";
import ExpenseTable from "../expenses/ExpenseTable";
import CategoryChart from "./CategoryChart";
import MonthlyChart from "./MonthlyChart";
import SummaryCards from "./SummaryCards";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [summary, setSummary] = useState(null);
  const [byCategory, setByCategory] = useState([]);
  const [monthly, setMonthly] = useState([]);
  const [categories, setCategories] = useState([]);
  const [expenses, setExpenses] = useState({ items: [], total: 0, page: 1, page_size: 10 });
  const [page, setPage] = useState(1);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      const [s, c, m, cats, ex] = await Promise.all([
        getSummary(),
        getByCategory(),
        getMonthly(6),
        getCategories(),
        getExpenses({ page, page_size: 10 }),
      ]);
      setSummary(s);
      setByCategory(c);
      setMonthly(m);
      setCategories(cats);
      setExpenses(ex);
      setError("");
    } catch {
      setError("Could not load data. Is the backend running?");
    }
  }, [page]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div className="page">
      <header>
        <h1>Expense Tracker</h1>
        <div>
          <span>{user?.email}</span>
          <button onClick={logout}>Log out</button>
        </div>
      </header>

      {error && <p className="error">{error}</p>}

      <SummaryCards summary={summary} />

      <div className="grid-2">
        <CategoryChart data={byCategory} />
        <MonthlyChart data={monthly} />
      </div>

      <div className="grid-2 wide-left">
        <ExpenseForm categories={categories} onAdded={() => { setPage(1); load(); }} />
        <ExpenseTable
          data={expenses}
          categories={categories}
          page={page}
          onPage={setPage}
          onChanged={load}
        />
      </div>
    </div>
  );
}
