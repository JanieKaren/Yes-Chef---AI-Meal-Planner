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
        <input
          type="text"
          placeholder="Search"
          class="search-input"
          v-model="searchQuery"
        />

        <select class="dropdown" v-model="filterType">
          <option value="All">All</option>
          <option value="Favorites">Favorites</option>
        </select>

        <button class="btn-primary" @click="applyFilters">Search</button>
        <button class="btn-secondary" @click="clearFilters">Show All</button>
      </div>

      <div v-if="loading" class="loading">Loading…</div>

      <!-- Recipe Cards -->
      <div v-else class="card-grid">
        <div v-if="recipes.length === 0" class="no-data">
          <p>No recipes found.</p>
        </div>

        <div v-else v-for="recipe in recipes" :key="recipe.title" class="recipe-card">
          <div class="card-header">
            <h3>{{ recipe.title }}</h3>
            <div class="card-actions">
              <button
                @click="toggleFavorite(recipe.id)"
                class="icon-button"
                aria-label="Toggle favorite"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  :fill="recipe.favorite ? '#e63946' : 'none'"
                  :stroke="recipe.favorite ? '#e63946' : '#444'"
                  viewBox="0 0 24 24"
                  width="24"
                  height="24"
                  class="heart-icon"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                  />
                </svg>
              </button>
            </div>
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

          <!-- Delete button at the bottom -->
          <div class="card-bottom">
            <button
              @click="deleteRecipe(recipe.id)"
              class="icon-button"
              aria-label="Delete recipe"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                stroke="#444"
                stroke-width="1.5"
                viewBox="0 0 24 24"
                width="20"
                height="20"
                class="trash-icon"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M3 6h18m-2 0v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div class="pagination" v-if="recipes.length > 0">
        <button
          class="pagination-btn"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          class="pagination-btn"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRecipesStore } from '@/stores/recipe'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const recipesStore = useRecipesStore()

// Computed values from the Pinia store
const recipes = computed(() => recipesStore.recipes)
const loading = computed(() => recipesStore.loading)
const currentPage = ref(1)
const totalPages = ref(1)
const searchQuery = ref('')
const filterType = ref('All')

// Initialize from URL parameters
onMounted(() => {
  const page = Number(route.query.page) || 1
  const search = route.query.search as string || ''
  const favorite = route.query.favorite === 'true'

  currentPage.value = page
  searchQuery.value = search
  filterType.value = favorite ? 'Favorites' : 'All'

  fetchRecipes()
})

const updateURL = () => {
  const query: Record<string, string> = {}

  if (currentPage.value > 1) query.page = currentPage.value.toString()
  if (searchQuery.value) query.search = searchQuery.value
  if (filterType.value === 'Favorites') query.favorite = 'true'

  router.replace({ query })
}

const fetchRecipes = async () => {
  await recipesStore.fetchRecipes({
    page: currentPage.value,
    search: searchQuery.value,
    favorite: filterType.value === 'Favorites' ? true : undefined
  })
  totalPages.value = recipesStore.totalPages
  updateURL()
}

const applyFilters = () => {
  currentPage.value = 1
  fetchRecipes()
}

const clearFilters = () => {
  searchQuery.value = ''
  filterType.value = 'All'
  currentPage.value = 1
  fetchRecipes()
}

const changePage = async (page: number) => {
  currentPage.value = page
  await fetchRecipes()
}

function toggleFavorite(id: number) {
  recipesStore.toggleFavorite(id)
}

const deleteRecipe = async (id: number) => {
  if (confirm('Are you sure you want to delete this recipe?')) {
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

.no-data p{
  font-size:large;
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
  font-family: inherit;
}

.dropdown {
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-family: inherit;
}

.controls button {
  border-radius: 12px;
  padding: 0.5rem 1.2rem;
  font-weight: 500;
  font-size: 1rem;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  margin-left: 0.25rem;
}

.controls .btn-primary {
  background: #E1F5CB;
  color: #2c3e50;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.controls .btn-primary:hover {
  background: #d4e9bc;
  color: #222;
}

.controls .btn-secondary {
  color: #2c3e50;
  border: 1px solid #2c3e50;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.controls .btn-secondary:hover {
  background: #E1F5CB;
  border-color: #E1F5CB;
  color: #2c3e50;
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

.card-header{
  display: flex;
  gap:10px
}

.card-header h3{
  flex: 2;
}


.card-actions{
  display: flex;
  justify-content: end;
  align-items: start;
}
.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  padding-left: 5px;

}

.icon-button svg {
  transition: fill 0.3s ease, stroke 0.3s ease;
}

/* Heart Icon Animations */
.heart-icon {
  transition: all 0.3s ease;
  transform-origin: center;
}

/* Hover Effects */
.icon-button:hover .heart-icon {
  transform: scale(1.1);
}

/* When NOT favorited (outlined state) */
.icon-button:hover .heart-icon:not([fill='#e63946']) {
  stroke: #e63946; /* Red outline on hover */
}

/* When favorited (filled state) */
.icon-button:hover .heart-icon[fill='#e63946'] {
  filter: drop-shadow(0 0 2px rgba(230, 57, 70, 0.5)); /* Glow effect */
}

/* Click Animation */
.icon-button:active .heart-icon {
  transform: scale(0.95);
}

/* Optional: Pulsate when favorited */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.heart-icon[fill='#e63946'] {
  animation: pulse 0.5s ease; /* One-time animation when favorited */
}


/* Add to your styles */
.trash-icon {
  transition: all 0.2s ease;
}

.icon-button:hover .trash-icon {
  stroke: #e63946;  /* Red on hover */
  transform: scale(1.1);
}

.icon-button:active .trash-icon {
  stroke: #c1121f;  /* Darker red on click */
  transform: scale(0.95);
}

.card-bottom {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-top: 0.5rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-btn:not(:disabled):hover {
  background-color: #f0f0f0;
}

.page-info {
  font-size: 0.9rem;
  color: #666;

}
@media (max-width: 1024px) {
  .page-container {
    padding: 1rem;
    max-width: 98vw;
  }
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  .recipe-card {
    width: 100%;
    max-width: 100%;
  }
}

@media (max-width: 700px) {
  .top-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .controls {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  .card-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .recipe-card {
    width: 100%;
    max-width: 100%;
    font-size: 0.95rem;
    padding: 0.75rem;
  }
  .page-title {
    font-size: 1.3rem;
  }
  .fridge-header {
    height: 90px;
  }
}

@media (max-width: 480px) {
  .page-container {
    padding: 0.5rem;
  }
  .recipe-card {
    font-size: 0.85rem;
    padding: 0.5rem;
  }
  .fridge-header {
    height: 60px;
  }
}
</style>
