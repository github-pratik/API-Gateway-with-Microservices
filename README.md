#API Gateway with Microservices

A scalable microservices architecture d
demonstrating an e-commerce backend with API Gateway pattern, featuring user management, product catalog, and order processing.

##Project Structure

```
microservices-demo/
├── docker-compose.yml
├── requirements.txt
├── gateway/
│   ├── Dockerfile
│   └── src/
│       ├── main.py
│       ├── auth.py
│       └── rate_limiter.py
├── services/
│   ├── user_service/
│   ├── order_service/
│   └── product_service/
└── frontend/
    ├── src/
    ├── public/
    └── package.json
```

## Architecture Overview 

## Features

- **API Gateway**
  - Centralized authentication using JWT
  - Rate limiting with Redis
  - Request routing to microservices

- **User Service**
  - User registration and management
  - Profile data storage
  - Authentication endpoints

- **Product Service**
  - Product catalog management
  - Inventory tracking
  - Product search and filtering

- **Order Service**
  - Order processing
  - Order history
  - Basic inventory management

- **Frontend**
  - React-based SPA
  - Bootstrap UI components
  - Responsive design

## Tech Stack

- **Backend**
  - Python 3.9
  - Flask
  - Redis
  - SQLite (Development)
  - PostgreSQL (Production)

- **Frontend**
  - React 18
  - React Router v6
  - Bootstrap 5

- **DevOps**
  - Docker
  - Docker Compose
  - Render.com deployment

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker and Docker Compose
- Redis 

2. Start the services using Docker Compose: 

```bash
docker compose up -d
```

3. Install frontend dependencies: 

```bash
cd frontend
npm install
```

4. Start the frontend development server: 

```bash
npm start
```

5. Access the services:
- Frontend: http://localhost:3000
- API Gateway: http://localhost:5001
- User Service: http://localhost:5002
- Order Service: http://localhost:5003
- Product Service: http://localhost:5004


### API Testing

Get a JWT token:

```bash
curl -X POST http://localhost:5001/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user"}'
```

Create a user:
```bash
curl -X POST http://localhost:5001/users/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "username": "test_user",
    "email": "test@example.com"
  }'
```

## Deployment

The project is configured for deployment on Render.com:

1. Backend services are deployed as Web Services
2. Redis is provided by Render.com
3. Frontend is deployed as a Static Site

## Environment Variables

```env
JWT_SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379
REACT_APP_API_URL=http://localhost:5001
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Academic Purposes Only

## Acknowledgments

- @Flask documentation
- @React documentation
- @Microservices architecture patterns




