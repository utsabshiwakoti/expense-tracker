import { useState } from "react";
import { errorMessage } from "../../api/client";
import { createExpense } from "../../api/endpoints";

const today = () => new Date().toISOString().slice(0, 10);

export default function ExpenseForm({ categories, onAdded }) {
  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [spentOn, setSpentOn] = useState(today());
  const [categoryId, setCategoryId] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await createExpense({
        amount: Number(amount),
        description,
        spent_on: spentOn,
        category_id: categoryId ? Number(categoryId) : null,
      });
      setAmount("");
      setDescription("");
      onAdded();
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="panel expense-form" onSubmit={handleSubmit}>
      <h2>Add expense</h2>
      <input type="number" step="0.01" min="0.01" placeholder="Amount"
        value={amount} onChange={(e) => setAmount(e.target.value)} required />
      <input type="text" placeholder="Description" maxLength={200}
        value={description} onChange={(e) => setDescription(e.target.value)} />
      <input type="date" value={spentOn}
        onChange={(e) => setSpentOn(e.target.value)} required />
      <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)}>
        <option value="">No category</option>
        {categories.map((c) => (
          <option key={c.id} value={c.id}>{c.name}</option>
        ))}
      </select>
      {error && <p className="error">{error}</p>}
      <button disabled={busy}>{busy ? "Adding..." : "Add"}</button>
    </form>
  );
}
