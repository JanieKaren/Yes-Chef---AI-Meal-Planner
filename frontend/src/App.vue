<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const handleLogout = async () => {
  try {
    await userStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>

<template>
  <div class="app">
    <nav class="navbar">
      <div class="navbar-brand">
        
        <router-link to="/" class="navbar-item">
          <img src="@/assets/images/logo.png" alt="Logo" class="logo" />
          Yes, Chef!
        </router-link>
      </div>
      <div class="navbar-menu">
        <template v-if="userStore.isAuthenticated">
            <router-link to="/ingredients" class="navbar-item">Ingredients</router-link>
            <router-link to="/profile" class="navbar-item">Profile</router-link>
            <a @click="handleLogout" class="navbar-item">Logout</a>
          </template>
          <template v-else>
            <router-link to="/login" class="navbar-item">Login</router-link>
            <router-link to="/register" class="navbar-item">Register</router-link>
          </template>
      </div>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: cornsilk;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.logo {
  height: 50px;
  margin-right: 10px;
  display: inline-block;
  vertical-align: middle;
}

.navbar-item {
  color: #34495e;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
  cursor: pointer;
  display: flex;
  align-items: center;
  height: 100%;
}

.navbar-item:hover {
  background-color: rgb(255, 219, 186);
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.main-content {
  flex: 1;
  width: 100%;
}
</style>
