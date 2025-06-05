<template>
  <div class="fridge-header">
  </div>
  <div class="ingredients-container">
    <div class="ingredients-header">
      <h1>My Fridge</h1>

      <router-link :to="{ name: 'new-ingredient' }" class="btn-primary">Add Ingredient</router-link>
    </div>
    <div class="search-form">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search ingredients..."
          class="search-input"
        >
        <select v-model="selectedCategory" class="category-select">
          <option value="">All Categories</option>
          <option v-for="[value, label] in categories" :key="value" :value="value">
            {{ label }}
          </option>
        </select>
        <select v-model="selectedCondition" class="condition-select">
          <option value="">All Conditions</option>
          <option value="expired">Expired</option>
          <option value="expiring_soon">Expiring Soon</option>
          <option value="expiring_week">Expiring This Week</option>
          <option value="good">Good</option>
        </select>
        <button @click="handleSearch" class="btn-primary">Search</button>
        <button @click="resetFilters" class="btn-secondary">Show All</button>
      </div>
    <div v-if="ingredientsStore.loading" class="loading">
      Loading Fridge Items...
    </div>
    <div v-else-if="ingredientsStore.error" class="error">
      {{ ingredientsStore.error }}
    </div>
    <div v-else>
      <div v-if="ingredientsStore.ingredients.length === 0" class="no-items">
        No Fridge Items Found
      </div>
      <div v-else class="ingredients-table-container">
        <table class="ingredients-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Expiration Date</th>
              <th>Condition</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ingredient in ingredientsStore.ingredients" :key="ingredient.id">
              <td>{{ ingredient.name }}</td>
              <td>{{ getCategoryLabel(ingredient.category) }}</td>
              <td>{{ ingredient.quantity }} {{ ingredient.unit }}</td>
              <td>{{ formatDate(ingredient.expiration_date) }}</td>
              <td>
                <span :class="getConditionClass(ingredient.expiration_date)">
                  {{ getConditionText(ingredient.expiration_date) }}
                </span>
              </td>
              <td class="actions-cell">
                <div class="action-buttons">
                  <router-link :to="{ name: 'edit-ingredient', params: { id: ingredient.id }}" class="btn-icon">
                    <span class="material-icons">edit</span>
                  </router-link>
                  <button @click="deleteIngredient(ingredient.id)" class="btn-icon">
                    <span class="material-icons">delete</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="pagination-controls" v-if="ingredientsStore.totalPages > 1">
    <button
      @click="updatePage(ingredientsStore.currentPage - 1)"
      :disabled="!ingredientsStore.previousPage"
      class="btn-page"
    >
      Previous
    </button>
    <span class="page-info">Page {{ ingredientsStore.currentPage }} of {{ ingredientsStore.totalPages }}</span>
    <button
      @click="updatePage(ingredientsStore.currentPage + 1)"
      :disabled="!ingredientsStore.nextPage"
      class="btn-page"
    >
      Next
    </button>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import { useIngredientsStore } from '@/stores/ingredients'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const ingredientsStore = useIngredientsStore()

const categories = [
  ['VEG', 'Vegetable'],
  ['FRUIT', 'Fruit'],
  ['LEGUME', 'Legumes & Beans'],
  ['MUSH', 'Mushroom'],
  ['GRAIN', 'Grains & Cereals'],
  ['BAKED', 'Baked Goods'],
  ['PORK', 'Pork'],
  ['CHICKEN', 'Chicken'],
  ['BEEF', 'Beef'],
  ['SEAFOOD', 'Seafood'],
  ['EGG', 'Eggs'],
  ['MEAT', 'Other Meat'],
  ['DAIRY', 'Dairy'],
  ['H&S', 'Herbs & Spices'],
  ['COND', 'Condiments & Sauces'],
  ['BEV', 'Beverages'],
  ['ALCO', 'Alcohol'],
  ['OTHER', 'Other']
]

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedCondition = ref('')

const resetFilters = async () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedCondition.value = ''
  await router.push({ query: { page: '1' } })
  await ingredientsStore.fetchIngredients(1)
}

const updatePage = async (page: number) => {
  await router.push({ query: { ...route.query, page: page.toString() } })
  await ingredientsStore.fetchIngredients(page)
}

const handleSearch = async () => {
  console.log('Search triggered with:', {
    searchQuery: searchQuery.value,
    category: selectedCategory.value,
    condition: selectedCondition.value
  })
  const queryParams: Record<string, string> = {}
  if (searchQuery.value) queryParams.search = searchQuery.value
  if (selectedCategory.value) queryParams.category = selectedCategory.value
  if (selectedCondition.value) queryParams.condition = selectedCondition.value
  queryParams.page = '1' // Reset to first page on new search

  console.log('Pushing route with params:', queryParams)
  await router.push({ query: queryParams })
  console.log('Fetching ingredients with params:', queryParams)
  await ingredientsStore.fetchIngredients(1, queryParams)
}

onMounted(() => {
  console.log('Component mounted, route query:', route.query)
  const page = Number(route.query.page) || 1
  const queryParams = {
    search: route.query.search as string,
    category: route.query.category as string,
    condition: route.query.condition as string
  }
  console.log('Initial fetch with params:', queryParams)
  ingredientsStore.fetchIngredients(page, queryParams)
})

// Watch for route query changes
watch(() => route.query, (newQuery) => {
  console.log('Route query changed:', newQuery)
  const page = Number(newQuery.page) || 1
  const queryParams = {
    search: newQuery.search as string,
    category: newQuery.category as string,
    condition: newQuery.condition as string
  }
  if (page !== ingredientsStore.currentPage || queryParams.search || queryParams.category || queryParams.condition) {
    console.log('Fetching ingredients with new params:', queryParams)
    ingredientsStore.fetchIngredients(page, queryParams)
  }
}, { deep: true })

const deleteIngredient = async (id: number) => {
  if (confirm('Are you sure you want to delete this ingredient?')) {
    await ingredientsStore.deleteIngredient(id)
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const getCategoryLabel = (categoryValue: string) => {
  const category = categories.find(([value]) => value === categoryValue)
  return category ? category[1] : categoryValue
}

const getConditionText = (expirationDate: string) => {
  const today = new Date()
  const expDate = new Date(expirationDate)
  const daysUntilExpiration = Math.ceil((expDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))

  if (daysUntilExpiration < 0) return 'Expired'
  if (daysUntilExpiration <= 3) return 'Expiring Soon'
  if (daysUntilExpiration <= 7) return 'Expiring This Week'
  return 'Good'
}

const getConditionClass = (expirationDate: string) => {
  const today = new Date()
  const expDate = new Date(expirationDate)
  const daysUntilExpiration = Math.ceil((expDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))

  if (daysUntilExpiration < 0) return 'condition-expired'
  if (daysUntilExpiration <= 3) return 'condition-warning'
  if (daysUntilExpiration <= 7) return 'condition-caution'
  return 'condition-good'
}
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

.ingredients-container {
  padding: 0.5rem 4rem;
}


.ingredients-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-block: 1rem;
}


.ingredients-table-container {
  overflow-x: auto;
  margin: 1rem 0;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.ingredients-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
}

.ingredients-table th,
.ingredients-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.ingredients-table th:first-child {
  border-top-left-radius: 12px;
}

.ingredients-table th:last-child {
  border-top-right-radius: 12px;
}

.ingredients-table tr:last-child td:first-child {
  border-bottom-left-radius: 12px;
}

.ingredients-table tr:last-child td:last-child {
  border-bottom-right-radius: 12px;
}

.ingredients-table th {
  background-color: #faf5ef;
  font-weight: bold;
  color: #2c3e50;
}

.ingredients-table tr:hover {
  background-color: #f8f6f4;
}

.actions-cell {
  white-space: nowrap;
  text-align: right;
  width: 100px;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
  border-radius: 6px;
  width: 36px;
  height: 36px;
}

.btn-icon:hover {
  transform: translateY(-2px);
  color: #2c3e50;
  background-color: #f8f6f4;
}

.btn-icon .material-icons {
  font-size: 20px;
}

.btn-icon:first-child:hover {
  color: #FFC07F;
  background-color: rgba(255, 192, 127, 0.1);
}

.btn-icon:last-child:hover {
  color: #dc3545;
  background-color: rgba(220, 53, 69, 0.1);
}

.condition-expired {
  color: #dc3545;
  font-weight: bold;
}

.condition-warning {
  color: #fd7e14;

  font-weight: bold;
}

.condition-caution {
  color: #ffc107;
  font-weight: bold;
}

.condition-good {
  color: #28a745;
  font-weight: bold;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

.no-items {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-info {
  color: #6c757d;
}

.btn-page {
  padding: 0.5rem 1rem;
  border: 1px solid #6c757d;
  border-radius: 4px;
  background-color: #fff;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-page:hover:not(:disabled) {
  background-color: #6c757d;
  color: #fff;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.search-form {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  background: #fff;
  border-radius: 20px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
}

.search-input {
  padding: 0.5rem 0.5rem 0.5rem 1rem;
  border-radius: 20px;
  border: 1px solid #ccc;
  flex: 2;
  font-family: inherit;
  font-size: 1rem;
  transition: border 0.2s, box-shadow 0.2s;
}

.category-select,
.condition-select {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  border: 1px solid #ccc;
  min-width: 140px;
  font-family: inherit;
  font-size: 1rem;
  transition: border 0.2s, box-shadow 0.2s;
}

.search-form button {
  border-radius: 12px;
  padding: 0.5rem 1.2rem;
  font-weight: 500;
  font-size: 1rem;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  margin-left: 0.25rem;
}

.search-form .btn-primary {
  background: #E1F5CB;
  color: #2c3e50;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.search-form .btn-secondary {
  color: #2c3e50;
  border: 1px solid #2c3e50;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.search-form .btn-primary:hover {
  background: #d4e9bc;
  color: #222;
}

.search-form .btn-secondary:hover {
  background: #E1F5CB;
  border-color: #E1F5CB;
  color: #2c3e50;
}

.search-input:focus,
.category-select:focus,
.condition-select:focus {
  outline: none;
  border-color: #FFC07F;
  box-shadow: 0 0 0 2px rgba(255,192,127,0.15);
  background: #fff;
}

@media (max-width: 1024px) {
  .ingredients-container {
    padding: 0.5rem 1rem;
  }
  .search-form {
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .ingredients-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .ingredients-container {
    padding: 0.5rem 0.5rem;
  }
  .search-form {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    padding: 1rem 0.5rem;
  }
  .search-input,
  .category-select,
  .condition-select {
    min-width: 0;
    width: 100%;
  }
  .search-form button {
    width: 100%;
    margin-left: 0;
  }
  .ingredients-table th,
  .ingredients-table td {
    padding: 0.5rem;
    font-size: 0.95rem;
  }
}

@media (max-width: 600px) {
  .fridge-header {
    height: 12vh;
    background-size: cover;
  }
  .ingredients-header h1 {
    font-size: 1.3rem;
  }
  .ingredients-table-container {
    box-shadow: none;
    border-radius: 0;
  }
  .ingredients-table th,
  .ingredients-table td {
    font-size: 0.85rem;
    padding: 0.4rem;
  }
  .pagination-controls {
    flex-direction: column;
    gap: 0.5rem;
  }
  .btn-page {
    width: 100%;
  }
}
</style>