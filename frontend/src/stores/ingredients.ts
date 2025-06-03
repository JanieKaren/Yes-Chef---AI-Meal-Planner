import { defineStore } from 'pinia'
import axios from 'axios'

interface Ingredient {
  id: number
  name: string
  icon_name: string | null
  category: string
  expiration_date: string
  quantity: number
  unit: string
}

interface IngredientsState {
  ingredients: Ingredient[]
  loading: boolean
  error: string | null
}

export const useIngredientsStore = defineStore('ingredients', {
  state: (): IngredientsState => ({
    ingredients: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchIngredients() {
      this.loading = true
      try {
        const response = await axios.get('/api/ingredients/')
        this.ingredients = response.data
        this.error = null
      } catch (error) {
        console.error('Failed to fetch ingredients:', error)
        this.error = 'Failed to fetch ingredients'
      } finally {
        this.loading = false
      }
    },

    async addIngredient(ingredient: Omit<Ingredient, 'id'>) {
      try {
        const response = await axios.post('/api/ingredients/', ingredient)
        this.ingredients.push(response.data)
        return true
      } catch (error) {
        console.error('Failed to add ingredient:', error)
        return false
      }
    },

    async updateIngredient(id: number, ingredient: Partial<Ingredient>) {
      try {
        const response = await axios.patch(`/api/ingredients/${id}/`, ingredient)
        const index = this.ingredients.findIndex(i => i.id === id)
        if (index !== -1) {
          this.ingredients[index] = response.data
        }
        return true
      } catch (error) {
        console.error('Failed to update ingredient:', error)
        return false
      }
    },

    async deleteIngredient(id: number) {
      try {
        await axios.delete(`/api/ingredients/${id}/`)
        this.ingredients = this.ingredients.filter(i => i.id !== id)
        return true
      } catch (error) {
        console.error('Failed to delete ingredient:', error)
        return false
      }
    }
  }
}) 