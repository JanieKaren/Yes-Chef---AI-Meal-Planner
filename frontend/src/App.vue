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

        <router-link to="/">
          <img src="@/assets/images/logo-1.png" alt="Logo" class="logo" />
          <span>Yes, Chef!</span>
        </router-link>
      </div>
      <div class="navbar-menu">
        <template v-if="userStore.isAuthenticated">
            <router-link to="/home" class="navbar-item" active-class="active">Home</router-link>
            <router-link to="/recipe" class="navbar-item" active-class="active">Recipes</router-link>
            <router-link to="/fridge" class="navbar-item" active-class="active">Fridge</router-link>
            <router-link to="/profile" class="navbar-item" active-class="active">Account</router-link>
            <a @click="handleLogout" class="navbar-item">Logout</a>
          </template>
          <template v-else>
            <router-link to="/login" class="navbar-item" active-class="active">Login</router-link>
            <router-link to="/register" class="navbar-item" active-class="active">Register</router-link>
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
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  flex: 1;
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  padding: 1rem;
}

.logo {
  height: 40px;
  margin-right: 10px;
  display: inline-block;
  vertical-align: middle;
}

.navbar-item {
  color: #34495e;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 1.5rem;
  position: relative;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.navbar-item:hover {
  background-color: rgba(255, 255, 255, 0.3);
  color: #1e1e1e;
}

.navbar-item.active {
  font-weight: 600;
  color: #1e1e1e;
}

.navbar-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 3px;
  background-color: #1e1e1e;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.navbar-item:hover::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40%;
  height: 2px;
  background-color: rgba(30, 30, 30, 0.3);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.navbar-item.active:hover::after {
  width: 80%;
  background-color: #1e1e1e;
}

.navbar-menu {
  width: 40%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: flex-end;
  background-color: #D2B48C;
  padding: 0 1rem;
}

span {
  font-family: 'Afacad', sans-serif;
  color: #497817;
  font-weight: bold;
}

.main-content {
  flex: 1;
  width: 100%;
}
</style>
