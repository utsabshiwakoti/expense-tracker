import api from "./client";

export const getSummary = (params) =>
  api.get("/analytics/summary", { params }).then((r) => r.data);

export const getByCategory = (params) =>
  api.get("/analytics/by-category", { params }).then((r) => r.data);

export const getMonthly = (months = 6) =>
  api.get("/analytics/monthly", { params: { months } }).then((r) => r.data);

export const getCategories = () =>
  api.get("/categories").then((r) => r.data);

export const getExpenses = (params) =>
  api.get("/expenses", { params }).then((r) => r.data);

export const createExpense = (body) =>
  api.post("/expenses", body).then((r) => r.data);

export const deleteExpense = (id) => api.delete(`/expenses/${id}`);
