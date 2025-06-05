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
          <div class="card-header">
            <h3 class="title-with-fav">
              {{ recipe.title }}
              <button
                @click="toggleFavorite(recipe.id)"
                class="favorite-btn"
                :aria-label="recipe.favorite ? 'Unfavorite' : 'Favorite'"
              >
                <i
                  :class="['fa', recipe.favorite ? 'fa-heart' : 'fa-heart-o']"
                  :style="{ color: recipe.favorite ? '#e63946' : '#444' }"
                ></i>
              </button>
            </h3>
          </div>
          <p>{{ recipe.description }}</p>

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

          <button @click="deleteRecipe(recipe.id)" class="delete-btn"><i class="material-icons">delete</i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRecipesStore } from '@/stores/recipe'

const recipesStore = useRecipesStore()

// Computed values from the Pinia store
const recipes = computed(() => recipesStore.recipes)
const loading = computed(() => recipesStore.loading)

onMounted(() => {
  recipesStore.fetchRecipes()
})

function toggleFavorite(id: number) {
  recipesStore.toggleFavorite(id)
}

const deleteRecipe = async (id: number) => {
  if (confirm('Are you sure you want to delete this ingredient?')) {
    const success = await recipesStore.deleteRecipe(id)
    if (!success) {
      alert('Failed to delete recipe.')
    }
  }
}


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
  padding: 0.5rem 0.5rem 0.5rem 1rem;
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
  display: grid;
  grid-template-columns: repeat(3, 300px);
  gap: 1rem;
  margin-bottom: 2rem;
}

.recipe-card {
  background-color: #fff;
  width: 300px;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  color: #333;
  font-size: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow: hidden;
  max-height: 500px;
  transition: transform 0.2s ease;
}

.recipe-card:hover {
  transform: translateY(-4px);
}

.recipe-card h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: #444;
}

.recipe-card p {
  margin-bottom: 0.5rem;
  color: #666;
  font-style: italic;
}

.recipe-card .section {
  margin-top: 0.5rem;
}

.recipe-card h4 {
  font-size: 1rem;
  margin-bottom: 0.25rem;
  color: #222;
  border-bottom: 1px solid #ddd;
  padding-bottom: 2px;
}

.recipe-card ul,
.recipe-card ol {
  margin: 0;
  padding-left: 1rem;
  max-height: 150px;
  overflow-y: auto;
  scrollbar-width: thin;
}

.recipe-card li {
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.recipe-card ul::-webkit-scrollbar,
.recipe-card ol::-webkit-scrollbar {
  width: 6px;
}

.recipe-card ul::-webkit-scrollbar-thumb,
.recipe-card ol::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}

.title-with-fav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.favorite-btn {
  font-size: 24px;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  margin-left: 0.25rem;
  display: flex;
  align-items: center;
}

.delete-btn {
  font-size: 24px;
  margin-top: auto;
  align-self: flex-end;
  background: none;
  border: none;
  color: #7c8585;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
</style>
