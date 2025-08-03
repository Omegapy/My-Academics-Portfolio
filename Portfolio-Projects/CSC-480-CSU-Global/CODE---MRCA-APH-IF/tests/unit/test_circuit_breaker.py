# -------------------------------------------------------------------------
# File: test_circuit_breaker.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: tests/unit/test_circuit_breaker.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the circuit breaker implementation in backend/circuit_breaker.py
# Tests state transitions, failure thresholds, exponential backoff, metrics
# tracking, and decorator functionality for external service protection.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Circuit Breaker Unit Tests

Comprehensive testing of the CircuitBreaker class and related functionality:
- State transitions (CLOSED -> OPEN -> HALF_OPEN -> CLOSED)
- Failure threshold management
- Exponential backoff behavior
- Metrics tracking and status reporting
- Decorator functionality
- Registry management
"""

import pytest
import time
import asyncio
from unittest.mock import Mock, patch, call
from typing import Dict, Any

# Import circuit breaker components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.circuit_breaker import (
    CircuitBreaker, CircuitState, CircuitBreakerConfig, 
    CircuitBreakerMetrics, CircuitBreakerError,
    circuit_breaker, get_circuit_breaker, 
    get_all_circuit_breakers, reset_all_circuit_breakers
)


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def test_config():
    """Provide test configuration for circuit breaker."""
    return CircuitBreakerConfig(
        failure_threshold=3,
        timeout_duration=2.0,
        success_threshold=2,
        max_timeout_duration=10.0,
        backoff_multiplier=2.0
    )

@pytest.fixture
def circuit_breaker_instance(test_config):
    """Provide clean circuit breaker instance for testing."""
    return CircuitBreaker("test_service", test_config)

@pytest.fixture(autouse=True)
def reset_registry():
    """Reset circuit breaker registry before each test."""
    reset_all_circuit_breakers()
    yield
    reset_all_circuit_breakers()


# =========================================================================
# Unit Tests for CircuitBreakerConfig
# =========================================================================

@pytest.mark.unit
class TestCircuitBreakerConfig:
    """Test CircuitBreakerConfig dataclass."""
    
    def test_default_configuration(self):
        """Test default configuration values."""
        config = CircuitBreakerConfig()
        
        assert config.failure_threshold == 5
        assert config.timeout_duration == 30.0
        assert config.success_threshold == 3
        assert config.max_timeout_duration == 300.0
        assert config.backoff_multiplier == 2.0
    
    def test_custom_configuration(self):
        """Test custom configuration values."""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            timeout_duration=5.0,
            success_threshold=1,
            max_timeout_duration=60.0,
            backoff_multiplier=1.5
        )
        
        assert config.failure_threshold == 2
        assert config.timeout_duration == 5.0
        assert config.success_threshold == 1
        assert config.max_timeout_duration == 60.0
        assert config.backoff_multiplier == 1.5


# =========================================================================
# Unit Tests for CircuitBreakerMetrics
# =========================================================================

@pytest.mark.unit
class TestCircuitBreakerMetrics:
    """Test CircuitBreakerMetrics functionality."""
    
    def test_metrics_initialization(self):
        """Test metrics initialization."""
        metrics = CircuitBreakerMetrics()
        
        assert metrics.total_requests == 0
        assert metrics.successful_requests == 0
        assert metrics.failed_requests == 0
        assert metrics.state_changes == 0
        assert metrics.last_failure_time is None
        assert metrics.consecutive_failures == 0
        assert metrics.consecutive_successes == 0
    
    def test_success_rate_calculation(self):
        """Test success rate calculation via get_status method."""
        # Create a circuit breaker to test the calculated success rate
        cb = CircuitBreaker("test_service")
        
        # Initially no requests
        status = cb.get_status()
        assert status["metrics"]["success_rate"] == 0.0
        
        # Manually update metrics for testing
        cb.metrics.total_requests = 10
        cb.metrics.successful_requests = 7
        cb.metrics.failed_requests = 3
        
        # Get status again - should calculate 70% success rate
        status = cb.get_status()
        assert status["metrics"]["success_rate"] == 70.0
    
    def test_reset_counts(self):
        """Test resetting consecutive counts."""
        metrics = CircuitBreakerMetrics()
        
        metrics.consecutive_failures = 5
        metrics.consecutive_successes = 3
        
        metrics.reset_counts()
        
        assert metrics.consecutive_failures == 0
        assert metrics.consecutive_successes == 0


# =========================================================================
# Unit Tests for CircuitBreaker State Management
# =========================================================================

@pytest.mark.unit
class TestCircuitBreakerStateTransitions:
    """Test circuit breaker state transition logic."""
    
    def test_initial_state(self, circuit_breaker_instance):
        """Test initial circuit breaker state."""
        cb = circuit_breaker_instance
        
        assert cb.state == CircuitState.CLOSED
        assert cb.metrics.total_requests == 0
        assert cb.metrics.state_changes == 0
    
    def test_closed_to_open_transition(self, circuit_breaker_instance):
        """Test transition from CLOSED to OPEN state."""
        cb = circuit_breaker_instance
        
        # Mock function that always fails
        def failing_function():
            raise Exception("Service failure")
        
        # Trigger failures to reach threshold
        for i in range(cb.config.failure_threshold):
            with pytest.raises(Exception):
                cb.call(failing_function)
        
        # Should transition to OPEN after threshold failures
        assert cb.state == CircuitState.OPEN
        assert cb.metrics.state_changes == 1
        assert cb.metrics.consecutive_failures == 0  # Reset after state change
    
    def test_open_blocks_requests(self, circuit_breaker_instance):
        """Test that OPEN state blocks requests."""
        cb = circuit_breaker_instance
        
        # Force to OPEN state
        cb._transition_to_open()
        
        # Should raise CircuitBreakerError
        def working_function():
            return "success"
        
        with pytest.raises(CircuitBreakerError) as exc_info:
            cb.call(working_function)
        
        assert "test_service" in str(exc_info.value)
        assert cb.state == CircuitState.OPEN
    
    def test_open_to_half_open_transition(self, circuit_breaker_instance):
        """Test transition from OPEN to HALF_OPEN state."""
        cb = circuit_breaker_instance
        
        # Force to OPEN state
        cb._transition_to_open()
        cb._last_failure_time = time.time() - cb._current_timeout - 1
        
        # Mock successful function
        def success_function():
            return "success"
        
        # Should allow request and transition to HALF_OPEN
        result = cb.call(success_function)
        
        assert result == "success"
        assert cb.state == CircuitState.HALF_OPEN
    
    def test_half_open_to_closed_transition(self, circuit_breaker_instance):
        """Test transition from HALF_OPEN to CLOSED state."""
        cb = circuit_breaker_instance
        
        # Force to HALF_OPEN state
        cb._transition_to_half_open()
        
        def success_function():
            return "success"
        
        # Execute successful requests to reach success threshold
        for i in range(cb.config.success_threshold):
            result = cb.call(success_function)
            assert result == "success"
        
        # Should transition back to CLOSED
        assert cb.state == CircuitState.CLOSED
    
    def test_half_open_to_open_on_failure(self, circuit_breaker_instance):
        """Test transition from HALF_OPEN back to OPEN on reaching failure threshold."""
        cb = circuit_breaker_instance
        
        # Force to HALF_OPEN state
        cb._transition_to_half_open()
        
        def failing_function():
            raise Exception("Service still failing")
        
        # Need to reach failure threshold (default 5) to transition to OPEN
        for i in range(cb.config.failure_threshold):
            with pytest.raises(Exception):
                cb.call(failing_function)
        
        assert cb.state == CircuitState.OPEN


# =========================================================================
# Unit Tests for Exponential Backoff
# =========================================================================

@pytest.mark.unit
class TestExponentialBackoff:
    """Test exponential backoff behavior."""
    
    def test_initial_timeout(self, circuit_breaker_instance):
        """Test initial timeout duration."""
        cb = circuit_breaker_instance
        
        assert cb._current_timeout == cb.config.timeout_duration
    
    def test_exponential_backoff_calculation(self, circuit_breaker_instance):
        """Test exponential backoff timeout calculation with max cap."""
        cb = circuit_breaker_instance
        initial_timeout = cb.config.timeout_duration  # 30.0
        multiplier = cb.config.backoff_multiplier     # 2.0
        max_timeout = cb.config.max_timeout_duration  # 300.0
        
        # First transition to OPEN
        cb._transition_to_open()
        expected_1 = min(initial_timeout * multiplier, max_timeout)
        assert cb._current_timeout == expected_1
        
        # Second transition to OPEN  
        cb._transition_to_open()
        expected_2 = min(expected_1 * multiplier, max_timeout)
        assert cb._current_timeout == expected_2
        
        # Third transition to OPEN
        cb._transition_to_open()
        expected_3 = min(expected_2 * multiplier, max_timeout)
        assert cb._current_timeout == expected_3
    
    def test_max_timeout_limit(self, circuit_breaker_instance):
        """Test maximum timeout duration limit."""
        cb = circuit_breaker_instance
        
        # Set current timeout beyond max
        cb._current_timeout = cb.config.max_timeout_duration * 2
        
        # Transition should cap at max timeout
        cb._transition_to_open()
        assert cb._current_timeout == cb.config.max_timeout_duration
    
    def test_timeout_reset_on_recovery(self, circuit_breaker_instance):
        """Test timeout reset when transitioning to CLOSED."""
        cb = circuit_breaker_instance
        
        # Increase timeout through multiple failures
        cb._current_timeout = 50.0
        
        # Transition to CLOSED should reset timeout
        cb._transition_to_closed()
        assert cb._current_timeout == cb.config.timeout_duration


# =========================================================================
# Unit Tests for Metrics Tracking
# =========================================================================

@pytest.mark.unit
class TestMetricsTracking:
    """Test metrics tracking functionality."""
    
    def test_successful_request_metrics(self, circuit_breaker_instance):
        """Test metrics for successful requests."""
        cb = circuit_breaker_instance
        
        def success_function():
            return "success"
        
        result = cb.call(success_function)
        
        assert result == "success"
        assert cb.metrics.total_requests == 1
        assert cb.metrics.successful_requests == 1
        assert cb.metrics.failed_requests == 0
        assert cb.metrics.consecutive_successes == 1
        assert cb.metrics.consecutive_failures == 0
    
    def test_failed_request_metrics(self, circuit_breaker_instance):
        """Test metrics for failed requests."""
        cb = circuit_breaker_instance
        
        def failing_function():
            raise Exception("Service error")
        
        with pytest.raises(Exception):
            cb.call(failing_function)
        
        assert cb.metrics.total_requests == 1
        assert cb.metrics.successful_requests == 0
        assert cb.metrics.failed_requests == 1
        assert cb.metrics.consecutive_successes == 0
        assert cb.metrics.consecutive_failures == 1
        assert cb.metrics.last_failure_time is not None
    
    def test_mixed_request_metrics(self, circuit_breaker_instance):
        """Test metrics for mixed successful and failed requests."""
        cb = circuit_breaker_instance
        
        def conditional_function(should_succeed):
            if should_succeed:
                return "success"
            else:
                raise Exception("failure")
        
        # Pattern: success, fail, success, fail
        cb.call(conditional_function, True)
        
        with pytest.raises(Exception):
            cb.call(conditional_function, False)
        
        cb.call(conditional_function, True)
        
        with pytest.raises(Exception):
            cb.call(conditional_function, False)
        
        assert cb.metrics.total_requests == 4
        assert cb.metrics.successful_requests == 2
        assert cb.metrics.failed_requests == 2
        
        # Check success rate via status
        status = cb.get_status()
        assert status["metrics"]["success_rate"] == 50.0
    
    def test_state_change_metrics(self, circuit_breaker_instance):
        """Test state change counting."""
        cb = circuit_breaker_instance
        initial_changes = cb.metrics.state_changes
        
        # Trigger state changes
        cb._transition_to_open()
        assert cb.metrics.state_changes == initial_changes + 1
        
        cb._transition_to_half_open()
        assert cb.metrics.state_changes == initial_changes + 2
        
        cb._transition_to_closed()
        assert cb.metrics.state_changes == initial_changes + 3


# =========================================================================
# Unit Tests for Status Reporting
# =========================================================================

@pytest.mark.unit
class TestStatusReporting:
    """Test status reporting functionality."""
    
    def test_get_status_closed_state(self, circuit_breaker_instance):
        """Test status reporting for CLOSED state."""
        cb = circuit_breaker_instance
        
        status = cb.get_status()
        
        assert status["name"] == "test_service"
        assert status["state"] == "closed"
        assert status["metrics"]["total_requests"] == 0
        assert status["metrics"]["success_rate"] == 0.0
        assert status["metrics"]["consecutive_failures"] == 0
        assert status["timeout_remaining"] == 0.0
        assert "last_failure_time" in status["metrics"]
        assert "current_timeout" in status
    
    def test_get_status_open_state(self, circuit_breaker_instance):
        """Test status reporting for OPEN state."""
        cb = circuit_breaker_instance
        
        # Force to OPEN state
        cb._transition_to_open()
        cb._last_failure_time = time.time()
        
        status = cb.get_status()
        
        assert status["state"] == "open"
        assert status["timeout_remaining"] > 0
        assert status["current_timeout"] > 0
    
    def test_get_status_with_metrics(self, circuit_breaker_instance):
        """Test status reporting with actual metrics."""
        cb = circuit_breaker_instance
        
        # Generate some metrics
        def mixed_function(succeed):
            if succeed:
                return "ok"
            raise Exception("fail")
        
        cb.call(mixed_function, True)
        
        with pytest.raises(Exception):
            cb.call(mixed_function, False)
        
        status = cb.get_status()
        
        assert status["metrics"]["total_requests"] == 2
        assert status["metrics"]["success_rate"] == 50.0
        assert status["metrics"]["consecutive_failures"] == 1


# =========================================================================
# Unit Tests for Async Support
# =========================================================================

@pytest.mark.unit
class TestAsyncSupport:
    """Test async function support."""
    
    @pytest.mark.asyncio
    async def test_async_successful_call(self, circuit_breaker_instance):
        """Test successful async function call."""
        cb = circuit_breaker_instance
        
        async def async_success_function():
            await asyncio.sleep(0.01)
            return "async_success"
        
        result = await cb.call_async(async_success_function)
        
        assert result == "async_success"
        assert cb.metrics.total_requests == 1
        assert cb.metrics.successful_requests == 1
    
    @pytest.mark.asyncio
    async def test_async_failed_call(self, circuit_breaker_instance):
        """Test failed async function call."""
        cb = circuit_breaker_instance
        
        async def async_failing_function():
            await asyncio.sleep(0.01)
            raise Exception("async_failure")
        
        with pytest.raises(Exception) as exc_info:
            await cb.call_async(async_failing_function)
        
        assert "async_failure" in str(exc_info.value)
        assert cb.metrics.total_requests == 1
        assert cb.metrics.failed_requests == 1
    
    @pytest.mark.asyncio
    async def test_async_circuit_breaker_error(self, circuit_breaker_instance):
        """Test CircuitBreakerError with async calls."""
        cb = circuit_breaker_instance
        
        # Force to OPEN state
        cb._transition_to_open()
        
        async def async_function():
            return "should_not_execute"
        
        with pytest.raises(CircuitBreakerError):
            await cb.call_async(async_function)


# =========================================================================
# Unit Tests for Decorator Functionality
# =========================================================================

@pytest.mark.unit
class TestDecoratorFunctionality:
    """Test circuit breaker decorator."""
    
    def test_decorator_sync_function(self, test_config):
        """Test decorator with synchronous function."""
        
        @circuit_breaker("sync_service", test_config)
        def sync_function(value):
            if value == "fail":
                raise Exception("Sync failure")
            return f"sync_{value}"
        
        # Test successful call
        result = sync_function("success")
        assert result == "sync_success"
        
        # Test failed call
        with pytest.raises(Exception):
            sync_function("fail")
    
    @pytest.mark.asyncio
    async def test_decorator_async_function(self, test_config):
        """Test decorator with asynchronous function."""
        
        @circuit_breaker("async_service", test_config)
        async def async_function(value):
            await asyncio.sleep(0.01)
            if value == "fail":
                raise Exception("Async failure")
            return f"async_{value}"
        
        # Test successful call
        result = await async_function("success")
        assert result == "async_success"
        
        # Test failed call
        with pytest.raises(Exception):
            await async_function("fail")
    
    def test_decorator_circuit_breaker_behavior(self, test_config):
        """Test that decorator enforces circuit breaker behavior."""
        
        @circuit_breaker("test_decorator_service", test_config)
        def unstable_function():
            raise Exception("Always fails")
        
        # Trigger failures to open circuit
        for _ in range(test_config.failure_threshold):
            with pytest.raises(Exception):
                unstable_function()
        
        # Next call should raise CircuitBreakerError
        with pytest.raises(CircuitBreakerError):
            unstable_function()


# =========================================================================
# Unit Tests for Registry Management
# =========================================================================

@pytest.mark.unit
class TestRegistryManagement:
    """Test circuit breaker registry functionality."""
    
    def setup_method(self):
        """Clear registry before each test for isolation."""
        from backend.circuit_breaker import _circuit_breakers, _registry_lock
        with _registry_lock:
            _circuit_breakers.clear()
    
    def test_get_circuit_breaker_creates_new(self):
        """Test that get_circuit_breaker creates new instances."""
        cb1 = get_circuit_breaker("new_service")
        
        assert cb1.name == "new_service"
        assert cb1.state == CircuitState.CLOSED
    
    def test_get_circuit_breaker_returns_existing(self):
        """Test that get_circuit_breaker returns existing instances."""
        cb1 = get_circuit_breaker("existing_service")
        cb2 = get_circuit_breaker("existing_service")
        
        assert cb1 is cb2  # Same instance
        assert cb1.name == cb2.name
    
    def test_get_all_circuit_breakers(self):
        """Test getting all registered circuit breakers."""
        # Create several circuit breakers
        cb1 = get_circuit_breaker("service1")
        cb2 = get_circuit_breaker("service2")
        cb3 = get_circuit_breaker("service3")
        
        all_breakers = get_all_circuit_breakers()
        
        assert len(all_breakers) == 3
        assert "service1" in all_breakers
        assert "service2" in all_breakers
        assert "service3" in all_breakers
        assert all_breakers["service1"] is cb1
        assert all_breakers["service2"] is cb2
        assert all_breakers["service3"] is cb3
    
    def test_reset_all_circuit_breakers(self):
        """Test resetting all circuit breakers."""
        # Create and modify circuit breakers
        cb1 = get_circuit_breaker("service1")
        cb2 = get_circuit_breaker("service2")
        
        # Trigger some state changes
        cb1._transition_to_open()
        cb2._transition_to_half_open()
        
        # Reset all
        reset_all_circuit_breakers()
        
        # Should still have the same breakers, but all reset to CLOSED state
        all_breakers = get_all_circuit_breakers()
        assert len(all_breakers) == 2
        assert all_breakers["service1"].state == CircuitState.CLOSED
        assert all_breakers["service2"].state == CircuitState.CLOSED
        
        # Getting same names should return same instances (registry pattern)
        new_cb1 = get_circuit_breaker("service1")
        assert new_cb1 is cb1  # Same instance from registry
        assert new_cb1.state == CircuitState.CLOSED  # But state should be reset


# =========================================================================
# Unit Tests for Error Handling
# =========================================================================

@pytest.mark.unit
class TestErrorHandling:
    """Test error handling in circuit breaker."""
    
    def test_circuit_breaker_error_attributes(self):
        """Test CircuitBreakerError attributes."""
        error = CircuitBreakerError("test_service", 30.5)
        
        assert error.service_name == "test_service"
        assert error.timeout_remaining == 30.5
        assert "test_service" in str(error)
        assert "30.5" in str(error)
    
    def test_function_exception_propagation(self, circuit_breaker_instance):
        """Test that original function exceptions are propagated."""
        cb = circuit_breaker_instance
        
        def function_with_specific_error():
            raise ValueError("Specific error message")
        
        with pytest.raises(ValueError) as exc_info:
            cb.call(function_with_specific_error)
        
        assert "Specific error message" in str(exc_info.value)
    
    def test_circuit_breaker_vs_function_exceptions(self, circuit_breaker_instance):
        """Test distinction between CircuitBreakerError and function exceptions."""
        cb = circuit_breaker_instance
        
        # Force circuit to OPEN
        cb._transition_to_open()
        
        def normal_function():
            return "success"
        
        # Should raise CircuitBreakerError, not function exception
        with pytest.raises(CircuitBreakerError):
            cb.call(normal_function)
    
    def test_reset_clears_state(self, circuit_breaker_instance):
        """Test that reset clears circuit breaker state."""
        cb = circuit_breaker_instance
        
        # Generate some state
        cb._transition_to_open()
        cb.metrics.total_requests = 10
        cb.metrics.failed_requests = 5
        
        # Reset
        cb.reset()
        
        # Should be back to initial state
        assert cb.state == CircuitState.CLOSED
        assert cb.metrics.total_requests == 0
        assert cb.metrics.failed_requests == 0
        assert cb._current_timeout == cb.config.timeout_duration


# =========================================================================
# Integration Tests for Circuit Breaker
# =========================================================================

@pytest.mark.unit
class TestCircuitBreakerIntegration:
    """Integration tests for complete circuit breaker workflows."""
    
    def test_complete_failure_recovery_cycle(self, circuit_breaker_instance):
        """Test complete failure and recovery cycle."""
        cb = circuit_breaker_instance
        
        # Phase 1: Normal operation
        def sometimes_failing_function(should_fail=False):
            if should_fail:
                raise Exception("Service error")
            return "success"
        
        # Successful requests
        for _ in range(3):
            result = cb.call(sometimes_failing_function, False)
            assert result == "success"
        
        assert cb.state == CircuitState.CLOSED
        assert cb.metrics.successful_requests == 3
        
        # Phase 2: Service starts failing
        for _ in range(cb.config.failure_threshold):
            with pytest.raises(Exception):
                cb.call(sometimes_failing_function, True)
        
        assert cb.state == CircuitState.OPEN
        
        # Phase 3: Circuit breaker blocks requests
        with pytest.raises(CircuitBreakerError):
            cb.call(sometimes_failing_function, False)
        
        # Phase 4: Wait for timeout and recovery
        cb._last_failure_time = time.time() - cb._current_timeout - 1
        
        # First request after timeout should transition to HALF_OPEN
        result = cb.call(sometimes_failing_function, False)
        assert result == "success"
        assert cb.state == CircuitState.HALF_OPEN
        
        # Phase 5: Successful requests should close circuit
        for _ in range(cb.config.success_threshold - 1):  # -1 because we already made one
            result = cb.call(sometimes_failing_function, False)
            assert result == "success"
        
        assert cb.state == CircuitState.CLOSED
    
    def test_intermittent_failures_dont_open_circuit(self, circuit_breaker_instance):
        """Test that intermittent failures below threshold don't open circuit."""
        cb = circuit_breaker_instance
        
        def intermittent_function(request_number):
            # Fail every 3rd request, but not consecutively
            if request_number % 3 == 0:
                raise Exception("Intermittent failure")
            return f"success_{request_number}"
        
        # Make requests that include failures but not consecutive ones
        for i in range(10):
            if i % 3 == 0:
                with pytest.raises(Exception):
                    cb.call(intermittent_function, i)
            else:
                result = cb.call(intermittent_function, i)
                assert result == f"success_{i}"
        
        # Circuit should remain closed due to non-consecutive failures
        assert cb.state == CircuitState.CLOSED
        assert cb.metrics.total_requests == 10
        assert cb.metrics.failed_requests > 0
        assert cb.metrics.successful_requests > 0 