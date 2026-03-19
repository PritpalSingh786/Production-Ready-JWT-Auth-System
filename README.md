Perfect bhai, ab main teri **poori updated README** likh deta hoon jo **current system ke saare features** (JWT, refresh token rotation, multi-device sessions, oldest session auto logout, Celery cleanup, send_session_killed_email) ko cover kare.

---

# Production Ready JWT Auth System

A **production-ready full-stack authentication system** built using **React and Django REST Framework**, implementing **secure JWT authentication with session management, refresh token rotation, token blacklisting, and email notifications for session security**.

This project demonstrates how to implement a **modern authentication workflow used in real production applications**, including **user registration, login, email verification, password reset, multi-device session management, and secure token handling**.

It can be used as a **starter template for full-stack applications requiring robust security**.

---

# Project Overview

This project provides a **complete authentication solution** with frontend and backend integration.

The system uses:

* **JWT Access Tokens** for protected API requests
* **Refresh Tokens** for maintaining sessions
* **Refresh Token Rotation** for enhanced security
* **Token Blacklisting** on logout
* **Session Limit Enforcement** (max 5 devices per user)
* **Oldest Session Auto-Logout** when limit exceeds
* **Email Notification for Killed Sessions**
* **Email Verification** for account activation
* **Password Reset Flow**

The goal is to demonstrate **secure authentication architecture commonly used in production systems** with high concurrency and multi-device support.

---

# Key Features

## Authentication

* User Registration
* User Login
* User Logout
* Email Verification
* Password Reset via Email

## Security Features

* JWT Authentication (Access + Refresh Token)
* Refresh Token Rotation
* Token Blacklisting on Logout
* Short-lived Access Tokens
* Protected API Routes
* Session Limit per User (max 5 active sessions)
* Oldest Session Auto-Logout (when limit exceeds)
* **Email Notification for Killed Sessions**
* Celery Beat based background cleanup for expired tokens and sessions
* Secure Password Reset Flow
* Email verification before login

## Frontend Features

* React-based UI
* Redux Toolkit for state management
* Protected routes
* Authentication state persistence
* API integration with Axios

## Backend Features

* Django REST Framework APIs
* Secure JWT implementation
* Custom authentication workflow with session management
* Email verification system
* Password reset functionality
* **send_session_killed_email** for notifying users when their session is terminated
* Celery Beat scheduled tasks for cleanup and enforcement

---

# Tech Stack

## Backend

* Django
* Django REST Framework
* Simple JWT
* Celery + Celery Beat for async tasks
* Python

## Frontend

* React
* Redux Toolkit
* React Router
* Axios

## Security

* JWT Access Tokens
* Refresh Tokens
* Refresh Token Rotation
* Token Blacklisting
* Multi-device Session Management
* Email Notifications for session security

---

# System Architecture

```
React Frontend
      │
      │ HTTP Requests
      ▼
Django REST API
      │
      │ JWT + Session Management
      ▼
Database (User & Session Data)
      │
      │ Celery Beat
      ▼
Background Token & Session Cleanup + Emails
```

The frontend communicates with the backend through REST APIs. Authentication is handled using **JWT tokens issued by the backend**, with **session enforcement, background cleanup, and email notifications**.

---

# Authentication & Session Flow

```
User Register
      │
      ▼
Email Verification
      │
      ▼
User Login
      │
      ▼
Access Token + Refresh Token Issued
      │
      ▼
Check User Session Limit
      │
      ├─ If <= 5 sessions → allow
      │
      └─ If > 5 sessions → logout oldest session
           │
           ▼
      send_session_killed_email(user_email, session_info)
      │
      ▼
Protected API Access
      │
      ▼
Access Token Expired
      │
      ▼
Refresh Token Sent
      │
      ▼
New Access Token Generated
      │
      ▼
Refresh Token Rotated
      │
      ▼
Old Refresh Token Invalid
```

---

# JWT Security Implementation

## Access Token

* Short-lived
* Used for accessing protected APIs

## Refresh Token

* Used to generate new access tokens
* Allows users to remain logged in without re-authentication
* Rotated on each use to prevent token replay attacks

---

## Refresh Token Rotation

Each time a refresh token is used:

1. A new access token is generated
2. A new refresh token is issued
3. The previous refresh token becomes invalid

This prevents **token replay attacks** and enhances security for multi-device logins.

---

## Token Blacklisting

When a user logs out:

* The refresh token is **added to the blacklist**
* Any request using this token is rejected
* Prevents **session hijacking or token reuse**

---

## Session Management & Security Emails

* Maximum **5 active sessions per user**
* On exceeding limit → **oldest session auto-logout**
* **Email Notification:**

  * User receives an email when a session is terminated due to **session limit exceeded**
  * Function: `send_session_killed_email(user_email, session_info)`
  * Ensures **user awareness of unexpected logins**
* **Celery Beat** handles background cleanup of expired sessions and tokens

---

# Project Structure

```
Production-Ready-JWT-Auth-System

backend
 ├── auth_app
 │   ├── models.py
 │   ├── views.py
 │   ├── serializers.py
 │   ├── urls.py
 │
 ├── project
 │   ├── settings.py
 │   ├── urls.py
 │
 └── manage.py

frontend
 ├── src
 │   ├── components
 │   ├── pages
 │   ├── redux
 │   ├── services
 │   └── App.js
```

---

# Installation Guide

## 1. Clone Repository

```
git clone https://github.com/PritpalSingh786/Production-Ready-JWT-Auth-System.git
cd Production-Ready-JWT-Auth-System
```

---

## 2. Backend Setup (Django)

```
cd backend
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000`

---

## 3. Frontend Setup (React)

```
cd frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

---

# API Endpoints

| Method | Endpoint                    | Description            |
| ------ | --------------------------- | ---------------------- |
| POST   | /api/register               | Register new user      |
| POST   | /api/login                  | Login user             |
| POST   | /api/logout                 | Logout user            |
| GET    | /api/authenticated          | Get authenticated user |
| POST   | /api/verify-email           | Verify email           |
| POST   | /api/request-password-reset | Request password reset |
| POST   | /api/reset-password         | Set new password       |

---

# Example Use Cases

* Authentication system for SaaS products
* Secure login system for web applications
* Multi-device login with session enforcement
* Learning JWT authentication with rotation and blacklisting
* Full-stack React + Django integration

---

# Future Improvements

* OAuth Login (Google / GitHub)
* Role-Based Access Control
* Docker support
* Redis-based token blacklist
* Rate limiting and API throttling

---

# What This Project Demonstrates

* Secure JWT authentication system
* Refresh token rotation implementation
* Token blacklisting strategy
* Multi-device session management with oldest session auto-logout
* **Email notification on killed sessions**
* Celery Beat based background cleanup
* React + Django full stack integration
* Production authentication workflow

---

# Author

**Pritpal Singh**

GitHub: [https://github.com/PritpalSingh786](https://github.com/PritpalSingh786)

---
