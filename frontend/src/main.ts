import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

// Configure axios
axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.withCredentials = true

// Add CSRF token to all requests
axios.interceptors.request.use(config => {
  const csrfToken = document.cookie.split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]
  
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
