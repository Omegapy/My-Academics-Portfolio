# MRCA Backend Tools - Agent Tools Package

[![Tools: LangChain](https://img.shields.io/badge/LangChain-000000?style=flat&logo=langchain&logoColor=white)](https://langchain.com/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=flat&logo=neo4j&logoColor=white)](https://neo4j.com/)

**Agent Tools Package for Advanced Parallel HybridRAG Technology**

**Specialized tools for querying the MSHA regulatory knowledge graph through VectorRAG, GraphRAG, and general query processing capabilities.**

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

## **What are MRCA Backend Tools?**

The MRCA Backend Tools package contains specialized agent tools that implement the core retrieval functionality for the Advanced Parallel HybridRAG system. These tools provide different approaches to querying the MSHA regulatory knowledge graph, enabling parallel execution of VectorRAG (semantic search) and GraphRAG (knowledge graph traversal) along with fallback general query processing.

### **Core Innovation: Parallel Tool Execution**

The tools package enables **true parallel retrieval** through:

- **Simultaneous Execution**: VectorRAG and GraphRAG tools run concurrently via `asyncio.gather()`
- **Specialized Retrieval**: Each tool optimized for specific query types and data patterns
- **Quality Assessment**: Built-in relevance scoring and confidence calculation
- **Performance Monitoring**: Real-time metrics collection for optimization

This approach provides:
- **VectorRAG Tool**: Semantic similarity search using 768-dimensional embeddings
- **GraphRAG Tool**: Knowledge graph traversal with automated Cypher generation
- **General Tool**: Fallback processing for edge cases and multi-source integration
- **Quality Control**: Comprehensive result validation and enhancement

---

## **Architecture**

```
┌──────────────────────────────────────────────────────────────────┐
│  MRCA Backend Tools Architecture                                 │
│                                                                  │
│  ┌─────────────────┐                    ┌─────────────────┐      │
│  │  Parallel Hybrid│ ◄────────────────  │   Main Backend  │      │
│  │   Engine        │    Tool Requests   │   (main.py)     │      │
│  └─────────────────┘                    └─────────────────┘      │
│            │                                                     │
│            ▼                                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Agent Tools Package (tools/)                              │  │
│  │                                                            │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │  │
│  │  │   vector.py     │  │   cypher.py     │  │ general.py │  │  │
│  │  │                 │  │                 │  │            │  │  │
│  │  │ VectorRAG Tool  │  │ GraphRAG Tool   │  │General     │  │  │
│  │  │ • Semantic      │  │ • Graph         │  │Query       │  │  │
│  │  │   Search        │  │   Traversal     │  │Tool        │  │  │
│  │  │ • Embedding     │  │ • Cypher        │  │            │  │  │
│  │  │   Generation    │  │   Generation    │  │            │  │  │
│  │  │ • Similarity    │  │ • Relationship  │  │            │  │  │
│  │  │   Scoring       │  │   Analysis      │  │            │  │  │
│  │  └─────────────────┘  └─────────────────┘  └────────────┘  │  │
│  │                                                            │  │
│  │            Parallel Execution via asyncio                  │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │  async def run_tools_parallel():                    │   │  │
│  │  │      vector_task = asyncio.create_task(vector)      │   │  │
│  │  │      graph_task = asyncio.create_task(cypher)       │   │  │
│  │  │      results = await asyncio.gather(tasks)          │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                    │                             │
│                                    ▼                             │
│                          ┌───────────────────┐                   │
│                          │    Neo4j Aura     │                   │
│                          │  Knowledge Graph  │                   │
│                          │  • Vector Index   │                   │
│                          │  • Graph Schema   │                   │
│                          │  • MSHA Entities  │                   │
│                          └───────────────────┘                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## **Core Tools**

### **VectorRAG Tool**

#### **`vector.py`** (654 lines)
Advanced semantic search implementation for mining regulatory content:

**Key Features:**
- **Embedding Generation**: Google Gemini embedding-001 model integration
- **Semantic Search**: High-performance vector similarity search in Neo4j
- **Relevance Scoring**: Advanced scoring algorithms for result ranking
- **Performance Optimization**: Efficient vector operations and caching

**Core Functions:**
```python
async def execute_vector_search(query: str, limit: int = 15)
async def generate_embeddings(text: str) -> List[float]
async def calculate_relevance_score(query: str, result: str) -> float
async def filter_and_rank_results(results: List[Dict]) -> List[Dict]
```

**Search Process:**
1. **Query Embedding**: Convert natural language to 768-dimensional vector
2. **Vector Search**: Query Neo4j vector index for similar content
3. **Relevance Scoring**: Calculate semantic similarity scores
4. **Result Filtering**: Remove duplicates and low-relevance results
5. **Quality Assessment**: Evaluate result quality and confidence

**Performance Metrics:**
- **Average Search Time**: 2-3 seconds for comprehensive queries
- **Embedding Dimension**: 768 (Google embedding-001)
- **Typical Results**: 10-15 highly relevant chunks
- **Confidence Range**: 85-95% for well-matched queries

#### **Usage Example:**
```python
from tools.vector import execute_vector_search

# Semantic search for mining safety equipment
results = await execute_vector_search(
    query="underground coal mining safety equipment requirements",
    limit=15
)

# Results include:
# - Relevant CFR sections
# - Confidence scores
# - Source metadata
# - Embedding similarity scores
```

### **GraphRAG Tool**

#### **`cypher.py`** (523 lines)
Knowledge graph traversal and relationship analysis for regulatory queries:

**Key Features:**
- **Cypher Generation**: Automated query generation from natural language
- **Graph Traversal**: Efficient exploration of regulatory entity relationships
- **Relationship Analysis**: Identification of regulatory connections and dependencies
- **Performance Monitoring**: Query optimization and execution tracking

**Core Functions:**
```python
async def execute_graph_search(query: str, max_depth: int = 3)
async def generate_cypher_query(natural_language: str) -> str
async def traverse_relationships(start_entities: List[str]) -> Dict
async def analyze_regulatory_connections(entities: List[str]) -> Dict
```

**Query Process:**
1. **Entity Extraction**: Identify key entities in natural language query
2. **Cypher Generation**: Create optimized graph traversal queries
3. **Graph Execution**: Run queries against Neo4j knowledge graph
4. **Relationship Analysis**: Analyze connections between regulatory concepts
5. **Result Synthesis**: Combine graph data into coherent responses

**Graph Schema:**
- **Document Nodes**: CFR sections and regulatory documents
- **Entity Nodes**: MSHA-specific regulatory entities
- **Relationship Types**: `CONTAINS`, `RELATES_TO`, `REQUIRES`, `REFERENCES`
- **Properties**: Text content, metadata, regulatory citations

#### **Usage Example:**
```python
from tools.cypher import execute_graph_search

# Graph traversal for methane monitoring regulations
results = await execute_graph_search(
    query="methane monitoring requirements underground coal mines",
    max_depth=3
)

# Results include:
# - Connected regulatory entities
# - Relationship paths
# - Regulatory dependencies
# - Cross-references
```

### **General Query Tool**

#### **`general.py`** (677 lines)
Fallback query processing and multi-source integration for comprehensive responses:

**Key Features:**
- **Multi-Source Integration**: Combines vector search, graph data, and external sources
- **Fallback Processing**: Handles edge cases and ambiguous queries
- **Quality Enhancement**: Improves results through post-processing
- **Error Recovery**: Graceful degradation when specialized tools fail

**Core Functions:**
```python
async def execute_general_search(query: str, context: Dict) -> Dict
async def integrate_multiple_sources(vector_results, graph_results) -> Dict
async def enhance_result_quality(raw_results: Dict) -> Dict
async def handle_fallback_scenarios(query: str, failed_tools: List[str]) -> Dict
```

**Processing Pipeline:**
1. **Query Analysis**: Determine best approach for ambiguous queries
2. **Multi-Source Retrieval**: Gather data from available sources
3. **Result Integration**: Combine different data types into unified response
4. **Quality Enhancement**: Improve clarity and regulatory accuracy
5. **Fallback Handling**: Provide reasonable responses for edge cases

**Use Cases:**
- **Complex Queries**: Multi-faceted regulatory questions
- **Ambiguous Input**: Unclear or incomplete user queries
- **Tool Failures**: When specialized tools encounter errors
- **Cross-Domain**: Queries spanning multiple regulatory areas

#### **Usage Example:**
```python
from tools.general import execute_general_search

# General processing for complex regulatory query
results = await execute_general_search(
    query="safety requirements for new mining equipment installation",
    context={"domain": "mining", "urgency": "high"}
)

# Results include:
# - Comprehensive regulatory guidance
# - Multiple source integration
# - Quality-enhanced responses
# - Fallback recommendations
```

---

## **Tool Integration**

### **Parallel Execution**

The tools are designed for concurrent execution in the Advanced Parallel Hybrid system:

```python
# Parallel tool execution pattern
async def run_parallel_retrieval(query: str, session_id: str):
    """Execute VectorRAG and GraphRAG tools simultaneously"""
    
    # Create parallel tasks
    vector_task = asyncio.create_task(
        execute_vector_search(query, limit=15)
    )
    
    graph_task = asyncio.create_task(
        execute_graph_search(query, max_depth=3)  
    )
    
    # Execute concurrently
    vector_results, graph_results = await asyncio.gather(
        vector_task, graph_task, return_exceptions=True
    )
    
    # Handle results and errors
    return process_parallel_results(vector_results, graph_results)
```

### **Performance Monitoring**

Each tool includes comprehensive performance tracking:

```python
class ToolMetrics:
    def __init__(self):
        self.execution_time: float = 0.0
        self.results_count: int = 0
        self.confidence_score: float = 0.0
        self.error_count: int = 0
        self.quality_score: float = 0.0

# Real-time metrics collection
async def track_tool_performance(tool_name: str, execution_func):
    start_time = time.time()
    
    try:
        results = await execution_func()
        metrics = calculate_success_metrics(results, start_time)
    except Exception as e:
        metrics = calculate_error_metrics(e, start_time)
    
    return results, metrics
```

---

## **Configuration**

### **Tool Configuration**

Each tool can be configured through environment variables:

```bash
# Vector Search Configuration
VECTOR_SEARCH_LIMIT=15
VECTOR_SIMILARITY_THRESHOLD=0.7
EMBEDDING_MODEL=embedding-001
VECTOR_INDEX_NAME=msha_embeddings

# Graph Search Configuration  
GRAPH_TRAVERSAL_DEPTH=3
CYPHER_TIMEOUT_SECONDS=30
MAX_GRAPH_RESULTS=20
RELATIONSHIP_TYPES=CONTAINS,RELATES_TO,REQUIRES

# General Tool Configuration
ENABLE_FALLBACK_PROCESSING=true
MULTI_SOURCE_INTEGRATION=true
QUALITY_ENHANCEMENT=true
ERROR_RECOVERY_MODE=graceful
```

### **ool Initialization**

Tools are initialized with database connections and configuration:

```python
# Tool initialization pattern
from tools import vector, cypher, general

# Initialize tools with shared database connection
async def initialize_tools(neo4j_driver, config):
    """Initialize all tools with shared resources"""
    
    vector_tool = await vector.initialize(
        driver=neo4j_driver,
        embedding_model=config.EMBEDDING_MODEL,
        search_limit=config.VECTOR_SEARCH_LIMIT
    )
    
    cypher_tool = await cypher.initialize(
        driver=neo4j_driver,
        max_depth=config.GRAPH_TRAVERSAL_DEPTH,
        timeout=config.CYPHER_TIMEOUT_SECONDS
    )
    
    general_tool = await general.initialize(
        driver=neo4j_driver,
        fallback_enabled=config.ENABLE_FALLBACK_PROCESSING
    )
    
    return vector_tool, cypher_tool, general_tool
```

---

## **Quality Assessment**

### **Result Quality Metrics**

Each tool implements quality assessment for its results:

#### **Vector Tool Quality**
```python
def assess_vector_quality(results: List[Dict]) -> float:
    """Assess semantic search result quality"""
    
    quality_factors = {
        "relevance_scores": calculate_avg_relevance(results),
        "result_diversity": calculate_diversity_score(results),
        "confidence_consistency": calculate_confidence_consistency(results),
        "source_coverage": calculate_source_coverage(results)
    }
    
    return weighted_quality_score(quality_factors)
```

#### **Graph Tool Quality**
```python
def assess_graph_quality(results: Dict) -> float:
    """Assess knowledge graph traversal quality"""
    
    quality_factors = {
        "relationship_relevance": assess_relationship_quality(results),
        "entity_coverage": calculate_entity_coverage(results),
        "path_coherence": assess_traversal_paths(results),
        "regulatory_accuracy": validate_regulatory_connections(results)
    }
    
    return weighted_quality_score(quality_factors)
```

### **Confidence Scoring**

Advanced confidence calculation for each tool:

```python
class ConfidenceCalculator:
    def __init__(self, tool_type: str):
        self.tool_type = tool_type
        self.scoring_weights = self._load_scoring_weights()
    
    def calculate_confidence(self, results: Dict, query_context: Dict) -> float:
        """Calculate tool-specific confidence score"""
        
        confidence_factors = {
            "result_quality": self._assess_result_quality(results),
            "query_match": self._assess_query_alignment(results, query_context),
            "source_reliability": self._assess_source_reliability(results),
            "processing_success": self._assess_processing_metrics(results)
        }
        
        return self._weighted_confidence_score(confidence_factors)
```

---

## **Error Handling**

### **Fault Tolerance**

Each tool implements comprehensive error handling:

#### **Graceful Degradation**
```python
async def execute_with_fallback(primary_tool, fallback_tool, query):
    """Execute tool with automatic fallback"""
    
    try:
        # Try primary tool
        results = await primary_tool.execute(query)
        if validate_results(results):
            return results
    except Exception as e:
        log_tool_error(primary_tool.__name__, e)
    
    try:
        # Fallback to secondary tool
        results = await fallback_tool.execute(query)
        return results
    except Exception as e:
        log_tool_error(fallback_tool.__name__, e)
        return create_error_response(query)
```

#### **Circuit Breaker Integration**
```python
from circuit_breaker import CircuitBreaker

class ToolWithCircuitBreaker:
    def __init__(self, tool_func, failure_threshold=5):
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=60,
            expected_exception=(ToolException,)
        )
        self.tool_func = tool_func
    
    async def execute(self, query):
        """Execute tool with circuit breaker protection"""
        return await self.circuit_breaker.call(self.tool_func, query)
```

---

## **Usage Examples**

### **Basic Tool Usage**

#### **Individual Tool Execution**
```python
import asyncio
from tools import vector, cypher, general

async def example_individual_tools():
    """Example of using each tool individually"""
    
    query = "What are the ventilation requirements for underground coal mines?"
    
    # Vector search for semantic similarity
    vector_results = await vector.execute_vector_search(query, limit=10)
    print(f"Vector results: {len(vector_results)} chunks found")
    
    # Graph search for regulatory relationships
    graph_results = await cypher.execute_graph_search(query, max_depth=2)
    print(f"Graph results: {len(graph_results)} entities found")
    
    # General search for comprehensive coverage
    general_results = await general.execute_general_search(query, {})
    print(f"General results: {general_results['status']}")

# Run example
asyncio.run(example_individual_tools())
```

#### **Parallel Tool Execution**
```python
async def example_parallel_execution():
    """Example of parallel tool execution"""
    
    query = "methane detection equipment requirements"
    
    # Create parallel tasks
    tasks = [
        vector.execute_vector_search(query, limit=15),
        cypher.execute_graph_search(query, max_depth=3),
        general.execute_general_search(query, {"priority": "safety"})
    ]
    
    # Execute all tools simultaneously
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    vector_results, graph_results, general_results = results
    print(f"Parallel execution completed in ~3-5 seconds")
    
    return {
        "vector": vector_results,
        "graph": graph_results, 
        "general": general_results
    }
```

### **Advanced Integration**

#### **Tool Result Fusion**
```python
from tools import vector, cypher, general
from context_fusion import FusionEngine

async def example_tool_fusion():
    """Example of combining tool results using context fusion"""
    
    query = "safety training requirements for new miners"
    
    # Execute tools in parallel
    vector_task = asyncio.create_task(vector.execute_vector_search(query))
    graph_task = asyncio.create_task(cypher.execute_graph_search(query))
    
    vector_results, graph_results = await asyncio.gather(vector_task, graph_task)
    
    # Fuse results using Advanced Parallel Hybrid
    fusion_engine = FusionEngine(strategy="advanced_hybrid")
    fused_results = await fusion_engine.fuse_parallel_results(
        vector_results=vector_results,
        graph_results=graph_results,
        query_context={"domain": "safety_training"}
    )
    
    return fused_results
```

---

## **Performance Optimization**

### **Optimization Strategies**

#### **Caching**
```python
from functools import lru_cache
import asyncio_cache

class CachedVectorTool:
    @asyncio_cache.cached(ttl=300)  # 5-minute cache
    async def execute_vector_search(self, query: str, limit: int = 15):
        """Cached vector search for repeated queries"""
        return await self._raw_vector_search(query, limit)
    
    @lru_cache(maxsize=1000)
    def generate_embeddings(self, text: str):
        """Cache embeddings for repeated text"""
        return self._raw_embedding_generation(text)
```

#### **Connection Pooling**
```python
class ToolManager:
    def __init__(self, neo4j_uri, pool_size=10):
        self.connection_pool = Neo4jConnectionPool(
            uri=neo4j_uri,
            max_connections=pool_size
        )
    
    async def get_tool_connection(self):
        """Get database connection from pool"""
        return await self.connection_pool.acquire()
    
    async def release_tool_connection(self, connection):
        """Return connection to pool"""
        await self.connection_pool.release(connection)
```

#### **Batch Processing**
```python
async def batch_vector_search(queries: List[str], batch_size: int = 5):
    """Process multiple queries in batches"""
    
    results = []
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        
        # Process batch in parallel
        batch_tasks = [
            vector.execute_vector_search(query) for query in batch
        ]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)
    
    return results
```

---

## **Testing**

### **Tool Testing**

#### **Unit Tests**
```python
import pytest
from tools import vector, cypher, general

class TestVectorTool:
    @pytest.mark.asyncio
    async def test_vector_search_basic(self):
        """Test basic vector search functionality"""
        query = "mining safety equipment"
        results = await vector.execute_vector_search(query, limit=5)
        
        assert len(results) <= 5
        assert all('confidence' in result for result in results)
        assert all(result['confidence'] > 0.5 for result in results)
    
    @pytest.mark.asyncio
    async def test_vector_search_empty_query(self):
        """Test vector search with empty query"""
        with pytest.raises(ValueError):
            await vector.execute_vector_search("", limit=5)

class TestCypherTool:
    @pytest.mark.asyncio
    async def test_graph_search_basic(self):
        """Test basic graph search functionality"""
        query = "ventilation requirements"
        results = await cypher.execute_graph_search(query, max_depth=2)
        
        assert 'entities' in results
        assert 'relationships' in results
        assert len(results['entities']) > 0
```

#### **Integration Tests**
```python
class TestToolIntegration:
    @pytest.mark.asyncio
    async def test_parallel_tool_execution(self):
        """Test parallel execution of multiple tools"""
        query = "methane monitoring underground coal mines"
        
        start_time = time.time()
        
        # Execute tools in parallel
        vector_task = asyncio.create_task(vector.execute_vector_search(query))
        graph_task = asyncio.create_task(cypher.execute_graph_search(query))
        
        vector_results, graph_results = await asyncio.gather(vector_task, graph_task)
        
        execution_time = time.time() - start_time
        
        # Verify parallel execution is faster than sequential
        assert execution_time < 10  # Should complete in under 10 seconds
        assert len(vector_results) > 0
        assert len(graph_results['entities']) > 0
```

---

## **Troubleshooting**

### **Common Issues**

#### **Tool Initialization Errors**
```
Error: Failed to initialize vector tool
```
**Solution**:
- Verify Neo4j database connectivity
- Check vector index exists: `SHOW INDEXES`
- Validate embedding model configuration
- Ensure sufficient database permissions

#### **Performance Issues**
```
Warning: Tool execution timeout
```
**Solution**:
- Optimize Neo4j queries and indexes
- Increase timeout configurations
- Monitor database resource usage
- Consider query result limiting

#### **Quality Issues**
```
Warning: Low confidence scores
```
**Solution**:
- Review query preprocessing
- Validate embedding model performance
- Check knowledge graph completeness
- Adjust similarity thresholds

### **Debugging Tools**

#### **Tool Performance Monitoring**
```python
async def debug_tool_performance():
    """Debug tool performance and identify bottlenecks"""
    
    query = "test query for performance debugging"
    
    # Monitor vector tool
    vector_start = time.time()
    vector_results = await vector.execute_vector_search(query)
    vector_time = time.time() - vector_start
    
    # Monitor graph tool
    graph_start = time.time()
    graph_results = await cypher.execute_graph_search(query)
    graph_time = time.time() - graph_start
    
    print(f"Vector tool: {vector_time:.2f}s, {len(vector_results)} results")
    print(f"Graph tool: {graph_time:.2f}s, {len(graph_results['entities'])} entities")
```

#### **Result Quality Analysis**
```python
def analyze_tool_results(vector_results, graph_results):
    """Analyze and compare tool result quality"""
    
    vector_quality = assess_vector_quality(vector_results)
    graph_quality = assess_graph_quality(graph_results)
    
    print(f"Vector quality: {vector_quality:.2f}")
    print(f"Graph quality: {graph_quality:.2f}")
    
    if vector_quality < 0.7:
        print("Warning: Vector results may be low quality")
    if graph_quality < 0.7:
        print("Warning: Graph results may be low quality")
```

---

## **Contributing**

### **Development Guidelines**

1. **Follow Tool Patterns**: Maintain consistent interfaces across all tools
2. **Implement Error Handling**: Comprehensive error handling and recovery
3. **Add Performance Monitoring**: Include metrics collection in new tools
4. **Write Tests**: Unit and integration tests for all tool functionality
5. **Document Changes**: Update README and inline documentation

### **Adding New Tools**

#### **Tool Template**
```python
# tools/new_tool.py
from typing import Dict, List, Any
import asyncio

class NewTool:
    """Template for creating new agent tools"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.metrics = ToolMetrics()
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Main execution method for the tool"""
        start_time = time.time()
        
        try:
            # Implement tool logic here
            results = await self._process_query(query, **kwargs)
            
            # Update metrics
            self.metrics.update_success(time.time() - start_time, results)
            
            return results
            
        except Exception as e:
            self.metrics.update_error(time.time() - start_time, e)
            raise
    
    async def _process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """Tool-specific query processing logic"""
        # Implement your tool's core functionality
        pass
    
    def get_metrics(self) -> Dict:
        """Return tool performance metrics"""
        return self.metrics.to_dict()
```

#### **Tool Registration**
```python
# tools/__init__.py
from .vector import VectorTool
from .cypher import CypherTool
from .general import GeneralTool
from .new_tool import NewTool

# Tool registry for dynamic loading
AVAILABLE_TOOLS = {
    "vector": VectorTool,
    "cypher": CypherTool,
    "general": GeneralTool,
    "new_tool": NewTool
}

def get_tool(tool_name: str, config: Dict):
    """Factory function for creating tool instances"""
    if tool_name not in AVAILABLE_TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    return AVAILABLE_TOOLS[tool_name](config)
```

---

© 2025 Alexander Samuel Ricciardi - MRCA Backend Tools Module  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System 
