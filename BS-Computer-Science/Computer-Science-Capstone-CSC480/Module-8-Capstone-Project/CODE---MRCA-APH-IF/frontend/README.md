# MRCA Frontend - Streamlit User Interface

[![Frontend: Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

**Advanced Parallel HybridRAG - Intelligent Fusion User Interface for Mining Regulatory Compliance Assistant**

**Streamlit-based web application provides access to MRCA's Advanced Parallel HybridRAG - Intelligent Fusion technology for mining safety regulation queries.**

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

## **What is MRCA Frontend?**

The MRCA Frontend is a professional Streamlit web application that provides users with an interface to access the Advanced Parallel HybridRAG - Intelligent Fusion technology. It offers real-time configuration options, performance analytics, and comprehensive mining regulatory compliance assistance through a modern, responsive user interface.

### **Core Features**

- **Dual-Mode AI Processing**: Traditional Agent + Advanced Parallel Hybrid modes
- **Real-Time Configuration**: Live fusion strategy and template selection  
- **Performance Analytics**: Processing times, confidence scores, fusion analysis
- **Professional Interface**: Modern design with health monitoring
- **Dynamic Settings**: 4 fusion strategies and 5 template types
- **Quality Feedback**: Automated response quality assessment

---

## **Architecture**

```
┌──────────────────────────────────────────────────────────┐
│  MRCA Frontend Architecture (Streamlit)                  │
│                                                          │
│  ┌─────────────────┐    HTTP/REST     ┌──────────────┐   │
│  │   User Browser  │ ◄──────────────► │   Frontend   │   │
│  │   (Port 8501)   │                  │   (bot.py)   │   │
│  └─────────────────┘                  └──────────────┘   │
│                                              │           │
│                                              ▼           │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Streamlit Application Components                │    │
│  │                                                  │    │
│  │  ┌─────────────────┐    ┌─────────────────┐      │    │
│  │  │  Configuration  │    │   Chat Interface│      │    │
│  │  │   Sidebar       │    │   & Messages    │      │    │
│  │  └─────────────────┘    └─────────────────┘      │    │
│  │                                                  │    │
│  │  ┌─────────────────┐    ┌─────────────────┐      │    │
│  │  │  Performance    │    │  Health Monitor │      │    │
│  │  │   Analytics     │    │  & System Info  │      │    │
│  │  └─────────────────┘    └─────────────────┘      │    │
│  └──────────────────────────────────────────────────┘    │
│                                              │           │
│                                              ▼           │
│                                     ┌─────────────────┐  │
│                                     │  Backend API    │  │
│                                     │  (Port 8000)    │  │
│                                     └─────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## **Key Components**

### **Core Files**

#### **`bot.py`** (1,115 lines)
Main Streamlit application providing:
- **Chat Interface**: Real-time conversation with AI assistant
- **Configuration Panel**: Live fusion strategy and template selection
- **Performance Metrics**: Processing times and confidence scores
- **Health Monitoring**: Backend service status and diagnostics
- **Session Management**: Persistent user sessions with unique IDs

#### **`requirements.txt`** 
Frontend-specific dependencies:
```txt
streamlit>=1.28.0
requests>=2.31.0
```

#### **`Dockerfile.frontend`** (208 lines)
Production-ready container configuration:
- **Multi-stage Build**: Optimized for production deployment
- **Health Checks**: Container-level health monitoring
- **Security**: Non-root user execution
- **Port Configuration**: Streamlit default port 8501

#### **`.streamlit/config.toml`**
Streamlit application configuration:
- **UI Customization**: Theme and layout settings
- **Performance**: Caching and optimization options
- **Security**: CORS and authentication settings

#### **`.streamlit/secrets.toml`**
Frontend-specific secrets configuration:
- **API Keys**: OpenAI, Gemini, and Neo4j credentials
- **Backend Communication**: Service authentication
- **Local Development**: Direct API access configuration
- **Security**: Automatically ignored by git (.gitignore)

### **Key Functions**

#### **Configuration Management**
```python
def display_parallel_hybrid_config():
    """Real-time configuration panel for Advanced Parallel Hybrid settings"""
    
def get_session_id():
    """Generate and manage unique session identifiers"""
```

#### **API Communication**
```python
def call_parallel_hybrid_api(user_input, session_id, fusion_strategy, template_type):
    """Primary function for backend API communication"""
    
def handle_processing_error(error):
    """Graceful error handling with user-friendly messages"""
```

#### **Performance Analytics**
```python
def display_parallel_hybrid_metrics(metadata):
    """Comprehensive performance and quality metrics display"""
    
def get_confidence_level(score):
    """Visual confidence score representation"""
```

#### **Health Monitoring**
```python
def display_system_health():
    """Real-time backend service health monitoring"""
```

---

## **Configuration Options**

### **Fusion Strategies**
Users can select from 4 research-based fusion strategies:
- **`advanced_hybrid`**: Research-based fusion with complementarity analysis (recommended)
- **`weighted_linear`**: Confidence-based linear combination
- **`max_confidence`**: Select highest confidence result with context
- **`adaptive_fusion`**: Dynamic strategy selection based on content

### **Template Types**
5 specialized response templates available:
- **`regulatory_compliance`**: Enhanced compliance-focused responses (recommended)
- **`research_based`**: Academic methodology with citations
- **`basic_hybrid`**: Simple combination template
- **`comparative_analysis`**: Source complementarity display
- **`confidence_weighted`**: Quality-adjusted responses

### **System Settings**
- **Session Persistence**: Automatic session ID generation and management
- **Error Recovery**: Graceful fallback for backend connectivity issues
- **Performance Tracking**: Real-time metrics collection and display
- **Quality Assessment**: Automated response quality evaluation

---

## **Usage**

### **Quick Start**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pip install -r requirements.txt

# Configure secrets (if running standalone)
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API keys

# Run Streamlit application
streamlit run bot.py

# Access application
# Open browser to: http://localhost:8501
```

### **Secrets Configuration**
The frontend requires API credentials for direct backend communication:

```bash
# Copy template and configure
cp .streamlit/secrets.toml.template .streamlit/secrets.toml

# Edit with your credentials:
# OPENAI_API_KEY = "sk-your-openai-key"
# GEMINI_API_KEY = "your-gemini-key"
# NEO4J_URI = "neo4j+s://your-instance.databases.neo4j.io"
# NEO4J_USERNAME = "neo4j"
# NEO4J_PASSWORD = "your-password"
```

**Important Notes:**
- Frontend `.streamlit/secrets.toml` is used when Streamlit runs directly
- Root `.streamlit/secrets.toml` is used by backend and Docker
- Both files should contain identical credentials
- Both files are automatically ignored by git

### **Docker Usage**
```bash
# Build frontend container
docker build -f Dockerfile.frontend -t mrca-frontend .

# Run container
docker run -p 8501:8501 \
  -e BACKEND_URL=http://backend:8000 \
  mrca-frontend

# Access application
# Open browser to: http://localhost:8501
```

### **Integration**
The frontend communicates with the backend via HTTP API:
```python
# Primary API endpoint
POST http://backend:8000/generate_parallel_hybrid

# Health monitoring  
GET http://backend:8000/health
GET http://backend:8000/parallel_hybrid/health
```

---

## **Environment Variables**

### **Required Configuration**
```bash
# Backend API Configuration
BACKEND_URL=http://localhost:8000        # Direct URL (development)
BACKEND_HOST=your-backend-host.com       # Host only (Render deployment)

# Optional Settings
STREAMLIT_SERVER_PORT=8501              # Custom port
STREAMLIT_SERVER_ADDRESS=0.0.0.0       # Bind address
```

### **Deployment-Specific**
```bash
# Render Cloud Platform
BACKEND_HOST=mrca-backend.onrender.com

# Docker Compose
BACKEND_URL=http://backend:8000

# Local Development  
BACKEND_URL=http://localhost:8000
```

---

## **User Interface Features**

### **Chat Interface**
- **Natural Language Queries**: Ask questions about mining regulations
- **Conversation History**: Persistent chat session with context
- **Message Formatting**: Professional response display with metadata
- **Error Handling**: User-friendly error messages and recovery

### **Configuration Panel**
- **Live Settings**: Real-time fusion strategy selection
- **Template Choice**: Dynamic response template configuration
- **Performance Mode**: Choose between Traditional Agent and Advanced Parallel Hybrid
- **Quality Control**: Confidence thresholds and quality settings

### **Analytics Dashboard**
- **Processing Metrics**: Response times and performance data
- **Confidence Scores**: Vector, Graph, and overall confidence levels
- **Quality Assessment**: Automated response quality evaluation
- **Fusion Analysis**: Breakdown of VectorRAG vs GraphRAG contributions

### **Health Monitoring**
- **Backend Status**: Real-time backend service connectivity
- **Component Health**: Individual system component status
- **Performance Tracking**: Historical performance metrics
- **Error Monitoring**: System error rates and diagnostics

---

## **Development**

### **Local Development**
```bash
# Setup development environment
cd frontend
pip install -r requirements.txt

# Run with hot reload
streamlit run bot.py --server.runOnSave true

# Access development server
# http://localhost:8501
```

### **Testing**
```bash
# Run frontend tests
python test_frontend.py

# Manual testing checklist:
# - Backend connectivity
# - Configuration panel functionality  
# - Chat interface responsiveness
# - Health monitoring accuracy
# - Error handling robustness
```

### **Dependencies**
```txt
streamlit>=1.28.0           # Core UI framework
requests>=2.31.0            # HTTP API communication
```

---

## **Troubleshooting**

### **Common Issues**

#### **Backend Connection Failed**
```
Error: Connection refused to backend API
```
**Solution**: 
- Verify backend is running on correct port
- Check BACKEND_URL environment variable
- Test API endpoint manually: `curl http://backend:8000/health`

#### **Slow Response Times**
```
Warning: Response time > 60 seconds
```
**Solution**:
- Check backend performance metrics
- Verify Neo4j database connectivity  
- Monitor API key quotas and rate limits

#### **Configuration Not Saving**
```
Issue: Settings reset on page refresh
```
**Solution**:
- Verify session state management
- Check browser local storage
- Clear Streamlit cache: `streamlit cache clear`

### **Health Checks**
```python
# Manual health verification
import requests

# Test backend connectivity
response = requests.get("http://localhost:8000/health")
print(f"Backend Status: {response.status_code}")

# Test Advanced Parallel Hybrid system
response = requests.get("http://localhost:8000/parallel_hybrid/health")
print(f"Parallel Hybrid Status: {response.json()}")
```

---

## **Performance Optimization**

### **Frontend Performance**
- **Caching**: Aggressive caching of API responses and configuration
- **Lazy Loading**: Components loaded on demand
- **Session Management**: Efficient session state handling
- **Resource Optimization**: Minimal JavaScript and CSS overhead

### **Metrics Tracking**
- **Response Times**: User interaction to response completion
- **API Latency**: Backend communication performance
- **UI Responsiveness**: Frontend rendering performance
- **Error Rates**: System reliability metrics

---

## **Security**

### **Security Features**
- **Session Isolation**: Unique session IDs prevent data leakage
- **Input Validation**: Sanitized user input processing
- **HTTPS Ready**: TLS/SSL support for production deployment
- **Environment Variables**: Secure configuration management

### **Best Practices**
- **No Credential Storage**: Frontend never stores API keys
- **Secure Communication**: All backend communication via HTTPS in production
- **Session Expiry**: Automatic session cleanup
- **Error Information**: Limited error details to prevent information disclosure

---

## **Deployment**

### **Production Deployment**
```bash
# Render Cloud Platform
git push origin main
# Automatic deployment via render.yaml

# Manual Docker Deployment
docker build -f Dockerfile.frontend -t mrca-frontend .
docker run -p 8501:8501 mrca-frontend
```

### **Configuration Management**
- **Environment-Specific**: Different configurations per deployment environment
- **Health Checks**: Container and application-level health monitoring
- **Scaling**: Horizontal scaling support for high traffic
- **Monitoring**: Comprehensive logging and metrics collection

---

## **Contributing**

### **Development Guidelines**
1. **Follow Streamlit Best Practices**: Efficient state management and caching
2. **Maintain UI/UX Standards**: Consistent design and user experience
3. **Test Thoroughly**: Frontend functionality and backend integration
4. **Document Changes**: Update README for new features or modifications

### **UI/UX Standards**
- **Responsive Design**: Mobile and desktop compatibility
- **Accessibility**: WCAG compliance for inclusive design
- **Performance**: Sub-2-second response times for UI interactions
- **Professional Appearance**: Clean, modern interface design

---

© 2025 Alexander Samuel Ricciardi - MRCA Frontend Module  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System 
