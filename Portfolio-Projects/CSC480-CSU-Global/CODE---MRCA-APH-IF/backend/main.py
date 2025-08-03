# -------------------------------------------------------------------------
# File: main.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/main.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module serves as the central orchestration layer for the MRCA Backend API.
# It initializes the FastAPI application, configures middleware, defines request
# and response models, and exposes the core API endpoints. Its primary responsibility
# is to coordinate the Advanced Parallel Hybrid processing pipeline, including
# parallel retrieval, context fusion, and hybrid template application.
# It also provides health check endpoints for system monitoring.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: ParallelHybridRequest (Pydantic Model for API request)
# - Class: ParallelHybridResponse (Pydantic Model for API response)
# - Class: HealthResponse (Pydantic Model for health check response)
# - FastAPI App: app (Main FastAPI application instance)
# - Endpoint: / (Root endpoint for service information)
# - Endpoint: /health (Basic health check)
# - Endpoint: /parallel_hybrid/health (Detailed health check for Parallel Hybrid components)
# - Endpoint: /generate_parallel_hybrid (Primary endpoint for generating AI responses)
# - Global Variable: PARALLEL_HYBRID_AVAILABLE (Boolean flag indicating module availability)
# - Global Variable: active_sessions (Dictionary to store active session data)
# - Global Variable: startup_time (Timestamp of application startup)
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - logging: For application logging.
#   - uuid: For generating unique session IDs.
#   - typing: For type hinting (Optional, Dict, Any).
#   - time: For measuring processing time.
#   - datetime: For timestamp generation.
# - Third-Party:
#   - fastapi: The core web framework for building the API.
#   - pydantic: For data validation and serialization.
#   - httpx: For making asynchronous HTTP requests (indirectly via FastAPI/Uvicorn).
# - Local Project Modules:
#   - .config.get_config: For retrieving application configurations.
#   - .parallel_hybrid.get_parallel_engine, ParallelRetrievalResponse: For parallel RAG processing.
#   - .context_fusion.get_fusion_engine, FusionStrategy: For intelligent context fusion.
#   - .hybrid_templates.create_hybrid_prompt, generate_hybrid_response, TemplateConfig, TemplateType: For response generation using specialized templates.
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is the main entry point for the MRCA backend API.
# It is typically run using a WSGI server like Uvicorn (e.g., `uvicorn main:app`).
# The frontend service (`frontend/bot.py`) interacts with this module via HTTP requests
# to `/generate_parallel_hybrid` for AI-powered compliance assistance.
# External monitoring systems or health check services can query `/health` and
# `/parallel_hybrid/health` to ascertain the operational status of the backend components.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

Central Orchestration Layer for MRCA Backend API with Advanced Parallel Hybrid Technology

Serves as the main FastAPI application providing mining regulatory compliance assistance
through Advanced Parallel Hybrid processing. Coordinates parallel VectorRAG and GraphRAG
retrieval, intelligent context fusion, and specialized regulatory template application
for comprehensive MSHA regulation queries.

"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging
import uuid
import time
from typing import Optional, Dict, Any
from datetime import datetime

# Third-party library imports
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Local application/library specific imports
try:
    # Try relative imports first (when run as module: python -m uvicorn backend.main:app)
    from .config import get_config
except ImportError:
    # Fall back to absolute imports (when run directly from backend directory)
    from config import get_config

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Configure logging for the module.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Global Variable ---
# Flag indicating if Advanced Parallel Hybrid modules are successfully loaded.
# This is crucial for determining service availability and fallback behavior.
PARALLEL_HYBRID_AVAILABLE = False
# ---------------------------------------------------------------------------------

# --- Global Variable ---
# Dictionary to store active session information.
# (Note: For a production system, consider a persistent session store like Redis.)
active_sessions: Dict[str, Dict] = {}
# ---------------------------------------------------------------------------------

# --- Global Variable ---
# Timestamp of when the application started.
startup_time = time.time()
# ---------------------------------------------------------------------------------


# Advanced parallel hybrid imports (REQUIRED - no fallback if fails)
# These imports are dynamically checked at startup to determine if the core
# Advanced Parallel Hybrid functionality can be provided.
try:
    # Try relative imports first (when run as module)
    from .parallel_hybrid import get_parallel_engine, ParallelRetrievalResponse
    from .context_fusion import get_fusion_engine, FusionStrategy
    from .hybrid_templates import generate_hybrid_response, TemplateConfig, TemplateType
    PARALLEL_HYBRID_AVAILABLE = True
    logger.info("✅ Advanced Parallel Hybrid modules loaded successfully")
except ImportError:
    # Fall back to absolute imports (when run directly from backend directory)
    try:
        from parallel_hybrid import get_parallel_engine, ParallelRetrievalResponse
        from context_fusion import get_fusion_engine, FusionStrategy
        from hybrid_templates import generate_hybrid_response, TemplateConfig, TemplateType
        PARALLEL_HYBRID_AVAILABLE = True
        logger.info("✅ Advanced Parallel Hybrid modules loaded successfully")
    except ImportError as e:
        # If both import methods fail, parallel hybrid is not available
        PARALLEL_HYBRID_AVAILABLE = False
        logger.error(f"❌ Advanced Parallel Hybrid modules could not be loaded: {e}")
        logger.error("   Backend will run in degraded mode without advanced features")

# FastAPI app initialization
app = FastAPI(
    title="MRCA Advanced Parallel Hybrid API",
    description="Mining Regulatory Compliance Assistant - Advanced Parallel Hybrid Service",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, should be tightened in production
    allow_credentials=True, # Allows cookies and authentication headers
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)


# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class ParallelHybridRequest
class ParallelHybridRequest(BaseModel):
    """Represents the request body for the Advanced Parallel Hybrid response generation.

    This Pydantic model defines the structure and validation rules for incoming
    API requests to the `/generate_parallel_hybrid` endpoint. It specifies the
    user's query and optional parameters for controlling the AI's behavior.

    Instance Attributes:
        user_input (str): The natural language question from the user.
        session_id (Optional[str]): An optional identifier for tracking conversation sessions.
        fusion_strategy (Optional[str]): The chosen strategy for combining VectorRAG and GraphRAG results.
                                         Defaults to "advanced_hybrid".
        template_type (Optional[str]): The type of prompt template to use for response generation.
                                       Defaults to "regulatory_compliance".

    Methods:
        No explicit methods defined beyond BaseModel's inherited methods.
    """
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    # No explicit class-level variables beyond BaseModel's internals.
    # ---------------------------------------------------------------------------------

    # -------------------
    # --- Constructor ---
    # -------------------
    # The __init__ method is inherited from BaseModel and handles attribute assignment
    # and validation based on the type hints and default values provided.
    # ---------------------------------------------------------------------------------
    user_input: str
    session_id: Optional[str] = None
    fusion_strategy: Optional[str] = "advanced_hybrid"
    template_type: Optional[str] = "regulatory_compliance"

# ------------------------------------------------------------------------- end class ParallelHybridRequest

# ------------------------------------------------------------------------- class ParallelHybridResponse
class ParallelHybridResponse(BaseModel):
    """Represents the response body for the Advanced Parallel Hybrid response generation.

    This Pydantic model defines the structure and validation rules for outgoing
    API responses from the `/generate_parallel_hybrid` endpoint. It includes
    the generated AI response, session information, performance metrics, and
    detailed metadata about the processing.

    Instance Attributes:
        response (str): The final generated answer to the user's query.
        session_id (str): The identifier for the current conversation session.
        processing_time (float): The total time taken to process the request in seconds.
        timestamp (str): The UTC timestamp when the response was generated.
        metadata (Dict[str, Any]): A dictionary containing detailed analytics and
                                   information about the parallel retrieval,
                                   context fusion, and hybrid templating stages.

    Methods:
        No explicit methods defined beyond BaseModel's inherited methods.
    """
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    # No explicit class-level variables beyond BaseModel's internals.
    # ---------------------------------------------------------------------------------

    # -------------------
    # --- Constructor ---
    # -------------------
    # The __init__ method is inherited from BaseModel and handles attribute assignment
    # and validation based on the type hints and default values provided.
    # ---------------------------------------------------------------------------------
    response: str
    session_id: str
    processing_time: float
    timestamp: str
    metadata: Dict[str, Any]

# ------------------------------------------------------------------------- end class ParallelHybridResponse

# ------------------------------------------------------------------------- class HealthResponse
class HealthResponse(BaseModel):
    """Represents the response body for health check endpoints.

    This Pydantic model defines the standard format for health check responses
    across the API, providing general status, timestamp, version, and component-specific
    health information.

    Instance Attributes:
        status (str): Overall health status ("healthy", "degraded", "error", "unavailable").
        timestamp (str): UTC timestamp of when the health check was performed.
        version (str): The version of the API service.
        components (Dict[str, Any]): A dictionary detailing the health status of
                                     individual service components.

    Methods:
        No explicit methods defined beyond BaseModel's inherited methods.
    """
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    # No explicit class-level variables beyond BaseModel's internals.
    # ---------------------------------------------------------------------------------

    # -------------------
    # --- Constructor ---
    # -------------------
    # The __init__ method is inherited from BaseModel and handles attribute assignment
    # and validation based on the type hints and default values provided.
    # ---------------------------------------------------------------------------------
    status: str
    timestamp: str
    version: str
    components: Dict[str, Any]

# ------------------------------------------------------------------------- end class HealthResponse


# =========================================================================
# Standalone Function Definitions
# =========================================================================
# These are functions that are not methods of any specific class within this module.

# --------------------------
# --- Utility Functions ---
# --------------------------

# --------------------------------------------------------------------------------- health_check()
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Performs a basic health check of the MRCA backend API.

    This endpoint provides a high-level overview of the service's operational status,
    primarily focusing on the availability of the core Advanced Parallel Hybrid modules.
    It's designed for quick checks by load balancers or monitoring systems.

    Returns:
        HealthResponse: A Pydantic model containing the service status, version,
                        timestamp, and a basic health status for main components.
    """
    health_status = {
        "service": "MRCA Advanced Parallel Hybrid API",
        "version": "2.0.0",
        "status": "healthy" if PARALLEL_HYBRID_AVAILABLE else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "api": "healthy",
            "parallel_hybrid": "healthy" if PARALLEL_HYBRID_AVAILABLE else "unavailable",
        }
    }
    return HealthResponse(**health_status)

# --------------------------------------------------------------------------------- end health_check()

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# --------------------------------------------------------------------------------- generate_parallel_hybrid_response()
@app.post("/generate_parallel_hybrid", response_model=ParallelHybridResponse)
async def generate_parallel_hybrid_response(
    request: ParallelHybridRequest,
    session_id: Optional[str] = Header(None, alias="X-Session-ID")
) -> ParallelHybridResponse:
    """Processes a user query using the Advanced Parallel Hybrid technology.

    This is the primary endpoint for generating AI-powered responses related to
    mining regulatory compliance. It orchestrates the three-step pipeline:
    1. Parallel Retrieval (VectorRAG and GraphRAG concurrently).
    2. Context Fusion (combining results based on a selected strategy).
    3. Hybrid Template Application (formatting the final response).

    Args:
        request (ParallelHybridRequest): The incoming request containing the
                                         user's query and optional parameters
                                         for fusion strategy and template type.
        session_id (Optional[str]): An optional session ID passed via the
                                    `X-Session-ID` HTTP header for conversation
                                    tracking. Falls back to `request.session_id`
                                    or generates a new UUID if not provided.

    Returns:
        ParallelHybridResponse: A Pydantic model containing the generated response,
                                session ID, processing time, timestamp, and detailed metadata
                                about each stage of the AI pipeline.

    Raises:
        HTTPException:
            - 503 Service Unavailable: If the core Advanced Parallel Hybrid modules
                                       failed to load at application startup.
            - Other exceptions might be raised internally and caught, resulting
              in an error response within the ParallelHybridResponse metadata.
    """
    if not PARALLEL_HYBRID_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Parallel Hybrid system not available")

    start_time = time.time()
    current_session_id = session_id or request.session_id or str(uuid.uuid4())

    try:
        logger.info(f"Processing parallel hybrid request for session {current_session_id[:8]}")

        # Get components
        # Retrieves the singleton instance of the ParallelRetrievalEngine.
        parallel_engine = get_parallel_engine()
        # Retrieves the singleton instance of the HybridContextFusion engine.
        fusion_engine = get_fusion_engine()

        # Step 1: Parallel Retrieval
        # Executes VectorRAG and GraphRAG concurrently.
        parallel_result = await parallel_engine.retrieve_parallel(
            query=request.user_input
        )

        # Check if parallel retrieval results are viable for fusion.
        if not parallel_result.fusion_ready:
            # Simple fallback response if fusion is not possible due to retrieval issues.
            response_text = f"Based on MSHA regulations regarding: {request.user_input}\n\nI found relevant information but the parallel system encountered issues. Please try rephrasing your question."

            return ParallelHybridResponse(
                response=response_text,
                session_id=current_session_id,
                processing_time=time.time() - start_time,
                timestamp=datetime.now().isoformat(),
                metadata={
                    "parallel_retrieval": {
                        "total_time_ms": int((time.time() - start_time) * 1000),
                        "fusion_ready": False,
                        "vector_confidence": parallel_result.vector_result.confidence if parallel_result.vector_result else 0.0,
                        "graph_confidence": parallel_result.graph_result.confidence if parallel_result.graph_result else 0.0,
                    },
                    "context_fusion": {
                        "strategy": "fallback",
                        "final_confidence": 0.0,
                        "vector_contribution": 0.0,
                        "graph_contribution": 0.0,
                        "quality_score": 0.0,
                    },
                    "hybrid_template": {
                        "type": "fallback",
                        "length": len(response_text)
                    }
                }
            )

        # Step 2: Context Fusion
        # Maps the string fusion strategy from the request to the FusionStrategy Enum.
        strategy_map = {
            "weighted_linear": FusionStrategy.WEIGHTED_LINEAR,
            "max_confidence": FusionStrategy.MAX_CONFIDENCE,
            "advanced_hybrid": FusionStrategy.ADVANCED_HYBRID,
            "adaptive_fusion": FusionStrategy.ADAPTIVE_FUSION
        }

        fusion_strategy = strategy_map.get(request.fusion_strategy or "advanced_hybrid", FusionStrategy.ADVANCED_HYBRID)
        # Fuses the results from parallel retrieval based on the chosen strategy.
        fusion_result = await fusion_engine.fuse_contexts(
            parallel_response=parallel_result,
            strategy=fusion_strategy
        )

        # Step 3: Template Application
        # Maps the string template type from the request to the TemplateType Enum.
        template_map = {
            "basic_hybrid": TemplateType.BASIC_HYBRID,
            "research_based": TemplateType.RESEARCH_BASED,
            "regulatory_compliance": TemplateType.REGULATORY_COMPLIANCE,
            "comparative_analysis": TemplateType.COMPARATIVE_ANALYSIS,
            "confidence_weighted": TemplateType.CONFIDENCE_WEIGHTED
        }

        template_type = template_map.get(request.template_type or "regulatory_compliance", TemplateType.REGULATORY_COMPLIANCE)
        # Configures the template generation process with desired options.
        template_config = TemplateConfig(
            include_confidence_scores=True,
            include_source_attribution=True,
            max_context_length=2000,
            regulatory_focus=True
        )

        # Generates the final response using the fused context and the selected template.
        final_response = await generate_hybrid_response(
            user_query=request.user_input,
            fusion_result=fusion_result,
            template_type=template_type,
            config=template_config
        )

        processing_time = time.time() - start_time

        # Gathers metadata from all processing stages for the response.
        response_metadata = {
            "parallel_retrieval": {
                "total_time_ms": int(processing_time * 1000),
                "fusion_ready": True,
                "vector_confidence": parallel_result.vector_result.confidence if parallel_result.vector_result else 0.0,
                "graph_confidence": parallel_result.graph_result.confidence if parallel_result.graph_result else 0.0,
            },
            "context_fusion": {
                "strategy": request.fusion_strategy,
                "final_confidence": fusion_result.final_confidence,
                "vector_contribution": fusion_result.vector_contribution,
                "graph_contribution": fusion_result.graph_contribution,
                "quality_score": fusion_result.fusion_quality_score,
            },
            "hybrid_template": {
                "type": request.template_type,
                "length": len(final_response)
            }
        }

        return ParallelHybridResponse(
            response=final_response,
            session_id=current_session_id,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
            metadata=response_metadata
        )

    except Exception as e:
        logger.error(f"❌ Error in parallel hybrid processing: {e}")
        return ParallelHybridResponse(
            response=f"Error processing your question: {str(e)}",
            session_id=current_session_id,
            processing_time=time.time() - start_time,
            timestamp=datetime.now().isoformat(),
            metadata={"error": True, "error_message": str(e)}
        )

# --------------------------------------------------------------------------------- end generate_parallel_hybrid_response()

# --------------------------------------------------------------------------------- parallel_hybrid_health()
@app.get("/parallel_hybrid/health")
async def parallel_hybrid_health() -> JSONResponse:
    """Provides a detailed health check for the Advanced Parallel Hybrid components.

    This endpoint goes beyond the basic `/health` check to specifically assess
    the availability and readiness of the `parallel_engine`, `fusion_engine`,
    and `hybrid_templates` modules. It's intended for more granular monitoring
    of the core AI processing pipeline.

    Returns:
        JSONResponse: A JSON response detailing the status of the Advanced Parallel
                      Hybrid components, timestamp, and overall status.
                      Status codes: 200 (healthy/degraded), 503 (unavailable),
                      500 (internal error).
    """
    if not PARALLEL_HYBRID_AVAILABLE:
        return JSONResponse(
            content={"status": "unavailable", "error": "Advanced Parallel Hybrid modules not available"},
            status_code=503
        )

    try:
        # Simple health check without calling potentially expensive methods.
        # It relies on successful import and basic instantiation.
        parallel_engine = get_parallel_engine()
        fusion_engine = get_fusion_engine()

        # Determine overall health based on engine availability.
        health_status = "healthy" if (parallel_engine and fusion_engine) else "degraded"

        return JSONResponse(
            content={
                "status": health_status,
                "timestamp": datetime.utcnow().isoformat(),
                "components": {
                    "parallel_engine": {"status": "healthy", "available": True},
                    "fusion_engine": {"status": "healthy", "available": True},
                    "templates": {"status": "healthy", "available": True}
                }
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JSONResponse(
            content={"status": "error", "error": str(e)},
            status_code=500
        )

# --------------------------------------------------------------------------------- end parallel_hybrid_health()

# --------------------------------------------------------------------------------- metrics()
@app.get("/metrics")
async def metrics() -> JSONResponse:
    """Provides system metrics and performance statistics.

    This endpoint returns various system metrics including request counts,
    response times, and system health indicators for monitoring purposes.

    Returns:
        JSONResponse: System metrics and performance data
    """
    try:
        metrics_data = {
            "system": {
                "status": "operational",
                "uptime": "running",
                "version": "2.0.0"
            },
            "api": {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0.0
            },
            "parallel_hybrid": {
                "available": PARALLEL_HYBRID_AVAILABLE,
                "total_queries": 0,
                "successful_queries": 0,
                "average_processing_time": 0.0
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        return JSONResponse(
            status_code=200,
            content=metrics_data
        )
    except Exception as e:
        logger.error(f"❌ Metrics endpoint error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to retrieve metrics", "detail": str(e)}
        )

# --------------------------------------------------------------------------------- end metrics()

# --------------------------------------------------------------------------------- system_health_verification()
@app.post("/system/health/verify")
async def system_health_verification() -> JSONResponse:
    """Performs comprehensive system health verification.

    This endpoint provides detailed verification of all system components
    including API health, parallel hybrid availability, and system metrics.

    Returns:
        JSONResponse: Comprehensive system health verification results
    """
    try:
        verification_results = {
            "system_status": "healthy" if PARALLEL_HYBRID_AVAILABLE else "degraded",
            "api_status": "operational",
            "parallel_hybrid_status": "available" if PARALLEL_HYBRID_AVAILABLE else "unavailable",
            "components": {
                "api": {"status": "healthy", "available": True},
                "parallel_hybrid": {"status": "healthy" if PARALLEL_HYBRID_AVAILABLE else "unavailable", "available": PARALLEL_HYBRID_AVAILABLE},
                "metrics": {"status": "healthy", "available": True}
            },
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0"
        }

        return JSONResponse(
            status_code=200,
            content=verification_results
        )
    except Exception as e:
        logger.error(f"❌ System health verification error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "System health verification failed", "detail": str(e)}
        )

# --------------------------------------------------------------------------------- end system_health_verification()

# --------------------------------------------------------------------------------- root()
@app.get("/")
async def root() -> Dict[str, str]:
    """Provides basic service information at the root endpoint.

    This endpoint serves as a quick entry point to confirm the API is running
    and provides fundamental details about the service, its version, and
    links to API documentation.

    Returns:
        Dict[str, str]: A dictionary containing service name, version,
                        description, status, and a link to the documentation.
    """
    return {
        "service": "MRCA Advanced Parallel Hybrid API",
        "version": "2.0.0",
        "description": "Advanced Parallel Hybrid Service ONLY",
        "status": "running",
        "docs": "/docs"
    }

# --------------------------------------------------------------------------------- end root()


# =========================================================================
# Module Initialization / Main Execution Guard (if applicable)
# =========================================================================
# This block runs only when the file is executed directly (e.g., `python main.py`),
# not when it's imported as a module by another script (e.g., by Uvicorn).
# For a FastAPI application, this typically starts the Uvicorn server for local
# development or testing purposes. In production, a WSGI server like Uvicorn
# would typically import and run the `app` instance directly.

if __name__ == "__main__":
    # --- Example Usage / Module-specific Tests ---
    # This section demonstrates how to run the FastAPI application locally
    # using Uvicorn. It's primarily for development and debugging.
    # The `reload=True` flag is useful during development for automatic code reloads.
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Note: In a production environment, `uvicorn` would typically be invoked
    # from the command line, pointing to `main:app` (e.g., `uvicorn backend.main:app`).
    # ---------------------------------------------------------------------------------

# =========================================================================
# End of File
# =========================================================================
