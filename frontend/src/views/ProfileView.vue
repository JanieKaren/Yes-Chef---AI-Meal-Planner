<template>
  <div class="profile-container">
    <h1>Profile</h1>
    
    <div class="profile-section">
      <h2>User Information</h2>
      <div class="info-card">
        <p><strong>Username:</strong> {{ userStore.user?.username }}</p>
        <p><strong>Email:</strong> {{ userStore.user?.email }}</p>
      </div>
    </div>

    <div class="profile-section">
      <h2>Dietary Preferences</h2>
      <div class="preferences-card">
        <div class="preferences-list">
          <div
            v-for="preference in userStore.account?.dietary_preferences"
            :key="preference"
            class="preference-tag"
          >
            {{ preference }}
          </div>
        </div>
        <button @click="showPreferencesModal = true" class="btn-secondary">
          Edit Preferences
        </button>
      </div>
    </div>

    <div class="profile-section">
      <h2>Fridge Inventory</h2>
      <div class="inventory-card">
        <div class="inventory-list">
          <div
            v-for="item in userStore.account?.fridge_inventory"
            :key="item"
            class="inventory-item"
          >
            {{ item }}
          </div>
        </div>
        <button @click="showInventoryModal = true" class="btn-secondary">
          Edit Inventory
        </button>
      </div>
    </div>

    <!-- Dietary Preferences Modal -->
    <div v-if="showPreferencesModal" class="modal">
      <div class="modal-content">
        <h2>Edit Dietary Preferences</h2>
        <div class="preferences-edit">
          <div
            v-for="preference in availablePreferences"
            :key="preference"
            class="preference-option"
          >
            <label>
              <input
                type="checkbox"
                :value="preference"
                v-model="selectedPreferences"
              />
              {{ preference }}
            </label>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="showPreferencesModal = false" class="btn-secondary">
            Cancel
          </button>
          <button @click="savePreferences" class="btn-primary">Save</button>
        </div>
      </div>
    </div>

    <!-- Fridge Inventory Modal -->
    <div v-if="showInventoryModal" class="modal">
      <div class="modal-content">
        <h2>Edit Fridge Inventory</h2>
        <div class="inventory-edit">
          <div class="form-group">
            <input
              type="text"
              v-model="newInventoryItem"
              placeholder="Add new item"
              class="form-control"
              @keyup.enter="addInventoryItem"
            />
          </div>
          <div class="inventory-items">
            <div
              v-for="(item, index) in inventoryItems"
              :key="index"
              class="inventory-item-edit"
            >
              <span>{{ item }}</span>
              <button @click="removeInventoryItem(index)" class="btn-icon">×</button>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="showInventoryModal = false" class="btn-secondary">
            Cancel
          </button>
          <button @click="saveInventory" class="btn-primary">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const showPreferencesModal = ref(false)
const showInventoryModal = ref(false)

const availablePreferences = [
  'Vegetarian',
  'Vegan',
  'Gluten-Free',
  'Dairy-Free',
  'Nut-Free',
  'Halal',
  'Kosher',
  'Pescatarian'
]

const selectedPreferences = ref<string[]>([])
const newInventoryItem = ref('')
const inventoryItems = ref<string[]>([])

onMounted(() => {
  selectedPreferences.value = userStore.account?.dietary_preferences || []
  inventoryItems.value = userStore.account?.fridge_inventory || []
})

const savePreferences = async () => {
  await userStore.updateDietaryPreferences(selectedPreferences.value)
  showPreferencesModal.value = false
}

const addInventoryItem = () => {
  if (newInventoryItem.value.trim()) {
    inventoryItems.value.push(newInventoryItem.value.trim())
    newInventoryItem.value = ''
  }
}

const removeInventoryItem = (index: number) => {
  inventoryItems.value.splice(index, 1)
}

const saveInventory = async () => {
  await userStore.updateFridgeInventory(inventoryItems.value)
  showInventoryModal.value = false
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-section {
  margin-bottom: 2rem;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.info-card, .preferences-card, .inventory-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.preferences-list, .inventory-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.preference-tag, .inventory-item {
  background-color: #e0e0e0;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.preferences-edit, .inventory-edit {
  margin-bottom: 1rem;
}

.preference-option {
  margin-bottom: 0.5rem;
}

.inventory-items {
  margin-top: 1rem;
}

.inventory-item-edit {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background-color: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.btn-icon {
  background: none;
  border: none;
  color: #e74c3c;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-primary, .btn-secondary {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  border: none;
  font-size: 1rem;
}

.btn-primary {
  background-color: #2c3e50;
  color: white;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}
</style> 