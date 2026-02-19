// src/api/users.api.js
import api from "./axios";

/* ================= LIST & READ ================= */

// Get all users (admin)
export const getUsers = (params = {}) =>
  api.get("/users/", { params });

// Get current logged-in user
export const getMe = () =>
  api.get("/users/me");

// Get single user by ID
export const getUserById = (id) =>
  api.get(`/users/${id}`);

/* ================= CREATE ================= */

// Create new user (admin)
export const createUser = (data) =>
  api.post("/users/", data);

/* ================= UPDATE ================= */

// Update user (partial update)
export const updateUser = (id, data) =>
  api.patch(`/users/${id}`, data);

/* ================= DELETE ================= */

// Delete user
export const deleteUser = (id) =>
  api.delete(`/users/${id}`);

/* ================= SEARCH (optional, advanced) ================= */

// Search users (cursor-based)
export const searchUsers = (params = {}) =>
  api.get("/users/search", { params });
