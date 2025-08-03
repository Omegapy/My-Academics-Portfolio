# MRCA Build Data - Knowledge Base Construction

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=flat&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)

**Data Pipeline and Knowledge Base Construction for Advanced Parallel HybridRAG - Intelligent Fusion Technology**

Automated scripts for downloading CFR documents, building knowledge graphs, 
and creating the hybrid vector/graph store that powers MRCA's Advanced Parallel HybridRAG - Intelligent Fusion system.

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

----

## **What is MRCA Build Data?**

The MRCA Build Data module contains automated scripts and tools for constructing the comprehensive knowledge base that powers the Advanced Parallel HybridRAG system. This includes downloading official MSHA regulatory documents, extracting and processing content, building knowledge graphs, and creating vector embeddings for semantic search.

### **Core Innovation: Hybrid Knowledge Store Construction**

The build process creates a **dual-mode knowledge store** optimized for parallel retrieval:

- **Vector Store**: 768-dimensional embeddings using Google Gemini for semantic search
- **Knowledge Graph**: Entity-relationship models with MSHA-specific regulatory connections  
- **Hybrid Integration**: Unified Neo4j database combining vector search and graph traversal
- **Quality Control**: Automated validation and optimization of knowledge representation

This directory contains the scripts for building and managing the MRCA knowledge base data.

##Scripts Overview

### `cfr_downloader.py`
Downloads Title 30 CFR PDF documents from govinfo.gov to build the regulatory knowledge base.

**Usage:**
```bash
cd build_data
python cfr_downloader.py
```

**What it does:**
- Downloads 3 volumes of Title 30 CFR (Mining Safety and Health Administration regulations)
- Creates `../data/cfr_pdf/` directory if it doesn't exist
- Saves PDFs with retry logic and rate limiting
- Handles network errors gracefully

**Output:**
- `../data/cfr_pdf/CFR-2024-title30-vol1.pdf` (Parts 1-99: General provisions and coal mine safety)
- `../data/cfr_pdf/CFR-2024-title30-vol2.pdf` (Parts 100-199: Coal mine health and safety)
- `../data/cfr_pdf/CFR-2024-title30-vol3.pdf` (Parts 200-End: Metal and nonmetal mine safety)

### `build_hybrid_store.py`
Builds the complete Advanced Parallel Hybrid knowledge store using Gemini 2.5 Pro.

**Usage:**
```bash
cd build_data
python build_hybrid_store.py
```

**What it does:**
- Reads PDFs from `../data/cfr_pdf/`
- Extracts and chunks text content
- Generates vector embeddings using Google embedding-001 model
- Extracts MSHA-specific entities and relationships using Gemini 2.5 Pro
- Builds Neo4j knowledge graph with both vector and graph components
- Creates vector index for semantic search

**Requirements:**
- Valid secrets configuration with API keys and Neo4j credentials
- Downloaded CFR PDFs (run cfr_downloader.py first)
- Secrets file at `../.streamlit/secrets.toml` (project root)

### `build_graph_debug.py`
Debug version of the graph builder for testing and troubleshooting.

**Usage:**
```bash
cd build_data
python build_graph_debug.py
```

**What it does:**
- Tests LLM transformer functionality
- Processes smaller chunks for debugging
- Creates detailed logs in `build_graph_debug.log`
- Useful for development and troubleshooting

---

## **Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│  MRCA Build Data Pipeline Architecture                          │
│                                                                 │
│  ┌─────────────────┐    Data Flow     ┌──────────────────────┐  │
│  │  govinfo.gov    │ ◄──────────────► │  cfr_downloader.py   │  │
│  │  (Official CFR) │                  │  (PDF Download)      │  │
│  └─────────────────┘                  └──────────────────────┘  │
│                                              │                  │
│                                              ▼                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Hybrid Store Construction Pipeline                      │   │
│  │                                                          │   │
│  │  Step 1: Document Processing (build_hybrid_store.py)     │   │
│  │  ┌─────────────────┐    ┌─────────────────────────┐      │   │
│  │  │  PDF Extraction │    │   Text Chunking         │      │   │
│  │  │  • Content      │    │   • Semantic Chunks     │      │   │
│  │  │  • Metadata     │    │   • Overlap Strategy    │      │   │
│  │  │  • Structure    │    │   • Size Optimization   │      │   │
│  │  └─────────────────┘    └─────────────────────────┘      │   │
│  │                                                          │   │
│  │  Step 2: AI Processing (Gemini 2.5 Pro)                  │   │
│  │  ┌─────────────────┐    ┌─────────────────────────┐      │   │
│  │  │ Entity Extract. │    │  Vector Embeddings      │      │   │
│  │  │ • MSHA Entities │    │  • 768-dimensional      │      │   │
│  │  │ • Relationships │    │  • Semantic Vectors     │      │   │
│  │  │ • Regulatory    │    │  • Similarity Search    │      │   │
│  │  │   Concepts      │    │    Optimization         │      │   │
│  │  └─────────────────┘    └─────────────────────────┘      │   │
│  │                                                          │   │
│  │  Step 3: Knowledge Graph Construction                    │   │
│  │  ┌────────────────────────────────────────────────┐      │   │
│  │  │  Neo4j Database Integration                    │      │   │
│  │  │  • Document Nodes    • Entity Nodes            │      │   │
│  │  │  • Text Chunks       • Relationships           │      │   │
│  │  │  • Vector Index      • Graph Schema            │      │   │
│  │  └────────────────────────────────────────────────┘      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                              │                  │
│                                              ▼                  │
│                                     ┌──────────────────┐        │
│                                     │    Neo4j Aura    │        │
│                                     │  Knowledge Base  │        │
│                                     │  • 26,429 Nodes  │        │
│                                     │  • Vector Index  │        │
│                                     │  • Graph Schema  │        │
│                                     └──────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## **Knowledge Base Statistics**

### **Final Database Composition**
- **Total Nodes**: 26,429+ comprehensive regulatory entities
- **Document Nodes**: 3 volumes of Title 30 CFR (Parts 1-999)
- **Text Chunks**: 5,575 semantically optimized chunks
- **MSHA Entities**: 20,851 extracted regulatory entities
- **Vector Embeddings**: 768-dimensional using Google embedding-001
- **Relationship Types**: `CONTAINS`, `RELATES_TO`, `REQUIRES`, `REFERENCES`

### **Processing Performance**
- **build_hybrid_store.py**: ~100 chunks/hour (production scale)
- **Total Build Time**: 4-6 hours for complete CFR dataset
- **Entity Extraction**: ~50 entities per chunk (average)
- **Vector Generation**: ~2 seconds per embedding
- **Database Optimization**: Automated index creation and validation

---

## **Configuration**

All scripts require a secrets file at `../.streamlit/secrets.toml` (project root) with:

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
```

**Setup Instructions:**
```bash
# From project root, copy template and configure
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your actual credentials

# Verify configuration from build_data directory
cd build_data
python -c "import sys; sys.path.append('..'); from backend.config import get_config; print('Config loaded successfully')"
```

## Typical Workflow

1. **Download regulatory data:**
   ```bash
   cd build_data
   python cfr_downloader.py
   ```

2. **Build knowledge graph:**
   ```bash
   python build_hybrid_store.py
   ```

3. **Verify system is ready:**
   - Check that `../data/cfr_pdf/` contains 3 PDF files
   - Verify Neo4j database has nodes and vector index
   - Test the Advanced Parallel Hybrid system

## Integration with MRCA

These scripts build the foundation for the MRCA Advanced Parallel Hybrid system:

- **VectorRAG**: Semantic search using vector embeddings
- **GraphRAG**: Entity relationship queries using knowledge graph
- **Parallel Processing**: Simultaneous execution of both methods
- **Context Fusion**: Research-based combination of results

## Performance

- **build_hybrid_store.py**: ~100 chunks/hour (production scale)
- **Total processing time**: ~4-6 hours for complete CFR dataset
- **Final database**: 26,429+ nodes with comprehensive vector index
- **Vector dimensions**: 768 (Google embedding-001 model)

## **Troubleshooting**

### **Common Issues**

#### **API Configuration Errors**
```
Error: Invalid API key or insufficient quota
```
**Solution**:
- Verify all API keys in `../.streamlit/secrets.toml` (project root)
- Check OpenAI and Gemini API quotas and billing
- Ensure Neo4j Aura database is active and accessible
- Confirm secrets file is not using placeholder values

#### **Database Connection Issues**
```
Error: Failed to connect to Neo4j database
```
**Solution**:
- Verify Neo4j URI format: `neo4j+s://hostname:7687`
- Check database credentials and network connectivity
- Ensure sufficient database storage space available

#### **Memory and Performance Issues**
```
Warning: Processing taking longer than expected
```
**Solution**:
- Monitor system RAM usage (recommend 8GB+ for full build)
- Check disk space for PDF storage and temporary files
- Consider processing smaller batches for limited resources

### **Debug Mode**
```bash
# Run debug version for detailed logging
cd build_data
python build_graph_debug.py

# Check detailed logs
tail -f build_graph_debug.log
```

---

## **Advanced Features**

### **Custom Configuration**
```python
# Modify chunk size and overlap in build_hybrid_store.py
CHUNK_SIZE = 1000        # Characters per chunk
CHUNK_OVERLAP = 200      # Overlap between chunks
BATCH_SIZE = 10          # Chunks processed per batch
```

### **Progress Monitoring**
```python
# Monitor build progress programmatically
from build_hybrid_store import BuildMonitor

monitor = BuildMonitor()
stats = monitor.get_current_stats()
print(f"Progress: {stats['chunks_processed']}/{stats['total_chunks']}")
```

### **Selective Processing**
```python
# Process specific CFR parts only
python build_hybrid_store.py --parts 100-199  # Coal mine safety only
python build_hybrid_store.py --volumes 1,2    # Exclude metal/nonmetal
```

---

## **Integration with MRCA System**

### **Knowledge Base Usage**
Once built, the knowledge base supports:
- **VectorRAG**: Semantic search using vector embeddings
- **GraphRAG**: Entity relationship traversal
- **Advanced Parallel Hybrid**: Simultaneous vector and graph queries
- **Quality Assessment**: Confidence scoring and result validation

### **Performance Optimization**
The build process optimizes for:
- **Fast Vector Search**: Optimized Neo4j vector indexes
- **Efficient Graph Traversal**: Relationship indexing for quick queries
- **Parallel Retrieval**: Database schema designed for concurrent access
- **Quality Results**: Entity extraction tuned for regulatory content

---

## **Contributing**

### **Development Guidelines**
1. **Test with Small Datasets**: Use debug scripts for development
2. **Monitor Resource Usage**: Ensure sufficient system resources
3. **Validate Data Quality**: Check entity extraction accuracy
4. **Document Changes**: Update README for configuration modifications

### **Research Opportunities**
- **Enhanced Entity Extraction**: Improved MSHA-specific entity recognition
- **Advanced Chunking**: Semantic-aware document segmentation
- **Quality Metrics**: Automated knowledge base quality assessment
- **Incremental Updates**: Support for updating existing knowledge bases

---

© 2025 Alexander Samuel Ricciardi - MRCA Build Data Module  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System 
