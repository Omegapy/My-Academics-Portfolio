# MRCA - Mining Regulatory Compliance Assistant - Advanced Parallel Hybrid - Intelligent Fusion (APH-IF) Technology

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=flat&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)

**An AI-powered regulatory compliance assistant providing mining safety guidance. 
The system uses a novel RAG system - Advanced Parallel HybridRAG - Intelligent Fusion.**

For more project documentation see the `Documents` folder.

---

MRCA Website: https://mrca-frontend.onrender.com/  

⚠️ This project has limited funds (I am a student). Once the monthly LLM usage fund limit is reached, the application will stop providing responses and will display an error message.  
Please contact me (a.omegapy@gmail.com) if this happend and you still want to try the application.

---

© 2025 Alexander Samuel Ricciardi - MRCA Frontend Module  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF) System 

---

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omega.py)   
Date: 07/25/2025

This project was part of my capstone project at CSU Global.

---

My Links:   

<i><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></i>
<i><a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></i>
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
<i><a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></i>
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)
<i><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></i>
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)    

---

## **What is MRCA?**

MRCA (Mining Regulatory Compliance Assistant) is a web application that uses an AI system to provide quick, reliable, 
and easy access to MSHA (Mine Safety and Health Administration) regulations using natural language queries. 
Built on novel **Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF)** technology.

### **Core Innovation: Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF)**

Unlike traditional (basic) RAG (Retrieval Augmented Generation) systems that use *sequential* processing, 
MRCA implements **Advanced Parallel HybridRAG (APH)** that performs **concurrent VectorRAG (semantic search) 
and GraphRAG (traversal search) queries** 
and fuses the queries results using **Intelligent Context Fusion (IF)** using a LLM or a LRM:

- **Traditional RAG**: `if condition: vector_search() else: graph_search()`
- **MRCA's Innovation**: `asyncio.gather(vector_task, graph_task)` - parallelism - `intelligent_context_fusion`

This approach combines:
- **VectorRAG**: Semantic similarity search using 768-dimensional Gemini embeddings
- **GraphRAG**: Knowledge graph traversal with automated Cypher generation
- **Context Fusion**: Intelligent combination using 4 research-based fusion strategies
- **Hybrid Templates**: 5 specialized response templates for different use cases

---

Preview:

| | |
|---|---|
| <img width="350" src="https://github.com/user-attachments/assets/2ebfeed2-ba58-4cef-a6e1-9288ff76eaf2" style="border: 5px solid grey;"> | <img width="350" src="https://github.com/user-attachments/assets/9c59f5c4-b661-4048-af6e-02669a501dc9" style="border: 5px solid grey;">

---

## **Key Features**

### **Advanced AI Processing**
- **Dual-Mode Interface**: Traditional Agent + Advanced Parallel Hybrid processing
- **4 Fusion Strategies**: Advanced Hybrid, Weighted Linear, Max Confidence, Adaptive
- **5 Template Types**: Regulatory Compliance, Research-Based, Comparative Analysis, etc.
- **Real-Time Configuration**: Live strategy and template selection

### **Professional Analytics**
- **Performance Metrics**: Processing times, confidence scores, quality assessments
- **Fusion Analysis**: Vector vs Graph contribution breakdown
- **Health Monitoring**: Component-level system diagnostics
- **Quality Feedback**: Automated response quality evaluation

### **Knowledge Base**
- **26,429 Total Nodes** in Neo4j knowledge graph
- **20,851 MSHA Entities** extracted from regulations
- **5,575 Text Chunks** with vector embeddings
- **Complete Title 30 CFR Coverage** (Parts 1-999)

### **Architecture**
- **Microservices Design**: Scalable FastAPI backend + Streamlit frontend
- **Cloud-Native**: Neo4j Aura cloud database integration
- **Docker Containerization**: Production-ready deployment
- **Health Monitoring**: Comprehensive fault tolerance and monitoring
- **Deployment**: Render cloud hosting platform implementing 2 services. One for the Frontend, and one for the Backend.

---

## **Quick Start**

### **Prerequisites**
- Docker Desktop (latest version)
- Python 3.12+
- API Keys: OpenAI, Google Gemini, Neo4j Aura

### **1. Clone Repository**
```bash
git clone <repository-url>
cd MRCA
```

### **2. Configure Secrets**
```bash
# Copy template and add your API keys to BOTH locations
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
cp .streamlit/secrets.toml.template frontend/.streamlit/secrets.toml

# Edit BOTH secrets.toml files with your credentials:
# OPENAI_API_KEY = "sk-your-openai-key"
# GEMINI_API_KEY = "your-gemini-key"
# NEO4J_URI = "neo4j+s://your-instance.databases.neo4j.io"
# NEO4J_USERNAME = "neo4j"
# NEO4J_PASSWORD = "your-password"

# Note: Both files are required:
# - .streamlit/secrets.toml (for backend and Docker)
# - frontend/.streamlit/secrets.toml (for Streamlit frontend)
```

### **3. Launch Application**
```bash
# Normal/basic launch
python3 launch_app.py
```

#### **Recommended - if basic launch issues arise**
```bash
# Starts services as detached background processes 
python3 start_services.py
```

#### **Advanced: Dev Container Launcher**
```bash
# Original launcher with monitoring with detached processes
python3 launch_devcontainer.py
```

#### **Stop Services**
```bash
# Stop all MRCA services
python3 stop_services.py
# OR manually:
pkill -f streamlit && pkill -f uvicorn
```

#### **Docker Compose (Production)**
```bash
# Build and start all services
docker-compose up --build -d

# Check status
docker-compose ps
```

### **4. Access Application**
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## **System Architecture**

```
┌──────────────────────────────────────────────────────────────┐
│  MRCA Advanced Parallel Hybrid Architecture                  │
│                                                              │
│  ┌─────────────────┐    HTTP/REST     ┌──────────────┐       │
│  │   Frontend      │ ◄──────────────► │   Backend    │       │
│  │   (Streamlit)   │                  │   (FastAPI)  │       │
│  │   Port 8501     │                  │   Port 8000  │       │
│  └─────────────────┘                  └──────────────┘       │
│                                              │               │
│                                              ▼               │
│  ┌──────────────────────────────────────────────────┐        │
│  │  Advanced Parallel Hybrid Processing Pipeline    │        │
│  │                                                  │        │
│  │  Step 1: Parallel Retrieval Engine               │        │
│  │  ┌─────────────────┐    ┌─────────────────┐      │        │
│  │  │   VectorRAG     │    │    GraphRAG     │      │        │
│  │  │ (async thread)  │    │ (async thread)  │      │        │
│  │  └─────────────────┘    └─────────────────┘      │        │
│  │                                                  │        │
│  │  Step 2: Context Fusion Engine                   │        │
│  │  ┌─────────────────────────────────────────┐     │        │
│  │  │  4 Fusion Strategies + Quality Analysis │     │        │
│  │  └─────────────────────────────────────────┘     │        │
│  │                                                  │        │
│  │  Step 3: Hybrid Template System                  │        │
│  │  ┌─────────────────────────────────────────┐     │        │
│  │  │  5 Template Types + Response Generation │     │        │
│  │  └─────────────────────────────────────────┘     │        │
│  └──────────────────────────────────────────────────┘        │
│                                              │               │
│                                              ▼               │
│                                     ┌─────────────────┐      │
│                                     │   Neo4j Aura    │      │
│                                     │   (Cloud DB)    │      │
│                                     └─────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

---

## **Technology Stack**

### **Core Technologies**
- **Backend**: Python 3.12 + FastAPI + Pydantic
- **Frontend**: Streamlit + Modern CSS
- **Database**: Neo4j Aura (cloud)
- **🤖 AI/ML**: OpenAI GPT-4o + Google Gemini + LangChain

### **Advanced Components**
- **Parallel Processing**: asyncio + ThreadPoolExecutor
- **Vector Search**: Neo4j Vector Index + Gemini embeddings
- **Graph Processing**: Cypher generation + GraphCypherQAChain
- **Context Fusion**: Custom research-based algorithms

### **Development Tools**
- **Containerization**: Docker + Docker Compose
- **onfiguration**: Pydantic settings + TOML secrets
- **Monitoring**: Health checks + Performance metrics
- **Error Handling**: Circuit breakers + Graceful degradation

---

## **Usage Examples**

### **Basic Usage**
1. **Launch Application**: `python3 start_services.py`
2. **Open Frontend**: Navigate to http://localhost:8501
3. **Configure Processing**: Select fusion strategy and template type
4. **Ask Questions**: Enter natural language queries about mining regulations

### **Connection Issue Prevention**
MRCA Beta v2.0.1 includes enhanced process management that **completely prevents connection errors**:

- **Detached Background Processes**: Services run independently of launcher scripts
- **Terminal Independence**: Services continue running even if terminal is closed
- **Script Independence**: Services persist after launcher script terminates
- **No More Reconnection Issues**: Robust process architecture prevents service interruption

### Launching App in Development

**How it works**: Both launchers (`start_services.py` and `launch_devcontainer.py`) now start services as true background processes using process group separation and I/O detachment. This means:
- Services **never stop unexpectedly** when scripts terminate
- You can safely **close terminals** without affecting running services
- **No connection errors** due to parent process termination
- Services remain **completely independent** and persistent

### **API Usage**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Query via API
curl -X POST http://localhost:8000/generate_parallel_hybrid \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "What safety equipment is required for underground coal mining?",
    "fusion_strategy": "advanced_hybrid",
    "template_type": "regulatory_compliance"
  }'
```

---

## **Configuration Options**

### **Fusion Strategies**
- **`advanced_hybrid`**: Research-based fusion with complementarity analysis (recommended)
- **`weighted_linear`**: Confidence-based linear combination
- **`max_confidence`**: Select highest confidence result with context
- **`adaptive_fusion`**: Dynamic strategy selection based on content

### **Template Types**
- **`regulatory_compliance`**: Enhanced compliance-focused responses (recommended)
- **`research_based`**: Academic methodology with citations
- **`basic_hybrid`**: Simple combination template
- **`comparative_analysis`**: Source complementarity display
- **`confidence_weighted`**: Quality-adjusted responses

### **Environment Variables**
```bash
# Core Configuration
OPENAI_API_KEY=sk-your-openai-key
GEMINI_API_KEY=your-gemini-key
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# Optional Settings
MRCA_DEBUG=false
FUSION_DEFAULT_STRATEGY=advanced_hybrid
TEMPLATE_DEFAULT_TYPE=regulatory_compliance
```

---

## **Performance Metrics**

### **System Capabilities**
- **Processing Time**: 10-60 seconds per query
- **Confidence Scoring**: 0-100% accuracy assessment
- **Quality Analysis**: Automated response quality evaluation
- **Parallel Efficiency**: ~2x faster than sequential processing

### **Knowledge Base Statistics**
- **Total Nodes**: 26,429 (Documents + Chunks + Entities)
- **Regulatory Coverage**: Complete Title 30 CFR (Parts 1-999)
- **Entity Extraction**: 20,851 MSHA-specific entities
- **Vector Embeddings**: 5,575 chunks with 768-dimensional vectors

---

## **Development**

### **Project Structure**
```
MRCA/
├── frontend/          # Streamlit UI application
├── backend/           # FastAPI service with Advanced Parallel Hybrid
├── build_data/        # Data pipeline and knowledge graph construction
├── data/              # CFR PDF documents and processed data
├── docker-compose.yml # Container orchestration
├── launch_app.py      # Intelligent application launcher
└── Documents/         # Project documentation
```

### **Development Setup**

#### **Standard Development**
```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Run comprehensive test suite
python -m pytest tests/

# Run unit tests only
python -m pytest tests/unit/

# Run with coverage report
python -m pytest --cov=backend tests/unit/

# Run specific test file
python -m pytest tests/unit/test_parallel_hybrid.py -v

```

#### **Docker-in-Docker Development**

For development in VS Code containers with full Docker support:

**Prerequisites:**
- VS Code with Dev Containers extension
- Docker Desktop running on host machine

**Setup:**
1. **Open in Dev Container**: Use the "Dev Containers: Reopen in Container" command
2. **Wait for Setup**: The dev container will automatically install Docker-in-Docker
3. **Launch with Docker**: Use the dedicated launcher for dev containers

```bash
# Method 1: Dedicated Docker launcher (Recommended)
./launch_docker.sh

# Method 2: Manual Docker Compose
docker-compose up --build -d

```

**What Docker-in-Docker Provides:**
- **Full Docker Support**: Complete Docker CLI and Compose functionality
- **Production Parity**: Identical to production Docker environment
- **Service Isolation**: Proper container networking and volume management
- **Port Forwarding**: Automatic VS Code/Cursor port forwarding to browser
- **Hot Reload**: Development changes reflected in real-time

**Accessing the Application:**
1. **Check PORTS Tab**: Look for forwarded ports 8501 and 8000 in VS Code/Cursor
2. **Click Port 8501**: Opens MRCA frontend directly in browser
3. **API Access**: Port 8000 provides backend API and documentation

**Troubleshooting Dev Containers:**
```bash
# Check Docker status
docker --version
docker info

# Verify services
docker-compose ps

# View logs
docker-compose logs --tail=20

# Stop services
docker-compose down
```

### **Building Knowledge Graph**
```bash
# Download CFR documents
cd build_data
python cfr_downloader.py

# Build hybrid knowledge store
python build_hybrid_store.py
```

---

## **API Documentation**

### **Core Endpoints**
- **`GET /`**: Service information and status
- **`GET /health`**: Basic health check
- **`GET /parallel_hybrid/health`**: Detailed component health
- **`POST /generate_parallel_hybrid`**: Main processing endpoint

### **Request Format**
```
{
  "user_input": "string",           // REQUIRED: Natural language question
  "session_id": "string",           // OPTIONAL: Session identifier
  "fusion_strategy": "string",      // OPTIONAL: Fusion algorithm
  "template_type": "string"         // OPTIONAL: Response template
}
```

### **Response Format**
```
{
  "response": "string",             // Generated response
  "processing_time": 12.34,         // Processing time in seconds
  "metadata": {
    "parallel_retrieval": { ... },   // Retrieval metrics
    "context_fusion": { ... },       // Fusion analysis
    "hybrid_template": { ... }       // Template information
  }
}
```

For complete API documentation, visit: http://localhost:8000/docs

---

## **System Requirements**

### **Minimum Requirements**
- **OS**: Linux, macOS, or Windows with WSL2
- **Memory**: 4 GB RAM
- **Storage**: 5 GB free space
- **Network**: High-speed internet for API calls

### **Recommended Requirements**
- **OS**: Linux or macOS
- **Memory**: 8 GB RAM
- **CPU**: 4+ cores
- **Storage**: 10 GB free space
- **Network**: Fiber/broadband connection

### **External Dependencies**
- **Neo4j Aura**: Cloud graph database
- **OpenAI API**: GPT-4o for text generation
- **Google Gemini API**: Embeddings and entity extraction

---

## **Security & Compliance**

### **Data Privacy**
- **No Personal Data Storage**: System processes regulatory queries only
- **API Key Security**: Encrypted environment variable management
- **Session Management**: Temporary session IDs with automatic cleanup

### **Regulatory Compliance**
- **Official Sources**: Uses official CFR documents from govinfo.gov
- **Citation Accuracy**: Preserves exact CFR section references
- **Disclaimer**: Provides informational guidance, not legal advice

---

## **Testing**

MRCA includes a comprehensive test suite covering all backend components with professional-grade testing patterns.

### **Test Suite Overview**

**9 Major Backend Components Fully Tested:**
- `test_config.py` - Configuration management and validation
- `test_llm.py` - LLM factory functions and lazy loading
- `test_database.py` - Enhanced Neo4j database operations
- `test_parallel_hybrid.py` - Parallel retrieval engine and async execution
- `test_context_fusion.py` - Fusion strategies and confidence scoring
- `test_hybrid_templates.py` - Template generation and response formatting
- `test_utils.py` - Session management and utility functions
- `test_tools.py` - Vector, Cypher, and General tool components
- `test_graph.py` - Graph operations and lazy loading patterns

### **Testing Features**

**Comprehensive Coverage:**
- **~2,000+ Individual Test Cases** across all components
- **Data Classes & Enums Testing** - Validation of all data structures
- **Core Functionality Testing** - All major methods and operations
- **Factory Functions Testing** - Singleton patterns and global instances
- **Error Handling Testing** - Comprehensive error scenarios and resilience
- **Edge Cases Testing** - Empty inputs, malformed data, performance limits
- **Integration Testing** - Cross-component interactions
- **Async Testing** - Proper async/await pattern testing
- **Thread Safety Testing** - Concurrent operation validation
- **Performance Testing** - Large dataset and memory efficiency

**Advanced Testing Patterns:**
- **Mock Strategies** for external dependencies (LLMs, databases, APIs)
- **Fixture Management** for consistent test data
- **Async Context Management** for proper resource handling
- **Error Propagation Testing** for comprehensive exception handling
- **Configuration Validation** for environment and setup testing
- **Health Check Integration** for system monitoring and diagnostics

### **Running Tests**

```bash
# Run all tests
python -m pytest tests/

# Run unit tests with verbose output
python -m pytest tests/unit/ -v

# Run with coverage report
python -m pytest --cov=backend tests/unit/ --cov-report=html

# Run specific component tests
python -m pytest tests/unit/test_parallel_hybrid.py -v
python -m pytest tests/unit/test_context_fusion.py -v

# Run async tests only
python -m pytest tests/unit/ -k "async" -v

# Run performance tests
python -m pytest tests/unit/ -k "performance" -v
```

### **Test Configuration**

Tests use pytest with the following key configurations:
- **pytest-asyncio** for async test support
- **pytest-cov** for coverage reporting
- **Comprehensive fixtures** in `conftest.py`
- **Mock isolation** for external dependencies
- **Parallel execution** support for faster test runs

---

## **Contributing**

### **Development Guidelines**
1. **Fork the repository** and create a feature branch
2. **Follow PEP 8** Python style guidelines
3. **Add comprehensive tests** for new features
4. **Update documentation** for API changes
5. **Submit pull requests** with clear descriptions

### **Code Quality Standards**
- **Type Hints**: Use type annotations for all functions
- **Error Handling**: Implement comprehensive error handling
- **Testing**: Maintain >90% test coverage with comprehensive unit tests
- **Documentation**: Include docstrings for all public functions
- **Test Patterns**: Follow established testing patterns (see existing test files)

### **Testing Requirements for Contributors**
- **Unit Tests**: Add tests for all new backend components
- **Mock Integration**: Properly isolate external dependencies
- **Async Testing**: Use pytest-asyncio for async functionality
- **Edge Cases**: Include error handling and edge case testing
- **Performance**: Add performance tests for scalability-critical code
- **Documentation**: Update test documentation for new test patterns

### **Areas for Contribution**
- **Performance Optimization**: Caching and response time improvements
- **New Fusion Strategies**: Research-based algorithm implementations
- **UI/UX Enhancements**: Frontend improvements and accessibility
- **Test Enhancement**: Integration and end-to-end test development
- **Documentation**: User guides and technical documentation

---

## **Acknowledgments**

- **MSHA**: Mine Safety and Health Administration for regulatory guidance
- **Neo4j**: Graph database technology and vector search capabilities
- **OpenAI**: Advanced language model technology
- **Google**: Gemini embedding and AI capabilities
- **LangChain**: LLM orchestration framework
- **Streamlit**: Modern web application framework

---

## **Support**

### **Getting Help**
- **Documentation**: Check the comprehensive documentation in `Documents/`
- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions for questions and tips
- **Health Checks**: Monitor system health at `/health` endpoints

### **Common Issues**
- **Connection Errors**: Verify API keys and network connectivity
- **Performance Issues**: Check system resources and timeout settings
- **Configuration Problems**: Validate secrets.toml and environment variables

---

## **Future Enhancements**

### **Research Opportunities**
- **New Fusion Algorithms**: Machine learning-based fusion strategies
- **Advanced NLP**: Improved entity extraction and relationship modeling
- **Performance Optimization**: GPU acceleration and distributed processing
- **Domain Expansion**: Other regulatory domains beyond mining

---

MRCA provides mining safety guidance. However, it is ultimate goal is to be a platform for testing 
the novel Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF) technology .

---

© 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
