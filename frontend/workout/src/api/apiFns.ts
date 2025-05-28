// API Functions
// api.ts

import api from "./axios";

export const getUserProfile = async () => {
  const response = await api.get("/user-info/");
  return response.data;
};
