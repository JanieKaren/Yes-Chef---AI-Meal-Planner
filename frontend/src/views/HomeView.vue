<script setup lang="ts">
import { useUserStore } from '../stores/user'
import { ref, onMounted, computed } from 'vue'
import { useIngredientsStore } from '@/stores/ingredients'
import { useRecipesStore } from '@/stores/recipe'
import axios from 'axios'

const userStore = useUserStore()
const ingredientsStore = useIngredientsStore()
const recipesStore = useRecipesStore()
const ingredients = computed(() => ingredientsStore.ingredients)
const recipes = computed(() => recipesStore.recipes.slice(0, 5)) // Get only first 5 recipes
const loading = ref(true)
const recipesLoading = ref(true)

const fetchIngredients = async () => {
  try {
    const response = await axios.get('/api/ingredients/', {
      params: {
        page: 1,
        condition: 'good' // Only show non-expired items
      }
    })
    ingredients.value = response.data.results.slice(0, 5) // Get only first 5 items
  } catch (error) {
    console.error('Error fetching ingredients:', error)
  } finally {
    loading.value = false
  }
}

const fetchRecipes = async () => {
  try {
    await recipesStore.fetchRecipes()
  } catch (error) {
    console.error('Error fetching recipes:', error)
  } finally {
    recipesLoading.value = false
  }
}

onMounted(() => {
  fetchIngredients()
  fetchRecipes()
})
</script>

<template>
  <div class="homepage">
    <section class="ai-generator-section">
      <div class="ai-generator-content">
        <h1>Looking for recipes? <br/> Let AI handle it!</h1>
        <p>Tailored to your ingredients, diet, needs, and preferences — no guesswork needed.</p>
        <div class="cta">
          <router-link to="/recipe-generator" class="btn btn-primary">Generate Recipes</router-link>
        </div>
      </div>
      <div class="padding-right">
        <div class="image-wrapper">
          <img src="@/assets/images/plate.png" alt="Plate" class="ai-image">
        </div>
        <div class="brown-background"></div>
      </div>

    </section>

    <section class="cookbook">
      <div class="section-content">
        <h2><strong>Your</strong> <span class="highlight">Cookbook</span></h2>
        <p>Your latest saved recipes</p>
        <div class="recipes-dashboard"> 
          <div class="recipes-grid">
            <div v-if="recipesLoading" class="loading">Loading recipes...</div>
            <div v-else-if="recipes.length === 0" class="no-items">
              No recipes found. Generate some recipes to get started!
            </div>
            <div v-else class="recipe-card" v-for="recipe in recipes" :key="recipe.id">
              <div class="recipe-content">
                <div class="recipe-info">
                  <h4 class="recipe-title">{{ recipe.title }}</h4>
                  <p class="recipe-description">{{ recipe.description }}</p>
                  <div class="recipe-ingredients">
                    <h5>Ingredients:</h5>
                    <ul>
                      <li v-for="(ingredient, index) in recipe.ingredients" :key="index">
                        {{ ingredient.quantity }} {{ ingredient.name }}
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="recipe-actions">
                  <button @click="recipesStore.toggleFavorite(recipe.id)" class="favorite-btn" :class="{ 'favorite-btn--active': recipe.favorite }">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                      <path fill="currentColor" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="cta">
            <router-link to="/recipe" class="btn btn-primary">View All Recipes</router-link>
          </div>
        </div>
      </div>
    </section>


    <section class="fridge-section">
      <div class="section-content">
        <h2><strong>Your</strong> <span class="highlight">Fridge</span></h2>
        <p>Manage your ingredients and plan your meals</p>
        <div class="fridge-dashboard">
          <div class="fridge-header">
            <h3>Recent Ingredients</h3>
            <span class="ingredient-count">{{ ingredients.length }} items</span>
          </div>
          <div class="fridge-items">
            <div v-if="loading" class="loading">Loading ingredients...</div>
            <div v-else-if="ingredients.length === 0" class="no-items">
              No ingredients found. Add some to your fridge!
            </div>
            <div v-else class="fridge-item" v-for="ingredient in ingredients" :key="ingredient.id">
              <div class="item-content">
                <div class="item-info">
                  <span class="item-name">{{ ingredient.name }}</span>
                  <span class="item-category">{{ ingredient.category }}</span>
                </div>
                <div class="item-details">
                  <span class="item-quantity">{{ ingredient.quantity }} {{ ingredient.unit }}</span>
                  <span class="item-expiry">Expires: {{ new Date(ingredient.expiration_date).toLocaleDateString() }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="cta">
            <router-link to="/fridge" class="btn btn-primary">View All Ingredients</router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
  .homepage {
    background-color: #ffff;
    color: #1e1e1e;
    display: flex;
    flex-direction: column;
  }

  section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: 2rem;
    position: relative;
  }

  .section-content {
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
  }

  .ai-generator-section {
    background-color: #ffff;
    display: flex;
    justify-content: center;
    padding: 4rem 2rem;
    position: relative;
  }

  .ai-generator-content {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 2rem;
    width: 100%;
    /* max-width: 600px; */
    z-index: 2;
  }

  .image-wrapper {
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -50%);
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: #D2B48C;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
  }

  .image-wrapper img {
    width: 90%;
    border-radius: 50%;
  }

  .brown-background {
    background-color: #D2B48C;
    position: absolute;
    top: 0;
    right: 0;
    width: 40%;
    height: 100%;
  }

  .cookbook {
    background-color: #D2B48C;
  }

  .cookbook h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .cookbook .highlight {
    color: #7f4d14;
    font-weight: 500;
  }

  .recipe-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
  }

  .recipe-card {
    width: 100%;
    height: 250px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }

  .fridge-section {
    background: white;
  }

  .fridge-section h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .fridge-section .highlight {
    color: #ffb87d;
    font-weight: 600;
  }

  .fridge-dashboard {
    background: #f8f8f8;
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
  }

  .fridge-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .fridge-header h3 {
    font-size: 1.2rem;
    color: #333;
    margin: 0;
  }

  .ingredient-count {
    color: #666;
    font-size: 0.9rem;
  }

  .fridge-items {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .fridge-item {
    background: white;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    transition: transform 0.2s ease;
  }

  .fridge-item:hover {
    transform: translateY(-2px);
  }

  .item-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .item-info {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .item-name {
    font-weight: 600;
    color: #333;
  }

  .item-category {
    font-size: 0.9rem;
    color: #666;
  }

  .item-details {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.3rem;
  }

  .item-quantity {
    font-weight: 500;
    color: #497817;
  }

  .item-expiry {
    font-size: 0.9rem;
    color: #ff6b6b;
  }

  .loading, .no-items {
    text-align: center;
    padding: 2rem;
    color: #666;
    background: white;
    border-radius: 12px;
  }

  .recipes-section {
    background-color: #f8f8f8;
  }

  .recipes-dashboard {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
  }

  .recipes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .recipes-header h3 {
    font-size: 1.2rem;
    color: #333;
    margin: 0;
  }

  .recipe-count {
    color: #666;
    font-size: 0.9rem;
  }

  .recipes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .recipe-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    transition: transform 0.2s ease;
    border: 1px solid #eee;
  }

  .recipe-card:hover {
    transform: translateY(-2px);
  }

  .recipe-content {
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .recipe-info {
    flex: 1;
  }

  .recipe-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
    margin: 0 0 0.5rem 0;
  }

  .recipe-description {
    font-size: 0.9rem;
    color: #666;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .recipe-actions {
    margin-left: 1rem;
  }

  .favorite-btn {
    background: none;
    border: none;
    padding: 0.5rem;
    cursor: pointer;
    color: #ccc;
    transition: color 0.2s ease;
  }

  .favorite-btn:hover {
    color: #ff6b6b;
  }

  .favorite-btn--active {
    color: #ff6b6b;
  }

  .favorite-btn svg {
    width: 24px;
    height: 24px;
  }

  .recipe-ingredients {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
  }

  .recipe-ingredients h5 {
    font-size: 0.9rem;
    color: #666;
    margin: 0 0 0.5rem 0;
  }

  .recipe-ingredients ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .recipe-ingredients li {
    font-size: 0.85rem;
    color: #666;
    background: #f8f8f8;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    white-space: nowrap;
  }

  .recipe-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    transition: transform 0.2s ease;
    border: 1px solid #eee;
    height: 100%;
  }

  .recipe-content {
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    height: 100%;
  }

  .recipe-info {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .recipe-description {
    font-size: 0.9rem;
    color: #666;
    margin: 0.5rem 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
