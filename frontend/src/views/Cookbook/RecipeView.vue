<template>
  <div class="recipe-page">
    <!-- Header image -->
    <div class="fridge-header"></div>

    <div class="page-container">
      <div class="top-bar">
        <h1 class="page-title">Recipe Book</h1>
        <router-link to="/recipe-generator" class="btn-primary">
          Generate a Recipe
        </router-link>
      </div>

      <!-- Search and Filter Controls -->
      <div class="controls">
        <input type="text" placeholder="Search" class="search-input" />
        <select class="dropdown">
          <option disabled selected>Type</option>
          <option>Breakfast</option>
          <option>Lunch</option>
          <option>Dinner</option>
        </select>
        <button class="btn-filter">Filter</button>
      </div>

      <div v-if="loading" class="loading">Loading…</div>

      <!-- Recipe Cards -->
      <div v-else class="card-grid">
        <div v-if="recipes.length === 0" class="no-data">
          <p>No recipes have been saved yet.</p>
        </div>

        <div v-else v-for="recipe in recipes" :key="recipe.title" class="recipe-card">
          <p>Recipe Card</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Ingredient {
  name: string
  quantity: string
}

interface SavedRecipe {
  title: string
  description: string
  ingredients: Ingredient[]
  steps: string[]
}

const recipes = ref<SavedRecipe[]>([])
const loading = ref(true)

onMounted(() => {
  try {
    const raw = localStorage.getItem('savedRecipes')
    if (raw) {
      const arr = JSON.parse(raw)
      if (Array.isArray(arr)) {
        recipes.value = arr.filter((item: any) => {
          return (
            item &&
            typeof item.title === 'string' &&
            typeof item.description === 'string' &&
            Array.isArray(item.ingredients) &&
            Array.isArray(item.steps) &&
            item.ingredients.every(
              (ing: any) =>
                ing && typeof ing.name === 'string' && typeof ing.quantity === 'string'
            ) &&
            item.steps.every((step: any) => typeof step === 'string')
          )
        }) as SavedRecipe[]
      }
    }
  } catch {
    recipes.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.recipe-page {
  width: 100%;
}

.fridge-header {
  background-image: url('@/assets/images/fridge-header.png'); /* Replace with actual image */
  background-repeat: no-repeat;
  background-size: cover;
  background-position: top center;
  height: 150px;
  width: 100%;
}

.page-container {
  padding: 2rem;
  max-width: 1000px;
  margin: auto;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.controls {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.search-input {
  padding: 0.5rem;
  border-radius: 20px;
  border: 1px solid #ccc;
  flex-grow: 1;
}

.dropdown {
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.btn-filter {
  background-color: #cbe5c9;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: flex-start;
}

.recipe-card {
  background-color: #eee;
  width: 150px;
  height: 150px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #555;
  font-weight: bold;
  font-size: 1rem;
}
</style>
