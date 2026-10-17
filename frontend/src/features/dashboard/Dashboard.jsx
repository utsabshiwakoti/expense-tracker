import { useAuth } from "../auth/AuthContext";

export default function Dashboard() {
  const { user, logout } = useAuth();
  return (
    <div className="page">
      <header>
        <h1>Expense Tracker</h1>
        <div>
          <span>{user?.email}</span>
          <button onClick={logout}>Log out</button>
        </div>
      </header>
      <p>Logged in. Charts coming next.</p>
    </div>
  );
}
