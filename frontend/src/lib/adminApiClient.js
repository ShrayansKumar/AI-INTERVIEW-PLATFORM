import axios from "axios";
import { useAdminAuthStore } from "../store/adminAuthStore";

const adminApiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

adminApiClient.interceptors.request.use((config) => {
  const token = useAdminAuthStore.getState().adminToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

adminApiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAdminAuthStore.getState().adminLogout();
    }
    return Promise.reject(error);
  },
);

export default adminApiClient;
