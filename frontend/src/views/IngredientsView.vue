<template>
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
      <div v-else class="ingredients-grid">
        <div v-for="ingredient in ingredientsStore.ingredients" :key="ingredient.id" class="ingredient-card">
          <div class="ingredient-header">
            <h3>{{ ingredient.name }}</h3>
            <div class="ingredient-actions">
              <button @click="editIngredient(ingredient)" class="btn-icon">✏️</button>
              <button @click="deleteIngredient(ingredient.id)" class="btn-icon">🗑️</button>
            </div>
          </div>
          <div class="ingredient-details">
            <p><strong>Category:</strong> {{ ingredient.category }}</p>
            <p><strong>Quantity:</strong> {{ ingredient.quantity }} {{ ingredient.unit }}</p>
            <p><strong>Expires:</strong> {{ formatDate(ingredient.expiration_date) }}</p>
          </div>
        </div>
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
</script>

<style scoped>
.ingredients-container {
  padding: 1rem;
}

.ingredients-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.ingredients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.ingredient-card {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ingredient-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.ingredient-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.25rem;
}

.ingredient-details p {
  margin: 0.5rem 0;
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