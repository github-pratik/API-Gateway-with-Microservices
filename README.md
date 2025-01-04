# Microservices API Gateway Project

## Problem Statement
In modern web applications, managing multiple services, handling authentication, rate limiting, and monitoring can become complex. This project implements an API Gateway pattern to solve these challenges by providing a single entry point for multiple microservices.

## Project Overview
This project implements a microservices architecture with an API Gateway that handles:
- Authentication and Authorization
- Rate Limiting
- Service Discovery
- Request Routing
- Monitoring and Telemetry

### Architecture
```
├── gateway/                  # API Gateway Service
│   ├── src/
│   │   ├── main.py          # Main gateway application
│   │   ├── auth.py          # Authentication handling
│   │   ├── rate_limiter.py  # Rate limiting implementation
│   │   └── telemetry.py     # Service monitoring
│   ├── requirements.txt
│   └── Dockerfile
├── services/
│   ├── user_service/        # User Management Service
│   ├── order_service/       # Order Management Service
│   └── product_service/     # Product Management Service
├── docker-compose.yml       # Service orchestration
└── .env                     # Environment configuration
```

<img src = "https://github.com/github-pratik/API-Gateway-with-Microservices/blob/main/images/archit_micro.png" alt="Architecture Diagram" width="70%"/>

<img src = "https://github.com/github-pratik/API-Gateway-with-Microservices/blob/main/images/flow_micro.png" alt="Flow Diagram" width="70%"/>



## Key Features
1. **API Gateway**
   - Central entry point for all client requests
   - Request routing to appropriate services
   - Authentication and authorization
   - Rate limiting to prevent abuse

2. **Microservices**
   - User Service: Handles user registration and authentication
   - Order Service: Manages order creation and tracking
   - Product Service: Handles product inventory and details

3. **Monitoring**
   - Request tracking
   - Service health checks
   - Performance metrics

## Technologies Used
- Python/Flask for microservices
- Redis for rate limiting and caching
- Docker for containerization
- JWT for authentication
- Environment variables for configuration

## Learning Outcomes
1. **Microservices Architecture**
   - Service decomposition
   - Inter-service communication
   - Service discovery

2. **API Gateway Pattern**
   - Request routing
   - Rate limiting implementation
   - Authentication middleware

3. **Docker & Containerization**
   - Multi-container applications
   - Service orchestration
   - Environment configuration

4. **Security**
   - JWT authentication
   - Rate limiting
   - Environment variable management

5. **Monitoring & Telemetry**
   - Health checks
   - Request tracking
   - Performance monitoring

## Setup and Installation
1. Clone the repository
```bash
git clone <repository-url>
```

2. Create .env file
```bash
cp .env.example .env
```

3. Build and run with Docker Compose
```bash
docker-compose up --build
```

## API Documentation
### User Service
```
POST /users/register
POST /users/login
GET /users/profile
```

### Product Service
```
GET /products
POST /products
GET /products/{id}
```

### Order Service
```
GET /orders
POST /orders
GET /orders/{id}
```

## Testing
Use Postman or curl to test the endpoints:

```bash
# Health Check
curl http://localhost:5001/health

# Register User
curl -X POST http://localhost:5001/users/register \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "password": "password123"
}'
```

## Future Improvements
1. Add service discovery
2. Implement circuit breakers
3. Add logging aggregation
4. Implement caching
5. Add API documentation with Swagger

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request




