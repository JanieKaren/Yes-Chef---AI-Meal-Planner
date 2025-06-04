<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <div class="home">
    <h1>Welcome to Yes, Chef!</h1>
    <p class="subtitle">Your personal meal planning assistant</p>
    
    <div class="features">
      <div class="feature-card">
        <h2>Track Ingredients</h2>
        <p>Keep track of your ingredients and their expiration dates</p>
      </div>
      <div class="feature-card">
        <h2>Plan Meals</h2>
        <p>Create meal plans based on your available ingredients</p>
      </div>
      <div class="feature-card">
        <h2>Save Recipes</h2>
        <p>Save your favorite recipes for quick access</p>
      </div>
    </div>

    <div class="cta">
      <router-link to="/register" class="btn-primary">Get Started</router-link>
      <router-link to="/login" class="btn-secondary">Login</router-link>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: bold;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature-card {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feature-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
}

.cta {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #2c3e50;
  color: white;
}

.btn-primary:hover {
  background-color: #34495e;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}
</style>
