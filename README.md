# auth-service
A scalable and modular authentication microservice built with Python. Features include user registration, login, JWT-based authentication, password hashing, and token refresh. Designed for easy integration and extensibility in modern web applications.

## Features
- User registration and login
- JWT-based authentication
- Password hashing with bcrypt
- Token refresh mechanism
- PostgreSQL database support
- Docker support for easy deployment
- Health checks for container orchestration
- Environment-based configuration
- Message queue integration for microservice communication

## Prerequisites
- Python 3.11+
- PostgreSQL database
- RabbitMQ message broker
- Docker (for containerized deployment)
- Docker Compose (for multi-container setups)

## Installation

### Local Development
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and configure your environment variables
5. Run database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t auth-service .
   ```

2. Use Docker Compose for development (includes PostgreSQL and RabbitMQ):
   ```bash
   docker compose up -d
   ```

3. Run database migrations:
   ```bash
   docker compose exec auth-service alembic upgrade head
   ```

## Environment Variables
- `APP_NAME`: Application name (default: "Auth Service")
- `APP_VERSION`: Application version (default: "1.0.0")
- `DEBUG`: Debug mode (default: False)
- `SECRET_KEY`: Secret key for JWT signing (required). **Note:** For production, use a strong, randomly generated secret key. You can generate one using: `openssl rand -hex 32`
- `DATABASE_URL`: Database connection URL (required)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time in minutes (default: 1440)
- `REFRESH_TOKEN_EXPIRE_MINUTES`: Refresh token expiration time in minutes (default: 43200)
- `ALGORITHM`: JWT algorithm (default: "HS256")
- `RABBITMQ_URL`: RabbitMQ connection URL (default: "amqp://guest:guest@localhost/")

## API Endpoints
- `POST /auth/signup`: User registration
- `POST /auth/login`: User login
- `POST /auth/refresh`: Refresh access token
- `POST /auth/logout`: User logout
- `GET /auth/me`: Get current user information
- `GET /`: Health check

## Message Queue Integration
The auth-service now publishes "UserCreated" events to a RabbitMQ message queue when a new user is created. This allows other microservices (like user-service) to react to new user registrations without shared databases.

When a user signs up:
1. The user is created in the auth-service database
2. A "UserCreated" event is published to the message queue
3. Other services can subscribe to this queue and react to new user registrations

## Testing
Run tests with:
```bash
python -m pytest tests/ -v
```

## Production Deployment

### Docker Deployment
For production deployment with Docker, you can use the provided docker-compose.yml as a starting point:

```bash
# Build and start the services
docker compose up -d

# Run database migrations
docker compose exec auth-service alembic upgrade head
```

### Kubernetes Deployment
For Kubernetes deployment, you would need to:
1. Create Kubernetes manifests for the service, database, and message broker
2. Use Kubernetes secrets for sensitive environment variables
3. Configure proper resource limits and health checks
4. Set up ingress for external access

### Environment Configuration
For production deployment, make sure to:
1. Set `DEBUG=False`
2. Use a strong, randomly generated `SECRET_KEY`
3. Configure a production database with proper credentials
4. Use HTTPS in production (configure TLS termination at the load balancer or ingress)
5. Set appropriate token expiration times
6. Use proper logging configuration
7. Implement proper monitoring and alerting
8. Regularly update dependencies and base images

### Security Considerations
1. Never commit secrets to version control
2. Use environment variables or secret management systems for sensitive data
3. Implement proper input validation and sanitization
4. Use HTTPS for all communications
5. Regularly rotate secrets and keys
6. Implement rate limiting to prevent abuse
7. Keep dependencies up to date
8. Regularly audit logs for suspicious activity

## Health Checks
The service includes health checks for container orchestration:
- Liveness probe: Checks if the service is responsive
- Readiness probe: Checks if the service is ready to handle requests

## Database Migrations
The service uses Alembic for database migrations:
- Create new migrations: `alembic revision --autogenerate -m "Description"`
- Apply migrations: `alembic upgrade head`
- Rollback migrations: `alembic downgrade -1`