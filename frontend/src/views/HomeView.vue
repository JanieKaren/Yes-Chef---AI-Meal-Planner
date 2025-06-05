<script setup lang="ts">
import { useUserStore } from '../stores/user'
import { ref, onMounted, computed } from 'vue'
import { useIngredientsStore } from '@/stores/ingredients'
import axios from 'axios'

const userStore = useUserStore()
const ingredientsStore = useIngredientsStore()
const ingredients = computed(() => ingredientsStore.ingredients)
const loading = ref(true)

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

onMounted(() => {
  fetchIngredients()
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
        <h2><span class="highlight">Your</span> <strong>Cookbook</strong></h2>
        <p>Your favorite recipes saved for easy access</p>
        <div class="recipe-grid">
          <div class="recipe-card" v-for="i in 4" :key="i"></div>
        </div>
        <div class="cta">
          <router-link to="/recipe" class="btn btn-primary">View Cookbook</router-link>
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
</style>
