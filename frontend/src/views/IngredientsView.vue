<template>
  <div class="fridge-header">
  </div>
  <div class="ingredients-container">
    <div class="ingredients-header">
      <h1>My Fridge</h1>
      <button @click="showAddModal = true" class="btn-primary">Add Ingredient</button>
    </div>

    <div v-if="ingredientsStore.loading" class="loading">
      Loading ingredients...
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
                  <button @click="editIngredient(ingredient)" class="btn-icon">✏️</button>
                  <button @click="deleteIngredient(ingredient.id)" class="btn-icon">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>{{ editingIngredient ? 'Edit' : 'Add' }} Ingredient</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="name">Name</label>
            <input
              type="text"
              id="name"
              v-model="form.name"
              required
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="category">Category</label>
            <select id="category" v-model="form.category" required class="form-control">
              <option v-for="[value, label] in categories" :key="value" :value="value">
                {{ label }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="quantity">Quantity</label>
            <input
              type="number"
              id="quantity"
              v-model="form.quantity"
              required
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="unit">Unit</label>
            <select id="unit" v-model="form.unit" required class="form-control">
              <option v-for="[value, label] in units" :key="value" :value="value">
                {{ label }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="expiration_date">Expiration Date</label>
            <input
              type="date"
              id="expiration_date"
              v-model="form.expiration_date"
              required
              class="form-control"
            />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showAddModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIngredientsStore } from '@/stores/ingredients'

const ingredientsStore = useIngredientsStore()
const showAddModal = ref(false)
const editingIngredient = ref<any>(null)

const form = ref({
  name: '',
  category: '',
  quantity: 0,
  unit: '',
  expiration_date: ''
})

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

const units = [
  ['g', 'Gram'],
  ['kg', 'Kilogram'],
  ['oz', 'Ounce'],
  ['lb', 'Pound'],
  ['ml', 'Milliliter'],
  ['l', 'Liter'],
  ['tsp', 'Teaspoon'],
  ['tbsp', 'Tablespoon'],
  ['cup', 'Cup'],
  ['pc', 'Piece'],
  ['bunch', 'Bunch'],
  ['slice', 'Slice'],
  ['pack', 'Pack'],
  ['bottle', 'Bottle'],
  ['can', 'Can']
]

onMounted(() => {
  ingredientsStore.fetchIngredients()
})

const editIngredient = (ingredient: any) => {
  editingIngredient.value = ingredient
  form.value = { ...ingredient }
  showAddModal.value = true
}

const deleteIngredient = async (id: number) => {
  if (confirm('Are you sure you want to delete this ingredient?')) {
    await ingredientsStore.deleteIngredient(id)
  }
}

const handleSubmit = async () => {
  if (editingIngredient.value) {
    await ingredientsStore.updateIngredient(editingIngredient.value.id, form.value)
  } else {
    await ingredientsStore.addIngredient(form.value)
  }
  showAddModal.value = false
  editingIngredient.value = null
  form.value = {
    name: '',
    category: '',
    quantity: 0,
    unit: '',
    expiration_date: ''
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
  padding: 1rem;
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
}

.btn-icon:hover {
  transform: scale(1.1);
}

.condition-expired {
  color: #e74c3c;
  font-weight: bold;
}

.condition-warning {
  color: #e67e22;
  font-weight: bold;
}

.condition-caution {
  color: #f1c40f;
  font-weight: bold;
}

.condition-good {
  color: #27ae60;
  font-weight: bold;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-primary {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
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
</style> 