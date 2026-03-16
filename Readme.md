<<<<<<< HEAD
# 🔐 Secure Product Inventory API

Production-Oriented FastAPI Backend with JWT, Refresh Token Rotation, Redis & RBAC

---

## 📌 Overview

A production-style backend API built using FastAPI, PostgreSQL, and Redis.

This project demonstrates real-world backend engineering concepts including:

- JWT Authentication (Access + Refresh Tokens)
- Refresh Token Rotation with Reuse Detection
- Redis-Based Rate Limiting
- Redis-Based Access Token Blacklisting
- Role-Based Access Control (RBAC)
- Background Token Cleanup Jobs
- Secure HTTPOnly Cookie Handling
- Multi-Session Awareness

Designed to reflect practical backend architecture used in modern applications.

---

## 🚀 Core Features

### 🔐 Authentication System

- User Signup (Email + Password)
- Secure Password Hashing (bcrypt)
- JWT Access Tokens
- Refresh Tokens stored in HTTPOnly cookies
- Refresh Token Rotation
- Refresh Token Reuse Detection (Breach Detection)
- Access Token Blacklisting using Redis

#### Logout Behavior

Logout invalidates:
- Current Access Token (added to Redis blacklist)
- Associated Refresh Token (revoked in DB)

---

### 🛡 Security Features
=======
```
# FastAPI Secure Product Inventory System 🔐📦

A **production-oriented backend system** built with **FastAPI**, demonstrating secure authentication, Redis-based token management, and scalable API design.

This project focuses on **backend architecture and security practices** commonly used in real-world applications.

---

# 🚀 Key Features

## 🔑 Authentication & Security

- JWT authentication
- Access token + refresh token flow
- Refresh token rotation
- Token reuse detection
- Secure logout using Redis token blacklist
- Password hashing with bcrypt
- OAuth2 bearer token authentication

---

## 🛡️ Authorization

- Role-Based Access Control (RBAC)
- Admin / User permission separation
- Protected API routes
- Secure dependency injection for role validation

---

## 📦 Product Inventory System

Admin capabilities:

- Create products
- Update products (PUT)
- Partial update (PATCH)
- Delete products

User capabilities:

- View products
- Add products to cart
- Manage cart items

---

## 🛒 Cart Management

- Add product to cart
- Update quantity
- Remove items
- Cart isolation per user

---

## ⚡ Redis Integration

Using **Redis for production-level backend features**

- Token blacklist storage
- Login rate limiting
- Refresh token security
- Fast token validation
- TTL based automatic cleanup

---

## ⏱️ Background Tasks

Using **APScheduler**

- Scheduled cleanup of expired tokens
- Background maintenance tasks

---

# 🛠️ Tech Stack

### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Redis
- APScheduler
- JWT (python-jose)
- passlib / bcrypt

### Frontend (Client)

- React
- Vite
- Axios

### Infrastructure

- Redis (Upstash)
- Deployment ready for Render / Vercel

---

# 📁 Project Structure

- HTTPOnly Refresh Cookies
- Login & Refresh Endpoint Rate Limiting
- Redis Token Blacklist
- Token Expiration Validation
- Role-Based Route Protection
- Background Cleanup of Expired Tokens
- Secure Session Invalidation

---

### 👥 Role-Based Access Control (RBAC)

Supported roles:

- admin
- user

Protected routes use dependency guards to restrict access.

---

### 📦 Product Management Features

- Create Product (Admin Only)
- Get All Products (Authenticated Users)
- Get Product by ID
- Update Product (PUT / PATCH)
- Delete Product

All endpoints are protected via JWT authentication.

---

## 🗄 Tech Stack

| Layer              | Technology        |
|--------------------|------------------|
| Framework          | FastAPI          |
| Database           | PostgreSQL       |
| ORM                | SQLAlchemy       |
| Cache              | Redis            |
| Authentication     | python-jose (JWT)|
| Password Hashing   | passlib (bcrypt) |
| Validation         | Pydantic         |
| Background Jobs    | APScheduler      |
| ASGI Server        | Uvicorn          |

---

## 🏗 Architecture Highlights

### 🔄 Authentication Flow

1. User logs in  
   → Access Token (JWT) returned  
   → Refresh Token stored in HTTPOnly cookie  

2. Access Token used in:

   Authorization: Bearer <token>

3. Refresh Token stored in database.

4. On Refresh:
   - Old refresh token revoked
   - New refresh token issued
   - Rotation enforced

5. On Logout:
   - Access token added to Redis blacklist
   - Refresh token revoked in database

---

### 🚦 Rate Limiting Strategy

- Redis counters per:
  - IP address
  - User

- TTL-based expiration
- Protects against brute-force attacks
- Separate limits for:
  - Login attempts
  - Refresh attempts

---

## 📂 Project Structure

```bash
fastapi-product-inventory/
│
├── frontend/
│
├── main.py
├── auth.py
├── auth_context.py
├── security.py
├── permissions.py
├── rate_limiter.py
├── redis_client.py
├── token_cleanup.py
├── decodingtokens.py
│
├── database.py
├── database_models.py
├── model.py
=======
fastapi-product-inventory
│
├── app
│
│ ├── core
│ │ ├── auth.py
│ │ ├── security.py
│ │ ├── redis_client.py
│ │ └── rate_limiter.py
│
│ ├── db
│ │ ├── database.py
│ │ └── database_models.py
│
│ ├── routers
│ │ ├── auth_router.py
│ │ ├── product_router.py
│ │ └── cart_router.py
│
│ ├── schemas
│ ├── services
│ ├── tasks
│ │ └── token_cleanup.py
│
│ └── main.py
│
├── frontend
│ ├── src
│ ├── components
│ ├── pages
│ └── api
>>>>>>> 2f605dd (feat: backend deployment setup and Redis integration)
│
├── requirements.txt
├── README.md
└── .gitignore
<<<<<<< HEAD
```
=======

````

>>>>>>> 2f605dd (feat: backend deployment setup and Redis integration)
---

# ⚙️ Local Setup

## 1️⃣ Clone Repository

<<<<<<< HEAD
### 1️⃣ Clone Repository

git clone <your-repo-url>
cd fastapi-project

---

### 2️⃣ Create Virtual Environment

python3 -m venv myenv
=======
```bash
git clone https://github.com/AkashAkuthota/fastapi-product-inventory.git
cd fastapi-product-inventory
````

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
>>>>>>> 2f605dd (feat: backend deployment setup and Redis integration)
source myenv/bin/activate

---

<<<<<<< HEAD
### 3️⃣ Install Dependencies
=======
## 3️⃣ Install Dependencies
>>>>>>> 2f605dd (feat: backend deployment setup and Redis integration)

pip install -r requirements.txt

---

<<<<<<< HEAD
### 4️⃣ Create .env File

SECRET_KEY=your_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=15  
REFRESH_TOKEN_EXPIRE_DAYS=7  
DATABASE_URL=postgresql://username:password@localhost:5432/dbname  
REDIS_URL=redis://localhost:6379  

---

### 5️⃣ Run Redis

redis-server

---

### 6️⃣ Run Application

uvicorn main:app --reload

---

### 7️⃣ Swagger Documentation

http://127.0.0.1:8000/docs

---

## 🔒 Production Notes

For production deployment:

- Set secure=True for cookies
- Enable HTTPS
- Protect Redis with authentication
- Never commit .env to GitHub
- Use Docker + Reverse Proxy (Nginx)
- Enable structured logging

---

## 🎯 Why This Project Is Production-Oriented

This project demonstrates:

- Stateless Authentication Design
- Token Lifecycle Management
- Secure Session Invalidation
- Abuse Prevention via Rate Limiting
- Scalable Architecture using Redis
- Separation of Authentication & Authorization (RBAC)
- Clean Modular Backend Structure

This is not just a CRUD API — it reflects real backend security engineering practices.

---

## 📌 Project Status

✅ Core Security & Session Management Complete  

### 🔄 Planned Improvements

- Multi-device Session Tracking
- Audit Logging
- Suspicious Activity Detection
- API Versioning
- Dockerized Deployment Setup
=======
## 4️⃣ Environment Variables

Create `.env`

```
SECRET_KEY=your_secret_key

REDIS_HOST=your_upstash_host
REDIS_PORT=6379
REDIS_PASSWORD=your_upstash_password

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 5️⃣ Run Backend

```
uvicorn app.main:app --reload
```

Swagger API docs:

```
http://localhost:8000/docs
```

---

# 🌐 Frontend Setup

```
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🔐 Authentication Flow

1️⃣ User signup
2️⃣ Password hashed using bcrypt

3️⃣ Login returns

```
access_token
refresh_token
```

4️⃣ Access token used for API requests

```
Authorization: Bearer <token>
```

5️⃣ Logout

* Token stored in Redis blacklist
* Access revoked immediately

---

# 📈 Security Features Implemented

* Secure password hashing
* JWT authentication
* Refresh token rotation
* Redis token blacklist
* Rate limiting
* RBAC authorization
* Token cleanup scheduler

---

# 📌 Project Purpose

This project demonstrates **backend engineering practices** such as:

* secure authentication systems
* scalable API design
* Redis-based security layers
* background task management
* modular backend architecture

---

# 📄 License

This project is for **educational and demonstration purposes**.

````

---
>>>>>>> 2f605dd (feat: backend deployment setup and Redis integration)
