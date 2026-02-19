import api from "./axios";

export const getItems = (params) =>
  api.get("/items/", {
    params,
    headers: {
      "Cache-Control": "no-cache",
    },
  });

export const createItem = (data) =>
  api.post("/items/", data);

export const updateItem = (id, data) =>
  api.patch(`/items/${id}`, data);

export const deleteItem = (id) =>
  api.delete(`/items/${id}`);

// Search items (cursor-based)
export const searchItems = (params = {}) =>
  api.get("/items/search", { params });