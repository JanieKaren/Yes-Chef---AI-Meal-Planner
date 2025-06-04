<script setup lang="ts">
</script>

<template>
  <div class="landing-page">
    <section class="ai-generator-section">
      <div class="ai-generator-content">
        <h1>Looking for recipes? <br/> Let AI handle it!</h1>
        <p>Tailored to your ingredients, diet, needs, and preferences — no guesswork needed.</p>
        <div class="cta">
          <router-link to="/login" class="btn">Get Started</router-link>
        </div>
      </div>
      <div class="image-wrapper">
        <img src="@/assets/images/plate.png" alt="Plate" class="ai-image">
      </div>
    </section>

    <section class="features">
      <h2>Why Choose YesChef?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <h3>AI-Powered Recipes</h3>
          <p>Get personalized recipe suggestions based on your ingredients and preferences</p>
        </div>
        <div class="feature-card">
          <h3>Smart Fridge</h3>
          <p>Keep track of your ingredients and never waste food again</p>
        </div>
        <div class="feature-card">
          <h3>Personal Cookbook</h3>
          <p>Save your favorite recipes and access them anytime</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing-page {
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
  position: relative;
  min-height: 350px;
}

.ai-generator-content {
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 2rem;
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
  padding: 0.5rem 1.5rem;
  display: inline-block;
}

.cta .btn {
  color: #ffffff;
  font-weight: 700;
  text-decoration: none;
}

.cta:hover {
  background-color: #3a5f12;
  transition: background-color 0.3s ease;
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

/* Features section */
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
</style> 