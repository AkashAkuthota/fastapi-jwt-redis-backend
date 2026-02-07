# FastAPI Product Inventory System 🔐📦

A backend-focused **Product Inventory & User Authentication API** built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.  
The project demonstrates real-world backend concepts including **JWT authentication**, **CRUD operations**, **database integration**, and **secure user management**.

---

## 🚀 Features

### 🔑 Authentication & Authorization
- User signup with email & password
- Secure password hashing
- User login with JWT access token
- Token-based authentication using OAuth2
- Token revocation (logout support)
- Active/inactive user handling

### 📦 Product Management
- Create, read, update, delete products
- Full update using PUT
- Partial update using PATCH
- Protected routes using JWT
- Response validation with Pydantic schemas

### 🗄️ Database
- PostgreSQL
- SQLAlchemy ORM
- Clean separation between:
  - Pydantic schemas
  - SQLAlchemy models
  - Database session handling

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Password Hashing:** passlib
- **Validation:** Pydantic
- **Server:** Uvicorn

---

## 📁 Project Structure

```

fastAPI project/
│
├── main.py                  # API routes & application logic
├── database.py              # DB engine & session
├── database_models.py       # SQLAlchemy models
├── model.py                 # Pydantic schemas
├── auth.py                  # JWT token creation
├── security.py              # Password hashing & verification
├── decodingtokens.py        # get_current_user logic
├── requirements.txt
│
├── frontend/                # Frontend (React) – basic integration
│
└── myenv/                   # Virtual environment (ignored in git)

````

---

## ⚙️ Setup Instructions

### 1. Clone repository
```bash
git clone <your-repo-url>
cd fastAPI-project
````

### 2. Create & activate virtual environment

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

* Create a database
* Update DB credentials in `database.py`

### 5. Run the server

```bash
uvicorn main:app --reload
```

### 6. API Docs

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 Authentication Flow

1. User signs up → password is hashed & stored
2. User logs in → JWT token is issued
3. Token is sent in `Authorization: Bearer <token>`
4. Protected routes validate token via `get_current_user`
5. Logout revokes token (stored in DB)

---

## 📌 Status

* Backend core complete
* JWT + logout implemented
* Frontend integration basic (to be enhanced later)

---

## 📄 License

This project is for learning and demonstration purposes.
