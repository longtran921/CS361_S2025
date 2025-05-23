# **Auth Provider Microservice**

**This microservice** handles user registration and authentication for the Social Scheduling Service. It provides endpoints for signing up and logging in users. It is implemented with Python, Flask, and SQLite.

## Base URL

```
http://localhost:5000
```

## Endpoints

### POST /signup

Register a new user.

**Request**

* Method: `POST`
* URL: `/signup`
* Headers:

  * `Content-Type: application/json`
* Body:

  ```json
  {
    "username": "longtran",
    "email": "long@example.com",
    "password": "mypassword"
  }
  ```

**Example**

```bash
curl -X POST http://localhost:5000/signup \
     -H "Content-Type: application/json" \
     -d '{"username":"longtran","email":"long@example.com","password":"mypassword"}'
```

**Responses**

* `201 Created`

  ```json
  { "message": "User registered successfully" }
  ```
* `409 Conflict`

  ```json
  { "error": "Username or email already exists" }
  ```

### POST /login

Authenticate an existing user.

**Request**

* Method: `POST`
* URL: `/login`
* Headers:

  * `Content-Type: application/json`
* Body:

  ```json
  {
    "email": "long@example.com",
    "password": "mypassword"
  }
  ```

**Example**

```bash
curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"email":"long@example.com","password":"mypassword"}'
```

**Responses**

* `200 OK`

  ```json
  { "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." }
  ```
* `401 Unauthorized`

  ```json
  { "error": "Invalid credentials" }
  ```

## How to Receive Data

All responses are in JSON format. Consume the response body directly; no additional wrapping or XML.

## Notes

* Use `application/json` for all requests.
* Store and attach the JWT token returned by `/login` for authenticated requests to other microservices.
* No sessions are maintained on the server; the service is stateless.
