<template>
  <div class="edit-ingredient-container">
    <section class="edit-ingredient-content">
      <h1>{{ isNew ? 'Add' : 'Edit' }} Ingredient</h1>
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
            min="1"
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
        <div class="form-actions">
          <button type="button" @click="goBack" class="btn-secondary">Cancel</button>
          <button type="submit" class="btn-primary">{{ isNew ? 'Add' : 'Save' }}</button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useIngredientsStore } from '@/stores/ingredients'

const route = useRoute()
const router = useRouter()
const ingredientsStore = useIngredientsStore()

const isNew = ref(true)
const form = ref({
  name: '',
  category: '',
  quantity: 1,
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

onMounted(async () => {
  const ingredientId = route.params.id
  if (ingredientId) {
    isNew.value = false
    const ingredient = ingredientsStore.ingredients.find(i => i.id === Number(ingredientId))
    if (ingredient) {
      form.value = { ...ingredient }
    } else {
      // If ingredient not found in store, fetch it
      await ingredientsStore.fetchIngredients()
      const fetchedIngredient = ingredientsStore.ingredients.find(i => i.id === Number(ingredientId))
      if (fetchedIngredient) {
        form.value = { ...fetchedIngredient }
      } else {
        router.push('/ingredients')
      }
    }
  }
})

const handleSubmit = async () => {
  if (isNew.value) {
    await ingredientsStore.addIngredient(form.value)
  } else {
    await ingredientsStore.updateIngredient(Number(route.params.id), form.value)
  }
  router.push('/ingredients')
}

const goBack = () => {
  router.push('/ingredients')
}
</script>

<style scoped>
.edit-ingredient-container {
  background-image: url("@/assets/images/grocerybag.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: top center;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  height: 100vh;
  padding: 2rem;
}
.edit-ingredient-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  mask: conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/30px 100%;
}

h1 {
  color: #FFD8B1;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #898989;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}


</style> 