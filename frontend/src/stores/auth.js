import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null
}),

getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role_id === 1,
    isEmploye: (state) => state.user?.role_id === 2,
},

actions: {
    setToken(token) {
    this.token = token
    localStorage.setItem('token', token)
    },
    setUser(user) {
    this.user = user
    localStorage.setItem('user', JSON.stringify(user))
    },
    logout() {
    this.token = null
    this.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    }
}
})