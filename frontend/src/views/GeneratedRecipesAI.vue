<!-- src/views/GeneratedRecipesAI.vue -->
<template>
  <div class="generated-recipes page-container">
    <h1 class="page-title">Your AI-Generated Recipes</h1>

    <div v-if="!recipes.length" class="no-recipes">
      <p>No recipes found. Please generate some first.</p>
      <router-link to="/recipe-generator" class="btn-primary">
        Back to Generator
      </router-link>
    </div>

    <div v-else>
      <!-- Grid container for three cards -->
      <div class="cards-container">
        <div
          class="card"
          v-for="(recipe, idx) in recipes"
          :key="idx"
        >
          <h3 class="card-title">{{ recipe.title }}</h3>

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
        </div>
      </div>

      <div class="actions">
        <router-link to="/recipe-generator" class="btn-secondary">
          Generate New Recipes
        </router-link>
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

interface Recipe {
  title: string
  ingredients: Ingredient[]
  steps: string[]
}

const recipes = ref<Recipe[]>([])

onMounted(() => {
  const raw = localStorage.getItem('generatedRecipes')
  if (raw) {
    try {
      const arr = JSON.parse(raw)
      if (Array.isArray(arr)) {
        // Only keep items that match { title: string, ingredients: [{ name, quantity }], steps: [string] }
        recipes.value = arr.filter((item: any) => {
          return (
            item &&
            typeof item.title === 'string' &&
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
        }) as Recipe[]
      }
    } catch {
      recipes.value = []
    }
    localStorage.removeItem('generatedRecipes')
  }
})
</script>

<style scoped>
.page-container {
  max-width: 800px;
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

.no-recipes {
  text-align: center;
  font-size: 1.1rem;
  color: #555;
}

.no-recipes p {
  margin-bottom: 1rem;
}

.btn-primary,
.btn-secondary {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  margin-top: 1rem;
  border-radius: 4px;
  text-decoration: none;
  color: white;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #2c3e50;
}

.btn-primary:hover {
  background-color: #34495e;
}

.btn-secondary {
  background-color: #95a5a6;
  margin-left: 1rem;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

/* Grid container for three cards */
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background: #fff;
  padding: 1rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.card-title {
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-size: 1.25rem;
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

.actions {
  text-align: center;
  margin-top: 1rem;
}
</style>
