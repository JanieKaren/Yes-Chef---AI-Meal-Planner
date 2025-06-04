<script setup lang="ts">

</script>

<template>
  <div class="homepage">
    <section class="ai-generator-section">
      <div class="ai-generator-content">
        <h1>Looking for recipes? <br/> Let AI handle it1</h1>
        <p>Tailored to your ingredients, diet, needs, and preferences — no guesswork needed.</p>
        <div class="cta">
          <a href="/recipe-generator" class="btn">Generate Recipes</a>
        </div>
      </div>
      <!-- <div class="orange-background"></div> -->

      <div class="image-wrapper">
        <img src="@/assets/images/plate.png" alt="Plate" class="ai-image">
      </div>
    </section>

    <section class="cookbook">
      <div>
        <h2><span class="highlight">The</span> <strong>Cookbook</strong></h2>
        <p>Some of your favorite recipes saved in case you want to taste them again ></p>
        <div class="recipe-grid">
          <div class="recipe-card" v-for="i in 4" :key="i"></div>
        </div>
      </div>
      <div class="cta">
        <a href="/recipe" class="btn">View Cookbook</a>
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
    padding: 0.5rem 1.5rem;
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
</style>
