# 🚗 ULEZ Compliance Checker

A lightning-fast, production-ready web application for checking vehicle compliance with emission zone regulations (ULEZ, CAZ, etc.). Built with FastAPI and optimized for performance with direct API integration.

![ULEZ Checker](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Performance](https://img.shields.io/badge/Response%20Time-<0.5s-brightgreen)

## ✨ Features

- **⚡ Lightning Fast**: Sub-second response times (avg. 0.46s)
- **🎯 Accurate Data**: Real vehicle information from official sources
- **🔄 Smart Caching**: 1-hour TTL for optimal performance
- **🛡️ Robust Fallback**: UK registration pattern heuristics when API unavailable
- **📱 Modern UI**: Responsive web interface with real-time results
- **🐳 Docker Ready**: Production-ready containerization
- **📊 Monitoring**: Built-in health checks and statistics
- **🔒 Secure**: Non-root container, minimal attack surface

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/jamier2007/ulez-checker.git
cd ulez-checker

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:5005
```

### Manual Installation

```bash
# Clone and setup
git clone https://github.com/jamier2007/ulez-checker.git
cd ulez-checker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
cd app && python main.py
```

## 📖 API Documentation

### Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Web interface | HTML |
| `/api/{registration}` | GET | JSON API | JSON |
| `/health` | GET | Health check | JSON |
| `/stats` | GET | Cache statistics | JSON |

### Example API Usage

```bash
# Check vehicle compliance
curl "http://localhost:5005/api/WO15CZY"

# Response
{
  "registration": "WO15CZY",
  "compliant": false,
  "make_model": "BMW 330D xDrive M Sport Auto",
  "year": 2015,
  "engine_category": "6b",
  "co2_emissions": 142,
  "charge": 12.5,
  "message": "Vehicle is not compliant with ULEZ standards"
}
```

## 🏗️ Architecture

### Performance Optimizations

1. **Direct API Integration**: Bypasses browser automation for 100x speed improvement
2. **Intelligent Caching**: Redis-ready with in-memory fallback
3. **Smart Fallback**: UK registration pattern analysis when API unavailable
4. **Lightweight Container**: ~200MB vs 2GB+ for browser-based solutions

### Technology Stack

- **Backend**: FastAPI (Python 3.11)
- **HTTP Client**: aiohttp for async requests
- **Containerization**: Docker with multi-stage builds
- **Frontend**: Vanilla JavaScript with modern CSS
- **Caching**: In-memory with Redis support

## 🐳 Docker Deployment

### Production Deployment

```bash
# Build production image
docker build -t ulez-checker:latest .

# Run with custom configuration
docker run -d \
  --name ulez-checker \
  -p 5005:5005 \
  -e PORT=5005 \
  --restart unless-stopped \
  ulez-checker:latest
```

### Docker Compose (Recommended)

```yaml
version: '3.8'
services:
  ulez-checker:
    image: ulez-checker:latest
    ports:
      - "5005:5005"
    environment:
      - PORT=5005
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5005/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 📊 Performance Metrics

| Metric | Before (Browser) | After (Direct API) | Improvement |
|--------|------------------|-------------------|-------------|
| Response Time | ~60+ seconds | **0.46 seconds** | **130x faster** |
| Build Time | ~2+ minutes | **12.8 seconds** | **9x faster** |
| Image Size | ~2GB+ | **~200MB** | **10x smaller** |
| Memory Usage | ~1GB+ | **~50MB** | **20x less** |
| Throughput | ~1 req/min | **107 req/min** | **100x more** |

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5005` | Application port |
| `PYTHONPATH` | `/app` | Python module path |
| `CACHE_TTL` | `3600` | Cache TTL in seconds |

### Customization

```python
# app/config.py
CACHE_TTL = 3600  # 1 hour
API_TIMEOUT = 15  # 15 seconds
MAX_RETRIES = 3
```

## 🧪 Testing

```bash
# Run performance tests
python test_performance.py

# Test specific registration
curl "http://localhost:5005/api/AB12CDE"

# Check health and stats
curl "http://localhost:5005/health"
curl "http://localhost:5005/stats"
```

## 📈 Monitoring

### Health Checks

- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

### Statistics

- **Cache hit rate**: Available at `/stats`
- **Response times**: Logged automatically
- **Error rates**: Monitored via health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Motorway.co.uk** for the vehicle data API
- **FastAPI** for the excellent web framework
- **Docker** for containerization support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/jamier2007/ulez-checker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jamier2007/ulez-checker/discussions)

---

**⚡ Built for speed, designed for scale, optimized for production.**
