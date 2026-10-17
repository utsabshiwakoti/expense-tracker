import { deleteExpense } from "../../api/endpoints";

export default function ExpenseTable({ data, categories, page, onPage, onChanged }) {
  const names = Object.fromEntries(categories.map((c) => [c.id, c.name]));
  const pages = Math.max(1, Math.ceil(data.total / data.page_size));

  async function handleDelete(id) {
    if (!window.confirm("Delete this expense?")) return;
    await deleteExpense(id);
    onChanged();
  }

  return (
    <div className="panel">
      <h2>Expenses</h2>
      {data.items.length === 0 ? (
        <p className="muted">No expenses yet. Add one above.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Date</th><th>Description</th><th>Category</th><th>Amount</th><th></th></tr>
            </thead>
            <tbody>
              {data.items.map((e) => (
                <tr key={e.id}>
                  <td>{e.spent_on}</td>
                  <td>{e.description || "—"}</td>
                  <td>{names[e.category_id] || "Uncategorized"}</td>
                  <td>${Number(e.amount).toFixed(2)}</td>
                  <td><button className="link" onClick={() => handleDelete(e.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className="pager">
        <button disabled={page <= 1} onClick={() => onPage(page - 1)}>Prev</button>
        <span>Page {page} of {pages}</span>
        <button disabled={page >= pages} onClick={() => onPage(page + 1)}>Next</button>
      </div>
    </div>
  );
}
