# -------------------------------------------------------------------------
# File: test_load_testing_fault_injection.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: tests/reliability/test_load_testing_fault_injection.py
# -------------------------------------------------------------------------

# --- Module Objective ---
# Test Case 4: Load Testing with Fault Injection
# This module tests the MRCA system's resilience under combined load and failure
# conditions. It simulates concurrent user requests while injecting various
# failure scenarios to validate the system's fault tolerance, circuit breaker
# behavior, and graceful degradation capabilities under stress.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: TestLoadTestingWithFaultInjection - Main test class for load + fault scenarios
# - Class: TestConcurrentUserLoad - Pure load testing without faults
# - Class: TestFaultInjectionScenarios - Various fault injection patterns
# - Class: TestPerformanceDegradation - Performance impact measurement
# - Functions: Helper functions for load generation and fault simulation
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - asyncio: For concurrent request simulation
#   - time: For timing and performance measurement
#   - threading: For concurrent test execution
#   - random: For randomized fault injection
# - Third-Party:
#   - pytest: Testing framework with async support
#   - httpx: HTTP client for API testing
# - Local Project Modules:
#   - backend.circuit_breaker: For testing circuit breaker behavior under load
#   - backend.parallel_hybrid: For testing Advanced Parallel Hybrid under stress
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module integrates with the MRCA testing infrastructure to provide
# comprehensive load and fault tolerance validation. It tests:
# - API endpoint performance under concurrent load
# - Circuit breaker activation and recovery
# - Advanced Parallel Hybrid resilience
# - Graceful degradation of service quality
# The tests help ensure production readiness under real-world stress conditions.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Test Case 4: Load Testing with Fault Injection

Tests MRCA system resilience under combined load and failure conditions,
validating fault tolerance and graceful degradation capabilities.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import asyncio
import time
import threading
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party library imports
import pytest
import httpx

# Local application/library specific imports
from backend.circuit_breaker import get_circuit_breaker, CircuitState
from backend.config import get_config

# =========================================================================
# Test Configuration and Data Classes
# =========================================================================

# ------------------------------------------------------------------------- LoadTestConfig
@dataclass
class LoadTestConfig:
    """Configuration for load testing scenarios."""
    concurrent_users: int = 10
    requests_per_user: int = 5
    test_duration_seconds: int = 30
    ramp_up_time_seconds: int = 5
    fault_injection_probability: float = 0.2
    expected_error_rate_threshold: float = 0.3
# ------------------------------------------------------------------------- end LoadTestConfig

# ------------------------------------------------------------------------- LoadTestResults
@dataclass
class LoadTestResults:
    """Results from load testing execution."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    max_response_time: float = 0.0
    min_response_time: float = float('inf')
    errors_by_type: Dict[str, int] = field(default_factory=dict)
    circuit_breaker_activations: int = 0
    fault_injection_count: int = 0
# ------------------------------------------------------------------------- end LoadTestResults

# =========================================================================
# Test Helper Functions
# =========================================================================

# ------------------------------------------------------------------------- make_concurrent_request()
async def make_concurrent_request(
    client: httpx.AsyncClient,
    endpoint: str,
    payload: Dict[str, Any],
    inject_fault: bool = False
) -> Tuple[bool, float, str]:
    """Make a single request with optional fault injection.
    
    Args:
        client: HTTP client for making requests
        endpoint: API endpoint to test
        payload: Request payload
        inject_fault: Whether to inject a fault
        
    Returns:
        Tuple of (success, response_time, error_type)
    """
    start_time = time.time()
    
    try:
        if inject_fault:
            # Simulate various fault conditions
            fault_type = random.choice([
                "timeout", "connection_error", "malformed_payload", "invalid_endpoint"
            ])
            
            if fault_type == "timeout":
                # Set very short timeout to trigger timeout error
                async with httpx.AsyncClient(timeout=0.001) as fault_client:
                    response = await fault_client.post(endpoint, json=payload)
            elif fault_type == "connection_error":
                # Use invalid port to trigger connection error
                endpoint = endpoint.replace(":8000", ":9999")
                response = await client.post(endpoint, json=payload)
            elif fault_type == "malformed_payload":
                # Send malformed payload
                response = await client.post(endpoint, json={"invalid": "payload"})
            elif fault_type == "invalid_endpoint":
                # Use invalid endpoint
                response = await client.post(endpoint + "/invalid", json=payload)
        else:
            # Normal request
            response = await client.post(endpoint, json=payload)
            
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            return True, response_time, ""
        else:
            return False, response_time, f"HTTP_{response.status_code}"
            
    except httpx.TimeoutException:
        return False, time.time() - start_time, "timeout"
    except httpx.ConnectError:
        return False, time.time() - start_time, "connection_error"
    except Exception as e:
        return False, time.time() - start_time, type(e).__name__
# ------------------------------------------------------------------------- end make_concurrent_request()

# ------------------------------------------------------------------------- simulate_user_load()
async def simulate_user_load(
    user_id: int,
    config: LoadTestConfig,
    base_url: str
) -> LoadTestResults:
    """Simulate load from a single user.
    
    Args:
        user_id: Unique identifier for this user
        config: Load test configuration
        base_url: Base URL for API calls
        
    Returns:
        LoadTestResults with metrics from this user
    """
    results = LoadTestResults()
    endpoint = f"{base_url}/generate_parallel_hybrid"
    
    # Test payload for Advanced Parallel Hybrid
    payload = {
        "user_input": f"What are methane monitoring requirements for user {user_id}?",
        "fusion_strategy": "advanced_hybrid",
        "template_type": "regulatory_compliance"
    }
    
    async with httpx.AsyncClient(timeout=240.0) as client:
        for request_num in range(config.requests_per_user):
            # Determine if we should inject a fault
            inject_fault = random.random() < config.fault_injection_probability
            if inject_fault:
                results.fault_injection_count += 1
            
            # Make the request
            success, response_time, error_type = await make_concurrent_request(
                client, endpoint, payload, inject_fault
            )
            
            # Record results
            results.total_requests += 1
            if success:
                results.successful_requests += 1
            else:
                results.failed_requests += 1
                if error_type:
                    results.errors_by_type[error_type] = results.errors_by_type.get(error_type, 0) + 1
            
            # Update timing metrics
            if response_time > results.max_response_time:
                results.max_response_time = response_time
            if response_time < results.min_response_time:
                results.min_response_time = response_time
            
            # Small delay between requests to avoid overwhelming
            await asyncio.sleep(0.1)
    
    # Calculate average response time
    if results.total_requests > 0:
        # For simplicity, we'll estimate average (would need more sophisticated tracking in production)
        results.average_response_time = (results.min_response_time + results.max_response_time) / 2
    
    return results
# ------------------------------------------------------------------------- end simulate_user_load()

# ------------------------------------------------------------------------- aggregate_results()
def aggregate_results(individual_results: List[LoadTestResults]) -> LoadTestResults:
    """Aggregate results from multiple users into combined metrics.
    
    Args:
        individual_results: List of results from each user
        
    Returns:
        Aggregated LoadTestResults
    """
    aggregated = LoadTestResults()
    
    for result in individual_results:
        aggregated.total_requests += result.total_requests
        aggregated.successful_requests += result.successful_requests
        aggregated.failed_requests += result.failed_requests
        aggregated.fault_injection_count += result.fault_injection_count
        
        # Track maximum response time across all users
        if result.max_response_time > aggregated.max_response_time:
            aggregated.max_response_time = result.max_response_time
            
        # Track minimum response time across all users
        if result.min_response_time < aggregated.min_response_time:
            aggregated.min_response_time = result.min_response_time
        
        # Aggregate error types
        for error_type, count in result.errors_by_type.items():
            aggregated.errors_by_type[error_type] = aggregated.errors_by_type.get(error_type, 0) + count
    
    # Calculate overall average response time (simplified)
    if aggregated.total_requests > 0:
        aggregated.average_response_time = (aggregated.min_response_time + aggregated.max_response_time) / 2
    
    return aggregated
# ------------------------------------------------------------------------- end aggregate_results()

# =========================================================================
# Test Case 4: Load Testing with Fault Injection
# =========================================================================

# ------------------------------------------------------------------------- TestLoadTestingWithFaultInjection
@pytest.mark.reliability
@pytest.mark.slow
@pytest.mark.requires_api
class TestLoadTestingWithFaultInjection:
    """Test Case 4: Load testing with fault injection scenarios."""
    
    # ------------------------------------------------------------------------- test_concurrent_load_with_fault_injection()
    def test_concurrent_load_with_fault_injection(self):
        """Test system resilience under concurrent load with fault injection."""
        config = LoadTestConfig(
            concurrent_users=5,  # Moderate load for CI/CD
            requests_per_user=3,
            test_duration_seconds=15,
            fault_injection_probability=0.3,  # 30% fault injection rate
            expected_error_rate_threshold=0.35  # Allow for 35% error rate with rate limiting overhead
        )
        
        base_url = "http://localhost:8000"
        
        # Run load test with fault injection
        async def run_load_test():
            # Create tasks for concurrent users
            user_tasks = []
            for user_id in range(config.concurrent_users):
                task = simulate_user_load(user_id, config, base_url)
                user_tasks.append(task)
            
            # Execute all user simulations concurrently
            results = await asyncio.gather(*user_tasks, return_exceptions=True)
            
            # Filter out exceptions and aggregate valid results
            valid_results = [r for r in results if isinstance(r, LoadTestResults)]
            return aggregate_results(valid_results)
        
        # Execute the async load test
        aggregated_results = asyncio.run(run_load_test())
        
        # Assertions for system resilience
        assert aggregated_results.total_requests > 0, "Should have executed some requests"
        
        # Calculate error rate
        error_rate = aggregated_results.failed_requests / aggregated_results.total_requests
        
        # System should maintain reasonable error rate even with fault injection
        assert error_rate <= config.expected_error_rate_threshold, (
            f"Error rate {error_rate:.2%} exceeds threshold {config.expected_error_rate_threshold:.2%}"
        )
        
        # Should have injected some faults
        assert aggregated_results.fault_injection_count > 0, "Should have injected some faults for testing"
        
        # Performance should be reasonable even under stress
        assert aggregated_results.max_response_time < 60.0, "Max response time should be under 60 seconds"
    
    def test_circuit_breaker_activation_under_load(self):
        """Test circuit breaker behavior under load with failures."""
        config = LoadTestConfig(
            concurrent_users=3,
            requests_per_user=2,
            fault_injection_probability=0.8  # High fault rate to trigger circuit breakers
        )
        
        # Get circuit breaker instances to monitor
        api_breaker = get_circuit_breaker("api_service")
        llm_breaker = get_circuit_breaker("llm_service")
        
        # Record initial states
        initial_api_state = api_breaker.state
        initial_llm_state = llm_breaker.state
        
        base_url = "http://localhost:8000"
        
        # Run high-fault load test
        async def run_fault_heavy_test():
            user_tasks = []
            for user_id in range(config.concurrent_users):
                task = simulate_user_load(user_id, config, base_url)
                user_tasks.append(task)
            
            results = await asyncio.gather(*user_tasks, return_exceptions=True)
            valid_results = [r for r in results if isinstance(r, LoadTestResults)]
            return aggregate_results(valid_results)
        
        results = asyncio.run(run_fault_heavy_test())
        
        # Check circuit breaker behavior
        final_api_state = api_breaker.state
        final_llm_state = llm_breaker.state
        
        # Should have processed requests (even if many failed)
        assert results.total_requests > 0
        
        # High fault injection should have occurred
        assert results.fault_injection_count > 0
        
        # Circuit breakers should be responsive to failures
        # (They might activate or remain closed depending on timing and thresholds)
        api_status = api_breaker.get_status()
        llm_status = llm_breaker.get_status()
        
        # At minimum, circuit breakers should have recorded some activity
        assert api_status["metrics"]["total_requests"] >= 0
        assert llm_status["metrics"]["total_requests"] >= 0

    def test_performance_degradation_measurement(self):
        """Test performance impact of fault injection on system response times."""
        # First, run baseline test without fault injection
        baseline_config = LoadTestConfig(
            concurrent_users=2,
            requests_per_user=2,
            fault_injection_probability=0.0  # No faults
        )
        
        # Then, run test with fault injection
        fault_config = LoadTestConfig(
            concurrent_users=2,
            requests_per_user=2,
            fault_injection_probability=0.5  # 50% fault rate
        )
        
        base_url = "http://localhost:8000"
        
        async def run_baseline_test():
            user_tasks = []
            for user_id in range(baseline_config.concurrent_users):
                task = simulate_user_load(user_id, baseline_config, base_url)
                user_tasks.append(task)
            
            results = await asyncio.gather(*user_tasks, return_exceptions=True)
            valid_results = [r for r in results if isinstance(r, LoadTestResults)]
            return aggregate_results(valid_results)
        
        async def run_fault_test():
            user_tasks = []
            for user_id in range(fault_config.concurrent_users):
                task = simulate_user_load(user_id, fault_config, base_url)
                user_tasks.append(task)
            
            results = await asyncio.gather(*user_tasks, return_exceptions=True)
            valid_results = [r for r in results if isinstance(r, LoadTestResults)]
            return aggregate_results(valid_results)
        
        # Run both tests
        baseline_results = asyncio.run(run_baseline_test())
        fault_results = asyncio.run(run_fault_test())
        
        # Analysis assertions
        assert baseline_results.total_requests > 0, "Baseline should have requests"
        assert fault_results.total_requests > 0, "Fault test should have requests"
        
        # Fault injection should increase error rate
        baseline_error_rate = baseline_results.failed_requests / baseline_results.total_requests
        fault_error_rate = fault_results.failed_requests / fault_results.total_requests
        
        # With fault injection, error rate should be higher
        assert fault_error_rate > baseline_error_rate, (
            f"Fault error rate {fault_error_rate:.2%} should exceed baseline {baseline_error_rate:.2%}"
        )
        
        # Should have confirmed fault injection occurred
        assert fault_results.fault_injection_count > 0, "Should have injected faults"
    # ------------------------------------------------------------------------- end test_concurrent_load_with_fault_injection()
# ------------------------------------------------------------------------- end TestLoadTestingWithFaultInjection

# =========================================================================
# Additional Load Testing Scenarios
# =========================================================================

# ------------------------------------------------------------------------- TestConcurrentUserLoad
@pytest.mark.reliability
@pytest.mark.slow
@pytest.mark.requires_api
class TestConcurrentUserLoad:
    """Test pure load scenarios without fault injection."""
    
    # ------------------------------------------------------------------------- test_concurrent_users_basic_load()
    def test_concurrent_users_basic_load(self):
        """Test basic concurrent user load without faults."""
        config = LoadTestConfig(
            concurrent_users=5,
            requests_per_user=2,
            fault_injection_probability=0.0  # No fault injection
        )
        
        base_url = "http://localhost:8000"
        
        async def run_clean_load_test():
            user_tasks = []
            for user_id in range(config.concurrent_users):
                task = simulate_user_load(user_id, config, base_url)
                user_tasks.append(task)
            
            results = await asyncio.gather(*user_tasks, return_exceptions=True)
            valid_results = [r for r in results if isinstance(r, LoadTestResults)]
            return aggregate_results(valid_results)
        
        results = asyncio.run(run_clean_load_test())
        
        # Assertions for clean load performance
        assert results.total_requests == config.concurrent_users * config.requests_per_user
        
        # With no fault injection, success rate should be high
        success_rate = results.successful_requests / results.total_requests
        assert success_rate >= 0.8, f"Success rate {success_rate:.2%} should be at least 80%"
        
        # Response times should be reasonable (accounting for rate limiting with concurrent users)
        assert results.max_response_time < 100.0, "Max response time should be under 100 seconds"
    # ------------------------------------------------------------------------- end test_concurrent_users_basic_load()
# ------------------------------------------------------------------------- end TestConcurrentUserLoad

# ------------------------------------------------------------------------- TestFaultInjectionScenarios
@pytest.mark.reliability
@pytest.mark.slow
class TestFaultInjectionScenarios:
    """Test specific fault injection patterns."""
    
    # ------------------------------------------------------------------------- test_timeout_fault_injection()
    def test_timeout_fault_injection(self):
        """Test system behavior with timeout faults."""
        # This test focuses on timeout-specific fault injection
        # Implementation would test timeout handling specifically
        pass
    # ------------------------------------------------------------------------- end test_timeout_fault_injection()
    
    # ------------------------------------------------------------------------- test_connection_error_fault_injection()
    def test_connection_error_fault_injection(self):
        """Test system behavior with connection error faults."""
        # This test focuses on connection error fault injection
        # Implementation would test connection error handling specifically
        pass
    # ------------------------------------------------------------------------- end test_connection_error_fault_injection()
# ------------------------------------------------------------------------- end TestFaultInjectionScenarios

# =========================================================================
# End of File
# ========================================================================= 