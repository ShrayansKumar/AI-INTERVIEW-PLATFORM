import { create } from "zustand";

export const useAdminAuthStore = create((set) => ({
  adminToken: sessionStorage.getItem("adminToken") || null,
  admin: null,

  setAdminAuth: (adminToken, admin) => {
    sessionStorage.setItem("adminToken", adminToken);
    set({ adminToken, admin });
  },

  adminLogout: () => {
    sessionStorage.removeItem("adminToken");
    set({ adminToken: null, admin: null });
  },
}));
