import { create } from 'zustand';

interface UserInfo {
  id: string;
  name: string;
}

interface ErrorMsg {
  msg: string;
}

interface UserState {
  user: UserInfo | null;
  isLoading: boolean;
  error: string | null;
  login: (
    account: string,
    password: string,
    callback: () => void,
  ) => Promise<void>;
  logout: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  isLoading: false,
  error: null,
  login: async (account, password, callback) => {
    set({ isLoading: true, error: null });
    try {
      const response: Promise<UserInfo> = new Promise((resolve, reject) => {
        setTimeout(() => {
          if (account === 'root' && password === '123456') {
            resolve({
              id: '1001',
              name: 'joker',
            });
          } else {
            reject({
              msg: '账户密码错误',
            });
          }
        }, 1000);
      });
      const res = await response;
      set({ user: res, isLoading: false });
      callback();
    } catch (e) {
      alert((e as ErrorMsg).msg);
      set({ isLoading: false });
    }
  },
  logout: () => {
    set({ user: null });
  },
}));
