<script setup lang="ts">
</script>

<template>
  <div class="landing-page">
   <section class="hero">
    <div class="hero-content">
      <div class="hero-img">
        <h1>Where <span>AI</span> meets <span>Appetite</span></h1>
        <p>Personalized recipes crafted from what’s <br>in your kitchen with Yes, Chef!</p>
      </div>
    </div>
   </section>
   <section class="features">
    
   </section>
   <section class="get-started">

   </section>
  </div>
</template>

<style scoped>

.hero {
  margin: 0;
  height: 90vh;
  background: linear-gradient(to right, white 60%, #FFD8B1 40%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  width: 95%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-img {
  background-image: url("@/assets/images/login_background.jpg");
  background-size: cover;
  background-position: center;
  height: 85vh;
  width: 100%;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 6rem 3rem;
  flex-direction: column;
}

h1 {
  font-weight: bold;
  font-size: 3.5rem;
  color: #1e1e1e;
  position: relative;
  z-index: 1;
  margin: 0;
  line-height: 1.2;
}

h1 span {
  color: #FFD8B1;
  font-weight: bold;
}

p{
  font-size: 1.5rem;
  font-weight: bold;
  padding-block: 1rem;
}

.features{
  height: 100vh;
  background-color: #FFD8B1;
}

</style>