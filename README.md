# 👨‍🍳 Yes, Chef!
**Your AI meal planner — where artificial intelligence meets appetite.**

---

## 🌟 Features
### 🤖 AI Recipe Generator  
Harness the power of artificial intelligence to generate unique and personalized recipes based on:
- Ingredients you already have at home  
- Your dietary preferences and restrictions (e.g., vegan, gluten-free)  
- Your desired cuisine or meal type (e.g., dinner, dessert, Italian)  
No more repetitive meals or decision fatigue — let AI inspire your next dish.

---

### 🧊 Smart Fridge Integration  
Digitally manage your fridge like never before:
- Add, update, and remove ingredients with ease  
- Track expiration dates to reduce food waste  
- Get recipe suggestions based on current fridge contents  
- Filter by available ingredients to save time and avoid unnecessary grocery runs  

---

### 📖 Personal Cookbook  
Your own organized, always-accessible online cookbook:
- Save your favorite AI-generated or custom recipes  
- Generate by meal type, cuisine, or dietary tags  
- Access your recipes anytime, from any device  
Never lose a great recipe to cluttered notes or screenshots again.

---

🎥 **Demo Video:** _[Insert video link here]_

🔗 **Explore Yes, Chef:** _[Insert live site or repo link here]_

---

## 📌 Overview
**Yes, Chef!** is a full-stack web application that helps users manage and discover recipes using AI. It's built with:

- **Frontend:** Vue.js 3 + TypeScript
- **Backend:** Django (Python)
- **Database:** SQLite
- **AI:** Meta LLama 4
- **Deployment :** Vercel (Vue.js) + Render (Django)

---

## 🏗️ Architecture

### 🖥️ Frontend
Built using:
- Vue.js 3 with TypeScript
- Vite (build tool)
- Pinia (state management)
- Vue Router (navigation)
- Axios (API requests)

#### Key Frontend Features
- Modular, component-based architecture
- Type-safe development
- State handling via Pinia
- Dynamic client-side routing
- Seamless API integration

---

### 🛠️ Backend
Built using:
- Django (Python web framework)
- SQLite
- REST API architecture

#### Key Backend Features
- RESTful API endpoints
- Recipe & fridge data models
- User authentication
- Input validation & data serialization

---
#### 🧠 AI Implementation
Powered by Meta's LLama 4 models:
- **Model Variants:**
  - `meta-llama/llama-4-maverick-17b-128e-instruct` (Frontend)
  - `meta-llama/llama-4-scout-17b-16e-instruct` (Backend)
- **Configuration:**
  - Temperature: 0.7 (balanced creativity)
  - Max Tokens: 600 (detailed recipes)
  - Top P: 0.9 (controlled randomness)
- **Features:**
  - Context-aware recipe generation
  - Ingredient compatibility checking
  - Dietary restriction compliance
  - Cuisine-specific adaptations
---

## 🚀 Getting Started

### 🔧 Prerequisites
- Node.js (for frontend)
- Python 3.x (for backend)
- npm or yarn (package manager)

---

### 🖥️ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 🖥️ Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py migrate
python manage.py runserver
```

## 🧪 Development

### 📚 API Documentation
The backend exposes RESTful endpoints for:

- 📋 Recipe management  
- 🔐 User authentication  
- 🧊 Ingredient & fridge data  

---

## 👥 Member Responsibilities

### 🧑‍💻 Cabusor
- **Development:**  
  - Collaborated to Recipe Generator Form

---

### 🧑‍💻 Cerio

---

### 🧑‍💻 De Pedro
- **Planning:**  
  - UI/UX for home, fridge, landing page

- **Development:**  
  - Vue-Django integration  
  - Models for fridge and recipes  
  - CRUD for fridge ingredients  
  - Filtering, searching, and pagination for fridge  
  - Landing page for unauthorized users  
  - Recipe Generator form UI  
  - Ingredient factories
  - Filtering, searching, and pagination for recipes
  - Fixing issues with Recipe Generator
  - Connecting diet and allergies of user
  - Dashboard for fridge and recipes
  - Vercel Deployment

- **Documentation:**  
  - README file  
  - Demo video

---

### 👩‍💻 Mejia  
- **Development:**  
  - Integration of Meta Llama
  - Prompt Creation
  - Recipe Generator using Meta Llama
  - Connecting Recipe List to Prompts

---
### 👨‍💻 Molanda  
- **Planning:**  
  - Application Logo
  - Application Color Theme
- **Development:**  
  - Improve overall UI
  - Ensure responsiveness across all devices
  - Home and Recipe Book pages
  - Vercel Deployment
---



