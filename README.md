---

# Production Ready JWT Auth System 🚀

A **production-ready full-stack authentication system** built using **React and Django REST Framework**, implementing **secure JWT authentication with real-time session management, refresh token rotation, token blacklisting, and WebSocket-based auto logout**.

This project demonstrates a **modern, scalable authentication workflow used in real-world production systems**, including **multi-device session control, real-time session invalidation, and secure token lifecycle management**.

---

# 🔥 Project Overview

This system provides a **complete and secure authentication solution** with both frontend and backend integration.

It includes:

* JWT-based authentication (Access + Refresh tokens)
* Refresh token rotation
* Token blacklisting
* Multi-device session management
* **Real-time auto logout using WebSockets**
* Email notifications for session activity
* Background cleanup using Celery Beat

---

# ⚡ Key Features

## 🔐 Authentication

* User Registration
* User Login
* User Logout
* Email Verification
* Password Reset via Email

---

## 🛡️ Security Features

* JWT Authentication (Access + Refresh Tokens)
* Short-lived Access Tokens
* Refresh Token Rotation
* Token Blacklisting
* Protected API Routes
* Email Verification before login
* Secure Password Reset Flow

---

## 📡 Advanced Session Management (NEW 🔥)

* Maximum **5 active sessions per user**
* **Oldest session auto-logout** when limit exceeds
* **Real-time session termination using WebSockets**
* **Device-level session targeting (via device_id)**
* **Redis-based channel layer for scalability**
* **Instant logout across devices (no API call required)**

---

## 📧 Email & Background Jobs

* Email notification on session termination
* Celery for async email handling
* Celery Beat for:

  * Expired token cleanup
  * Session cleanup

---

## 🎨 Frontend Features

* React-based UI
* Redux Toolkit state management
* Protected routes
* Axios interceptors for token refresh
* **Auto logout handling (WebSocket + fallback)**
* Token expiry detection

---

## ⚙️ Backend Features

* Django REST Framework APIs
* Simple JWT integration
* Custom session management logic
* WebSocket support using Django Channels
* Redis-based real-time communication
* Secure authentication workflows

---

# 🧠 System Architecture

```
React Frontend
      │
      │ HTTP + WebSocket
      ▼
Django REST API + Channels
      │
      │ JWT + Session Management
      ▼
Database (User + Device + Tokens)
      │
      │ Redis (Channel Layer)
      ▼
Real-time Session Events
      │
      ▼
Celery + Celery Beat
      │
      ▼
Background Jobs + Emails
```

---

# 🔄 Authentication & Session Flow

```
User Login
      │
      ▼
JWT Issued (Access + Refresh + device_id)
      │
      ▼
WebSocket Connection Established
      │
      ▼
Session Limit Check (max 5)
      │
      ├─ If ≤ 5 → allow
      │
      └─ If > 5 → kill oldest session
              │
              ▼
   🔥 WebSocket Event Sent (SESSION_KILLED)
              │
              ▼
   Frontend receives → Auto Logout
              │
              ▼
   Email Notification Sent
```

---

# 🔐 JWT Security Implementation

## Access Token

* Short-lived
* Used for API authentication

## Refresh Token

* Used to generate new access tokens
* Stored securely (HttpOnly cookie for web)

---

## 🔁 Refresh Token Rotation

Each refresh request:

1. New access token issued
2. New refresh token generated
3. Old refresh token invalidated

👉 Prevents **token replay attacks**

---

## 🚫 Token Blacklisting

* On logout → refresh token is blacklisted
* Prevents reuse of stolen tokens

---

# ⚡ Real-Time Auto Logout (NEW 🔥)

* Implemented using **WebSockets + Redis**
* Each device has a unique **device_id**
* When session limit exceeds:

  * Old session identified
  * WebSocket event sent to that device
  * User logged out instantly

👉 No polling, no delay — **instant logout**

---

# 📁 Project Structure

```
backend/
 ├── users/
 │   ├── models.py
 │   ├── serializers.py
 │   ├── views.py
 │   ├── consumers.py   🔥 (WebSocket)
 │   ├── middleware.py  🔥 (JWT Auth)
 │
 ├── project/
 │   ├── settings.py
 │   ├── asgi.py        🔥 (Channels)
 │
frontend/
 ├── src/
 │   ├── components/
 │   ├── pages/
 │   ├── features/
 │   ├── api/
 │   ├── socket/        🔥 (WebSocket client)
 │   ├── utils/
 │   └── App.js
```

---

# ⚙️ Installation Guide

## Backend

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Frontend

```
cd frontend
npm install
npm start
```

---

## Redis (Required for WebSocket)

```
sudo service redis start
```

---

# 🔌 API Endpoints

| Method | Endpoint                    | Description        |
| ------ | --------------------------- | ------------------ |
| POST   | /api/register               | Register user      |
| POST   | /api/login                  | Login              |
| POST   | /api/logout                 | Logout             |
| POST   | /api/token/refresh          | Refresh token      |
| POST   | /api/verify-email           | Email verification |
| POST   | /api/request-password-reset | Request reset      |
| POST   | /api/reset-password         | Reset password     |

---

# 🎯 Use Cases

* SaaS authentication systems
* Multi-device login apps
* Secure enterprise login systems
* Learning JWT + WebSockets + Redis

---

# 🚀 Future Improvements

* OAuth (Google / GitHub)
* Role-based access control (RBAC)
* Docker deployment
* Admin session control panel
* Active devices UI (like Gmail)

---

# 🧠 What This Project Demonstrates

* Secure JWT authentication architecture
* Refresh token rotation
* Token blacklisting
* Multi-device session management
* **Real-time session invalidation (WebSocket + Redis)**
* Scalable backend architecture
* Full-stack integration (React + Django)

---

# 👨‍💻 Author

**Pritpal Singh**

GitHub: [https://github.com/PritpalSingh786](https://github.com/PritpalSingh786)

---
