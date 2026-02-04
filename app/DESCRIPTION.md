# 📘 FastAPI Starter Template – API Documentation

## 🚀 Overview

The **FastAPI Starter Template API** is a production-ready backend boilerplate built with **FastAPI**, providing a complete foundation for modern web applications. It includes:

* 🔐 JWT-based Authentication
* 👤 User Management
* 📦 Item (CRUD + Search)
* 📁 File Upload, Download & Search
* 🧠 Pagination & Cursor-based Search
* ❤️ Health Checks & Metrics
* 🔎 REST + GraphQL support
* 📚 Auto-generated API Docs (Swagger / Scalar)

This API is designed to be **secure, scalable, and developer-friendly**.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **Auth:** OAuth2 Password Flow (JWT)
* **Validation:** Pydantic
* **Docs:** OpenAPI 3.1, Swagger UI, Scalar
* **Protocols:** REST + GraphQL

---
## 🖼️ Architecture Diagram
![FLOWCHART DIAGRAM](http://127.0.0.1:8000/static/download.svg)
---
## 🔐 Authentication

The API uses **OAuth2 Password Bearer Authentication**.

### Obtain Access Token

**Endpoint**

```
POST /auth/token
```

**Request (form-data)**

```json
{
  "username": "user@example.com",
  "password": "strongpassword"
}
```

**Response**

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

➡️ Use the token in headers:

```
Authorization: Bearer <access_token>
```

---

## 🔑 Password Recovery

### Forgot Password

```
POST /auth/forgot-password
```

**Request**

```json
{
  "email": "user@example.com"
}
```

Sends a password reset token to the user’s email.

---

### Reset Password

```
POST /auth/reset-password
```

**Request**

```json
{
  "token": "reset_token",
  "new_password": "newStrongPassword"
}
```

---

## 👤 Users API

### Create User

```
POST /users/
```

🔐 Requires Authentication

**Request**

```json
{
  "email": "user@example.com",
  "password": "password",
  "full_name": "John Doe",
  "role": "user"
}
```

---

### Get All Users

```
GET /users/?skip=0&limit=100
```

---

### Search Users

```
GET /users/search
```

**Query Parameters**

* `q` – search keyword
* `role` – user role
* `is_active` – true / false
* `cursor` – pagination cursor
* `limit` – number of results

---

### Get Current User

```
GET /users/me
```

---

### Get User by ID

```
GET /users/{user_id}
```

---

### Update User

```
PATCH /users/{user_id}
```

**Request**

```json
{
  "full_name": "Updated Name",
  "is_active": true,
  "role": "admin"
}
```

---

### Delete User

```
DELETE /users/{user_id}
```

---

## 📦 Items API

### Create Item

```
POST /items/
```

**Request**

```json
{
  "title": "Laptop",
  "description": "Gaming laptop",
  "price": 1200
}
```

---

### List Items (Pagination)

```
GET /items/?page=1&size=10
```

**Filters**

* `search`
* `min_price`
* `max_price`
* `owner_id`

---

### Fast Search Items (Cursor-based)

```
GET /items/search
```

---

### Get Item by ID

```
GET /items/{item_id}
```

---

### Update Item

```
PATCH /items/{item_id}
```

---

### Delete Item

```
DELETE /items/{item_id}
```

---

## 📁 Files API

### Upload File

```
POST /files/upload
```

**Request**

* `multipart/form-data`
* Field: `file`

**Response**

```json
{
  "id": 1,
  "original_filename": "doc.pdf",
  "stored_filename": "uuid.pdf",
  "file_size": 204800,
  "uploaded_at": "2024-01-01T12:00:00"
}
```

---

### List Uploaded Files

```
GET /files/
```

---

### Search Files

```
GET /files/search
```

**Filters**

* `q`
* `min_size`
* `max_size`
* `uploaded_by`
* `cursor`
* `limit`

---

### Download File

```
GET /files/download?file_id=1
```

or

```
GET /files/download?filename=uuid.pdf
```

---

### Get File Metadata

```
GET /files/{file_id}
```

---

### Delete File

```
DELETE /files/{file_id}
```

---

## ❤️ Health & Monitoring

### Health Check

```
GET /health/
```

Used by load balancers and uptime monitors.

---

### Metrics

```
GET /health/metrics
```

Useful for Prometheus / monitoring tools.

---

## 🔎 GraphQL API

### GraphiQL Playground

```
GET /graphql
```

### GraphQL Queries & Mutations

```
POST /graphql
```

Allows flexible querying alongside REST APIs.

---

## 📚 API Documentation

### Swagger UI

```
/docs
```

### Scalar API Reference

```
/docs/scalar
```

---

## 🔐 Security

* JWT Bearer Authentication
* Role-based access
* Protected routes for users, items, and files

---

## 📄 License

* **License:** Apache 2.0 (MIT identifier included)
* **Author:** Kunal Hedaoo
* **Contact:** [kunalhedaoodevops@gmail.com](mailto:kunalhedaoodevops@gmail.com)

---

## ✅ Conclusion

This FastAPI Starter Template provides a **complete backend foundation** for building secure, scalable applications with minimal setup. It’s ideal for:

* SaaS products
* Admin dashboards
* REST + GraphQL backends
* File-handling applications

Happy building! 🚀
