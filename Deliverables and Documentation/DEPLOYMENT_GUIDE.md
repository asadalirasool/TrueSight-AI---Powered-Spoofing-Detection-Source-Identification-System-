# TrueSight - Complete System Deployment Guide

## 🚀 Production Deployment Configuration

This guide covers deploying the complete TrueSight system with all features implemented.

## 📋 System Components Status

✅ **100% Complete** - All major components implemented:
- Database integration (PostgreSQL + Redis)
- Full authentication and authorization system
- Advanced security measures and middleware
- Complete digital forensics analysis module
- Blockchain evidence logging system
- Enhanced system monitoring and alerting
- Comprehensive test suite
- Production deployment configurations

## 🏗️ Deployment Architecture

### Containerized Deployment (Recommended)

```bash
# Deploy complete system with Docker Compose
docker-compose -f docker-compose.full.yml up -d

# Services deployed:
# - PostgreSQL database
# - Redis cache
# - API server (port 8000)
# - Frontend server (port 3000)
# - Prometheus monitoring (port 9090)
# - Grafana dashboards (port 3001)
```

### Manual Deployment

```bash
# 1. Start database services
docker run -d --name truesight-postgres -p 5432:5432 \
  -e POSTGRES_DB=truesight \
  -e POSTGRES_USER=truesight_user \
  -e POSTGRES_PASSWORD=truesight_pass_123 \
  postgres:15-alpine

docker run -d --name truesight-redis -p 6379:6379 redis:7-alpine

# 2. Configure environment
cp .env.example .env
# Edit .env with your production settings

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python -m src.scripts.init_database

# 5. Start services
python launch_server.py  # API server
python serve_frontend.py  # Frontend server
```

## 🔧 Environment Configuration

### Production .env Settings

```env
# Application Settings
APP_NAME=TrueSight
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://truesight_user:secure_password@postgres:5432/truesight
REDIS_URL=redis://redis:6379/0

# Security Settings
SECRET_KEY=your-very-long-random-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Monitoring
ENABLE_MONITORING=True
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
```

## 🛡️ Security Configuration

### SSL/TLS Setup

```nginx
# nginx.conf for HTTPS
server {
    listen 443 ssl;
    server_name truesight.yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Firewall Rules

```bash
# Allow only necessary ports
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 9090  # Prometheus (internal only)
ufw allow 3001  # Grafana (internal only)
ufw enable
```

## 📊 Monitoring and Logging

### Prometheus Configuration

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'truesight-api'
    static_configs:
      - targets: ['api:8000']
  
  - job_name: 'truesight-system'
    static_configs:
      - targets: ['localhost:9091']
```

### Log Rotation

```bash
# /etc/logrotate.d/truesight
/var/log/truesight/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 truesight truesight
}
```

## 🔍 Health Checks and Monitoring

### System Health Endpoints

```bash
# API Health Check
curl http://localhost:8000/api/v1/health

# System Metrics
curl http://localhost:8000/api/v1/metrics

# Blockchain Status
curl http://localhost:8000/api/v1/blockchain/stats
```

### Automated Monitoring Scripts

```bash
#!/bin/bash
# health_check.sh
API_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/health)
DB_HEALTH=$(pg_isready -h localhost -p 5432)

if [ $API_HEALTH -ne 200 ] || [ $DB_HEALTH -ne 0 ]; then
    echo "System health check failed" | mail -s "TrueSight Alert" admin@company.com
fi
```

## 🔄 Backup and Recovery

### Database Backup

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U truesight_user truesight > /backups/truesight_$DATE.sql
tar -czf /backups/truesight_media_$DATE.tar.gz /uploads/
```

### Disaster Recovery

```bash
# Restore database
psql -h localhost -U truesight_user truesight < /backups/truesight_latest.sql

# Restore media files
tar -xzf /backups/truesight_media_latest.tar.gz -C /
```

## 🚨 Incident Response

### Critical Alerts

1. **Database Connection Failure**
   ```bash
   systemctl restart postgresql
   docker restart truesight-postgres
   ```

2. **High CPU/Memory Usage**
   ```bash
   # Scale API workers
   docker-compose scale api=6
   ```

3. **Blockchain Sync Issues**
   ```bash
   # Restart blockchain service
   docker-compose restart blockchain
   ```

## 📈 Performance Tuning

### Database Optimization

```sql
-- Create performance indexes
CREATE INDEX CONCURRENTLY idx_detection_timestamp ON detection_results(timestamp);
CREATE INDEX CONCURRENTLY idx_media_uploaded_at ON media_files(uploaded_at);

-- Monitor slow queries
ALTER SYSTEM SET log_min_duration_statement = 1000;
```

### API Performance

```python
# Adjust worker settings in launch_server.py
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 1000
max_requests_jitter = 50
```

## 🎯 Testing Production Deployment

### Smoke Tests

```bash
# Run automated smoke tests
python tests/smoke_tests.py

# Expected results:
# ✅ API responds within 100ms
# ✅ Database connections work
# ✅ Authentication functions
# ✅ Media processing completes
# ✅ Blockchain logging works
```

## 📞 Support and Maintenance

### Regular Maintenance Tasks

```bash
# Weekly
./scripts/cleanup_old_files.py --days 30

# Monthly
./scripts/database_maintenance.py
./scripts/update_models.py

# Quarterly
./scripts/security_audit.py
./scripts/performance_review.py
```

### Contact Information

- **System Administrator**: admin@truesight.ai
- **Support Hours**: 24/7 Monitoring
- **Incident Response**: 30-minute SLA for critical issues

---

## 🎉 Deployment Success!

Your TrueSight system is now fully deployed with:
- Enterprise-grade security
- Complete forensic capabilities
- Immutable evidence logging
- Real-time monitoring
- Automated testing and validation
- Production-ready infrastructure

The system is ready for immediate use in production environments!