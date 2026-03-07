---

# Production Ready JWT Auth System

A **production-ready full-stack authentication system** built using **React and Django REST Framework** implementing secure **JWT authentication with refresh token rotation and token blacklisting**.

This project demonstrates how to implement a **modern authentication workflow** used in real production applications including **user registration, login, email verification, password reset, protected APIs, and secure token management**.

It can be used as a **starter template for full-stack applications requiring a secure authentication system**.

---

# Project Overview

This project provides a **complete authentication solution** with frontend and backend integration.

The system uses:

* **JWT Access Tokens** for protected API requests
* **Refresh Tokens** for maintaining sessions
* **Refresh Token Rotation** for enhanced security
* **Token Blacklisting** on logout
* **Email Verification** for account activation
* **Password Reset Flow**

The goal of this project is to demonstrate **secure authentication architecture commonly used in production systems**.

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
* Secure Password Reset Flow
* Email verification before login

## Frontend Features

* React based UI
* Redux Toolkit for state management
* Protected routes
* Authentication state persistence
* API integration with Axios

## Backend Features

* Django REST Framework APIs
* Secure JWT implementation
* Custom authentication workflow
* Email verification system
* Password reset functionality

---

# Tech Stack

## Backend

* Django
* Django REST Framework
* Simple JWT
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

---

# System Architecture

```
React Frontend
      │
      │ HTTP Requests
      ▼
Django REST API
      │
      │ JWT Authentication
      ▼
Database (User Data)
```

The frontend communicates with the backend through REST APIs. Authentication is handled using **JWT tokens issued by the backend**.

---

# Authentication Flow

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

* Short lived
* Used for accessing protected APIs

## Refresh Token

* Used to generate new access tokens
* Allows users to remain logged in without re-authentication

---

## Refresh Token Rotation

Each time a refresh token is used:

1. A new access token is generated
2. A new refresh token is issued
3. The previous refresh token becomes invalid

This prevents **token replay attacks**.

---

## Token Blacklisting

When a user logs out:

* The refresh token is **added to the blacklist**
* Any request using this token is rejected
* Prevents **session hijacking or token reuse**

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

## 1 Clone Repository

```
git clone https://github.com/PritpalSingh786/Production-Ready-JWT-Auth-System.git

cd Production-Ready-JWT-Auth-System
```

---

# Backend Setup (Django)

Navigate to backend directory

```
cd backend
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run database migrations

```
python manage.py migrate
```

Start backend server

```
python manage.py runserver
```

Backend will run at

```
http://127.0.0.1:8000
```

---

# Frontend Setup (React)

Navigate to frontend directory

```
cd frontend
```

Install dependencies

```
npm install
```

Start development server

```
npm start
```

Frontend will run at

```
http://localhost:3000
```

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
* Learning JWT authentication
* Learning React + Django full stack development

---

# Future Improvements

* OAuth Login (Google / GitHub)
* Role Based Access Control
* Docker support
* Redis based token blacklist
* Rate limiting and API throttling

---

# What This Project Demonstrates

* Secure JWT authentication system
* Refresh token rotation implementation
* Token blacklisting strategy
* React + Django full stack integration
* Production authentication workflow

---

# Author

**Pritpal Singh**

GitHub
[https://github.com/PritpalSingh786](https://github.com/PritpalSingh786)

---

If you find this project useful, consider giving it a ⭐ on GitHub.

---
