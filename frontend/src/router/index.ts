import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('../views/LandingPage.vue'),
      meta: { isPublic: true }
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
      meta: { isPublic: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { isPublic: true }
    },
    {
      path: '/recipe-generator',
      name: 'recipe-generator',
      component: () => import('../views/RecipeGeneratorView.vue'),
    },
    {
      path: '/generated-recipes',
      name: 'generated-recipes',
      component: () => import('../views/GeneratedRecipesAI.vue'),
      props: false
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
      name: 'RecipeView',
      component: () => import('../views/Cookbook/RecipeView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // Skip auth checks for public routes
  if (to.meta.isPublic) {
    // If user is already authenticated and tries to access login/register,
    // redirect them to home
    if (userStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
      next({ name: 'home' })
    } else {
      next()
    }
    return
  }

  // Initialize auth if not already done
  if (!userStore.isInitialized) {
    try {
      await userStore.initialize()
    } catch (error) {
      console.error('Failed to initialize auth:', error)
      // Continue with navigation even if initialization fails
    }
  }

  // Handle protected routes
  if (to.meta.requiresAuth) {
    if (userStore.isAuthenticated) {
      next()
    } else {
      next({ name: 'login' })
    }
    return
  }

  // Allow access to non-protected routes
  next()
})

export default router