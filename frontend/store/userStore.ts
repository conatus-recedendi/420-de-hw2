import { user } from "@nextui-org/theme";
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : "http://localhost:8000/api";

type User = {
  id: number;
  age: number;
  gender: string;
  income: number;
  education: string;
  region: string;
  loyalty_status: string;
  purchase_frequency: string;
  purchase_amount: number;
  product_category: string;
  promotion_usage: number;
  satisfaction_score: number;
};

interface UserStore {
  user: null | User;
  recommendedCategory: string;
  openPopup: boolean;
  userList: User[];
  fetchUserList: () => Promise<void>;
  fetchPredict: (userId: string) => Promise<void>;
  selectUser: (userId: number) => void;
  closeModal: () => void;
}

export const userStore = create<UserStore>()(
  persist(
    (set, get) => ({
      user: null,
      recommendedCategory: "",
      openPopup: false,
      userList: [],
      fetchUserList: async () => {
        const response = await fetch(`${URL}/user`);
        const data = await response.json();
        set({ userList: data });
      },
      selectUser: (userId: number) => {
        const res = get().userList.find((u) => u.id === userId);
        if (res) set({ user: res });
      },
      fetchPredict: async (userId: string) => {
        const response = await fetch(`${URL}/predict/${userId}`);
        const data = await response.json();
        if (data.predict_popup) {
          set({ openPopup: true });
        }
        if (data.predict_category) {
          set({ recommendedCategory: data.predict_category });
        }
      },
      closeModal: () => {
        set({ openPopup: false });
      },
    }),
    {
      name: "user-store",
      storage: createJSONStorage(() => localStorage),
    }
  )
);
