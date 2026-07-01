import { create } from 'zustand'
import axios from 'axios'

interface User {
  id: string
  email: string
  name: string
}

interface AuthState {
  token: string | null
  user: User | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, name: string) => Promise<void>
  logout: () => void
  init: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  login: async (email, password) => {
    const { data } = await axios.post('/api/auth/login', { email, password })
    set({ token: data.access_token, user: data.user })
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  },
  register: async (email, password, name) => {
    const { data } = await axios.post('/api/auth/register', { email, password, name })
    set({ token: data.access_token, user: data.user })
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  },
  logout: () => {
    set({ token: null, user: null })
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
  init: () => {
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    if (token && user) {
      set({ token, user: JSON.parse(user) })
    }
  },
}))
