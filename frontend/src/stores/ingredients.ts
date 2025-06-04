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
  currentPage: number
  totalPages: number
  nextPage: number | null
  previousPage: number | null
}

export const useIngredientsStore = defineStore('ingredients', {
  state: (): IngredientsState => ({
    ingredients: [],
    loading: false,
    error: null,
    currentPage: 1,
    totalPages: 1,
    nextPage: null,
    previousPage: null
  }),

  actions: {
    async fetchIngredients(page = 1, queryParams: { search?: string; category?: string; condition?: string } = {}) {
      console.log('Store: fetchIngredients called with:', { page, queryParams })
      this.loading = true
      try {
        const params = new URLSearchParams({
          page: page.toString(),
          ...(queryParams.search && { search: queryParams.search }),
          ...(queryParams.category && { category: queryParams.category }),
          ...(queryParams.condition && { condition: queryParams.condition })
        })
        
        console.log('Store: Making API request with params:', params.toString())
        const response = await axios.get(`/api/ingredients/?${params.toString()}`)
        console.log('Store: API response:', response.data)
        
        this.ingredients = response.data.results
        this.currentPage = response.data.current_page
        this.totalPages = response.data.num_pages
        this.nextPage = response.data.next_page
        this.previousPage = response.data.previous_page
        this.error = null
      } catch (error) {
        console.error('Store: Failed to fetch ingredients:', error)
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