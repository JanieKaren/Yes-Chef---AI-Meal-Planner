<!-- src/views/GeneratedRecipesAI.vue -->
<template>
  <div class="generated-recipes page-container">
    <h1 class="page-title">Your AI-Generated Recipes</h1>

    <div v-if="!recipes.length" class="no-recipes">
      <p>No recipes found. Please generate some first.</p>
      <router-link to="/recipe-generator" class="btn-primary">
        Back to Generator
      </router-link>
    </div>

    <div v-else>
      <!-- Grid container for three cards -->
      <div class="cards-container">
        <div
          class="card"
          v-for="(recipe, idx) in recipes"
          :key="idx"
        >
          <h3 class="card-title">{{ recipe.title }}</h3>
          <p class="card-description">{{ recipe.description }}</p>

          <div class="section">
            <h4>Ingredients</h4>
            <ul>
              <li v-for="(ing, i) in recipe.ingredients" :key="i">
                {{ ing.quantity }} {{ ing.name }}
              </li>
            </ul>
          </div>

          <div class="section">
            <h4>Steps</h4>
            <ol>
              <li v-for="(step, sIdx) in recipe.steps" :key="sIdx">
                {{ step }}
              </li>
            </ol>
          </div>

          <!-- SAVE BUTTON -->
          <div class="save-button-container">
            <button
              class="btn-save"
              :disabled="saving[idx]"
              @click="save(recipe, idx)"
            >
              <span v-if="!saving[idx] && !saved[idx]">Save</span>
              <span v-if="saving[idx]">Saving...</span>
              <span v-if="saved[idx]">Saved ✓</span>
            </button>
            <p v-if="saveErrors[idx]" class="error-text">
              {{ saveErrors[idx] }}
            </p>
          </div>
        </div>
      </div>

      <div class="actions">
        <router-link to="/recipe-generator" class="btn-secondary">
          Generate New Recipes
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRecipesStore } from '@/stores/recipe'
import { saveRecipeToBackend } from '@/stores/recipe'

interface Ingredient {
  name: string
  quantity: string
}

interface GeneratedRecipe {
  title: string
  description: string
  ingredients: Ingredient[]
  steps: string[]
}

const recipesStore = useRecipesStore()
const recipes = ref<GeneratedRecipe[]>([])
const saving = ref<boolean[]>([])
const saved = ref<boolean[]>([])
const saveErrors = ref<string[]>([])

const router = useRouter()

onMounted(() => {
  const raw = localStorage.getItem('generatedRecipes')
  if (raw) {
    try {
      const arr = JSON.parse(raw)
      if (Array.isArray(arr)) {
        recipes.value = arr.filter((item: any) => {
          return (
            item &&
            typeof item.title === 'string' &&
            typeof item.description === 'string' &&
            Array.isArray(item.ingredients) &&
            Array.isArray(item.steps) &&
            item.ingredients.every(
              (ing: any) =>
                ing &&
                typeof ing.name === 'string' &&
                typeof ing.quantity === 'string'
            ) &&
            item.steps.every((step: any) => typeof step === 'string')
          )
        }) as GeneratedRecipe[]
      }
    } catch {
      recipes.value = []
    }

    // Prepare a parallel array for saving state
    saving.value = recipes.value.map(() => false)
    saved.value = recipes.value.map(() => false)
    saveErrors.value = recipes.value.map(() => '')

    localStorage.removeItem('generatedRecipes')
  }
})

async function save(recipe: GeneratedRecipe, index: number) {
  if (saved.value[index]) return
  
  saving.value[index] = true
  saveErrors.value[index] = ''

  try {
    const payload: GeneratedRecipe = {
      title: recipe.title,
      description: recipe.description,
      ingredients: recipe.ingredients,
      steps: recipe.steps
    }

    await saveRecipeToBackend(payload)

    saved.value[index] = true
    alert('Recipe saved successfully!')
  } catch (err) {
    saveErrors.value[index] = 'Failed to save recipe.'
    console.error('Failed to save recipe', err)
  } finally {
    saving.value[index] = false
  }
}


</script>

<style scoped>
/* (Your existing styles here) */
.page-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 2rem;
}

.no-recipes {
  text-align: center;
  font-size: 1.1rem;
  color: #555;
}

.no-recipes p {
  margin-bottom: 1rem;
}

.btn-primary,
.btn-secondary {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  margin-top: 1rem;
  border-radius: 4px;
  text-decoration: none;
  color: white;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #2c3e50;
}

.btn-primary:hover {
  background-color: #34495e;
}

.btn-secondary {
  background-color: #95a5a6;
  margin-left: 1rem;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

/* Grid container for three cards */
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background: #fff;
  padding: 1rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.card-title {
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-size: 1.25rem;
}

.card-description {
  margin-bottom: 0.75rem;
  color: #555;
  font-size: 0.95rem;
}

.section {
  margin-top: 0.75rem;
}

.section h4 {
  margin-bottom: 0.25rem;
  font-size: 1rem;
  color: #444;
}

.section ul,
.section ol {
  padding-left: 1.25rem;
  margin: 0;
}

.save-button-container {
  margin-top: 1rem;
}

.btn-save {
  background-color: #28a745;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
}

.btn-save:disabled {
  background-color: #94d3a2;
  cursor: not-allowed;
}

.error-text {
  margin-top: 0.5rem;
  color: #c00;
  font-size: 0.85rem;
}

.actions {
  text-align: center;
  margin-top: 1rem;
}
</style>
