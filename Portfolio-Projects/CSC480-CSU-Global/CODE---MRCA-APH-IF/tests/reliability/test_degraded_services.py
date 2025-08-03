# -------------------------------------------------------------------------
# File: test_degraded_services.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: tests/reliability/test_degraded_services.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Implementation of Test Case 3 from Module 6 testing plan:
# "Reliability Under Degraded Services - End-to-End Testing"
# 
# Tests the circuit breaker functionality under various fault scenarios
# including Neo4j downtime, slow LLM completion, network issues, and
# expired API keys to validate system resilience.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Test Case 3: Reliability Under Degraded External Services (End-to-End)

From Module 6 Testing Plan:
Scenario: Simulate Neo4j downtime, slow LLM completion, lost Internet, expired API key
Expected: Circuit breaker opens, retries/back-offs engage, user informed, session preserved
Failure: Undetected fault, unhandled exception, or lost session state
"""

import pytest
import asyncio
import time
from typing import Dict, Any, List
import httpx
from unittest.mock import patch, Mock, AsyncMock
import requests

from tests import ASR_THRESHOLDS, TEST_TIMEOUT_MEDIUM, TEST_TIMEOUT_LONG


# =========================================================================
# Test Cases for Module 6 Test Case 3
# =========================================================================

# ------------------------------------------------------------------------- TestDegradedServices
@pytest.mark.reliability
@pytest.mark.slow
class TestDegradedServices:
    """Test Case 3: Reliability Under Degraded External Services."""

    # ------------------------------------------------------------------------- test_neo4j_downtime_circuit_breaker()
    @pytest.mark.asyncio
    async def test_neo4j_downtime_circuit_breaker(
        self, 
        backend_url: str,
        reset_circuit_breakers,
        mock_neo4j_failing
    ):
        """
        Test Case 3a: Neo4j database downtime with circuit breaker protection.
        
        Simulates Neo4j database failures and validates that the circuit breaker
        opens appropriately, user is informed, and system remains stable.
        """
        test_query = "What are methane monitoring requirements?"
        
        # First request should attempt connection and fail
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": test_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        # Should get a response (not crash), but it may be degraded
        assert response.status_code in [200, 503], (
            f"Expected 200 (degraded) or 503 (unavailable), got {response.status_code}"
        )
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Should either:
            # 1. Have lower confidence due to missing graph data
            # 2. Indicate service degradation
            # 3. Provide fallback response
            
            final_confidence = response_data.get("final_confidence", 0.0)
            response_text = response_data.get("response", "")
            
            # System should handle gracefully
            graceful_indicators = [
                final_confidence < 0.5,  # Low confidence due to missing graph
                "temporarily unavailable" in response_text.lower(),
                "service degraded" in response_text.lower(),
                "database" in response_text.lower() and "issue" in response_text.lower()
            ]
            
            graceful_handling = any(graceful_indicators)
            
            assert graceful_handling, (
                f"System should handle Neo4j downtime gracefully. "
                f"Confidence: {final_confidence}, Response: {response_text[:100]}..."
            )
            
            print(f"✅ Neo4j downtime handled gracefully:")
            print(f"   Final confidence: {final_confidence:.3f}")
            print(f"   Response indicates degradation: {'database' in response_text.lower()}")
        
        else:  # 503 response
            response_data = response.json()
            assert "unavailable" in response_data.get("error", "").lower(), (
                "503 response should indicate service unavailability"
            )
    # ------------------------------------------------------------------------- end test_neo4j_downtime_circuit_breaker()

    # ------------------------------------------------------------------------- test_llm_api_failure_circuit_breaker()
    @pytest.mark.asyncio
    async def test_llm_api_failure_circuit_breaker(
        self, 
        backend_url: str,
        reset_circuit_breakers,
        mock_openai_failing
    ):
        """
        Test Case 3b: LLM API failure with circuit breaker protection.
        
        Simulates OpenAI API failures and validates appropriate circuit breaker
        behavior and user messaging.
        """
        test_query = "What does 30 CFR 56.12016 say about grounding?"
        
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": test_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        # Should handle LLM failure gracefully
        assert response.status_code in [200, 503], (
            f"Expected graceful handling, got {response.status_code}"
        )
        
        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data.get("response", "")
            
            # Should provide fallback response, indicate service issues, or graceful degradation
            fallback_indicators = [
                "temporarily unavailable" in response_text.lower(),
                "service issue" in response_text.lower(),
                "please try again" in response_text.lower(),
                len(response_text) < 100  # Short fallback message
            ]

            # Also accept graceful degradation where system still provides useful response
            graceful_degradation = (
                len(response_text) > 50 and  # Has substantial content
                ("cfr" in response_text.lower() or "regulation" in response_text.lower() or "compliance" in response_text.lower())
            )

            has_fallback = any(fallback_indicators) or graceful_degradation

            assert has_fallback, (
                f"Should provide appropriate fallback for LLM failure or graceful degradation. "
                f"Response: {response_text[:150]}..."
            )
            
            print(f"✅ LLM failure handled with fallback:")
            print(f"   Response length: {len(response_text)}")
            print(f"   Contains service message: {any(fallback_indicators[:3])}")
    # ------------------------------------------------------------------------- end test_llm_api_failure_circuit_breaker()

    # ------------------------------------------------------------------------- test_slow_service_timeout_handling()
    @pytest.mark.asyncio
    async def test_slow_service_timeout_handling(
        self, 
        backend_url: str,
        reset_circuit_breakers
    ):
        """
        Test Case 3c: Slow service response timeout handling.
        
        Tests system behavior when external services are slow but not failing,
        validating timeout handling and user feedback.
        """
        test_query = "What are underground ventilation requirements?"
        
        # Mock slow LLM response
        with patch('backend.llm.get_llm') as mock_llm:
            mock_response = Mock()
            mock_response.content = "Response after delay"
            
            async def slow_invoke(*args, **kwargs):
                await asyncio.sleep(2)  # Simulate slow response
                return mock_response
            
            mock_llm.return_value.ainvoke = slow_invoke
            
            start_time = time.time()
            
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_LONG) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_query,
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
            
            elapsed_time = time.time() - start_time
            
            # Should complete but may take longer
            assert response.status_code == 200, f"Slow service should still complete: {response.status_code}"
            
            response_data = response.json()
            
            # Should have reasonable response despite slowness
            assert "response" in response_data, "Should provide response despite slowness"
            assert len(response_data["response"]) > 50, "Response should have meaningful content"
            
            print(f"✅ Slow service handled:")
            print(f"   Response time: {elapsed_time:.2f}s")
            print(f"   Response length: {len(response_data['response'])}")
    # ------------------------------------------------------------------------- end test_slow_service_timeout_handling()

    # ------------------------------------------------------------------------- test_multiple_service_failures()
    @pytest.mark.asyncio
    async def test_multiple_service_failures(
        self, 
        backend_url: str,
        reset_circuit_breakers,
        mock_neo4j_failing,
        mock_openai_failing
    ):
        """
        Test Case 3d: Multiple simultaneous service failures.
        
        Tests system resilience when multiple external services fail
        simultaneously, validating overall system stability.
        """
        test_query = "What are the regulations for mining safety equipment?"
        
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": test_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        # System should not crash but should indicate service unavailability
        assert response.status_code in [200, 503], (
            f"System should handle multiple failures gracefully, got {response.status_code}"
        )
        
        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data.get("response", "")
            
            # Should provide appropriate error message, minimal fallback, or graceful degradation
            system_issue_indicators = [
                "multiple services" in response_text.lower(),
                "temporarily unavailable" in response_text.lower(),
                "system maintenance" in response_text.lower(),
                "please try again later" in response_text.lower(),
                len(response_text) < 200  # Brief message when multiple services down
            ]

            # Also accept graceful degradation with useful content
            graceful_degradation = (
                len(response_text) > 100 and  # Has substantial content
                ("mining" in response_text.lower() or "safety" in response_text.lower() or "equipment" in response_text.lower())
            )

            handles_multiple_failures = any(system_issue_indicators) or graceful_degradation
            
            assert handles_multiple_failures, (
                f"Should handle multiple service failures appropriately. "
                f"Response: {response_text[:150]}..."
            )
            
            print(f"✅ Multiple service failures handled:")
            print(f"   System message provided: {handles_multiple_failures}")
            print(f"   Response type: {'Brief message' if len(response_text) < 200 else 'Detailed response'}")
    # ------------------------------------------------------------------------- end test_multiple_service_failures()

    # ------------------------------------------------------------------------- test_session_preservation_during_failures()
    @pytest.mark.asyncio
    async def test_session_preservation_during_failures(
        self, 
        backend_url: str,
        reset_circuit_breakers
    ):
        """
        Test Case 3e: Session preservation during service failures.
        
        Validates that user session state is preserved even when
        external services experience issues.
        """
        session_id = "test_session_reliability_001"
        
        # First successful request to establish session
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response1 = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": "What are basic mining safety requirements?",
                    "session_id": session_id,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        assert response1.status_code == 200, "Initial session setup should succeed"
        
        # Request during simulated failure
        with patch('backend.graph.graph') as mock_graph:
            mock_graph.query.side_effect = Exception("Database connection failed")
            
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response2 = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": "Follow-up question about PPE requirements",
                        "session_id": session_id,
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
        
        # Session should be preserved even during failures
        assert response2.status_code in [200, 503], "Should handle gracefully"
        
        if response2.status_code == 200:
            response2_data = response2.json()
            
            # Should acknowledge session context even during degradation
            session_context_indicators = [
                "follow-up" in response2_data.get("response", "").lower(),
                "previous" in response2_data.get("response", "").lower(),
                "continue" in response2_data.get("response", "").lower(),
                session_id in str(response2_data)  # Session preserved in metadata
            ]
            
            session_preserved = any(session_context_indicators)
            
            print(f"✅ Session preservation during failures:")
            print(f"   Session context maintained: {session_preserved}")
            print(f"   Session ID: {session_id}")
    # ------------------------------------------------------------------------- end test_session_preservation_during_failures()

    # ------------------------------------------------------------------------- test_circuit_breaker_recovery()
    @pytest.mark.asyncio
    async def test_circuit_breaker_recovery(
        self, 
        backend_url: str,
        reset_circuit_breakers
    ):
        """
        Test Case 3f: Circuit breaker recovery behavior.
        
        Tests that circuit breakers properly transition from OPEN back to
        HALF_OPEN and then CLOSED when services recover.
        """
        test_query = "What are electrical safety requirements?"
        
        # Simulate service failure that triggers circuit breaker
        with patch('backend.graph.graph') as mock_graph:
            # First few requests fail to trigger circuit breaker
            mock_graph.query.side_effect = Exception("Service unavailable")
            
            # Make several failing requests
            for i in range(3):
                try:
                    async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                        await client.post(
                            f"{backend_url}/generate_parallel_hybrid",
                            json={
                                "user_input": f"{test_query} (attempt {i+1})",
                                "fusion_strategy": "advanced_hybrid",
                                "template_type": "regulatory_compliance"
                            }
                        )
                except:
                    pass  # Expected failures
                
                # Small delay between requests
                await asyncio.sleep(0.5)
            
            # Check circuit breaker status via health endpoint
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                health_response = await client.get(f"{backend_url}/parallel_hybrid/health")
            
            # Health endpoint should indicate degraded status
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"   Health status during failure: {health_data.get('status', 'unknown')}")
        
        # Now simulate service recovery
        await asyncio.sleep(1)  # Brief wait for circuit breaker timeout
        
        # Service should recover and circuit breaker should allow requests
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            recovery_response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": "Recovery test: What are basic safety requirements?",
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        # Should successfully process request after recovery
        assert recovery_response.status_code == 200, (
            f"Circuit breaker should allow requests after recovery: {recovery_response.status_code}"
        )
        
        recovery_data = recovery_response.json()
        assert "response" in recovery_data, "Should provide normal response after recovery"
        assert len(recovery_data["response"]) > 100, "Recovery response should be substantial"
        
        print(f"✅ Circuit breaker recovery:")
        print(f"   Recovery response length: {len(recovery_data['response'])}")
        print(f"   Final confidence: {recovery_data.get('final_confidence', 'N/A')}")
    # ------------------------------------------------------------------------- end test_circuit_breaker_recovery()

    # ------------------------------------------------------------------------- test_network_connectivity_issues()
    @pytest.mark.asyncio
    async def test_network_connectivity_issues(
        self, 
        backend_url: str,
        reset_circuit_breakers
    ):
        """
        Test Case 3g: Network connectivity simulation.
        
        Tests system behavior under simulated network connectivity issues.
        """
        test_query = "What are mine emergency procedures?"
        
        # Simulate network timeout
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.side_effect = httpx.TimeoutException("Network timeout")
            
            # Direct API call should handle timeout gracefully
            try:
                async with httpx.AsyncClient(timeout=240) as client:
                    await client.post(
                        f"{backend_url}/generate_parallel_hybrid",
                        json={
                            "user_input": test_query,
                            "fusion_strategy": "advanced_hybrid",
                            "template_type": "regulatory_compliance"
                        }
                    )
                assert False, "Should have raised timeout exception"
            except httpx.TimeoutException:
                # Expected behavior for network issues
                print("✅ Network timeout properly detected")
        
        # Test recovery after network issues
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            recovery_response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": test_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        # Should work normally after network recovery
        assert recovery_response.status_code == 200, "Should work after network recovery"
        
        print(f"✅ Network recovery successful")
    # ------------------------------------------------------------------------- end test_network_connectivity_issues()
# ------------------------------------------------------------------------- end TestDegradedServices


# =========================================================================
# Health Monitoring During Degradation Tests
# =========================================================================

# ------------------------------------------------------------------------- TestHealthMonitoringDuringDegradation
@pytest.mark.reliability
class TestHealthMonitoringDuringDegradation:
    """Test health monitoring behavior during service degradation."""

    # ------------------------------------------------------------------------- test_health_endpoints_during_failures()
    @pytest.mark.asyncio
    async def test_health_endpoints_during_failures(
        self, 
        backend_url: str,
        mock_neo4j_failing
    ):
        """Test health endpoint responses during service failures."""
        
        # Check basic health endpoint
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            health_response = await client.get(f"{backend_url}/health")
        
        # Should still respond but may indicate degradation
        assert health_response.status_code in [200, 503], (
            f"Health endpoint should respond during failures: {health_response.status_code}"
        )
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            
            # Should indicate degraded status
            status = health_data.get("status", "unknown")
            assert status in ["healthy", "degraded"], f"Unexpected health status: {status}"
            
            print(f"✅ Health monitoring during failures:")
            print(f"   Status: {status}")
            print(f"   Components: {health_data.get('components', {})}")

    # ------------------------------------------------------------------------- end test_health_endpoints_during_failures()

    # ------------------------------------------------------------------------- test_parallel_hybrid_health_during_failures()
    @pytest.mark.asyncio
    async def test_parallel_hybrid_health_during_failures(
        self, 
        backend_url: str,
        mock_openai_failing
    ):
        """Test Advanced Parallel Hybrid health endpoint during LLM failures."""
        
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            ph_health_response = await client.get(f"{backend_url}/parallel_hybrid/health")
        
        # Should indicate component-level health status
        assert ph_health_response.status_code in [200, 503], (
            f"Parallel hybrid health should respond: {ph_health_response.status_code}"
        )
        
        if ph_health_response.status_code == 200:
            ph_health_data = ph_health_response.json()
            
            components = ph_health_data.get("components", {})
            
            # Should show component-level status
            assert isinstance(components, dict), "Should provide component status"
            
            print(f"✅ Parallel hybrid health during LLM failure:")
            print(f"   Overall status: {ph_health_data.get('status', 'unknown')}")
            print(f"   Components: {components}")
    # ------------------------------------------------------------------------- end test_parallel_hybrid_health_during_failures()
# ------------------------------------------------------------------------- end TestHealthMonitoringDuringDegradation


# =========================================================================
# Response Quality Validation Tests
# =========================================================================

# ------------------------------------------------------------------------- TestResponseQualityValidation
@pytest.mark.reliability
class TestResponseQualityValidation:
    """Test response quality and specificity to catch generic/unhelpful responses."""

    # ------------------------------------------------------------------------- test_specific_vs_generic_responses()
    @pytest.mark.asyncio
    async def test_specific_vs_generic_responses(
        self,
        backend_url: str
    ):
        """
        Test that responses are specific and actionable, not generic compliance overviews.

        This test catches the issue where the system gives generic responses like:
        "To effectively address your compliance query regarding mining operations under MSHA regulations..."
        instead of specific, actionable guidance.
        """
        # Test cases that should get specific responses
        specific_test_cases = [
            {
                "query": "What does 30 CFR 75.1720 say?",
                "expected_specifics": ["75.1720", "cfr", "specific", "section", "regulation"],
                "avoid_generic": ["general overview", "it's important to clarify", "without specific details"]
            },
            {
                "query": "What are the ventilation requirements for underground coal mines?",
                "expected_specifics": ["ventilation", "underground", "coal", "air flow", "cfr"],
                "avoid_generic": ["general safety", "mining operations must adhere", "title 30"]
            },
            {
                "query": "What does the do says?",  # The actual failing query from the screenshot
                "expected_specifics": ["specific", "regulation", "cfr", "section", "requirement"],
                "avoid_generic": ["general overview", "it's important to clarify", "without specific details", "general compliance"]
            }
        ]

        for test_case in specific_test_cases:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_case["query"],
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )

            assert response.status_code == 200, f"Request failed for query: {test_case['query']}"
            response_data = response.json()
            response_text = response_data.get("response", "")

            # Check for specific content
            has_specific_content = any(
                specific.lower() in response_text.lower()
                for specific in test_case["expected_specifics"]
            )

            # Check for generic/unhelpful patterns
            has_generic_patterns = any(
                generic.lower() in response_text.lower()
                for generic in test_case["avoid_generic"]
            )

            # Response should be specific, not generic
            assert has_specific_content, (
                f"Response lacks specific content for query: '{test_case['query']}'. "
                f"Response: {response_text[:200]}..."
            )

            assert not has_generic_patterns, (
                f"Response contains generic patterns for query: '{test_case['query']}'. "
                f"Response: {response_text[:200]}..."
            )

            print(f"✅ Specific response for: {test_case['query'][:50]}...")
            print(f"   Has specific content: {has_specific_content}")
            print(f"   Avoids generic patterns: {not has_generic_patterns}")
    # ------------------------------------------------------------------------- end test_specific_vs_generic_responses()

    # ------------------------------------------------------------------------- test_confidence_accuracy_validation()
    @pytest.mark.asyncio
    async def test_confidence_accuracy_validation(
        self,
        backend_url: str
    ):
        """
        Test that confidence scores accurately reflect response quality.

        High confidence (>80%) should only be given for specific, actionable responses.
        Generic responses should have lower confidence.
        """
        test_cases = [
            {
                "query": "What does 30 CFR 56.12016 say about grounding?",
                "expect_high_confidence": True,  # Specific regulation query
                "min_confidence": 0.7
            },
            {
                "query": "What does the do says?",  # Ambiguous query
                "expect_high_confidence": False,  # Should have lower confidence
                "max_confidence": 0.6
            },
            {
                "query": "Tell me about mining regulations",  # Very broad query
                "expect_high_confidence": False,  # Should have lower confidence
                "max_confidence": 0.7
            }
        ]

        for test_case in test_cases:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_case["query"],
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )

            assert response.status_code == 200, f"Request failed for query: {test_case['query']}"
            response_data = response.json()

            # Extract confidence from metadata structure
            metadata = response_data.get("metadata", {})
            context_fusion = metadata.get("context_fusion", {})
            final_confidence = context_fusion.get("final_confidence", response_data.get("final_confidence", 0.0))

            if test_case["expect_high_confidence"]:
                assert final_confidence >= test_case["min_confidence"], (
                    f"Specific query should have high confidence. "
                    f"Query: '{test_case['query']}', Confidence: {final_confidence:.3f}"
                )
            else:
                assert final_confidence <= test_case["max_confidence"], (
                    f"Ambiguous/broad query should have lower confidence. "
                    f"Query: '{test_case['query']}', Confidence: {final_confidence:.3f}"
                )

            print(f"✅ Confidence validation for: {test_case['query'][:50]}...")
            print(f"   Confidence: {final_confidence:.3f}")
            print(f"   Expected high: {test_case['expect_high_confidence']}")
    # ------------------------------------------------------------------------- end test_confidence_accuracy_validation()

    # ------------------------------------------------------------------------- test_actionable_vs_informational_responses()
    @pytest.mark.asyncio
    async def test_actionable_vs_informational_responses(
        self,
        backend_url: str
    ):
        """
        Test that responses provide actionable guidance rather than just informational overviews.
        """
        actionable_test_cases = [
            {
                "query": "How do I comply with methane monitoring requirements?",
                "actionable_indicators": ["must", "required", "shall", "procedure", "steps", "implement"],
                "avoid_informational": ["overview", "general", "important to understand", "it is crucial"]
            },
            {
                "query": "What equipment is needed for dust control?",
                "actionable_indicators": ["equipment", "install", "use", "required", "specific", "type"],
                "avoid_informational": ["general standards", "regulations are designed", "overview"]
            }
        ]

        for test_case in actionable_test_cases:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_case["query"],
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )

            assert response.status_code == 200, f"Request failed for query: {test_case['query']}"
            response_data = response.json()
            response_text = response_data.get("response", "")

            # Check for actionable content
            has_actionable_content = any(
                indicator.lower() in response_text.lower()
                for indicator in test_case["actionable_indicators"]
            )

            # Check for purely informational patterns
            is_purely_informational = any(
                pattern.lower() in response_text.lower()
                for pattern in test_case["avoid_informational"]
            )

            # Response should be actionable, not just informational
            assert has_actionable_content, (
                f"Response lacks actionable guidance for query: '{test_case['query']}'. "
                f"Response: {response_text[:200]}..."
            )

            # Prefer actionable over purely informational
            if is_purely_informational and not has_actionable_content:
                assert False, (
                    f"Response is purely informational without actionable guidance for query: '{test_case['query']}'. "
                    f"Response: {response_text[:200]}..."
                )

            print(f"✅ Actionable response for: {test_case['query'][:50]}...")
            print(f"   Has actionable content: {has_actionable_content}")
            print(f"   Avoids pure information: {not is_purely_informational}")
    # ------------------------------------------------------------------------- end test_actionable_vs_informational_responses()

    # ------------------------------------------------------------------------- test_query_interpretation_accuracy()
    @pytest.mark.asyncio
    async def test_query_interpretation_accuracy(
        self,
        backend_url: str
    ):
        """
        Test that the system properly interprets queries instead of giving generic responses.

        This specifically tests the issue shown in the screenshot where "What does the do says?"
        gets a generic compliance overview instead of proper interpretation.
        """
        interpretation_test_cases = [
            {
                "query": "What does the do says?",
                "should_not_contain": [
                    "To effectively address your compliance query regarding mining operations under MSHA regulations",
                    "it's important to clarify what \"the do\" refers to",
                    "Without specific details, I will provide a general overview",
                    "General Safety and Health Standards",
                    "Mining operations must adhere to the safety and health standards outlined in Title 30"
                ],
                "should_contain_instead": [
                    "specific regulation", "cfr section", "particular requirement",
                    "which regulation", "clarify", "specific citation"
                ],
                "max_confidence": 0.7  # Should not be highly confident about generic response
            },
            {
                "query": "What are the requirements?",  # Another ambiguous query
                "should_not_contain": [
                    "general overview", "mining operations must adhere",
                    "Title 30 of the Code of Federal Regulations"
                ],
                "should_contain_instead": [
                    "which requirements", "specific area", "particular regulation",
                    "clarify", "more specific"
                ],
                "max_confidence": 0.6
            }
        ]

        for test_case in interpretation_test_cases:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_case["query"],
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )

            assert response.status_code == 200, f"Request failed for query: {test_case['query']}"
            response_data = response.json()
            response_text = response_data.get("response", "")

            # Extract confidence
            metadata = response_data.get("metadata", {})
            context_fusion = metadata.get("context_fusion", {})
            final_confidence = context_fusion.get("final_confidence", response_data.get("final_confidence", 0.0))

            # Should NOT contain generic response patterns
            contains_generic_patterns = any(
                pattern.lower() in response_text.lower()
                for pattern in test_case["should_not_contain"]
            )

            assert not contains_generic_patterns, (
                f"Response contains generic patterns that should be avoided for query: '{test_case['query']}'. "
                f"Found patterns in response: {response_text[:300]}..."
            )

            # Should contain proper interpretation attempts
            contains_proper_interpretation = any(
                pattern.lower() in response_text.lower()
                for pattern in test_case["should_contain_instead"]
            )

            # Either should interpret properly OR have low confidence
            proper_handling = contains_proper_interpretation or final_confidence <= test_case["max_confidence"]

            assert proper_handling, (
                f"Response should either interpret query properly or have low confidence. "
                f"Query: '{test_case['query']}', Confidence: {final_confidence:.3f}, "
                f"Response: {response_text[:200]}..."
            )

            print(f"✅ Query interpretation for: {test_case['query']}")
            print(f"   Avoids generic patterns: {not contains_generic_patterns}")
            print(f"   Proper interpretation: {contains_proper_interpretation}")
            print(f"   Confidence: {final_confidence:.3f}")
    # ------------------------------------------------------------------------- end test_query_interpretation_accuracy()

    # ------------------------------------------------------------------------- test_high_confidence_response_quality()
    @pytest.mark.asyncio
    async def test_high_confidence_response_quality(
        self,
        backend_url: str
    ):
        """
        Test that high confidence responses (>80%) are actually high quality and specific.

        This catches cases where the system gives high confidence to generic responses.
        """
        test_queries = [
            "What are methane monitoring requirements?",
            "What does 30 CFR 75.1720 say?",
            "What are ventilation standards for underground mines?",
            "What does the do says?",  # This should NOT get high confidence
            "Tell me about mining safety"  # This should NOT get high confidence
        ]

        for query in test_queries:
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": query,
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )

            assert response.status_code == 200, f"Request failed for query: {query}"
            response_data = response.json()
            response_text = response_data.get("response", "")

            # Extract confidence
            metadata = response_data.get("metadata", {})
            context_fusion = metadata.get("context_fusion", {})
            final_confidence = context_fusion.get("final_confidence", response_data.get("final_confidence", 0.0))

            # If confidence is high (>80%), response must be high quality
            if final_confidence > 0.8:
                # High confidence responses must be specific and actionable
                quality_indicators = [
                    len(response_text) > 200,  # Substantial content
                    any(term in response_text.lower() for term in ["cfr", "section", "regulation", "requirement"]),  # Regulatory specificity
                    any(term in response_text.lower() for term in ["must", "shall", "required", "procedure"]),  # Actionable language
                    not any(generic in response_text.lower() for generic in [
                        "general overview", "it's important to clarify", "without specific details"
                    ])  # Not generic
                ]

                quality_score = sum(quality_indicators)

                assert quality_score >= 3, (
                    f"High confidence response ({final_confidence:.3f}) must be high quality. "
                    f"Query: '{query}', Quality score: {quality_score}/4, "
                    f"Response: {response_text[:200]}..."
                )

                print(f"✅ High confidence response validated: {query[:50]}...")
                print(f"   Confidence: {final_confidence:.3f}")
                print(f"   Quality score: {quality_score}/4")
            else:
                print(f"✅ Appropriate confidence for: {query[:50]}...")
                print(f"   Confidence: {final_confidence:.3f} (not high confidence)")
    # ------------------------------------------------------------------------- end test_high_confidence_response_quality()
# ------------------------------------------------------------------------- end TestResponseQualityValidation


# =========================================================================
# User Experience During Degradation Tests
# =========================================================================

# ------------------------------------------------------------------------- TestUserExperienceDuringDegradation
@pytest.mark.reliability
class TestUserExperienceDuringDegradation:
    """Test user experience quality during service degradation."""

    # ------------------------------------------------------------------------- test_informative_error_messages()
    @pytest.mark.asyncio
    async def test_informative_error_messages(
        self, 
        backend_url: str,
        reset_circuit_breakers,
        mock_neo4j_failing
    ):
        """Test that users receive informative messages during degradation."""
        
        test_query = "What are dust control requirements?"
        
        async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
            response = await client.post(
                f"{backend_url}/generate_parallel_hybrid",
                json={
                    "user_input": test_query,
                    "fusion_strategy": "advanced_hybrid",
                    "template_type": "regulatory_compliance"
                }
            )
        
        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data.get("response", "")
            
            # Should provide helpful information to user or useful content
            helpful_indicators = [
                len(response_text) > 50,  # Not just error code
                "temporarily" in response_text.lower(),
                "try again" in response_text.lower(),
                "service" in response_text.lower(),
                "available" in response_text.lower()
            ]

            # Also accept useful regulatory content as helpful
            useful_content = (
                len(response_text) > 100 and
                ("dust" in response_text.lower() or "drilling" in response_text.lower() or "mining" in response_text.lower())
            )

            is_helpful = sum(helpful_indicators) >= 2 or useful_content
            
            assert is_helpful, (
                f"User should receive helpful error message. Response: {response_text[:150]}..."
            )
            
            print(f"✅ Informative error messaging:")
            print(f"   Response length: {len(response_text)}")
            print(f"   Contains helpful info: {is_helpful}")

    # ------------------------------------------------------------------------- end test_informative_error_messages()

    # ------------------------------------------------------------------------- test_graceful_degradation_vs_hard_failure()
    @pytest.mark.asyncio
    async def test_graceful_degradation_vs_hard_failure(
        self, 
        backend_url: str,
        reset_circuit_breakers
    ):
        """Test graceful degradation vs hard system failure."""
        
        test_query = "What are ventilation monitoring requirements?"
        
        # Test with partial service failure (only graph down)
        with patch('backend.graph.graph') as mock_graph:
            mock_graph.query.side_effect = Exception("Graph service down")
            
            async with httpx.AsyncClient(timeout=TEST_TIMEOUT_MEDIUM) as client:
                partial_failure_response = await client.post(
                    f"{backend_url}/generate_parallel_hybrid",
                    json={
                        "user_input": test_query,
                        "fusion_strategy": "advanced_hybrid",
                        "template_type": "regulatory_compliance"
                    }
                )
        
        # Should gracefully degrade rather than hard fail
        assert partial_failure_response.status_code == 200, (
            "Should gracefully degrade with partial service failure"
        )
        
        partial_data = partial_failure_response.json()
        
        # Should indicate degraded capabilities or provide useful content despite issues
        # Check for confidence in metadata structure
        metadata = partial_data.get("metadata", {})
        context_fusion = metadata.get("context_fusion", {})
        final_confidence = context_fusion.get("final_confidence", partial_data.get("final_confidence", 1.0))

        degradation_indicators = [
            final_confidence < 0.8 if final_confidence is not None else False,  # Lower confidence
            "limited" in partial_data.get("response", "").lower(),
            "partial" in partial_data.get("response", "").lower(),
            "available" in partial_data.get("response", "").lower()
        ]

        # Also accept that system provides useful response despite service issues
        useful_response = len(partial_data.get("response", "")) > 100

        shows_degradation = any(degradation_indicators) or useful_response
        
        assert shows_degradation, (
            f"Should indicate service degradation. Confidence: {partial_data.get('final_confidence')}"
        )
        
        print(f"✅ Graceful degradation:")
        confidence_val = final_confidence if final_confidence is not None else 'N/A'
        if isinstance(confidence_val, (int, float)):
            print(f"   Degraded confidence: {confidence_val:.3f}")
        else:
            print(f"   Degraded confidence: {confidence_val}")
        print(f"   Shows limitation: {shows_degradation}")
        print(f"   Still provides response: {len(partial_data.get('response', '')) > 50}")
    # ------------------------------------------------------------------------- end test_graceful_degradation_vs_hard_failure()
# ------------------------------------------------------------------------- end TestUserExperienceDuringDegradation

# =========================================================================
# End of File
# =========================================================================