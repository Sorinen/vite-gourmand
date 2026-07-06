# Vite & Gourmand 🍽️

Application web de traiteur événementiel à La Réunion.

## 🌐 Démo en ligne

- **Frontend** : https://zotpresta.re
- **API** : https://api.zotpresta.re/docs

---

## 📋 Description

## 📋 Description

Vite & Gourmand est une application web fullstack développée pour Julie et José, un couple de traiteurs événementiels basés à Bordeaux. 

L'application permet à leurs clients de consulter les menus proposés, passer des commandes en ligne pour leurs événements (mariages, anniversaires, séminaires...), et laisser des avis après prestation. Julie et José disposent d'un espace d'administration complet pour gérer leurs commandes, menus et clients.

---

## 🚀 Fonctionnalités

### Côté client
- Consultation des menus avec filtres (thème, régime)
- Inscription et connexion
- Passage de commande en ligne
- Suivi de ses commandes
- Dépôt d'avis après prestation

### Côté admin
- Dashboard avec statistiques (MongoDB)
- Gestion des commandes (changement de statut)
- Gestion des menus (créer, modifier, supprimer)
- Validation des avis clients
- Gestion des messages de contact

### Côté employé
- Gestion des commandes
- Validation des avis

---

## 🛠️ Stack technique

### Frontend
- Vue.js 3 (Composition API)
- Vue Router
- Pinia (state management)
- Axios
- Vite

### Backend
- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- MongoDB (Motor)
- JWT (python-jose)

### Déploiement
- Hostinger VPS
- Dokploy
- Docker / Docker Compose
- Traefik (reverse proxy)
- Nginx (serveur frontend)

---

## ⚙️ Installation locale

### Prérequis
- Docker Desktop
- Node.js 20+
- Python 3.13

### Backend

```bash
cd backend
docker compose up -d
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Charger les données initiales

```bash
docker exec -i vite_gourmand_postgres psql -U postgres -d vite_gourmand < docs/data_initiales.sql
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Compte admin par défaut
- **Email** : admin@traiteur.re
- **Mot de passe** : AdminSecret123!

---

## 🏗️ Architecture

vite-gourmand/

├── backend/
│   ├── app/
│   │   ├── models/        # Modèles SQLAlchemy
│   │   ├── schemas/       # Schémas Pydantic
│   │   ├── crud/          # Opérations base de données
│   │   ├── routes/        # Endpoints FastAPI
│   │   ├── services/      # Logique métier
│   │   └── utils/         # JWT, mail, sécurité
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/         # Pages Vue.js
│   │   ├── components/    # Composants réutilisables
│   │   ├── stores/        # Store Pinia
│   │   ├── services/      # API Axios
│   │   └── router/        # Vue Router
│   └── Dockerfile
├── docs/
│   └── data_initiales.sql
└── docker-compose.yml

---

## 🗄️ Base de données

### PostgreSQL — 16 entités
ROLE, UTILISATEUR, THEME, REGIME, ALLERGENE, TYPE_PLAT, MENU, PLAT, IMAGE_MENU, MENU_PLAT, PLAT_ALLERGENE, COMMANDE, HISTORIQUE_STATUT, AVIS, HORAIRE, CONTACT

### MongoDB
Statistiques des commandes par menu (chiffre d'affaires, nombre de commandes)

---

## 🔐 Sécurité
- Authentification JWT (HS256, 8h)
- Hashage des mots de passe (bcrypt)
- Protection des routes par rôle (Admin, Employé, Client)
- CORS configuré

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre du **TP Développeur Web et Web Mobile** (Studi ECF 2026).