// src/api/auth.api.js
import api from "./axios";

export const login = async (data) => {
  const form = new URLSearchParams();
  form.append("username", data.username);
  form.append("password", data.password);

  const res = await api.post("/auth/token", form);
  localStorage.setItem("access_token", res.data.access_token);
  return res.data;
};

export const forgotPassword = (email) =>
  api.post(
    "/auth/forgot-password",
    email,
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

export const resetPassword = (payload) =>
  api.post("/auth/reset-password", payload);
