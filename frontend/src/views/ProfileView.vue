<template>
  <div class="background-container">
    <div class="profile-container">
      <div class="profile-header">
        <img src="@/assets/images/profile_header.png" alt="profile-header-image">
      <h1>User Profile</h1>
    </div>
    <div class="information">
      <div class="profile-section">
      <h2>Account Information</h2>
      <div class="info-card">
        <div class="field">
          <label>Firstname:</label>
          <input v-if="isEditing" v-model="editableUser.first_name" />
          <p v-else>{{ userStore.user?.first_name }}</p>
        </div>
        <div class="field">
          <label>Lastname:</label>
          <input v-if="isEditing" v-model="editableUser.last_name" />
          <p v-else>{{ userStore.user?.last_name }}</p>
        </div>
        <div class="field">
          <label>Username:</label>
          <input v-if="isEditing" v-model="editableUser.username" />
          <p v-else>{{ userStore.user?.username }}</p>
        </div>
        <div class="field">
          <label>Email:</label>
          <input v-if="isEditing" v-model="editableUser.email" />
          <p v-else>{{ userStore.user?.email }}</p>
        </div>
        <button @click="toggleEdit" class="btn-secondary">
            {{ isEditing ? 'Cancel' : 'Edit' }}
          </button>
          <button v-if="isEditing" @click="saveChanges" class="btn-primary">Save</button>
        
      </div>
    </div>
      <div class="user-preference">
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
        <h2>Allergies</h2>
        <div class="preferences-card">
          <div class="preferences-list">
            <div
              v-for="allergy in userStore.account?.allergies"
              :key="allergy"
              class="preference-tag"
            >
              {{ allergy }}
            </div>
          </div>
          <button @click="showAllergyModal = true" class="btn-secondary">
            Edit Allergies
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

      <!-- Allergies Modal -->
      <div v-if="showAllergyModal" class="modal">
        <div class="modal-content">
          <h2>Edit Allergies</h2>
          <div class="preferences-edit">
            <div
              v-for="allergy in availableAllergies"
              :key="allergy"
              class="preference-option"
            >
              <label>
                <input
                  type="checkbox"
                  :value="allergy"
                  v-model="selectedAllergies"
                />
                {{ allergy }}
              </label>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="showAllergyModal = false" class="btn-secondary">Cancel</button>
            <button @click="saveAllergies" class="btn-primary">Save</button>
          </div>
        </div>
      </div>

      </div>

    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
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


onMounted(() => {
  selectedPreferences.value = userStore.account?.dietary_preferences || []
  selectedAllergies.value = userStore.account?.allergies || []
})

const savePreferences = async () => {
  const success = await userStore.updateDietaryPreferences(selectedPreferences.value)
  if (success) {
    showPreferencesModal.value = false
  } else {
    alert('Something went wrong while saving preferences.')

  }
  
}


const isEditing = ref(false)
const editableUser = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: ''
})

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (isEditing.value) {
    Object.assign(editableUser, {
      first_name: userStore.user?.first_name,
      last_name: userStore.user?.last_name,
      username: userStore.user?.username,
      email: userStore.user?.email
    })
  }
}

async function saveChanges() {
  if (isEditing.value && userStore.user) {
    try {
      const updatedUser = await userStore.updateUserInfo({ ...editableUser })
      if (updatedUser) {
        isEditing.value = false
      }
    } catch (error) {
      console.error('Failed to update user info:', error)
    }
  }
}

const showAllergyModal = ref(false)

const availableAllergies = [
  'Peanuts', 'Tree Nuts', 'Milk', 'Eggs', 'Fish', 'Shellfish', 'Soy', 'Wheat',
  'Sesame', 'Gluten', 'Lactose', 'Corn'
]

const selectedAllergies = ref<string[]>([])

const saveAllergies = async () => {
  const success = await userStore.updateAllergies(selectedAllergies.value)
  if (success) {
    alert('Allergies saved')
    showAllergyModal.value = false
  } else {
    alert('Something went wrong while saving allergies.')
  }
}


</script>

<style scoped>
.background-container {
 padding: 2rem 1rem;
 background-color: #fdfaf6;
 min-height: calc(100vh - 100px);
 display: flex;
 flex-direction: column;
 align-items: center;
 background-image: url("@/assets/images/profile_background.jpg");
 background-size: contain;
 background-position: top left;
 
}

.profile-container{
  padding: 20px;
  border-radius: 8px;
  background-color: white;
  min-width: 800px;
}

.information {
  margin-top: 1rem;
  max-width: 800px;
  padding: 2rem;
  padding-top: 0;
  
}

.profile-header{
 text-align: center;
 font-family: 'Aclonica', sans-serif;
}


.profile-section {
  margin-bottom: 0.5rem;
  margin-top: 1rem;
}

h1 {
  color: #2c3e50;
  
}

h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.info-card, .preferences-card {
  background-color: rgb(245, 231, 204);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-preference{
  margin-top: 10px;
}

.preferences-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.preference-tag {
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

.info-card .btn-secondary {
  margin-right: 20px;
}

.btn-primary:hover, .btn-secondary:hover{
  background-color: orange;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.user-info {
 max-width: 500px;
 margin: 2rem auto;
 padding: 1.5rem;
 border-radius: 12px;
 background-color: #f9f9f9;
 box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.profile-section h2 {
 margin-bottom: 0.5rem;
 font-size: 1.5rem;
 color: #333;
 
}
.info-card .field {
 display: flex;
 flex-direction: column;
 margin-bottom: 1rem;
}
.field label {
 font-weight: 600;
 margin-bottom: 0.3rem;
 color: #555;
}
.field input {
 padding: 0.5rem;
 border: 1px solid #ccc;
 border-radius: 6px;
 font-size: 1rem;
}
.field p {
 font-size: 1rem;
 color: #2c3e50;
}


</style> 