# Auth Service Documentation

## Overview

The Auth Service is a scalable and modular microservice built with Python using the FastAPI framework. It provides core authentication functionalities for web applications, including user registration, login, JWT-based authentication, password hashing, and token refresh.

## Features

- User Registration (Signup)
- User Login
- JWT-based Authentication
- Password Hashing (using bcrypt)
- Access and Refresh Token Management
- User Information Retrieval
- Logout (client-side)

## API Endpoints

### Authentication

All authentication endpoints are prefixed with `/auth`.

#### `POST /auth/signup`

Registers a new user.

- **Request Body**:
  - `username` (string, required): The desired username.
  - `email` (string, required): The user's email address.
  - `password` (string, required): The user's password.

- **Response**:
  - `id` (integer): The unique identifier for the user.
  - `username` (string): The username of the created user.
  - `email` (string): The email of the created user.
  - `is_active` (boolean): Indicates if the user account is active.

- **Errors**:
  - `400 Bad Request`: If the username or email is already registered.

#### `POST /auth/login`

Authenticates a user and provides JWT tokens.

- **Request Body**:
  - `username` (string, required): The user's username.
  - `password` (string, required): The user's password.

- **Response**:
  - `access_token` (string): The JWT access token for API requests.
  - `refresh_token` (string): The JWT refresh token to obtain a new access token.
  - `token_type` (string): The type of token, usually "bearer".

- **Errors**:
  - `401 Unauthorized`: If the credentials are incorrect.

#### `POST /auth/refresh`

Refreshes an expired access token using a refresh token.

- **Request Body**:
  - `refresh_token` (string, required): A valid refresh token.

- **Response**:
  - `access_token` (string): The new JWT access token.
  - `refresh_token` (string): The (currently unchanged) refresh token.
  - `token_type` (string): The type of token, usually "bearer".

- **Errors**:
  - `401 Unauthorized`: If the refresh token is invalid.

#### `POST /auth/logout`

Logs out a user (client-side operation).

- **Response**:
  - `message` (string): Confirmation message "Logout successful".

#### `GET /auth/me`

Retrieves information about the currently authenticated user.

- **Authentication**: Requires a valid access token in the `Authorization` header (e.g., `Bearer <access_token>`).

- **Response**:
  - `id` (integer): The user's unique identifier.
  - `username` (string): The user's username.
  - `email` (string): The user's email.
  - `is_active` (boolean): Indicates if the user account is active.

## Data Models (Schemas)

### User

- `id` (integer): Unique identifier.
- `username` (string): Unique username.
- `email` (string): Unique email address.
- `is_active` (boolean): Account status.

### Token

- `access_token` (string): JWT access token.
- `refresh_token` (string): JWT refresh token.
- `token_type` (string): Type of token (e.g., "bearer").

## Security

- Passwords are securely hashed using bcrypt.
- Authentication is managed via JSON Web Tokens (JWT).
- Access tokens have a short lifespan (default 24 hours).
- Refresh tokens have a longer lifespan (default 30 days) and are used to obtain new access tokens without re-authentication.

## Configuration

The service is configured using environment variables, typically loaded from a `.env` file. Key settings include:

- `SECRET_KEY`: A secret key for JWT signing.
- `DATABASE_URL`: The URL for the database connection.
- `DEBUG`: Enables or disables debug mode.

## Project Structure

The project follows a modular structure:

- `app/`: Contains the main application code.
  - `api/`: Defines API routes.
  - `core/`: Core application logic (settings).
  - `crud/`: Database operations (Create, Read, Update, Delete).
  - `db/`: Database connection and session management.
  - `models/`: Database models (ORM).
  - `schemas/`: Pydantic models for data validation.
  - `services/`: Business logic for authentication.
  - `utils/`: Utility functions (security, password hashing, JWT).
  - `main.py`: Entry point of the application.
- `tests/`: Contains test cases.
- `requirements.txt`: Lists project dependencies.
- `Dockerfile`: Instructions for containerizing the application.
- `alembic/`: Database migration scripts.