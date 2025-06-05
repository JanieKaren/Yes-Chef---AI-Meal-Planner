<template>
  <div class="register-container">
    <form @submit.prevent="handleRegister" class="register-form">
      <h1>Create an Account</h1>
      <p>Already have an account? <router-link to="/login" style="color: #FF825C; text-decoration: underline;">Login</router-link></p>
      <div class="form-group">
        <label for="firstname">Firstname</label>
        <input
          type="text"
          id="firstname"
          v-model="form.firstname"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="lastname">Lastname</label>
        <input
          type="text"
          id="lastname"
          v-model="form.lastname"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          v-model="form.email"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="form.password"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="form.confirmPassword"
          required
          class="form-control"
        />
      </div>
      <button type="submit" class="btn-primary" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register' }}
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

const form = ref({
  firstname: '',
  lastname: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const success = await userStore.register(
      form.value.firstname,
      form.value.lastname,
      form.value.username,
      form.value.email,
      form.value.password
    )
    if (success) {
      router.push('/home')
    } else {
      error.value = 'Registration failed'
    }
  } catch (e) {
    error.value = 'An error occurred during registration'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: start;
  align-items: center;
  min-height: calc(100vh - 100px);
  background-image: url("@/assets/images/landing-bg.png");
  background-size: cover;
}

.register-form {
  background-color: white;
  padding: 3rem;
  margin: 2rem 9rem;
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
  margin-bottom: 0.5rem;
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
  color: black;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
  font-family: "Afacad", sans-serif;
}

.btn-primary:hover {
  background-color: #FFD8B1;
}

.btn-primary:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  margin-top: 1rem;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.login-link a {
  color: #2c3e50;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>