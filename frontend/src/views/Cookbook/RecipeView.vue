<!-- src/views/RecipeView.vue -->
<template>
  <div class="recipe-page">
    <div class="fridge-header"></div>
    <div class="page-container">
      <h1 class="page-title">Saved Recipes</h1>

      <div v-if="loading" class="loading">
        Loading…
      </div>

      <div v-else>
        <div v-if="recipes.length === 0" class="no-data">
          <p>No recipes have been saved yet.</p>
          <router-link to="/recipe-generator" class="btn-primary">
            Generate a Recipe
          </router-link>
        </div>

        <ul v-else class="saved-list">
          <li
            v-for="recipe in recipes"
            :key="recipe.title"
            class="saved-card"
          >
            <h2>{{ recipe.title }}</h2>
            <p class="saved-description">{{ recipe.description }}</p>

            <div class="section">
              <h4>Ingredients</h4>
              <ul>
                <li v-for="(ing, i) in recipe.ingredients" :key="i">
                  {{ ing.quantity }} {{ ing.name }}
                </li>
              </ul>
            </div>

            <div class="section">
              <h4>Steps</h4>
              <ol>
                <li v-for="(step, sIdx) in recipe.steps" :key="sIdx">
                  {{ step }}
                </li>
              </ol>
            </div>
          </li>
        </ul>
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
                ing &&
                typeof ing.name === 'string' &&
                typeof ing.quantity === 'string'
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
  .fridge-header {
    background-image: url("@/assets/images/fridge-header.png");
    background-size: contain;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: top center;
    height: 20vh;
    width: 100vw;
  }

  .page-container {
    max-width: 700px;
    margin: 2rem auto;
    padding: 1rem;
    background: #f9f9f9;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .page-title {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #2c3e50;
    font-size: 2rem;
  }

  .loading {
    text-align: center;
    font-size: 1.1rem;
    color: #555;
  }

  .no-data {
    text-align: center;
    font-size: 1.1rem;
    color: #555;
  }

  .saved-list {
    list-style: none;
    padding: 0;
  }

  .saved-card {
    margin-bottom: 1.5rem;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: #fff;
  }

  .saved-card h2 {
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }

  .saved-description {
    margin-bottom: 1rem;
    color: #555;
    font-size: 0.95rem;
  }

  .section {
    margin-top: 0.75rem;
  }

  .section h4 {
    margin-bottom: 0.25rem;
    font-size: 1rem;
    color: #444;
  }

  .section ul,
  .section ol {
    padding-left: 1.25rem;
    margin: 0;
  }

  .btn-primary {
    display: inline-block;
    background-color: #2c3e50;
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.2s;
    margin-top: 1rem;
  }

  .btn-primary:hover {
    background-color: #34495e;
  }
</style>
