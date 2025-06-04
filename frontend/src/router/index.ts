import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('../views/LandingPage.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
     // ← New route for Recipe Generator
    {
      path: '/recipe-generator',
      name: 'recipe-generator',
      component: () => import('../views/RecipeGeneratorView.vue'),
      // If you want only authenticated users to see it, add: meta: { requiresAuth: true }
    },

    {
    path: '/generated-recipes',
    name: 'generated-recipes',
    component: () => import('../views/GeneratedRecipesAI.vue'),
    props: false // we'll pull data from localStorage instead of props
    },



    {
      path: '/fridge',
      name: 'ingredients',
      component: () => import('../views/Fridge/IngredientsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/fridge/new',
      name: 'new-ingredient',
      component: () => import('../views/Fridge/EditIngredientView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/fridge/:id/edit',
      name: 'edit-ingredient',
      component: () => import('../views/Fridge/EditIngredientView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/recipe',
      name: 'Recipe',
      component: () => import('../views/Cookbook/RecipeView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // Check authentication status if not already checked
  if (!userStore.isAuthenticated && userStore.user === null) {
    await userStore.checkAuth()
  }

  // Handle protected routes
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'landing' })
  }
  // Handle guest-only routes
  else if (to.meta.requiresGuest && userStore.isAuthenticated) {
    next({ name: 'home' })
  }
  else {
    next()
  }
})

export default router