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
          <router-link to="/recipe-generator" class="btn">Generate Recipes</router-link>
        </div>
      </div>
      <div class="image-wrapper">
        <img src="@/assets/images/plate.png" alt="Plate" class="ai-image">
      </div>
    </section>

    <section class="cookbook">
      <div>
        <h2><span class="highlight">Your</span> <strong>Cookbook</strong></h2>
        <p>Your favorite recipes saved for easy access</p>
        <div class="recipe-grid">
          <div class="recipe-card" v-for="i in 4" :key="i"></div>
        </div>
      </div>
      <div class="cta">
        <router-link to="/recipe" class="btn">View Cookbook</router-link>
      </div>
    </section>

    <section class="fridge-section">
      <h2><strong>Your</strong> <span class="highlight">Fridge</span></h2>
      <p>Manage your ingredients and plan your meals</p>
      <div class="fridge-content">
        <div class="fridge-image"></div>
        <div class="fridge-list">
          <div class="fridge-item" v-for="i in 5" :key="i"></div>
        </div>
      </div>
      <div class="cta">
        <router-link to="/fridge" class="btn">Check Fridge</router-link>
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

  .ai-generator-section {
    background-color: #ffff;
    display: flex;
    justify-content: center;
    padding: 4rem 2rem 2rem;
    justify-content: center;
    padding: 4rem 2rem 2rem;
    position: relative;
    min-height: 350px;
  }

  .ai-generator-content {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 2rem;
    /* max-width: 1100px; */
    width: 100%;
  }

  h1 {
    font-family: "Aclonica", sans-serif;
  }

  .text {
    flex: 1;
  }

  .text h1 {
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }

  .text p {
    font-size: 1rem;
    margin-bottom: 1.5rem;
    max-width: 350px;
  }

  .cta {
    background-color: #497817;
    border: none;
    border-radius: 20px;
    font-weight: 600;
    cursor: pointer;
    /* padding: 0.5rem 1.5rem; */
    display: inline-block;
  }

  .cta .btn {
    color: #ffffff;
    font-weight: 700;
  }

  .image-wrapper {
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
    /* z-index: 0; */
  }

  /* Cookbook */
  .cookbook {
    display: flex;
    flex-direction: column;
    padding: 2rem 2rem 4rem;
    background-color: #FFD8B1;
    gap: 2rem;
  }

  .cookbook h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .cookbook .highlight {
    color: #a86e2d;
    font-weight: 500;
  }

  .cookbook p {
    font-size: 0.9rem;
    color: #444;
    margin-bottom: 1.5rem;
  }

  .recipe-grid {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .recipe-card {
    width: 150px;
    height: 180px;
    background: #d9d9d9;
    border-radius: 12px;
  }

  .fridge-section {
    padding: 2rem;
    background: white;
    color: #1e1e1e;
  }

  .fridge-section h2 {
    font-size: 1.5rem;
    margin-bottom: 0.3rem;
  }

  .fridge-section .highlight {
    color: #ffb87d;
    font-weight: 600;
  }

  .fridge-section p {
    font-size: 0.9rem;
    color: #444;
    margin-bottom: 1.5rem;
  }

  .fridge-content {
    display: flex;
    gap: 2rem;
    align-items: flex-start;
  }

  .fridge-image {
    width: 180px;
    height: 280px;
    background: #d9d9d9;
    border-radius: 8px;
  }

  .fridge-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
  }

  .fridge-item {
    height: 40px;
    background: #d9d9d9;
    border-radius: 8px;
  }

  /* New styles for features section */
  .features {
    padding: 4rem 2rem;
    background-color: #f8f8f8;
  }

  .features h2 {
    text-align: center;
    margin-bottom: 2rem;
    font-size: 2rem;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .feature-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .feature-card h3 {
    color: #497817;
    margin-bottom: 1rem;
  }

  .feature-card p {
    color: #666;
    line-height: 1.5;
  }

  /* Update existing styles */
  .cta .btn {
    color: #ffffff;
    font-weight: 700;
    text-decoration: none;
  }

  .cta:hover {
    background-color: #3a5f12;
    transition: background-color 0.3s ease;
  }

</style>
