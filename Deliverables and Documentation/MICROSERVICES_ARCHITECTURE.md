# TrueSight Microservices Architecture Documentation

## Overview
This document describes the microservices architecture implemented for the TrueSight deepfake detection system, separating the monolithic application into independent, scalable services.

## Architecture Components

### 1. Service Structure
```
microservices/
├── detection/          # Multi-modal deepfake detection service
│   ├── core/          # Core detection engine and models
│   ├── api/           # API endpoints (FastAPI)
│   └── tests/         # Service-specific tests
├── forensic/          # Digital forensic attribution service
│   ├── core/          # Forensic analysis engine
│   ├── api/           # API endpoints
│   └── tests/         # Tests
├── blockchain/        # Blockchain evidence logging service
│   ├── core/          # Blockchain integration
│   ├── api/           # API endpoints
│   └── tests/         # Tests
├── auth/             # Authentication and authorization service
│   ├── core/         # Auth engine and user management
│   ├── api/          # API endpoints
│   └── tests/        # Tests
├── gateway/          # API Gateway for routing
└── service_discovery.py  # Service discovery mechanism
```

### 2. Individual Services

#### Detection Service (Port 8001)
- **Purpose**: Multi-modal deepfake detection (video, audio, image)
- **Components**: 
  - LNCLIP video detector
  - Wav2Vec2 audio detector
  - Multilingual Urdu detector
  - Lip-sync analysis
- **Dependencies**: ML models, database, storage
- **Endpoints**: `/detect`, `/health`, `/models/status`

#### Forensic Service (Port 8002)
- **Purpose**: Digital forensic attribution analysis
- **Components**:
  - PRNU noise analysis
  - GAN classifier
  - Metadata analyzer
- **Dependencies**: Image processing libraries, database
- **Endpoints**: `/analyze`, `/health`, `/modules/status`

#### Blockchain Service (Port 8003)
- **Purpose**: Evidence logging to blockchain
- **Components**:
  - Ethereum smart contract integration
  - Evidence hashing and verification
  - Transaction management
- **Dependencies**: Web3.py, Ethereum node
- **Endpoints**: `/log`, `/verify/{hash}`, `/health`, `/status`

#### Authentication Service (Port 8004)
- **Purpose**: User authentication and authorization
- **Components**:
  - JWT token generation/validation
  - User management
  - API key management
- **Dependencies**: Database, bcrypt, PyJWT
- **Endpoints**: `/login`, `/register`, `/api-keys`, `/health`

#### API Gateway (Port 8000)
- **Purpose**: Central entry point and request routing
- **Features**:
  - Load balancing
  - Authentication proxy
  - Service discovery integration
  - Rate limiting (future)
- **Endpoints**: `/detect`, `/forensics/analyze`, `/blockchain/log`, `/auth/login`, `/health`, `/services`

### 3. Service Discovery

The system implements a centralized service registry:

- **Registry Service**: Tracks all available services
- **Heartbeat Mechanism**: Services periodically report health status
- **Automatic Cleanup**: Removes dead services from registry
- **Service Lookup**: Clients can discover services by name

### 4. Inter-Service Communication

Services communicate securely using:
- **Service Tokens**: Authentication between services
- **HTTP/REST**: Standard RESTful APIs
- **Async Processing**: Non-blocking I/O operations
- **Error Handling**: Graceful failure recovery

### 5. Data Management

#### Shared Database
All services connect to a central PostgreSQL database with:
- SQLAlchemy ORM models
- Alembic migrations
- Connection pooling
- Proper indexing

#### Data Isolation
Each service manages its own data entities while sharing common models:
- Users and authentication data
- Media files and processing metadata
- Detection results and forensic reports
- Blockchain evidence logs

### 6. Containerization

Each service is containerized with:
- **Dockerfiles**: Optimized builds for each service
- **Base Images**: Python 3.10 slim for minimal footprint
- **Health Checks**: Container health monitoring
- **Resource Limits**: CPU and memory constraints

### 7. Orchestration

#### Docker Compose Setup
The `docker-compose.yml` defines:
- Service dependencies and startup order
- Network configuration
- Volume mounts for persistent data
- Health check configurations
- Port mappings

#### Service Dependencies
```
gateway → auth, detection, forensic, blockchain
detection → auth, database
forensic → auth, database
blockchain → auth, database
auth → database
all services → service-registry
```

## Deployment Architecture

### Development Environment
```bash
docker-compose up --build
```

### Production Considerations
- Kubernetes deployment manifests
- Load balancer configuration
- Persistent volume claims
- Secret management
- Monitoring and logging

## Security Features

### Authentication
- JWT tokens for user sessions
- Service-to-service authentication
- API key management
- Role-based access control

### Data Protection
- Database encryption
- Secure file storage
- Transport encryption (HTTPS)
- Input validation and sanitization

## Monitoring and Observability

### Health Checks
- Service-level health endpoints
- Database connectivity checks
- Model loading verification
- Resource utilization monitoring

### Logging
- Structured logging with timestamps
- Service correlation IDs
- Error tracking and reporting
- Performance metrics

## Testing Strategy

### Service-Level Testing
- Unit tests for core logic
- Integration tests for APIs
- Mock external dependencies
- Performance benchmarks

### System Testing
- End-to-end workflow testing
- Service discovery validation
- Load and stress testing
- Failure scenario simulation

## Future Enhancements

### Scalability
- Horizontal pod autoscaling
- Database read replicas
- Caching layers (Redis)
- Message queues for async processing

### Advanced Features
- Circuit breaker pattern
- Distributed tracing
- Advanced load balancing
- Multi-region deployment

## Usage Examples

### Starting the System
```bash
# Build and start all services
docker-compose up --build

# Start specific services
docker-compose up detection-service auth-service
```

### Testing Services
```bash
# Run microservices tests
python microservices_test.py

# Test individual service health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

### Making API Calls
```bash
# Through gateway
curl -X POST http://localhost:8000/detect -F "media_url=https://example.com/video.mp4"

# Direct service calls
curl -X POST http://localhost:8001/detect -F "media_url=https://example.com/video.mp4"
```

This microservices architecture provides a robust, scalable foundation for the TrueSight deepfake detection platform while maintaining the flexibility to evolve and expand individual components independently.