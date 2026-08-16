# QuickTurf Backend

> Backend API for QuickTurf, a turf booking SaaS platform built with FastAPI and PostgreSQL.

QuickTurf Backend provides the REST API, authentication, booking management, turf administration, payment tracking, database operations, and business logic required to operate the QuickTurf platform.

---

## 🚀 Overview

QuickTurf is a turf booking system that allows customers to book sports turfs while enabling turf administrators to manage their facilities, sports, time slots, bookings, and payment information.

The backend is designed using a layered architecture to keep API handling, business logic, and database operations separated.

### Core Responsibilities

- User and admin authentication
- Turf management
- Sports management
- Time-slot management
- Turf search
- Booking creation and management
- Double-booking prevention
- Payment and due-amount tracking
- Membership discount handling
- Invoice generation
- WhatsApp link generation
- Database migrations

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | JWT / Token-based Authentication |
| Database Migration | Alembic |
| API Documentation | Swagger |
| Server | Uvicorn |

---


## 📁 Project Structure

A simplified backend structure:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── models/
│   │   ├── ...
│   │
│   ├── schemas/
│   │   ├── ...
│   │
│   ├── routes/
│   │   ├── ...
│   │
│   ├── services/
│   │   ├── ...
│   │
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── turf_repository.py
│   │   ├── booking_repository.py
│   │   └── ...
│   │
│   ├── factories/
│   │   ├── ...
│   │
│   ├── observers/
│   │   ├── ...
│   │
│   └── tests/
│       ├── ...
│
├── alembic/
│   ├── versions/
│   └── ...
│
├── requirements.txt
├── .env
└── ...
```

> The exact structure may differ depending on the current backend branch.

---

## 🧩 Design Patterns

QuickTurf uses several design patterns to improve maintainability, modularity, and separation of concerns.

### Factory Pattern

The Factory Pattern centralizes the creation of domain objects.

Examples:

```text
BookingFactory
TurfFactory
```

This avoids scattering object-creation logic throughout the application.

### Observer Pattern

The Observer Pattern allows different components to react to booking-related events.

Examples:

```text
BookingSubject
    │
    ├── InvoiceObserver
    │
    └── WhatsAppObserver
```

This reduces coupling between booking creation and follow-up actions.

### Repository Pattern

The Repository Pattern separates database access from business logic.

Examples:

```text
BaseRepository<T>
    │
    ├── TurfRepository
    │
    └── BookingRepository
```

Benefits include:

- Cleaner services
- Reusable database operations
- Easier testing
- Better separation of concerns

---

## 🔐 Authentication

QuickTurf uses token-based authentication for protected API operations.

Typical authentication flow:

```text
Client
  │
  ▼
Login Request
  │
  ▼
Authentication Endpoint
  │
  ▼
Credentials Validation
  │
  ▼
Access Token
  │
  ▼
Protected API Requests
```

Protected administrative endpoints require a valid access token.

Authentication-related responsibilities include:

- Login
- Password validation
- Access-token generation
- Protected routes
- Authorization checks
- Password change

---

## 🗄️ Database

QuickTurf uses **PostgreSQL** as its primary relational database.

Major domain entities include:

- Users
- Turfs
- Sports
- Time Slots
- Bookings
- Payment information
- Membership information

Simplified relationship:

```text
User
 │
 └──────────────┐
                │
                ▼
             Booking
             /     \
            /       \
           ▼         ▼
        Turf      Payment
         │
         ├── Sports
         │
         └── Time Slots
```

---

## 🔄 Database Migrations

Database schema changes are managed with **Alembic**.

Apply the latest migrations:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

Create a new migration when required:

```bash
alembic revision --autogenerate -m "your migration message"
```

---

## 📡 API

The QuickTurf backend exposes RESTful APIs for the main application resources.

Major API areas include:

```text
/auth
/turfs
/sports
/time-slots
/bookings
/users
/payments
```

The exact routes depend on the current implementation.

### API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 📋 Main User Stories

| ID | User Story |
|---|---|
| US-01 | Create Turf |
| US-02 | Turf Admin Login |
| US-03 | Change Password |
| US-04 | Manage Sports |
| US-05 | Manage Time Slots |
| US-06 | Search & Book Turf |
| US-07 | Create Booking |

---

## 📅 Booking Workflow

The backend booking workflow is approximately:

```text
Booking Request
      │
      ▼
Validate Request Data
      │
      ▼
Validate Turf
      │
      ▼
Validate Selected Slot
      │
      ▼
Check Slot Availability
      │
      ▼
Calculate Booking Amount
      │
      ▼
Apply Membership Discount
      │
      ▼
Create Booking
      │
      ▼
Store Payment Information
      │
      ▼
Generate Booking/Invoice Data
      │
      ▼
Return API Response
```

### Booking Data

A booking can contain information such as:

- Customer name
- Phone
- Email
- Notes
- Turf
- Sport
- Time slot
- Booking date
- Paid amount
- Due amount
- Payment status
- Membership discount

---

## 🚫 Double-Booking Prevention

One of the important backend responsibilities is preventing multiple bookings for the same turf slot.

Before creating a booking, the backend checks whether the requested slot is already booked.

```text
New Booking Request
        │
        ▼
Check Existing Booking
        │
     ┌──┴──┐
     │     │
   Exists  Available
     │     │
     ▼     ▼
 Reject   Create
 Booking  Booking
```

This ensures that unavailable slots cannot be booked again.

---

## 💰 Payment Information

The backend stores payment-related information associated with bookings.

Examples include:

- Total booking amount
- Paid amount
- Due amount
- Payment status
- Membership discount

The backend can calculate the remaining due amount from the booking/payment information.

Example:

```text
Total Amount = 2000
Paid Amount  = 1200
Due Amount   = 800
```

---

## 🧾 Invoice

Booking-related invoice information can be generated after a successful booking.

The invoice may contain:

- Booking information
- Customer information
- Turf information
- Date and time
- Total amount
- Paid amount
- Due amount
- Payment status

---

## 📱 WhatsApp Integration

The backend can generate WhatsApp contact links from booking/customer information.

This allows booking-related communication to be initiated through WhatsApp without tightly coupling the booking logic to the messaging mechanism.

The implementation uses the Observer Pattern through components such as:

```text
WhatsAppObserver
```

---

## ⚙️ Local Development Setup

### Prerequisites

Install:

- Python 3.11+
- PostgreSQL
- Git

Verify:

```bash
python --version
psql --version
git --version
```

---

### 1. Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd QuickTurf
```

---

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .myvenv
.myvenv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .myvenv
source .myvenv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/quickturf
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE quickturf;
```

Then update the database connection string:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/quickturf
```

---

### 6. Run Migrations

```bash
alembic upgrade head
```

---

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

---

## 🔒 Security

The backend follows common security practices such as:

- Token-based authentication
- Password hashing
- Environment-based secret management
- Pydantic input validation
- Protected administrative routes
- Database-level access through the application layer
- CORS configuration
- Avoiding hard-coded credentials

### Important


### `ModuleNotFoundError`

Make sure the virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## 🚀 Production Deployment

For production deployment, the backend requires:

- Python-compatible hosting
- PostgreSQL database
- Environment variables
- Production database migrations
- Proper CORS configuration
- Secure authentication configuration

Example production command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Production secrets should be configured through the hosting provider's environment-variable system rather than committed to source control.

---

## 📊 Backend Design Principles

The backend follows these principles:

### Separation of Concerns

API routes, business logic, and database access are separated.

### Reusability

Common database operations are abstracted into repositories.

### Maintainability

Services and design patterns keep the codebase modular.

### Testability

Business logic and database operations can be tested independently.

### Scalability

The layered architecture allows additional features and resources to be introduced without heavily modifying existing components.

---

## 🔮 Future Improvements

Potential backend improvements include:

- Online payment gateway integration
- Role-based access control
- Rate limiting
- Redis caching
- Background task processing
- Email/SMS notifications
- Advanced booking analytics
- Revenue reporting APIs
- Audit logging
- Improved API versioning
- Increased test coverage
- Docker-based deployment

---

### Project

**QuickTurf — Turf Booking SaaS**

QuickTurf was developed as a collaborative software engineering project with a focus on REST API development, database design, authentication, software architecture, testing, and deployment.


## ⭐ QuickTurf Backend

**FastAPI · PostgreSQL · SQLAlchemy · Alembic · Pytest**

**Find. Book. Play.**
