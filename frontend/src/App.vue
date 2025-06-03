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
 <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          Yes, Chef!
        </router-link>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
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
      </div>
    </nav>
  <main class="main-content">
      <router-view></router-view>
  </main>
  
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #2c3e50;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-item {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  margin: 0 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  cursor: pointer;
}

.navbar-item:hover {
  background-color: #34495e;
}

.main-content {
  width: 100%;
}
</style>
