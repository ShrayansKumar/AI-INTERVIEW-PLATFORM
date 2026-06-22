import { create } from "zustand";
import axios from "axios";

export const useAuthStore = create((set, get) => ({
  accessToken: localStorage.getItem("accessToken") || null,
  refreshToken: localStorage.getItem("refreshToken") || null,
  user: null,
  authChecked: false,

  setAuth: (accessToken, refreshToken, user) => {
    localStorage.setItem("accessToken", accessToken);
    localStorage.setItem("refreshToken", refreshToken);
    set({ accessToken, refreshToken, user, authChecked: true });
  },

  setAccessToken: (accessToken) => {
    localStorage.setItem("accessToken", accessToken);
    set({ accessToken });
  },

  logout: () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    set({
      accessToken: null,
      refreshToken: null,
      user: null,
      authChecked: true,
    });
  },

  // Called once on app load — tries to silently refresh before showing the modal
  initAuth: async () => {
    const { refreshToken } = get();
    if (!refreshToken) {
      set({ authChecked: true });
      return;
    }

    try {
      const baseURL =
        import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
      const response = await axios.post(`${baseURL}/api/v1/auth/refresh`, {
        refresh_token: refreshToken,
      });
      get().setAccessToken(response.data.access_token);
    } catch {
      get().logout();
    } finally {
      set({ authChecked: true });
    }
  },

  // Fetches the full user profile (name, email, profile_picture_url)
  // Called after login/refresh succeeds, so the dropdown has real data to show.
  fetchCurrentUser: async () => {
    try {
      const apiClient = (await import("../lib/apiClient")).default;
      const response = await apiClient.get("/api/v1/auth/me");
      set({ user: response.data });
    } catch {
      // Silently ignore -- not critical if this fails
    }
  },
}));
