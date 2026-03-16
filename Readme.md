# FastAPI Secure Product Inventory System 🔐📦

A **production-oriented backend system** built with **FastAPI**, demonstrating secure authentication, Redis-based token management, and scalable API design.

This project focuses on **backend architecture and security practices** commonly used in real-world applications.

---

# 🚀 Key Features

## 🔑 Authentication & Security

* JWT authentication
* Access token + refresh token flow
* Refresh token rotation
* Token reuse detection
* Secure logout using Redis token blacklist
* Password hashing with bcrypt
* OAuth2 bearer token authentication

---

## 🛡️ Authorization

* Role-Based Access Control (RBAC)
* Admin / User permission separation
* Protected API routes
* Secure dependency injection for role validation

---

## 📦 Product Inventory System

Admin capabilities:

* Create products
* Update products (PUT)
* Partial update (PATCH)
* Delete products

User capabilities:

* View products
* Add products to cart
* Manage cart items

---

## 🛒 Cart Management

* Add product to cart
* Update quantity
* Remove items
* Cart isolation per user

---

## ⚡ Redis Integration

Using **Redis for production-level backend features**

* Token blacklist storage
* Login rate limiting
* Refresh token security
* Fast token validation
* TTL based automatic cleanup

---

## ⏱️ Background Tasks

Using **APScheduler**

* Scheduled cleanup of expired tokens
* Background maintenance tasks

---

# 🛠 Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Redis
* APScheduler
* JWT (python-jose)
* passlib / bcrypt

### Frontend (Client)

* React
* Vite
* Axios

### Infrastructure

* Redis (Upstash)
* Deployment ready for Render / Vercel

---

# 📁 Project Structure

```
fastapi-product-inventory
│
├── app
│   ├── core
│   │   ├── auth.py
│   │   ├── security.py
│   │   ├── redis_client.py
│   │   └── rate_limiter.py
│   │
│   ├── db
│   │   ├── database.py
│   │   └── database_models.py
│   │
│   ├── routers
│   │   ├── auth_router.py
│   │   ├── product_router.py
│   │   └── cart_router.py
│   │
│   ├── schemas
│   ├── services
│   ├── tasks
│   │   └── token_cleanup.py
│   │
│   └── main.py
│
├── frontend
│   ├── src
│   ├── components
│   ├── pages
│   └── api
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Local Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/AkashAkuthota/fastapi-jwt-redis-backend.git
cd fastapi-jwt-redis-backend
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

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

```bash
uvicorn app.main:app --reload
```

Swagger API docs:

```
http://localhost:8000/docs
```

---

# 🌐 Frontend Setup

```bash
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
