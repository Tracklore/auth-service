# Auth-Service Message Queue Implementation

## Summary of Changes

### New Features Added
1. **Message Queue Integration**: Implemented RabbitMQ integration for publishing "UserCreated" events
2. **Event-Driven Architecture**: Auth-service now publishes events when users are created, allowing other services to react
3. **Improved Microservice Communication**: Replaced shared database approach with message-based communication

### Files Modified/Added

#### New Files
1. `app/services/message_queue.py` - Message queue client implementation
2. Updated `requirements.txt` - Added `aiormq` dependency for RabbitMQ integration

#### Modified Files
1. `app/core/settings.py` - Added RabbitMQ URL configuration
2. `app/services/auth.py` - Added event publishing to signup function
3. `app/main.py` - Added startup/shutdown event handlers for message queue
4. `.env` - Added RabbitMQ URL configuration
5. `.env.example` - Added RabbitMQ URL example
6. `docker-compose.yml` - Added RabbitMQ service
7. `README.md` - Documented new message queue functionality

### Implementation Details

#### Message Queue Client
- Uses `aiormq` library for RabbitMQ integration
- Implements connection management with automatic reconnection
- Publishes "UserCreated" events with user data (ID, username, email)
- Gracefully handles message queue unavailability without blocking user creation

#### Event Structure
```json
{
  "event_type": "UserCreated",
  "user_id": 123,
  "username": "johndoe",
  "email": "john@example.com",
  "timestamp": 1234567890.123
}
```

#### Flow
1. User signs up through `/auth/signup` endpoint
2. User is created in auth-service database
3. "UserCreated" event is published to RabbitMQ
4. User-service (or other services) can subscribe to this event and create their own records

### Benefits
1. **Decoupled Services**: Services no longer need shared databases
2. **Scalability**: Services can scale independently
3. **Reliability**: Message queue provides buffering if services are temporarily unavailable
4. **Extensibility**: Easy to add more event types or subscribers
5. **Maintainability**: Clear separation of concerns between services

### Docker Configuration
- Added RabbitMQ service to docker-compose.yml
- Configured health checks for all services
- Updated environment variables to use service names for networking

### Environment Variables
- `RABBITMQ_URL`: Configures connection to RabbitMQ (default: amqp://guest:guest@rabbitmq:5672/)

## Testing
The message queue integration has been designed to not block user creation if the message queue is unavailable, ensuring the auth-service remains functional even if other services are down.