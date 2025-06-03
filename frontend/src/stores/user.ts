import { defineStore } from 'pinia'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
}

interface Account {
  id: number
  user: number
  // Add other account fields as needed
}

interface UserState {
  user: User | null
  account: Account | null
  isAuthenticated: boolean
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    account: null,
    isAuthenticated: false
  }),

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await axios.post('/api/auth/login/', { username, password })
        if (response.data.user && response.data.account) {
          this.user = response.data.user
          this.account = response.data.account
          this.isAuthenticated = true
        }
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    async register(username: string, email: string, password: string) {
      try {
        const response = await axios.post('/api/auth/register/', { username, email, password })
        if (response.data.user && response.data.account) {
          this.user = response.data.user
          this.account = response.data.account
          this.isAuthenticated = true
        }
      } catch (error) {
        console.error('Registration failed:', error)
        throw error
      }
    },

    async logout() {
      try {
        await axios.post('/api/auth/logout/')
        this.user = null
        this.account = null
        this.isAuthenticated = false
      } catch (error) {
        console.error('Logout failed:', error)
        throw error
      }
    },

    async checkAuth() {
      try {
        const response = await axios.get('/api/auth/user/')
        if (response.data.user && response.data.account) {
          this.user = response.data.user
          this.account = response.data.account
          this.isAuthenticated = true
        }
      } catch (error) {
        this.user = null
        this.account = null
        this.isAuthenticated = false
      }
    },

    async updateDietaryPreferences(preferences: string[]) {
      try {
        const response = await axios.post(`/api/accounts/${this.account.id}/update_dietary_preferences/`, {
          dietary_preferences: preferences
        })
        this.account = response.data
        return true
      } catch (error) {
        console.error('Failed to update dietary preferences:', error)
        return false
      }
    },

    async updateFridgeInventory(inventory: string[]) {
      try {
        const response = await axios.post(`/api/accounts/${this.account.id}/update_fridge_inventory/`, {
          fridge_inventory: inventory
        })
        this.account = response.data
        return true
      } catch (error) {
        console.error('Failed to update fridge inventory:', error)
        return false
      }
    }
  }
}) 