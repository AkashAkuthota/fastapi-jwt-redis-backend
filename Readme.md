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
│
├── requirements.txt
├── README.md
└── .gitignore
```
---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

git clone <your-repo-url>
cd fastapi-project

---

### 2️⃣ Create Virtual Environment

python3 -m venv myenv
source myenv/bin/activate

---

### 3️⃣ Install Dependencies

pip install -r requirements.txt

---

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
