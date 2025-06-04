<script setup lang="ts">
</script>

<template>
  <div class="landing-page">
   <section class="hero">
    <div class="hero-content">
      <div class="hero-img">
        <h1>Where <span>AI</span> meets <span>Appetite</span></h1>
        <p>Personalized recipes crafted from what's <br>in your kitchen with Yes, Chef!</p>
      </div>
    </div>
   </section>
   <section class="features">
     <article>
       <i class="fa fa-magic"></i>
       <h2>Looking for recipes? Let AI handle it!</h2>
       <p>Tailored to your ingredients, diet, needs, and preferences — no guesswork needed.</p>
     </article>
     <article>
       <i class="fa fa-list-alt"></i>
       <h2>Your Fridge, but Smarter</h2>
       <p>Connect your fridge to your recipes. Track what you have, reduce waste, and get recipes that match exactly what's on your shelf.</p>
     </article>
     <article>
       <i class="fa fa-book"></i>
       <h2>Your Personal Online Cookbook</h2>
       <p>Store, organize, and revisit your favorite recipes — all in one place. No more screenshots or cluttered notes. Your culinary life, streamlined.</p>
     </article>
   </section>
   <section class="get-started">
    <h1>Start your Culinary Journey with Yes, Chef!</h1>
    <div class="cta">
      <router-link to="/register" class="btn-primary">Get Started</router-link>
      <router-link to="/login" class="btn-secondary">Login</router-link>
    </div>
   </section>
  </div>
</template>

<style scoped>
.landing-page {
  font-family: 'Afacad', sans-serif;
}

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
  font-family: 'Aclonica', sans-serif;
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

p {
  font-family: 'Afacad', sans-serif;
  font-size: 1.5rem;
  font-weight: bold;
  padding-block: 1rem;
}

.features {
  
  background-color: #FFD8B1;
  padding: 4rem 2rem;
  display: flex;
  flex-direction: row;
  gap: 2rem;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

.features article {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 20px;
  width: 30%;
  min-width: 300px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  flex: 1;
}

.features article:hover {
  transform: translateY(-5px);
}

.features i {
  font-size: 2.5rem;
  color: #1e1e1e;
  margin-bottom: 1.5rem;
}

.features h2 {
  font-family: 'Aclonica', sans-serif;
  font-size: 1.8rem;
  font-weight: bold;
  color: #1e1e1e;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.features p {
  font-family: 'Afacad', sans-serif;
  font-size: 1.1rem;
  line-height: 1.6;
  color: #1e1e1e;
  font-weight: normal;
  margin: 0 auto;
} 

.get-started {
  padding: 6rem 2rem;
  text-align: center;
  background-color: white;
}

.get-started h1 {
  font-size: 2.8rem;
  margin-bottom: 2.5rem;
  color: #1e1e1e;
}

.cta {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  align-items: center;
}

.btn-primary, .btn-secondary {
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-family: 'Afacad', sans-serif;
  font-size: 1.2rem;
  font-weight: bold;
  text-decoration: none;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.btn-primary {
  background-color: #FFD8B1;
  color: #1e1e1e;
  border: 2px solid #FFD8B1;
}

.btn-secondary {
  background-color: transparent;
  color: #1e1e1e;
  border: 2px solid #FFD8B1;
}

.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

</style>