<script setup lang="ts">
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
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
      <div class="image-wrapper">
        <img src="@/assets/images/plate.png" alt="Plate" class="ai-image">
      </div>
      <div class="orange-background"></div>
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
          <div class="fridge-items">
            <div class="fridge-item" v-for="i in 5" :key="i">
              <div class="item-content">
                <span class="item-name">Ingredient {{ i }}</span>
                <span class="item-quantity">2 units</span>
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
    font-family: "Afacad", sans-serif;
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
    max-width: 600px;
    z-index: 2;
  }

  h1 {
    font-family: "Aclonica", sans-serif;
    font-size: 2.5rem;
    line-height: 1.2;
  }

  .image-wrapper {
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -50%);
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: #FFD8B1;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
  }

  .image-wrapper img {
    width: 90%;
    border-radius: 50%;
  }

  .orange-background {
    background-color: #FFD8B1;
    position: absolute;
    top: 0;
    right: 0;
    width: 40%;
    height: 100%;
  }

  

  .cookbook {
    background-color: #FFD8B1;
  }

  .cookbook h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .cookbook .highlight {
    color: #a86e2d;
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

  .fridge-items {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .fridge-item {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }

  .item-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .item-name {
    font-weight: 600;
  }

  .item-quantity {
    color: #666;
  }
</style>
