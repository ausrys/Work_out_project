import axios from "axios";

// Create axios instance with base URL and default headers
const api = axios.create({
  baseURL: "http://localhost:8000/",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

export default api;
