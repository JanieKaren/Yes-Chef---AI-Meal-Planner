<template>
  <div class="recipe-page">
    <h1>Recipes</h1>
    <ul>
      <li v-for="recipe in recipes" :key="recipe.id">
        <h2>{{ recipe.title }}</h2>
        <p>{{ recipe.description }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const recipes = ref([
  { id: 1, title: 'Spaghetti Carbonara', description: 'A classic Italian pasta dish.' },
  { id: 2, title: 'Chicken Curry', description: 'A spicy and savory chicken curry.' }
])

onMounted(() => {
  // Fetch recipes from API here in the future
})
</script>

<style scoped>
.recipe-page {
  padding: 2rem;
}
</style>