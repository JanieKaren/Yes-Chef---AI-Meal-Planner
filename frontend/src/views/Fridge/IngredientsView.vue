<template>
  <div class="fridge-header">
  </div>
  <div class="ingredients-container">
    <div class="ingredients-header">
        <h1>My Fridge</h1>
        <router-link :to="{ name: 'new-ingredient' }" class="btn-primary">Add Ingredient</router-link>
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
                  <router-link :to="{ name: 'edit-ingredient', params: { id: ingredient.id }}" class="btn-icon">✏️</router-link>
                  <button @click="deleteIngredient(ingredient.id)" class="btn-icon">🗑️</button>
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
      class="btn-secondary"
    >
      Previous
    </button>
    <span class="page-info">Page {{ ingredientsStore.currentPage }} of {{ ingredientsStore.totalPages }}</span>
    <button 
      @click="updatePage(ingredientsStore.currentPage + 1)"
      :disabled="!ingredientsStore.nextPage"
      class="btn-secondary"
    >
      Next
    </button>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
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

const updatePage = async (page: number) => {
  await router.push({ query: { ...route.query, page: page.toString() } })
  await ingredientsStore.fetchIngredients(page)
}

onMounted(() => {
  const page = Number(route.query.page) || 1
  ingredientsStore.fetchIngredients(page)
})

// Watch for route query changes
watch(() => route.query.page, (newPage) => {
  if (newPage) {
    const page = Number(newPage)
    if (page !== ingredientsStore.currentPage) {
      ingredientsStore.fetchIngredients(page)
    }
  }
})

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
  margin-bottom: 2rem;
}


.ingredients-table-container {
  overflow-x: auto;
  margin: 1rem 0;
}

.ingredients-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ingredients-table th,
.ingredients-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.ingredients-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #2c3e50;
}

.ingredients-table tr:hover {
  background-color: #f8f9fa;
}

.actions-cell {
  white-space: nowrap;
  text-align: right;
  width: 100px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.25rem;
  transition: transform 0.2s;
  text-decoration: none;
}

.btn-icon:hover {
  transform: scale(1.1);
}

.condition-expired {
  color: #dc3545;
  font-weight: bold;
}

.condition-warning {
  color: #ffc107;
  font-weight: bold;
}

.condition-caution {
  color: #fd7e14;
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

.btn-secondary {
  padding: 0.5rem 1rem;
  border: 1px solid #6c757d;
  border-radius: 4px;
  background-color: #fff;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #6c757d;
  color: #fff;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 