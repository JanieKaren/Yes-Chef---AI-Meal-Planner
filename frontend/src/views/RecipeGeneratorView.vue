<!-- src/views/RecipeGeneratorView.vue -->
<template>
  <div class="recipe-generator page-container">
    <h1 class="page-title">AI Recipe Generator</h1>
    <p class="instructions">
      1) Make sure your Django backend is running and exposes <code>/api/recipes/</code>.<br />
      2) Replace <code>DJANGO_BACKEND_URL</code> below if it lives somewhere else.
    </p>

    <form class="recipe-form" @submit.prevent="onGenerate">
      <div class="form-group">
        <label for="type">Recipe Type</label>
        <select id="type" v-model="form.type" required>
          <option>Appetizer</option>
          <option>Main Course</option>
          <option>Side Dish</option>
          <option>Dessert</option>
          <option>Snack</option>
          <option>Beverage</option>
        </select>
      </div>

      <div class="form-group">
        <label for="cuisine">Cuisine</label>
        <select id="cuisine" v-model="form.cuisine" required>
          <option>Chinese</option>
          <option>Indian</option>
          <option>Italian</option>
          <option>Mexican</option>
          <option>Middle Eastern</option>
          <option>Fusion</option>
        </select>
      </div>

      <div class="form-group">
        <label for="time">Time It Takes</label>
        <select id="time" v-model="form.time" required>
          <option>Under 15 min</option>
          <option>15–30 min</option>
          <option>30–60 min</option>
          <option>60+ min</option>
        </select>
      </div>

      <div class="form-group">
        <label for="style">Nutritional Style</label>
        <select id="style" v-model="form.style" required>
          <option>Healthy</option>
          <option>Low-Carb</option>
          <option>High-Protein</option>
          <option>Whole Foods</option>
          <option>Vegan</option>
          <option>Vegetarian</option>
        </select>
      </div>

    
      <div class="form-group" :class="{ selected: form.diets.length }">
  <label>Diet &amp; Allergies</label>
  <div class="checkbox-group" v-for="option in dietOptions" :key="option">
    <label :for="`diet-${option}`" class="custom-checkbox-label">
      <input
        type="checkbox"
        :value="option"
        v-model="form.diets"
        :id="`diet-${option}`"
      />
      <span class="custom-checkbox"></span>
      {{ option }}
    </label>
  </div>
</div>

      <div class="form-group">
        <label for="notes">Other Preferences</label>
        <textarea
          id="notes"
          v-model="form.notes"
          rows="2"
          placeholder="no cilantro, extra spicy, kid-friendly"
        ></textarea>
      </div>

      <div style="text-align: center;">
    <button type="submit" id="generate-btn" :disabled="loading">
        <span v-if="!loading">Generate Recipes</span>
        <span v-else>
            Generating
            <span class="spinner"></span>
        </span>
    </button>
</div>

    </form>

    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'
import { useIngredientsStore } from '@/stores/ingredients'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  type: 'Dessert',
  cuisine: 'Chinese',
  time: 'Under 15 min',
  style: 'Healthy',
  ingredients: '',
  diets: [] as string[],
  notes: ''
})

// 1. Instantiate the Pinia store
const ingredientsStore = useIngredientsStore()

// 2. Copy/paste (or import) your "condition" helper from IngredientsView.vue
const getConditionText = (expirationDate: string) => {
  const today = new Date()
  const expDate = new Date(expirationDate)
  const daysUntilExpiration = Math.ceil((expDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))

  if (daysUntilExpiration < 0) return 'Expired'
  if (daysUntilExpiration <= 3) return 'Expiring Soon'
  if (daysUntilExpiration <= 7) return 'Expiring This Week'
  return 'Good'
}

// 3. Fetch all ingredients on mount so store is populated
onMounted(() => {
  ingredientsStore.fetchIngredients(1)
})

// 4. Create a computed string of only "Good" ingredients (with quantity/unit)
const goodIngredientsList = computed(() => {
  return ingredientsStore.ingredients
    .filter(i => getConditionText(i.expiration_date) === 'Good')
    .map(i => `${i.name} ${i.quantity} ${i.unit}`)
    .join(', ')
})

const dietOptions = [
  'Gluten-free',
  'Dairy-free',
  'Nut-free',
  'Keto',
  'Paleo'
]

const loading = ref(false)
const errorMessage = ref('')

async function onGenerate() {
  errorMessage.value = ''
  loading.value = true

  // 1) Build a prompt that forces JSON‐only output
  const promptText = `
You are an AI chef. Given:
  • Ingredients: ${goodIngredientsList.value}
  • Recipe Type: ${form.type}
  • Cuisine: ${form.cuisine}
  • Time: ${form.time}
  • Nutritional Style: ${form.style}
  • Dietary Restrictions: ${form.diets.join(', ') || 'none'}
  • Other Preferences: ${form.notes || 'none'}

Produce exactly three distinct recipe objects. 
**Output must be valid JSON ONLY**—an array of three items. 
Each item must have exactly these keys:
  • "title"  : string
  • "ingredients": an array of objects, each with:
    – "name": string
    – "quantity": string (amount in cups, grams, etc.; approximate is fine as long as it does not exceed what you have)
  • "steps"  : an array of strings

Do NOT include any extra words, numbering, markdown, or commentary. 
Return exactly:
[
  {
    "title": "Example Recipe 1",
    "ingredients": [
      { "name": "Ingredient A", "quantity": "2 cups" },
      { "name": "Ingredient B", "quantity": "1 tbsp" }
    ],
    "steps": [
      "Do X",
      "Do Y",
      "Do Z"
    ]
  },
  {
    "title": "Example Recipe 2",
    "ingredients": [
      { "name": "Ingredient C", "quantity": "3 slices" },
      { "name": "Ingredient D", "quantity": "200g" }
    ],
    "steps": [
      "Step 1",
      "Step 2",
      "Step 3"
    ]
  },
  {
    "title": "Example Recipe 3",
    "ingredients": [
      { "name": "Ingredient E", "quantity": "1 cup" },
      { "name": "Ingredient F", "quantity": "2 tsp" }
    ],
    "steps": [
      "First do this",
      "Then do that",
      "Finally do the other"
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
        model: 'meta-llama/llama-4-scout-17b-16e-instruct',
        prompt: promptText,
        max_tokens: 600,     // bump up if needed so the JSON fits
        temperature: 0.7,
        top_p: 0.9
      })
    })

    if (!res.ok) {
      const errText = await res.text()
      throw new Error(`API Error ${res.status}: ${errText}`)
    }

    const data = await res.json()
    // assume the back‐end returns something like: { choices: [ { text: '[…JSON…]' } ] }
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

    // Validate that parsed is an array of length 3
    if (!Array.isArray(parsed) || parsed.length !== 3) {
      console.error('Parsed not an array of length 3:', parsed)
      throw new Error('Unexpected JSON format: expected an array of exactly 3 recipes.')
    }

    // Optionally: further validate each object has title/ingredients/steps
    parsed.forEach((item: any, idx: number) => {
      if (
        typeof item.title !== 'string' ||
        !Array.isArray(item.ingredients) ||
        !Array.isArray(item.steps)
      ) {
        throw new Error(`Recipe #${idx + 1} is missing required fields.`)
      }
    })

    // Save to localStorage as a JSON string
    localStorage.setItem('generatedRecipes', JSON.stringify(parsed))

    // Navigate to the “generated recipes” page
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

.page-container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 2rem;
}

.instructions {
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: #555;
}

.recipe-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.25rem;
  display: block;
  color: #2c3e50;
}

.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  resize: vertical;
  font-size: 0.95rem;
  color: #2c3e50;
  transition: background-color 0.2s ease;
}


.checkbox-group {
  display: inline-block;
  margin-right: 1rem;
  margin-bottom: 0.5rem;
  align-items: start;
  position: relative;
}

.checkbox-group input {
  margin-right: 0.25rem;
}

button[type='submit'] {
  background-color: #28a745;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 600;
  margin-top: 0.5rem;
  display: inline-flex;
  align-items: center;
}

button[disabled] {
  background-color: #94d3a2;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 3px solid rgba(255, 255, 255, 0.6);
  border-top: 3px solid #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-left: 8px;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

.error {
  color: #c00;
  margin-top: 1rem;
  font-weight: 500;
}

.page-container:hover {
  background: #e6f9e6; /* Light green on hover */
  transition: background 0.3s;
}

</style>
