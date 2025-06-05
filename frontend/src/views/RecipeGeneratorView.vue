<!-- src/views/RecipeGeneratorView.vue -->
<template>
  <div class="recipe-generator">
    <div class="recipe-generator__container">
      <div style="display: flex; align-items: center;justify-content:center ;gap: 10px;">
        <img :src="aiLogo" alt="AI Logo" style="width: 50px; height: 50px;">
        <h1 class="page-title">AI Recipe Generator</h1>
      </div>
      <p class="recipe-generator__instructions">
        Create delicious recipes based on your preferences and available ingredients.
      </p>

      <div v-if="!hasIngredients" class="warning-message">
        <p>⚠️ You don't have any ingredients in your fridge yet.</p>
        <router-link to="/fridge" class="btn btn-secondary">Add Ingredients</router-link>
      </div>

      <form class="recipe-form" @submit.prevent="onGenerate">
        <div class="recipe-form__grid">
          <div class="form-group">
            <label for="type">Recipe Type</label>
            <select
              id="type"
              v-model="form.type"
              required
              class="form-control"
            >
              <option v-for="type in recipeTypes" :key="type" :value="type">
                {{ type }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="cuisine">Cuisine</label>
            <select
              id="cuisine"
              v-model="form.cuisine"
              required
              class="form-control"
            >
              <option v-for="cuisine in cuisines" :key="cuisine" :value="cuisine">
                {{ cuisine }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="time">Time It Takes</label>
            <select
              id="time"
              v-model="form.time"
              required
              class="form-control"
            >
              <option v-for="time in timeOptions" :key="time" :value="time">
                {{ time }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="style">Nutritional Style</label>
            <select
              id="style"
              v-model="form.style"
              required
              class="form-control"
            >
              <option v-for="style in nutritionalStyles" :key="style" :value="style">
                {{ style }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <div class="dietary-info">
            <div class="dietary-info__header">
              <label>Your Dietary Preferences & Allergies</label>
              <router-link to="/profile" class="btn btn-secondary">Edit in Profile</router-link>
            </div>
            <div class="dietary-info__content">
              <div v-if="userStore.account?.dietary_preferences?.length" class="dietary-info__section">
                <h4>Dietary Preferences:</h4>
                <div class="dietary-tags">
                  <span v-for="pref in userStore.account.dietary_preferences" :key="pref" class="dietary-tag">
                    {{ pref }}
                  </span>
                </div>
              </div>
              <div v-if="userStore.account?.allergies?.length" class="dietary-info__section">
                <h4>Allergies:</h4>
                <div class="dietary-tags">
                  <span v-for="allergy in userStore.account.allergies" :key="allergy" class="dietary-tag dietary-tag--allergy">
                    {{ allergy }}
                  </span>
                </div>
              </div>
              <div v-if="!userStore.account?.dietary_preferences?.length && !userStore.account?.allergies?.length" class="dietary-info__empty">
                No dietary preferences or allergies set. Click "Edit in Profile" to add them.
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="notes">Other Preferences</label>
          <textarea
            id="notes"
            v-model="form.notes"
            rows="2"
            placeholder="E.g., extra spicy, kid-friendly, no cilantro"
            class="form-control"
          ></textarea>
        </div>

        <div class="form-actions">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading || !isFormValid"
          >
            <span v-if="!loading">Generate Recipes</span>
            <span v-else class="loading">
              <span class="loading__spinner"></span>
              Generating...
            </span>
          </button>
        </div>
      </form>

      <Transition name="fade">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import aiLogo from '@/assets/images/logo-1.png'
import { reactive, ref, computed, onMounted } from 'vue'
import { useIngredientsStore } from '@/stores/ingredients'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const ingredientsStore = useIngredientsStore()
const userStore = useUserStore()

// Constants
const recipeTypes = [
  'Appetizer',
  'Main Course',
  'Side Dish',
  'Dessert',
  'Snack',
  'Beverage'
]

const cuisines = [
  'Chinese',
  'Indian',
  'Italian',
  'Mexican',
  'Middle Eastern',
  'Fusion'
]

const timeOptions = [
  'Under 15 min',
  '15–30 min',
  '30–60 min',
  '60+ min'
]

const nutritionalStyles = [
  'Healthy',
  'Low-Carb',
  'High-Protein',
  'Whole Foods',
  'Vegan',
  'Vegetarian'
]

const dietOptions = [
  'Gluten-free',
  'Dairy-free',
  'Nut-free',
  'Keto',
  'Paleo'
]

// State
const form = reactive({
  type: 'Main Course',
  cuisine: 'Italian',
  time: '30–60 min',
  style: 'Healthy',
  diets: [] as string[],
  notes: ''
})

const loading = ref(false)
const errorMessage = ref('')

// Computed
const isFormValid = computed(() => {
  return form.type && form.cuisine && form.time && form.style
})

const goodIngredientsList = computed(() => {
  return ingredientsStore.ingredients
    .filter(i => getConditionText(i.expiration_date) === 'Good')
    .map(i => `${i.name} ${i.quantity} ${i.unit}`)
    .join(', ')
})

const hasIngredients = computed(() => {
  return ingredientsStore.ingredients.length > 0
})

// Methods
const getConditionText = (expirationDate: string) => {
  const today = new Date()
  const expDate = new Date(expirationDate)
  const daysUntilExpiration = Math.ceil((expDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))

  if (daysUntilExpiration < 0) return 'Expired'
  if (daysUntilExpiration <= 3) return 'Expiring Soon'
  if (daysUntilExpiration <= 7) return 'Expiring This Week'
  return 'Good'
}

const toggleDiet = (diet: string) => {
  const index = form.diets.indexOf(diet)
  if (index === -1) {
    form.diets.push(diet)
  } else {
    form.diets.splice(index, 1)
  }
}

// Initialize user preferences
onMounted(() => {
  if (userStore.account) {
    // Add user's dietary preferences to the form
    form.diets = [...userStore.account.dietary_preferences]

    // Add user's allergies to the notes if any
    if (userStore.account.allergies && userStore.account.allergies.length > 0) {
      form.notes = `Allergies: ${userStore.account.allergies.join(', ')}`
    }
  }
})

async function onGenerate() {
  errorMessage.value = ''

  if (!hasIngredients.value) {
    errorMessage.value = 'Please add some ingredients to your fridge first. You can add ingredients from the "My Fridge" page.'
    return
  }

  if (goodIngredientsList.value === '') {
    errorMessage.value = 'You don\'t have any non-expired ingredients. Please add some fresh ingredients to your fridge first.'
    return
  }

  loading.value = true

  const promptText = `
You are an AI chef. Given:
  • Available Ingredients: ${goodIngredientsList.value}
  • Recipe Type: ${form.type}
  • Cuisine: ${form.cuisine}
  • Time: ${form.time}
  • Nutritional Style: ${form.style}
  • Dietary Restrictions: ${form.diets.join(', ') || 'none'}
  • Other Preferences: ${form.notes || 'none'}

IMPORTANT RULES:
1. ONLY use ingredients from the "goodIngredientsList"
2. DO NOT make up or invent new ingredients
3. If you need an ingredient not in the list, skip that recipe and create a different one
4. Each ingredient name must be a real, valid food item
5. STRICTLY AVOID any ingredients that the user is allergic to
6. Ensure recipes comply with all dietary restrictions specified

Produce exactly three distinct recipe objects.
**Output must be valid JSON ONLY**—an array of three items.
Each item must have exactly these keys:
  • "title"  : string
  • "description" : string (a brief one sentence summary)
  • "ingredients": an array of objects, each with:
    – "name": string (must be a real ingredient from goodIngredientsList)
    – "quantity": string (amount in cups, grams, etc.; approximate is fine as long as it does not exceed what you have)
  • "steps"  : an array of strings

Do NOT include any extra words, numbering, markdown, or commentary.
Return exactly:
[
  {
    "title": "Example Recipe 1",
    "description": "A short appetizing summary of the dish.",
    "ingredients": [
      { "name": "Ingredient A", "quantity": "2 cups" },
      { "name": "Ingredient B", "quantity": "1 tbsp" }
    ],
    "steps": [
      "Do X",
      "Do Y",
      "Do Z",
      "etc"
    ]
  },
  {
    "title": "Example Recipe 2",
    "description": "A short appetizing summary of the dish.",
    "ingredients": [
      { "name": "Ingredient C", "quantity": "3 slices" },
      { "name": "Ingredient D", "quantity": "200g" }
    ],
    "steps": [
      "Step 1",
      "Step 2",
      "Step 3",
      "etc"
    ]
  },
  {
    "title": "Example Recipe 3",
    "description": "A short appetizing summary of the dish.",
    "ingredients": [
      { "name": "Ingredient E", "quantity": "1 cup" },
      { "name": "Ingredient F", "quantity": "2 tsp" }
    ],
    "steps": [
      "First do this",
      "Then do that",
      "Finally do the other",
      "etc"
    ]
  }
]
`.trim()


  try {
    const DJANGO_BACKEND_URL = 'http://localhost:8000'
    const res = await fetch(`${DJANGO_BACKEND_URL}/api/recipes/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'meta-llama/llama-4-maverick-17b-128e-instruct',
        prompt: promptText,
        max_tokens: 600,
        temperature: 0.7,
        top_p: 0.9
      })
    })

    if (!res.ok) {
      const errText = await res.text()
      throw new Error(`API Error ${res.status}: ${errText}`)
    }

    const data = await res.json()
    const rawText: string = data.choices?.[0]?.text ?? data.result
    if (!rawText) {
      throw new Error('No response from Llama.')
    }

    let parsed: unknown
    try {
      parsed = JSON.parse(rawText.trim())
    } catch (jsonErr) {
      console.error('Failed to parse JSON:', rawText)
      throw new Error('Invalid JSON returned by Llama. Check prompt/schema.')
    }

    if (!Array.isArray(parsed) || parsed.length !== 3) {
      throw new Error('Unexpected JSON format: expected an array of exactly 3 recipes.')
    }

    parsed.forEach((item: any, idx: number) => {
      if (
        typeof item.title !== 'string' ||
        !Array.isArray(item.ingredients) ||
        !Array.isArray(item.steps)
      ) {
        throw new Error(`Recipe #${idx + 1} is missing required fields.`)
      }

      item.ingredients.forEach((ing: any, ingIdx: number) => {
        if (typeof ing.name !== 'string' || typeof ing.quantity !== 'string') {
          throw new Error(`Recipe #${idx + 1}, ingredient #${ingIdx + 1} has invalid format.`)
        }

        if (/[0-9]/.test(ing.name) || /[^a-zA-Z\s-]/.test(ing.name)) {
          throw new Error(`Recipe #${idx + 1} contains invalid ingredient name: "${ing.name}". Ingredients must be real food items.`)
        }
      })
    })

    localStorage.setItem('generatedRecipes', JSON.stringify(parsed))
    router.push({ name: 'generated-recipes' })
  } catch (err: any) {
    console.error(err)
    errorMessage.value = err.message || 'Unknown generation error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.recipe-generator {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
  padding: 2rem 1rem;
}

.recipe-generator__container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.recipe-generator__title {
  font-size: 2.5rem;
  color: #2c3e50;
  text-align: center;
  margin-bottom: 1rem;
  font-weight: 700;
}

.recipe-generator__instructions {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.recipe-form__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-control:focus {
  border-color: #4CAF50;
  outline: none;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.diet-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.diet-button {
  padding: 0.625rem 1.25rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #4a5568;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.diet-button:hover {
  border-color: #4CAF50;
  color: #4CAF50;
  transform: translateY(-1px);
}

.diet-button--selected {
  background: #4CAF50;
  border-color: #4CAF50;
  color: white;
}

.diet-button--selected:hover {
  background: #43A047;
  color: white;
}

.form-actions {
  text-align: center;
  margin-top: 2rem;
}

.loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading__spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #FEE2E2;
  border: 1px solid #EF4444;
  border-radius: 8px;
  color: #B91C1C;
  text-align: center;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .recipe-generator__container {
    padding: 1.5rem;
  }

  .recipe-generator__title {
    font-size: 2rem;
  }

  .recipe-form__grid {
    grid-template-columns: 1fr;
  }
}

.warning-message {
  background: #FFF3CD;
  border: 1px solid #FFE69C;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.warning-message p {
  color: #856404;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.dietary-info {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.dietary-info__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.dietary-info__header label {
  margin-bottom: 0;
  font-size: 1.1rem;
}

.dietary-info__section {
  margin-bottom: 1rem;
}

.dietary-info__section h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.dietary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.dietary-tag {
  background: #4CAF50;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.9rem;
}

.dietary-tag--allergy {
  background: #e74c3c;
}

.dietary-info__empty {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}
</style>
