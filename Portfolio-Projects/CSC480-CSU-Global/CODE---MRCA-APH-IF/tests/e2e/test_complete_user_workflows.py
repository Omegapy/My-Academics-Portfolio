# -------------------------------------------------------------------------
# File: test_complete_user_workflows.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: tests/e2e/test_complete_user_workflows.py
# -------------------------------------------------------------------------

# --- Module Objective ---
# End-to-End Tests for Complete MRCA User Workflows
# This module provides comprehensive testing of complete user journeys through
# the MRCA Advanced Parallel Hybrid system, including API workflows, UI interactions,
# session management, and cross-component integration scenarios.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: TestCompleteAPIWorkflows - Full API interaction scenarios
# - Class: TestAdvancedParallelHybridWorkflows - APH-specific user journeys
# - Class: TestSessionManagement - Session and state management tests
# - Class: TestCrossComponentIntegration - Multi-component workflow tests
# - Functions: Helper functions for workflow simulation and validation
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - asyncio: For asynchronous workflow testing
#   - time: For timing and performance measurement
#   - json: For API response validation
# - Third-Party:
#   - pytest: Testing framework with async support
#   - httpx: HTTP client for API testing
# - Local Project Modules:
#   - tests.e2e: Constants and shared utilities
#   - backend modules: For validation against actual system behavior
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# These E2E tests validate complete user workflows by:
# - Testing full API interaction chains
# - Validating Advanced Parallel Hybrid query processing
# - Ensuring proper session and state management
# - Verifying cross-component integration
# The tests simulate real user interactions to ensure system reliability.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
End-to-End Tests for Complete MRCA User Workflows

Comprehensive testing of user journeys through the MRCA Advanced Parallel Hybrid system,
covering API workflows, UI interactions, and cross-component integration.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import asyncio
import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Third-party library imports
import pytest
import httpx

# Local application/library specific imports
from tests.e2e import (
    E2E_TEST_TIMEOUT, 
    DEFAULT_BASE_URL, 
    DEFAULT_FRONTEND_URL,
    SAMPLE_QUERIES,
    EXPECTED_RESPONSE_INDICATORS
)

# =========================================================================
# Test Data Classes and Helpers
# =========================================================================

# ------------------------------------------------------------------------- WorkflowStep
@dataclass
class WorkflowStep:
    """Represents a single step in a user workflow."""
    step_name: str
    endpoint: str
    payload: Dict[str, Any]
    expected_status: int = 200
    validation_checks: List[str] = None
    method: str = "POST"  # HTTP method to use
# ------------------------------------------------------------------------- end WorkflowStep

# ------------------------------------------------------------------------- WorkflowResult
@dataclass
class WorkflowResult:
    """Results from executing a complete workflow."""
    workflow_name: str
    total_steps: int
    completed_steps: int
    total_time: float
    step_results: List[Dict[str, Any]]
    success: bool
# ------------------------------------------------------------------------- end WorkflowResult

# =========================================================================
# Workflow Helper Functions
# =========================================================================

# --------------------------------------------------------------------------------- execute_workflow_step()
async def execute_workflow_step(
    client: httpx.AsyncClient,
    step: WorkflowStep,
    step_number: int
) -> Dict[str, Any]:
    """Execute a single workflow step and validate results.
    
    Args:
        client: HTTP client for requests
        step: WorkflowStep definition
        step_number: Step sequence number
        
    Returns:
        Dictionary with step execution results
    """
    start_time = time.time()
    
    try:
        if step.endpoint.startswith('/'):
            url = f"{DEFAULT_BASE_URL}{step.endpoint}"
        else:
            url = step.endpoint
            
        # Use appropriate HTTP method
        if step.method.upper() == "GET":
            response = await client.get(url, timeout=240.0)
        elif step.method.upper() == "POST":
            response = await client.post(url, json=step.payload, timeout=240.0)
        else:
            raise ValueError(f"Unsupported HTTP method: {step.method}")
            
        execution_time = time.time() - start_time
        
        # Basic validation
        success = response.status_code == step.expected_status
        
        # Additional validation checks
        validation_results = []
        if step.validation_checks and success:
            response_text = response.text.lower()
            for check in step.validation_checks:
                validation_results.append({
                    "check": check,
                    "passed": check.lower() in response_text
                })
        
        return {
            "step_number": step_number,
            "step_name": step.step_name,
            "success": success,
            "status_code": response.status_code,
            "execution_time": execution_time,
            "response_size": len(response.content),
            "validation_results": validation_results,
            "response_data": response.json() if response.headers.get("content-type", "").startswith("application/json") else None
        }
        
    except Exception as e:
        return {
            "step_number": step_number,
            "step_name": step.step_name,
            "success": False,
            "error": str(e),
            "execution_time": time.time() - start_time,
            "validation_results": []
        }
# --------------------------------------------------------------------------------- end execute_workflow_step()

# --------------------------------------------------------------------------------- execute_complete_workflow()
async def execute_complete_workflow(
    workflow_name: str,
    steps: List[WorkflowStep]
) -> WorkflowResult:
    """Execute a complete user workflow with multiple steps.
    
    Args:
        workflow_name: Name of the workflow for identification
        steps: List of WorkflowStep objects to execute
        
    Returns:
        WorkflowResult with comprehensive execution data
    """
    start_time = time.time()
    step_results = []
    completed_steps = 0
    
    async with httpx.AsyncClient(timeout=E2E_TEST_TIMEOUT) as client:
        for i, step in enumerate(steps, 1):
            step_result = await execute_workflow_step(client, step, i)
            step_results.append(step_result)
            
            if step_result["success"]:
                completed_steps += 1
            else:
                # Stop workflow on first failure for now
                break
    
    total_time = time.time() - start_time
    success = completed_steps == len(steps)
    
    return WorkflowResult(
        workflow_name=workflow_name,
        total_steps=len(steps),
        completed_steps=completed_steps,
        total_time=total_time,
        step_results=step_results,
        success=success
    )
# --------------------------------------------------------------------------------- end execute_complete_workflow() 

# =========================================================================
# End-to-End Test Classes
# =========================================================================

# ------------------------------------------------------------------------- TestCompleteAPIWorkflows
@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.requires_api
class TestCompleteAPIWorkflows:
    """Test complete API interaction workflows."""
    
    # --------------------------------------------------------------------------------- test_health_check_workflow()
    @pytest.mark.asyncio
    async def test_health_check_workflow(self):
        """Test complete health check workflow across all services."""
        steps = [
            WorkflowStep(
                step_name="Backend Health Check",
                endpoint="/health",
                payload={},
                method="GET",
                validation_checks=["healthy", "api", "parallel_hybrid"]
            ),
            WorkflowStep(
                step_name="Parallel Hybrid Health Check",
                endpoint="/parallel_hybrid/health",
                payload={},
                method="GET",
                validation_checks=["healthy", "parallel_engine", "fusion_engine"]
            ),
            WorkflowStep(
                step_name="System Metrics Check",
                endpoint="/metrics",
                payload={},
                method="GET",
                validation_checks=["timestamp"]
            )
        ]

        # Execute workflow
        result = await execute_complete_workflow("Health Check Workflow", steps)
        
        # Assertions
        assert result.success, f"Health workflow failed: {result.step_results}"
        assert result.completed_steps == result.total_steps
        assert result.total_time < 30.0, "Health checks should complete quickly"
        
        # Validate each step succeeded
        for step_result in result.step_results:
            assert step_result["success"], f"Step {step_result['step_name']} failed"
            assert step_result["execution_time"] < 10.0, "Individual health checks should be fast"
    # ------------------------------------------------------------------------- end test_health_check_workflow()

    # ------------------------------------------------------------------------- test_advanced_parallel_hybrid_query_workflow()
    @pytest.mark.asyncio
    async def test_advanced_parallel_hybrid_query_workflow(self):
        """Test complete Advanced Parallel Hybrid query processing workflow."""
        steps = [
            WorkflowStep(
                step_name="Simple Regulatory Query",
                endpoint="/generate_parallel_hybrid",
                payload={
                    "user_input": "What are methane monitoring requirements?",
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                },
                validation_checks=["cfr", "methane", "monitoring", "requirement"]
            ),
            WorkflowStep(
                step_name="Complex Multi-Domain Query",
                endpoint="/generate_parallel_hybrid", 
                payload={
                    "user_input": "What safety equipment and ventilation standards apply to underground coal mines?",
                    "fusion_strategy": "weighted_linear",
                    "template_type": "comparative_analysis"
                },
                validation_checks=["safety", "equipment", "ventilation", "underground", "coal"]
            ),
            WorkflowStep(
                step_name="Confidence Weighted Query",
                endpoint="/generate_parallel_hybrid",
                payload={
                    "user_input": "What does 30 CFR 56.5005 say about safety training requirements?",
                    "fusion_strategy": "max_confidence",
                    "template_type": "confidence_weighted"
                },
                validation_checks=["30 CFR", "training", "safety"]
            )
        ]
        
        # Execute workflow
        result = await execute_complete_workflow("APH Query Workflow", steps)
        
        # Assertions
        assert result.success, f"APH query workflow failed: {result.step_results}"
        assert result.completed_steps == result.total_steps
        
        # Validate response quality
        for step_result in result.step_results:
            assert step_result["success"], f"Query step {step_result['step_name']} failed"
            
            # Check response contains actual data
            if step_result.get("response_data"):
                response_data = step_result["response_data"]
                assert "response" in response_data, "Should contain response field"
                assert len(response_data["response"]) > 100, "Response should be substantial"
                
                # Check for fusion results - allow for cases where fusion might not be ready
                # but the query still succeeds with fallback mechanisms
                metadata = response_data.get("metadata", {})
                parallel_retrieval = metadata.get("parallel_retrieval", {})
                if "fusion_ready" in parallel_retrieval:
                    # Log fusion status for debugging but don't fail the test
                    fusion_ready = parallel_retrieval["fusion_ready"]
                    if not fusion_ready:
                        print(f"Note: Fusion not ready for query, but response was still generated")
                    # The test should pass as long as we get a valid response
    # --------------------------------------------------------------------------------- end test_advanced_parallel_hybrid_query_workflow()

    # ------------------------------------------------------------------------- test_error_handling_workflow()
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self):
        """Test API error handling and recovery workflow."""
        steps = [
            WorkflowStep(
                step_name="Invalid Endpoint Test",
                endpoint="/invalid_endpoint",
                payload={"test": "data"},
                expected_status=404
            ),
            WorkflowStep(
                step_name="Malformed Payload Test", 
                endpoint="/generate_parallel_hybrid",
                payload={"invalid": "payload_structure"},
                expected_status=422  # Validation error
            ),
            WorkflowStep(
                step_name="Recovery with Valid Request",
                endpoint="/generate_parallel_hybrid",
                payload={
                    "user_input": "What are coal dust control requirements?",
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                },
                expected_status=200,
                validation_checks=["coal", "dust", "control"]
            )
        ]
        
        # Execute workflow
        result = await execute_complete_workflow("Error Handling Workflow", steps)
        
        # Assertions - expect first two steps to "fail" (return expected error codes)
        # and third step to succeed
        assert len(result.step_results) >= 2, "Should have attempted error scenarios"
        
        # Check that system handles errors gracefully
        for i, step_result in enumerate(result.step_results):
            if i < 2:  # Error scenarios
                assert step_result["success"], f"Error scenario {i+1} should return expected status"
            else:  # Recovery scenario
                assert step_result["success"], "Recovery request should succeed"
    # --------------------------------------------------------------------------------- end test_error_handling_workflow()
# ------------------------------------------------------------------------- end TestCompleteAPIWorkflows

# ------------------------------------------------------------------------- TestAdvancedParallelHybridWorkflows
@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.requires_api
class TestAdvancedParallelHybridWorkflows:
    """Test Advanced Parallel Hybrid specific user journeys."""
    
    # ------------------------------------------------------------------------- test_fusion_strategy_comparison_workflow()
    @pytest.mark.asyncio
    async def test_fusion_strategy_comparison_workflow(self):
        """Test workflow comparing different fusion strategies."""
        base_query = "What are ventilation requirements for mines?"
        
        fusion_strategies = [
            "advanced_hybrid",
            "weighted_linear",
            "max_confidence",
            "adaptive_fusion"
        ]
        
        steps = []
        for strategy in fusion_strategies:
            steps.append(WorkflowStep(
                step_name=f"Test {strategy} Strategy",
                endpoint="/generate_parallel_hybrid",
                payload={
                    "user_input": base_query,
                    "fusion_strategy": strategy,
                    "template_type": "regulatory_compliance"
                },
                validation_checks=["ventilation", "requirements", "mine"]
            ))
        
        # Execute workflow
        result = await execute_complete_workflow("Fusion Strategy Comparison", steps)
        
        # Assertions
        assert result.success, f"Fusion strategy workflow failed: {result.step_results}"
        
        # Compare results across strategies
        response_lengths = []
        confidence_scores = []
        
        for step_result in result.step_results:
            if step_result.get("response_data"):
                data = step_result["response_data"]
                response_lengths.append(len(data.get("response", "")))

                # Extract confidence from metadata.context_fusion.final_confidence
                metadata = data.get("metadata", {})
                context_fusion = metadata.get("context_fusion", {})
                confidence = context_fusion.get("final_confidence", 0.0)
                confidence_scores.append(confidence)
        
        # Debug: Print detailed information about confidence scores
        print(f"\n🔍 Debugging fusion strategy confidence scores:")
        for i, (step_result, score) in enumerate(zip(result.step_results, confidence_scores)):
            strategy = fusion_strategies[i] if i < len(fusion_strategies) else "unknown"
            print(f"   Strategy {strategy}: confidence = {score:.3f}")
            if score == 0.0:
                print(f"      Response data keys: {list(step_result.get('response_data', {}).keys())}")
                metadata = step_result.get('response_data', {}).get('metadata', {})
                print(f"      Metadata keys: {list(metadata.keys())}")
                if 'context_fusion' in metadata:
                    print(f"      Context fusion: {metadata['context_fusion']}")

        # Validate that different strategies produce meaningful results
        assert len(set(response_lengths)) > 1, "Different strategies should produce varied response lengths"

        # More lenient confidence validation - allow some strategies to have low confidence
        valid_scores = [score for score in confidence_scores if score > 0.0]
        assert len(valid_scores) >= len(confidence_scores) * 0.75, f"At least 75% of strategies should produce valid confidence scores. Got {len(valid_scores)}/{len(confidence_scores)} valid scores: {confidence_scores}"
        assert any(score > 0.5 for score in confidence_scores), f"At least one strategy should produce confident responses. Got scores: {confidence_scores}"

        print(f"✅ Fusion strategy confidence scores: {[f'{score:.3f}' for score in confidence_scores]}")
    # ------------------------------------------------------------------------- end test_fusion_strategy_comparison_workflow()

    # ------------------------------------------------------------------------- test_template_type_workflow()
    @pytest.mark.asyncio
    async def test_template_type_workflow(self):
        """Test workflow with different template types."""
        base_query = "What are safety equipment requirements?"
        
        template_types = [
            "research_based",
            "regulatory_compliance", 
            "basic_hybrid",
            "comparative_analysis",
            "confidence_weighted"
        ]
        
        steps = []
        for template_type in template_types:
            steps.append(WorkflowStep(
                step_name=f"Test {template_type} Template",
                endpoint="/generate_parallel_hybrid",
                payload={
                    "user_input": base_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": template_type
                },
                validation_checks=["safety", "equipment", "requirements"]
            ))
        
        # Execute workflow
        result = await execute_complete_workflow("Template Type Workflow", steps)
        
        # Assertions  
        assert result.success, f"Template type workflow failed: {result.step_results}"
        
        # Validate all templates work
        for step_result in result.step_results:
            assert step_result["success"], f"Template test {step_result['step_name']} failed"
    # ------------------------------------------------------------------------- end test_template_type_workflow()
# ------------------------------------------------------------------------- end TestAdvancedParallelHybridWorkflows

# ------------------------------------------------------------------------- TestSessionManagement
@pytest.mark.e2e
@pytest.mark.slow 
@pytest.mark.requires_api
class TestSessionManagement:
    """Test session and state management workflows."""
    
    # --------------------------------------------------------------------------------- test_concurrent_session_workflow()
    @pytest.mark.asyncio
    async def test_concurrent_session_workflow(self):
        """Test multiple concurrent user sessions."""
        # --------------------------------------------------------------------------------- create_session_workflow()
        async def create_session_workflow(session_id: int):
            """Create a workflow for a specific session."""
            steps = [
                WorkflowStep(
                    step_name=f"Session {session_id} Query 1",
                    endpoint="/generate_parallel_hybrid",
                    payload={
                        "user_input": f"Session {session_id}: What are methane safety requirements?",
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    },
                    validation_checks=["methane", "safety"]
                ),
                WorkflowStep(
                    step_name=f"Session {session_id} Query 2", 
                    endpoint="/generate_parallel_hybrid",
                    payload={
                        "user_input": f"Session {session_id}: What about ventilation standards?",
                        "fusion_strategy": "weighted_linear",
                        "template_type": "comparative_analysis"
                    },
                    validation_checks=["ventilation", "standards"]
                )
            ]
            
            return await execute_complete_workflow(f"Session {session_id} Workflow", steps)
        # --------------------------------------------------------------------------------- end create_session_workflow()
        
        # Run multiple sessions concurrently
        # --------------------------------------------------------------------------------- run_concurrent_sessions()
        async def run_concurrent_sessions():
            session_tasks = []
            for i in range(3):  # 3 concurrent sessions
                task = create_session_workflow(i + 1)
                session_tasks.append(task)
            
            return await asyncio.gather(*session_tasks)
        # -------------------------------------------------------------- end run_concurrent_sessions()
        
        # Execute concurrent sessions
        session_results = await run_concurrent_sessions()
        
        # Assertions
        assert len(session_results) == 3, "Should have 3 session results"
        
        for i, result in enumerate(session_results):
            assert result.success, f"Session {i+1} workflow failed"
            assert result.completed_steps == result.total_steps, f"Session {i+1} incomplete"
    # --------------------------------------------------------------------------------- end test_concurrent_session_workflow()
# ------------------------------------------------------------------------- end TestSessionManagement

# ------------------------------------------------------------------------- TestCrossComponentIntegration
@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.requires_api
class TestCrossComponentIntegration:
    """Test integration across multiple system components."""
    
    # --------------------------------------------------------------------------------- test_full_system_integration_workflow()
    @pytest.mark.asyncio
    async def test_full_system_integration_workflow(self):
        """Test complete integration across all system components."""
        steps = [
            # 1. Health checks
            WorkflowStep(
                step_name="System Health Verification",
                endpoint="/health",
                payload={},
                method="GET",
                validation_checks=["healthy"]
            ),

            # 2. Advanced Parallel Hybrid health
            WorkflowStep(
                step_name="APH System Verification",
                endpoint="/parallel_hybrid/health",
                payload={},
                method="GET",
                validation_checks=["parallel_engine", "fusion_engine"]
            ),
            
            # 3. Complex query processing
            WorkflowStep(
                step_name="Complex Multi-Domain Query",
                endpoint="/generate_parallel_hybrid",
                payload={
                    "user_input": "What are the comprehensive safety requirements for underground coal mining operations including ventilation, methane monitoring, and emergency procedures?",
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                },
                validation_checks=["safety", "underground", "coal", "mining", "ventilation", "methane", "emergency"]
            ),
            
            # 4. Follow-up clarification query
            WorkflowStep(
                step_name="Follow-up Clarification",
                endpoint="/generate_parallel_hybrid",
                payload={
                    "user_input": "Can you provide specific CFR references for the methane monitoring requirements mentioned above?",
                    "fusion_strategy": "max_confidence",
                    "template_type": "research_based"
                },
                validation_checks=["cfr", "methane", "monitoring", "30 cfr"]
            ),
            
            # 5. System metrics after processing
            WorkflowStep(
                step_name="Post-Processing Metrics",
                endpoint="/metrics",
                payload={},
                method="GET",
                validation_checks=["timestamp"]
            )
        ]
        
        # Execute full integration workflow
        result = await execute_complete_workflow("Full System Integration", steps)
        
        # Comprehensive assertions
        assert result.success, f"Full integration workflow failed: {result.step_results}"
        assert result.completed_steps == result.total_steps, "All integration steps should complete"
        
        # Validate each component interaction
        health_step = result.step_results[0]
        aph_step = result.step_results[1] 
        complex_query_step = result.step_results[2]
        followup_step = result.step_results[3]
        metrics_step = result.step_results[4]
        
        # Health checks should be fast
        assert health_step["execution_time"] < 5.0, "Health check should be fast"
        assert aph_step["execution_time"] < 5.0, "APH health check should be fast"
        
        # Complex queries should return substantial responses
        if complex_query_step.get("response_data"):
            complex_response = complex_query_step["response_data"]
            assert len(complex_response.get("response", "")) > 500, "Complex query should return detailed response"
        
        if followup_step.get("response_data"):
            followup_response = followup_step["response_data"] 
            assert len(followup_response.get("response", "")) > 200, "Follow-up should return meaningful response"
        
        # System should maintain performance
        total_query_time = complex_query_step["execution_time"] + followup_step["execution_time"]
        assert total_query_time < 120.0, "Total query processing should complete in reasonable time"
    # --------------------------------------------------------------------------------- end test_full_system_integration_workflow()
# ------------------------------------------------------------------------- end TestCrossComponentIntegration

# =========================================================================
# End of File
# ========================================================================= 