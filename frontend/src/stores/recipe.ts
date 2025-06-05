// stores/recipes.ts
import { defineStore } from 'pinia'
import axios from 'axios'

export interface Ingredient {
  name: string
  quantity: string
  unit?: string
}

export interface Recipe {
  id: number
  title: string
  description: string
  ingredients: Ingredient[]
  steps: string[]
  created_at?: string
  favorite?: boolean
}

interface RecipesState {
  recipes: Recipe[]
  loading: boolean
  error: string | null
  currentPage: number
  totalPages: number
  nextPage: number | null
  previousPage: null
}

// Optional: for protected routes
function getAuthHeaders() {
  const token = localStorage.getItem('token')
  return {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
}

export async function saveRecipeToBackend(recipe: Omit<Recipe, 'id'>) {
  const response = await axios.post('/api/save-recipe/', recipe, {
    headers: getAuthHeaders()
  })
  return response.data
}

export const useRecipesStore = defineStore('recipes', {
  state: (): RecipesState => ({
    recipes: [],
    loading: false,
    error: null,
    currentPage: 1,
    totalPages: 1,
    nextPage: null,
    previousPage: null
  }),

  actions: {
    async fetchRecipes(params: { page?: number; search?: string; favorite?: boolean } = {}) {
      this.loading = true
      try {
        const queryParams = new URLSearchParams({
          ...(params.page && { page: params.page.toString() }),
          ...(params.search && { search: params.search }),
          ...(params.favorite !== undefined && { favorite: params.favorite.toString() })
        })

        const response = await axios.get(`/api/save-recipe/?${queryParams.toString()}`)
        this.recipes = response.data.results
        this.currentPage = response.data.current_page
        this.totalPages = response.data.num_pages
        this.nextPage = response.data.next_page
        this.previousPage = response.data.previous_page
        this.error = null
      } catch (error) {
        console.error('Failed to fetch recipes:', error)
        this.error = 'Failed to fetch recipes'
      } finally {
        this.loading = false
      }
    },
    
    async deleteRecipe(id: number) {
      this.loading = true
      try {
        await axios.delete(`/api/recipes-detail/${id}/`, {
          headers: getAuthHeaders()
        })
        this.recipes = this.recipes.filter(recipe => recipe.id !== id)
        return true
      } catch (error) {
        console.error('Failed to delete recipe:', error)
        return false
      } finally {
        this.loading = false
      }
    },

    async toggleFavorite(id: number) {
      const recipe = this.recipes.find(r => r.id === id)
      if (!recipe) return

      // Optimistic UI update
      recipe.favorite = !recipe.favorite

      try {
        await axios.patch(`/api/recipes-detail/${id}/`, { favorite: recipe.favorite }, {
          headers: getAuthHeaders()
        })
      } catch (error) {
        console.error('Failed to toggle favorite:', error)
        // Revert on failure
        recipe.favorite = !recipe.favorite
      }
    }
  }
})