import { defineStore } from 'pinia'
import { apiClient } from '@/api' // Import the configured apiClient instance

interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

interface Account {
  id: number
  user: number
  dietary_preferences: string[];  
  fridge_inventory: string[]; 
  allergies: string[];   
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
        const response = await apiClient.post('/auth/login/', { username, password })
        if (response.data.user && response.data.account) {
          this.user = response.data.user
          this.account = response.data.account
          this.isAuthenticated = true
          // Store authentication state
          localStorage.setItem('isAuthenticated', 'true')
        }
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    async register(firstname: string, lastname: string, username: string, email: string, password: string): Promise<boolean> {
      try {
        const response = await apiClient.post('/auth/register/', { firstname, lastname, username, email, password })
        if (response.data.user && response.data.account) {
          this.user = response.data.user
          this.account = response.data.account
          this.isAuthenticated = true
          // Store authentication state
          localStorage.setItem('isAuthenticated', 'true')
          return true
        }
        return false
      } catch (error) {
        console.error('Registration failed:', error)
        return false
      }
    },

    async logout() {
      try {
        await apiClient.post('/auth/logout/')
        this.user = null
        this.account = null
        this.isAuthenticated = false
        // Clear authentication state
        localStorage.removeItem('isAuthenticated')
      } catch (error) {
        console.error('Logout failed:', error)
        throw error
      }
    },

    async checkAuth() {
      try {
        const response = await apiClient.get('/auth/user/')
        if (response.data.user && response.data.account) {
          this.user = response.data.user
          this.account = response.data.account
          this.isAuthenticated = true
          // Store authentication state
          localStorage.setItem('isAuthenticated', 'true')
        } else {
          this.clearAuth()
        }
      } catch (error) {
        this.clearAuth()
      }
    },

    clearAuth() {
      this.user = null
      this.account = null
      this.isAuthenticated = false
      localStorage.removeItem('isAuthenticated')
    },

    async updateDietaryPreferences(preferences: string[]) {
      if (!this.account) return false;
      try {
        const response = await apiClient.post(`/accounts/${this.account.id}/update_dietary_preferences/`, {
          dietary_preferences: preferences
        })
        this.account = response.data
        return true
      } catch (error) {
        console.error('Failed to update dietary preferences:', error)
        return false
      }
    },

    async updateAllergies(allergies_list: string[]) {
      if (!this.account) return false;
      try {
        const response = await apiClient.post(`/accounts/${this.account.id}/update_allergies/`, {
          allergies: allergies_list
        })
        return true
      } catch (error) {
        console.error('Error updating allergies:', error)
        return false
      }
    },

    async updateFridgeInventory(inventory: string[]) {
      if (!this.account) return false;
      try {
        const response = await apiClient.post(`/accounts/${this.account.id}/update_fridge_inventory/`, {
          fridge_inventory: inventory
        })
        this.account = response.data
        return true
      } catch (error) {
        console.error('Failed to update fridge inventory:', error)
        return false
      }
    },

    async updateUserInfo(updatedInfo: Partial<User>) {
      if (!this.user) return null
      try {
        const response = await apiClient.put(`/users/${this.user.id}/`, updatedInfo)
        this.user = response.data
        return this.user
      } catch (error) {
        console.error('Error updating user info:', error)
        throw error
      }
    }
  }
}) 