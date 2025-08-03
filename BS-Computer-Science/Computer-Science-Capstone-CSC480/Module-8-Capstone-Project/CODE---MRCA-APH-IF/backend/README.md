# MRCA Backend - Advanced Parallel Hybrid  - Intelligent Fusion (APH-IF) API

[![Backend: FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=flat&logo=neo4j&logoColor=white)](https://neo4j.com/)

**Advanced Parallel HybridRAG API for Mining Regulatory Compliance Assistant**

**FastAPI-based backend implementing novel Advanced Parallel HybridRAG - Intelligent Fusion technology 
with simultaneous VectorRAG and GraphRAG execution for enhanced mining regulatory compliance assistance.**

For more project documentation see the `Documents` folder.

---

© 2025 Alexander Samuel Ricciardi - MRCA Frontend Module  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF) System 

---

Author: Alexander Ricciardi  
Date: 07/25/2025

This project was part of my capstone project at CSU Global.

---

MRCA Website: https://mrca-frontend.onrender.com/  

⚠️ This project has limited funds (I am a student). Once the monthly LLM usage fund limit is reached, the application will stop providing responses and will display an error message.  
Please contact me (a.omegapy@gmail.com) if this happend and you still want to try the application.

---

## **What is MRCA Backend?**

The MRCA Backend is a high-performance FastAPI application that implements the core Advanced Parallel HybridRAG technology. It serves as the central orchestration layer for mining regulatory compliance queries, coordinating parallel VectorRAG and GraphRAG retrieval, intelligent context fusion, and specialized template-based response generation.

### **Core Innovation: Advanced Parallel Hybrid**

Unlike traditional RAG systems that use sequential processing, MRCA Backend implements **true parallelism**:

- **Traditional RAG**: `if condition: vector_search() else: graph_search()`
- **MRCA Innovation**: `asyncio.gather(vector_task, graph_task)` - **concurrent execution**

This approach combines:
- **VectorRAG**: Semantic similarity search using 768-dimensional Gemini embeddings
- **GraphRAG**: Knowledge graph traversal with automated Cypher generation
- **Context Fusion**: Intelligent combination using 4 research-based fusion strategies
- **Hybrid Templates**: 5 specialized response templates for different use cases

---

## **Architecture**

```
┌────────────────────────────────────────────────────────────────────┐
│  MRCA Backend Architecture (FastAPI + Advanced Parallel Hybrid)    │
│                                                                    │
│  ┌─────────────────┐    HTTP/REST     ┌──────────────────────┐     │
│  │   Frontend      │ ◄──────────────► │   FastAPI Server     │     │
│  │   (Port 8501)   │                  │   main.py (8000)     │     │
│  └─────────────────┘                  └──────────────────────┘     │
│                                              │                     │
│                                              ▼                     │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │  Advanced Parallel Hybrid Processing Pipeline            │      │
│  │                                                          │      │
│  │  Step 1: Parallel Retrieval (parallel_hybrid.py)         │      │
│  │  ┌─────────────────┐    ┌─────────────────────────┐      │      │
│  │  │   VectorRAG     │    │      GraphRAG           │      │      │
│  │  │  (tools/vector) │    │   (tools/cypher)        │      │      │
│  │  │ async execution │    │   async execution       │      │      │
│  │  └─────────────────┘    └─────────────────────────┘      │      │
│  │                                                          │      │
│  │  Step 2: Context Fusion (context_fusion.py)              │      │
│  │  ┌──────────────────────────────────────────────────┐    │      │
│  │  │  4 Fusion Strategies + Quality Analysis          │    │      │
│  │  │  • Advanced Hybrid  • Weighted Linear            │    │      │
│  │  │  • Max Confidence   • Adaptive Fusion            │    │      │
│  │  └──────────────────────────────────────────────────┘    │      │
│  │                                                          │      │
│  │  Step 3: Template Generation (hybrid_templates.py)       │      │
│  │  ┌──────────────────────────────────────────────────┐    │      │
│  │  │  5 Template Types + Response Generation          │    │      │
│  │  │  • Regulatory Compliance  • Research Based       │    │      │
│  │  │  • Basic Hybrid          • Comparative Analysis  │    │      │
│  │  │  • Confidence Weighted                           │    │      │
│  │  └──────────────────────────────────────────────────┘    │      │
│  └──────────────────────────────────────────────────────────┘      │
│                                              │                     │
│                                              ▼                     │
│                                     ┌─────────────────┐            │
│                                     │   Neo4j Aura    │            │
│                                     │   Cloud Database│            │
│                                     │  26,429+ nodes  │            │
│                                     └─────────────────┘            │
└────────────────────────────────────────────────────────────────────┘
```

---

## **Key Components**

### **Core API Module**

#### **`main.py`**  
Central FastAPI orchestration layer:
- **API Endpoints**: RESTful endpoints for frontend communication
- **Request/Response Models**: Pydantic models for data validation
- **Health Monitoring**: Comprehensive health check system
- **Session Management**: User session tracking and analytics
- **Error Handling**: Graceful error recovery and reporting

**Key Endpoints:**
```python
POST /generate_parallel_hybrid    # Primary AI processing endpoint
GET  /health                     # Basic health check
GET  /parallel_hybrid/health     # Advanced system health
GET  /                          # Service information
```

### **Advanced Parallel Hybrid Engine**

#### **`parallel_hybrid.py`**  
Core parallel processing implementation:
- **Async Coordination**: Manages simultaneous VectorRAG and GraphRAG execution
- **Performance Monitoring**: Real-time metrics collection and analysis
- **Quality Assessment**: Automated evaluation of retrieval quality
- **Error Recovery**: Circuit breaker patterns for fault tolerance

**Key Functions:**
```python
async def get_parallel_retrieval(query, session_id)
async def execute_parallel_search(vector_task, graph_task)
async def monitor_performance(start_time, components)
```

#### **`context_fusion.py`**   
Intelligent context fusion implementation:
- **4 Fusion Strategies**: Research-based algorithms for combining results
- **Quality Analysis**: Automated assessment of fusion effectiveness
- **Complementarity Detection**: Analysis of how sources complement each other
- **Confidence Scoring**: Advanced confidence calculation algorithms

**Fusion Strategies:**
```python
class FusionStrategy(Enum):
    ADVANCED_HYBRID = "advanced_hybrid"      # Research-based (recommended)
    WEIGHTED_LINEAR = "weighted_linear"      # Confidence-based linear
    MAX_CONFIDENCE = "max_confidence"        # Highest confidence selection
    ADAPTIVE_FUSION = "adaptive_fusion"      # Dynamic strategy selection
```

#### **`hybrid_templates.py`**   
Specialized response template system:
- **5 Template Types**: Different response formats for various use cases
- **Dynamic Generation**: AI-powered template selection and customization
- **Quality Control**: Template-specific quality assessment
- **Regulatory Focus**: MSHA compliance-oriented response formatting

**Template Types:**
```python
class TemplateType(Enum):
    REGULATORY_COMPLIANCE = "regulatory_compliance"  # Enhanced compliance
    RESEARCH_BASED = "research_based"               # Academic methodology
    BASIC_HYBRID = "basic_hybrid"                   # Simple combination
    COMPARATIVE_ANALYSIS = "comparative_analysis"   # Source comparison
    CONFIDENCE_WEIGHTED = "confidence_weighted"     # Quality-adjusted
```

### **Infrastructure Components**

#### **`config.py`**   
Comprehensive configuration management:
- **Environment Variables**: Secure configuration loading
- **API Key Management**: OpenAI, Gemini, Neo4j credential handling
- **Settings Validation**: Pydantic-based configuration validation
- **Secrets Integration**: Automatic `.streamlit/secrets.toml` loading

#### **`database.py`**   
Neo4j database integration:
- **Connection Management**: Robust database connection handling
- **Vector Search**: High-performance vector similarity search
- **Graph Queries**: Cypher query execution and optimization
- **Health Monitoring**: Database connectivity and performance monitoring

#### **`llm.py`**   
LLM integration and management:
- **Multi-Provider Support**: OpenAI GPT-4o + Google Gemini integration
- **Prompt Engineering**: Optimized prompts for regulatory compliance
- **Rate Limiting**: API quota management and throttling
- **Error Handling**: Graceful LLM service failure recovery

#### **`circuit_breaker.py`**   
Advanced fault tolerance system:
- **Circuit Breaker Pattern**: Prevents cascading failures
- **Health Monitoring**: Component-level health tracking
- **Automatic Recovery**: Self-healing system capabilities
- **Performance Tracking**: Real-time performance metrics

#### **`utils.py`** (227 lines)
Utility functions and helpers:
- **Text Processing**: Document chunking and preprocessing
- **Validation**: Input validation and sanitization
- **Logging**: Structured logging and error reporting
- **Performance**: Caching and optimization utilities

### **Agent Tools Package**

#### **`tools/`** Directory
Specialized tools for knowledge graph querying:

**`tools/vector.py`**   
- **VectorRAG Implementation**: Semantic similarity search
- **Embedding Generation**: Google Gemini embedding integration
- **Performance Optimization**: Efficient vector operations
- **Quality Assessment**: Relevance scoring and filtering

**`tools/cypher.py`**   
- **GraphRAG Implementation**: Knowledge graph traversal
- **Cypher Generation**: Automated query generation from natural language
- **Relationship Analysis**: Entity relationship exploration
- **Performance Monitoring**: Query optimization and caching

**`tools/general.py`**   
- **General Query Processing**: Fallback query handling
- **Multi-Source Integration**: Combines multiple data sources
- **Quality Control**: Response validation and enhancement
- **Error Recovery**: Graceful degradation for edge cases

### **Production Components**

#### **`Dockerfile.backend`**   
Production-ready containerization:
- **Multi-stage Build**: Optimized for production deployment
- **Security**: Non-root user execution and security hardening
- **Health Checks**: Container-level health monitoring
- **Performance**: Optimized for high-throughput processing

#### **`requirements.txt`**   
Comprehensive dependency management:
```txt
fastapi>=0.104.0           # Core API framework
uvicorn>=0.24.0           # ASGI server
neo4j>=5.15.0             # Graph database driver
openai>=1.3.0             # OpenAI API integration
google-generativeai       # Google Gemini integration
langchain>=0.0.350        # LLM orchestration
pydantic>=2.5.0           # Data validation
asyncio                   # Async programming
```

---

## **API Documentation**

### **Core Endpoints**

#### **POST /generate_parallel_hybrid**
Primary endpoint for Advanced Parallel Hybrid processing:

**Request Model:**
```python
class ParallelHybridRequest(BaseModel):
    user_input: str                    # REQUIRED: Natural language query
    session_id: Optional[str] = None   # OPTIONAL: Session identifier  
    fusion_strategy: Optional[str] = "advanced_hybrid"  # Fusion algorithm
    template_type: Optional[str] = "regulatory_compliance"  # Response template
```

**Response Model:**
```python
class ParallelHybridResponse(BaseModel):
    response: str                      # Generated AI response
    processing_time: float             # Total processing time (seconds)
    session_id: str                   # Session identifier
    metadata: Dict[str, Any]          # Detailed processing metadata
```

**Usage Example:**
```bash
curl -X POST http://localhost:8000/generate_parallel_hybrid \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "What safety equipment is required for underground coal mining?",
    "fusion_strategy": "advanced_hybrid",
    "template_type": "regulatory_compliance"
  }'
```

#### **GET /health**
Basic health check endpoint:
```python
{
  "status": "healthy",
  "timestamp": "2025-01-XX 12:00:00 UTC",
  "uptime_seconds": 3600,
  "version": "2.0.0"
}
```

#### **GET /parallel_hybrid/health**
Comprehensive system health check:
```python
{
  "status": "healthy",
  "parallel_hybrid_ready": true,
  "components": {
    "database": {"status": "healthy", "response_time": 0.05},
    "vector_search": {"status": "healthy", "index_size": 5575},
    "graph_queries": {"status": "healthy", "node_count": 26429},
    "llm_services": {"status": "healthy", "providers": ["openai", "gemini"]},
    "fusion_engine": {"status": "healthy", "strategies": 4}
  },
  "performance": {
    "avg_response_time": 35.2,
    "success_rate": 0.98,
    "error_rate": 0.02
  }
}
```

---

## **Configuration**

### **Environment Variables**

#### **Required Configuration**
```bash
# Core API Keys
OPENAI_API_KEY=sk-your-openai-key
GEMINI_API_KEY=your-gemini-key

# Neo4j Database
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io  
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# Optional Settings
MRCA_DEBUG=false
FUSION_DEFAULT_STRATEGY=advanced_hybrid
TEMPLATE_DEFAULT_TYPE=regulatory_compliance
```

#### **Advanced Configuration**
```bash
# Performance Tuning
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT_SECONDS=300
VECTOR_SEARCH_LIMIT=20
GRAPH_TRAVERSAL_DEPTH=3

# Circuit Breaker Settings
CIRCUIT_BREAKER_FAILURE_THRESHOLD=5
CIRCUIT_BREAKER_RECOVERY_TIMEOUT=60
CIRCUIT_BREAKER_EXPECTED_EXCEPTION_TOLERANCE=0.1

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=structured
ENABLE_PERFORMANCE_LOGGING=true
```

### **Secrets Configuration**
The backend automatically loads configuration from multiple `.streamlit/secrets.toml` locations in priority order:

1. **`.streamlit/secrets.toml`** (project root - preferred for backend/Docker)
2. **`../streamlit/secrets.toml`** (parent directory fallback)
3. **`frontend/.streamlit/secrets.toml`** (frontend directory fallback)

**Setup Instructions:**
```bash
# Copy template to both required locations
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
cp .streamlit/secrets.toml.template frontend/.streamlit/secrets.toml

# Edit both files with your actual credentials
```

**Configuration Format:**
```toml
# OpenAI Configuration
OPENAI_API_KEY = "sk-your-openai-api-key"

# Google Gemini Configuration
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-2.5-pro"

# Neo4j Database Configuration
NEO4J_URI = "neo4j+s://your-database.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "your-password"

# Advanced Parallel Hybrid Configuration
FUSION_DEFAULT_STRATEGY = "advanced_hybrid"
TEMPLATE_DEFAULT_TYPE = "regulatory_compliance"
```

**Important Notes:**
- Both secrets files are required for proper operation
- Root `.streamlit/secrets.toml` is used by backend and Docker
- Frontend `.streamlit/secrets.toml` is used by Streamlit when running directly
- Both files are automatically ignored by git (.gitignore)

---

## **Usage**

### **Development Setup**
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure secrets
# Ensure BOTH secrets files exist with valid API keys:
# - .streamlit/secrets.toml (project root)
# - frontend/.streamlit/secrets.toml (frontend directory)

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
# http://localhost:8000/docs
```

### **Docker Usage**
```bash
# Build backend container
docker build -f Dockerfile.backend -t mrca-backend .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e GEMINI_API_KEY=your-key \
  -e NEO4J_URI=your-uri \
  -e NEO4J_USERNAME=neo4j \
  -e NEO4J_PASSWORD=your-password \
  mrca-backend

# Access API
# http://localhost:8000/docs
```

### **Module Execution**
```bash
# Run as Python module (recommended for imports)
python -m uvicorn backend.main:app --reload

# Run directly from backend directory
cd backend
uvicorn main:app --reload
```

---

## **Performance Metrics**

### **System Capabilities**

#### **Processing Performance**
- **Average Response Time**: 30-45 seconds (comprehensive analysis)
- **Parallel Efficiency**: ~2x faster than sequential processing
- **Concurrent Users**: Up to 10 simultaneous requests
- **Throughput**: 80-120 queries per hour (production scale)

#### **Quality Metrics**
- **Confidence Scoring**: 0-100% accuracy assessment
- **Success Rate**: 98%+ successful responses
- **Error Rate**: <2% system errors
- **Quality Assessment**: Automated response quality evaluation

#### **Resource Usage**
- **Memory**: 2-4 GB RAM (depending on concurrent load)
- **CPU**: 2-4 cores (optimal performance)
- **Network**: High-speed internet required for API calls
- **Storage**: 500 MB for application + logs

### **Advanced Parallel HybridRAG - Intelligent Fusion Metrics**

#### **Retrieval Performance**
```python
{
  "vector_search": {
    "average_time": 2.3,        # seconds
    "confidence_range": "0.85-0.95",
    "results_returned": 15
  },
  "graph_search": {
    "average_time": 5.8,        # seconds  
    "confidence_range": "0.70-0.85",
    "nodes_traversed": 150
  },
  "parallel_efficiency": 2.1,   # speedup vs sequential
  "total_processing": 35.2      # seconds
}
```

#### **Fusion Analysis**
```python
{
  "fusion_strategy": "advanced_hybrid",
  "fusion_quality": 0.92,
  "complementarity_score": 0.87,
  "final_confidence": 1.0,
  "vector_contribution": 0.65,
  "graph_contribution": 0.35
}
```

---

## **Development**

### **Local Development**
```bash
# Setup development environment
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --log-level debug

# Access interactive API docs
# http://localhost:8000/docs
```

### **Testing**
```bash
# Health check
curl http://localhost:8000/health

# Advanced health check
curl http://localhost:8000/parallel_hybrid/health

# Test parallel hybrid endpoint
curl -X POST http://localhost:8000/generate_parallel_hybrid \
  -H "Content-Type: application/json" \
  -d '{"user_input": "What are methane monitoring requirements?"}'
```

### **Adding New Features**

#### **New Fusion Strategy**
```python
# Add to context_fusion.py
class FusionStrategy(Enum):
    YOUR_STRATEGY = "your_strategy"

async def your_fusion_strategy(vector_result, graph_result):
    # Implement your fusion logic
    pass
```

#### **New Template Type**
```python
# Add to hybrid_templates.py
class TemplateType(Enum):
    YOUR_TEMPLATE = "your_template"

def create_your_template(context, metadata):
    # Implement your template logic
    pass
```

---

## **Troubleshooting**

### **Common Issues**

#### **Configuration Errors**
```
Error: Configuration validation failed
```
**Solution**:
- Verify **both** secrets files exist and contain valid API keys:
  - `.streamlit/secrets.toml` (project root)
  - `frontend/.streamlit/secrets.toml` (frontend directory)
- Check environment variables are properly set
- Validate Neo4j database connectivity
- Ensure secrets files are not using placeholder values

#### **Database Connection Issues**
```
Error: Failed to connect to Neo4j database
```
**Solution**:
- Verify Neo4j URI format: `neo4j+s://hostname:7687`
- Check username/password credentials
- Test database connectivity: `neo4j cypher-shell`

#### **API Rate Limiting**
```
Error: OpenAI API rate limit exceeded
```
**Solution**:
- Monitor API usage and quotas
- Implement request throttling
- Consider upgrading API tier

#### **Performance Issues**
```
Warning: Response time > 60 seconds
```
**Solution**:
- Check Neo4j database performance
- Monitor API response times
- Verify system resource availability

### **Debugging**

#### **Enable Debug Logging**
```bash
export MRCA_DEBUG=true
export LOG_LEVEL=DEBUG
uvicorn main:app --log-level debug
```

#### **Circuit Breaker Status**
```python
# Check circuit breaker health
import requests
response = requests.get("http://localhost:8000/parallel_hybrid/health")
print(response.json()["components"])
```

#### **Performance Monitoring**
```python
# Monitor processing metrics
response = requests.post("http://localhost:8000/generate_parallel_hybrid", 
                        json={"user_input": "test query"})
metadata = response.json()["metadata"]
print(f"Processing time: {metadata['processing_time']}")
```

---

## **Security**

### **Security Features**

#### **API Security**
- **Input Validation**: Pydantic model validation for all requests
- **Rate Limiting**: Request throttling to prevent abuse
- **CORS Configuration**: Secure cross-origin resource sharing
- **Environment Variables**: Secure credential management

#### **Database Security**
- **Encrypted Connections**: TLS/SSL for all Neo4j connections
- **Authentication**: Username/password authentication
- **Access Control**: Read-only database access for safety

#### **LLM Security**
- **API Key Protection**: Secure credential storage
- **Request Validation**: Input sanitization and validation
- **Error Information**: Limited error details to prevent information disclosure

### **Best Practices**
- **Secrets Management**: Never commit API keys to version control
- **HTTPS Only**: Use HTTPS in production deployment
- **Regular Updates**: Keep dependencies updated for security patches
- **Monitoring**: Comprehensive logging and error tracking

---

## **Deployment**

### **Production Deployment**

#### **Render Cloud Platform**
```yaml
# render.yaml
services:
  - type: web
    name: mrca-backend
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: GEMINI_API_KEY  
        sync: false
      - key: NEO4J_URI
        sync: false
```

#### **Docker Production**
```bash
# Build production image
docker build -f Dockerfile.backend -t mrca-backend:latest .

# Run with production settings
docker run -d \
  --name mrca-backend \
  -p 8000:8000 \
  --env-file .env.production \
  --restart unless-stopped \
  mrca-backend:latest
```

#### **Performance Optimization**
```bash
# Production uvicorn settings
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --access-log \
  --log-level info
```

---

## **Contributing**

### **Development Guidelines**
1. **Follow FastAPI Best Practices**: Async/await patterns and dependency injection
2. **Maintain Type Hints**: Comprehensive type annotations for all functions
3. **Test Thoroughly**: Unit tests for all components and integration tests
4. **Document Changes**: Update README and API documentation

### **Research Opportunities**
- **New Fusion Algorithms**: Machine learning-based fusion strategies
- **Performance Optimization**: GPU acceleration and distributed processing
- **Advanced NLP**: Improved entity extraction and relationship modeling
- **Quality Metrics**: Enhanced response quality assessment algorithms

---

© 2025 Alexander Samuel Ricciardi - MRCA Backend Module  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System 
