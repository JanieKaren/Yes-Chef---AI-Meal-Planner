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
    error: null
  }),

  actions: {
    async fetchRecipes() {
      this.loading = true
      try {
        const response = await axios.get('/api/save-recipe/')
        this.recipes = response.data
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