import api from "./axios";

export const getCart = () => api.get("/cart");

export const addToCart = (data) =>
  api.post("/cart/add", data);

export const updateCart = (productId, data) =>
  api.patch(`/cart/update/${productId}`, data);

export const removeCart = (productId) =>
  api.delete(`/cart/remove/${productId}`);