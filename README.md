# 🩸 Blood Bank Management API

A production-ready REST API that connects blood donors with hospitals in need, featuring intelligent blood compatibility matching, an emergency response system, real-time inventory tracking, and donation eligibility management.

**🔗 Live Demo:** [blood-bank-api-production-3275.up.railway.app/docs](https://blood-bank-api-production-3275.up.railway.app/docs)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)

---

## 📋 Overview

Blood shortages are a critical, life-threatening problem. Hospitals urgently need a way to find compatible, available donors quickly — especially during emergencies. This API solves that problem by intelligently matching donors to hospitals based on medical blood compatibility rules, donor availability, and location.

Unlike a simple CRUD application, this project implements real medical domain logic: blood-type compatibility (O-negative universal donor, AB-positive universal receiver), donation eligibility rules (age, weight, and the mandatory 90-day gap between donations), and an emergency-response endpoint that creates a request and auto-matches nearby donors in a single call.

---

## ✨ Key Features

### 🔐 Authentication & Security
- JWT-based authentication with OAuth2 password flow
- Bcrypt password hashing
- Rate limiting on login endpoints to prevent brute-force attacks
- Environment-based secrets management (no hardcoded credentials)

### 🩸 Intelligent Donor Matching
- Medically accurate blood compatibility engine (all 8 blood types)
- Finds compatible, available donors filtered by location
- Handles universal donors (O-) and universal receivers (AB+)

### 🚨 Emergency Response System
- Single-call endpoint that creates a blood request AND auto-matches nearby compatible donors
- Prioritizes donors in the same city as the requesting hospital

### 💉 Donation Management
- Records donations with automatic donor-stat updates
- Enforces the 90-day eligibility rule (rejects donors who donated too recently)
- Validates donor eligibility (age 18–65, minimum weight 50kg)

### 📦 Real-Time Inventory
- Tracks blood stock per hospital per blood type
- Automatic shortage alerts when stock falls below critical levels
- Upsert pattern prevents duplicate inventory records

### 📊 Statistics Dashboard
- Aggregated analytics using SQL `COUNT` and `GROUP BY`
- Donor distribution by blood group and city
- Redis-cached responses for performance

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | FastAPI |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic |
| **Caching** | Redis |
| **Auth** | JWT (python-jose), Bcrypt (passlib) |
| **Migrations** | Alembic |
| **Rate Limiting** | SlowAPI |
| **Testing** | Pytest |
| **Deployment** | Railway, Docker |

---

## 🏗️ Architecture

The project follows a clean, layered architecture with clear separation of concerns:

```
blood-bank-api/
├── app/
│   ├── main.py              # App entry point + middleware
│   ├── config.py            # Centralized settings (env vars)
│   ├── database.py          # DB connection + session
│   ├── models.py            # SQLAlchemy models (6 tables)
│   ├── schemas.py           # Pydantic validation models
│   ├── crud.py              # Database access layer
│   ├── auth.py              # Authentication logic
│   ├── cache.py             # Redis caching layer
│   ├── logger.py            # Request logging
│   └── routers/             # Feature-organized endpoints
│       ├── auth.py
│       ├── donors.py
│       ├── hospitals.py
│       ├── requests.py
│       ├── donations.py
│       ├── inventory.py
│       ├── emergency.py
│       └── stats.py
├── alembic/                 # Database migrations
├── tests/                   # Pytest test suite
├── Dockerfile
└── requirements.txt
```

**Database Schema:** Six related tables (`users`, `donors`, `hospitals`, `blood_requests`, `donations`, `blood_inventory`) with foreign-key relationships.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis (optional — caching degrades gracefully if unavailable)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hrushii1305/blood-bank-api.git
   cd blood-bank-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** — create a `.env` file:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:password@localhost/bloodbank
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_HOURS=24
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open the interactive docs** at `http://localhost:8000/docs`

---

## 📖 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive a JWT |
| POST | `/token` | OAuth2 token endpoint |

### Donors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/donors` | List donors (paginated, filterable) |
| POST | `/donors` | Register a donor 🔒 |
| GET | `/donors/{id}` | Get a specific donor |
| PUT | `/donors/{id}` | Update donor availability 🔒 |
| DELETE | `/donors/{id}` | Delete a donor 🔒 |
| GET | `/donors/match/{blood_group}` | Find compatible donors |

### Emergency & Donations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/emergency` | Create request + auto-match donors 🔒 |
| POST | `/donations` | Record a donation 🔒 |
| GET | `/donations` | View donation history |

### Inventory & Stats
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/inventory` | Update blood stock 🔒 |
| GET | `/inventory/shortage` | Get shortage alerts |
| GET | `/stats` | Overall statistics dashboard |

🔒 = Requires authentication

---

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

The suite covers authentication, input validation, protected-route access control, and the blood-matching logic, running against an isolated in-memory test database.

---

## 👤 Author

**Hrushikesh Saini**
GitHub: [@hrushii1305](https://github.com/hrushii1305)

---

## 📄 License

This project is open source and available under the MIT License.
