const money = (v) =>
  Number(v).toLocaleString(undefined, { style: "currency", currency: "USD" });

export default function SummaryCards({ summary }) {
  if (!summary) return null;
  return (
    <div className="cards">
      <div className="card">
        <span>Total spent</span>
        <strong>{money(summary.total)}</strong>
      </div>
      <div className="card">
        <span>Expenses</span>
        <strong>{summary.count}</strong>
      </div>
      <div className="card">
        <span>Average</span>
        <strong>{money(summary.average)}</strong>
      </div>
    </div>
  );
}
