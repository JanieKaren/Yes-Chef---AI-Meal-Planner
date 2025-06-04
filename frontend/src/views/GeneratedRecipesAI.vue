<!-- src/views/GeneratedRecipesAI.vue -->
<template>
  <div class="generated-recipes page-container">
    <h1 class="page-title">Your AI‐Generated Recipes</h1>

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
          v-for="(rec, idx) in recipes"
          :key="idx"
        >
          <h3>Recipe {{ idx + 1 }}</h3>
          <pre>{{ rec }}</pre>
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

const recipes = ref<string[]>([])

onMounted(() => {
  const raw = localStorage.getItem('generatedRecipes')
  if (raw) {
    try {
      const arr = JSON.parse(raw)
      if (Array.isArray(arr)) {
        recipes.value = arr.filter(item => typeof item === 'string')
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

.card h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.card pre {
  white-space: pre-wrap;
  font-size: 0.95rem;
  color: #333;
}

.actions {
  text-align: center;
  margin-top: 1rem;
}
</style>
