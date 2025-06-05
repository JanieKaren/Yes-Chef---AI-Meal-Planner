<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h1>Login</h1>
      <p>Don't have an Account? <router-link to="/register" style="color: #FF825C; text-decoration: underline;">Sign Up</router-link></p>
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          class="form-control"
        />
      </div>
      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await userStore.login(username.value, password.value)
    router.push('/')
  } catch (e: any) {
    if (e.response?.status === 401) {
      error.value = 'Invalid username or password'
    } else {
      error.value = 'An error occurred during login'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: start;
  align-items: center;
  min-height: calc(100vh - 100px);
  background-image: url("@/assets/images/landing-bg.png");
  background-size: cover;
  padding: 1rem;
}

.login-form {
  background-color: white;
  padding: 2rem;
  margin: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

h1 {
  text-align: center;
  font-weight: bold;
  margin-bottom: 10px;
  color: #2c3e50;
}

p {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background-color: #FFC07F;
  color: #5e4a0d;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 2rem;
  font-family: "Afacad", sans-serif;
}

.btn-primary:hover {
  background-color: #FFD8B1;
}

.btn-primary:disabled {
  background-color: #e2d1bf;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  margin-top: 1rem;
}

@media screen and (max-width: 768px) {
  .login-container {
    justify-content: center;
  }
  
  .login-form {
    margin: 1rem;
    padding: 1.5rem;
  }
}

@media screen and (max-width: 480px) {
  .login-form {
    margin: 0.5rem;
    padding: 1rem;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  .form-control {
    font-size: 0.9rem;
  }
  
  .btn-primary {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
}
</style>