# -------------------------------------------------------------------------
# File: circuit_breaker.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25 
# File Path: backend/circuit_breaker.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module implements the Circuit Breaker pattern for external service resilience
# in the MRCA backend system. It provides protection against cascading failures when
# external services (Neo4j, OpenAI, Gemini) become unavailable by temporarily blocking
# requests to failing services and allowing gradual recovery testing. The module
# includes configurable failure thresholds, exponential backoff, and comprehensive
# metrics tracking for monitoring service health and circuit breaker effectiveness.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Enum: CircuitState - Circuit breaker states (CLOSED, OPEN, HALF_OPEN)
# - Class: CircuitBreakerConfig - Configuration dataclass for circuit breaker behavior
# - Class: CircuitBreakerMetrics - Metrics tracking dataclass for performance monitoring
# - Class: CircuitBreakerError - Custom exception for circuit breaker open state
# - Class: CircuitBreaker - Main circuit breaker implementation with state management
# - Function: circuit_breaker() - Decorator for easy circuit breaker protection
# - Function: get_circuit_breaker() - Factory function for circuit breaker instances
# - Function: get_all_circuit_breakers() - Registry accessor for all circuit breakers
# - Function: reset_all_circuit_breakers() - Registry reset utility function
# - Global Variables: _circuit_breakers, _registry_lock - Thread-safe registry management
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - time: For timing operations and timeout calculations
#   - logging: For circuit breaker operation logging and debugging
#   - enum: For circuit breaker state enumeration
#   - typing: For type hints (Callable, Any, Optional, Dict)
#   - dataclasses: For configuration and metrics data structures
#   - threading.Lock: For thread-safe registry and state management
#   - asyncio: For asynchronous function support and coroutine detection
#   - functools.wraps: For decorator implementation
# - Third-Party: None
# - Local Project Modules: None
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is used throughout the MRCA backend for protecting external service calls:
# - llm.py: Uses circuit breakers to protect OpenAI and Gemini API calls
# - graph.py: Uses circuit breakers to protect Neo4j database connections
# - database.py: Integrates with enhanced database layer for resilience
# - tools/: Various tool modules use circuit breakers for external service protection
# The circuit breaker pattern prevents cascading failures and provides graceful degradation
# when external services experience issues.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Circuit Breaker Implementation for External Service Resilience

Provides circuit breaker pattern to protect against cascading failures
when external services (Neo4j, OpenAI, Gemini) become unavailable.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import time
import logging
import asyncio
from enum import Enum
from typing import Callable, Any, Optional, Dict
from dataclasses import dataclass, field
from threading import Lock
from functools import wraps

# Third-party library imports
# (None for this module)

# Local application/library specific imports
# (None for this module)

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# Global circuit breaker registry and thread lock for singleton pattern
_circuit_breakers: Dict[str, 'CircuitBreaker'] = {}
_registry_lock = Lock()

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class CircuitState
class CircuitState(Enum):
    """Circuit breaker states.

    This enumeration defines the three possible states of a circuit breaker
    following the classic circuit breaker pattern for resilient system design.

    Class Attributes:
        CLOSED: Normal operation state, requests are allowed through.
        OPEN: Circuit is open, requests are blocked to protect downstream services.
        HALF_OPEN: Testing state, limited requests allowed to test service recovery.

    Instance Attributes:
        Inherits from Enum

    Methods:
        Inherits from Enum
    """
    CLOSED = "closed"      # Normal operation, requests allowed
    OPEN = "open"          # Circuit is open, requests blocked
    HALF_OPEN = "half_open"  # Testing if service is recovered
# ------------------------------------------------------------------------- end class CircuitState

# ------------------------------------------------------------------------- class CircuitBreakerConfig
@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior.

    This dataclass defines all configurable parameters for circuit breaker
    operation including failure thresholds, timeout durations, and backoff
    behavior for resilient service protection.

    Class Attributes:
        None

    Instance Attributes:
        failure_threshold (int): Number of failures before opening. Defaults to 5.
        timeout_duration (float): Seconds to wait before trying again. Defaults to 30.0.
        success_threshold (int): Successes needed to close from half-open. Defaults to 3.
        max_timeout_duration (float): Maximum timeout duration. Defaults to 300.0.
        backoff_multiplier (float): Exponential backoff multiplier. Defaults to 2.0.

    Methods:
        None (dataclass with default values)
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    failure_threshold: int = 5          # Number of failures before opening
    timeout_duration: float = 30.0     # Seconds to wait before trying again
    success_threshold: int = 3          # Successes needed to close from half-open
    max_timeout_duration: float = 300.0  # Maximum timeout duration
    backoff_multiplier: float = 2.0    # Exponential backoff multiplier
# ------------------------------------------------------------------------- end class CircuitBreakerConfig

# ------------------------------------------------------------------------- class CircuitBreakerMetrics
@dataclass
class CircuitBreakerMetrics:
    """Metrics tracking for circuit breaker.

    This dataclass tracks comprehensive metrics for circuit breaker operations
    including request counts, timing information, and state change history
    for monitoring and debugging purposes.

    Class Attributes:
        None

    Instance Attributes:
        total_requests (int): Total number of requests processed.
        successful_requests (int): Number of successful requests.
        failed_requests (int): Number of failed requests.
        state_changes (int): Number of state transitions.
        last_failure_time (Optional[float]): Timestamp of last failure.
        last_success_time (Optional[float]): Timestamp of last success.
        consecutive_failures (int): Current consecutive failure count.
        consecutive_successes (int): Current consecutive success count.

    Methods:
        reset_counts(): Reset consecutive counters.
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    state_changes: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    
    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # ------------------------------------------------------------------------- reset_counts()
    def reset_counts(self) -> None:
        """Reset consecutive counters.

        This method resets the consecutive failure and success counters,
        typically called during state transitions to start fresh counting.
        """
        self.consecutive_failures = 0
        self.consecutive_successes = 0
    # ------------------------------------------------------------------------- end reset_counts()
 
# ------------------------------------------------------------------------- end class CircuitBreakerMetrics
 
# ------------------------------------------------------------------------- class CircuitBreakerError
class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open.

    This custom exception is raised when a circuit breaker is in the OPEN state
    and blocks requests to protect downstream services. It provides information
    about the service name and remaining timeout duration.

    Class Attributes:
        None

    Instance Attributes:
        service_name (str): Name of the protected service.
        timeout_remaining (float): Seconds remaining until retry is allowed.

    Methods:
        Inherits from Exception
    """
    
    # -------------------
    # --- Constructor ---
    # -------------------
    
    # ------------------------------------------------------------------------- __init__()
    def __init__(self, service_name: str, timeout_remaining: float) -> None:
        """Initialize CircuitBreakerError with service information.

        Creates an exception indicating that the circuit breaker is open
        and requests are being blocked for the specified service.

        Args:
            service_name (str): Name of the protected service.
            timeout_remaining (float): Seconds until retry is allowed.
        """
        self.service_name = service_name
        self.timeout_remaining = timeout_remaining
        super().__init__(
            f"Circuit breaker is OPEN for {service_name}. "
            f"Retry in {timeout_remaining:.1f}s"
        )
    # ------------------------------------------------------------------------- end __init__()

# ------------------------------------------------------------------------- class CircuitBreaker
class CircuitBreaker:
    """Circuit Breaker implementation for external service calls.

    This class implements the circuit breaker pattern to protect against cascading
    failures by temporarily blocking requests to failing services and allowing
    gradual recovery testing. It provides configurable thresholds, exponential
    backoff, and comprehensive metrics tracking.

    Class Attributes:
        None

    Instance Attributes:
        name (str): Unique name for this circuit breaker instance.
        config (CircuitBreakerConfig): Configuration settings for behavior.
        state (CircuitState): Current circuit breaker state.
        metrics (CircuitBreakerMetrics): Performance and operation metrics.
        lock (Lock): Thread synchronization lock.
        _last_failure_time (Optional[float]): Timestamp of last failure.
        _current_timeout (float): Current timeout duration with backoff.

    Methods:
        _should_allow_request(): Determine if request should be allowed.
        _record_success(): Record successful operation and update state.
        _record_failure(): Record failed operation and update state.
        _transition_to_open(): Transition to OPEN state.
        _transition_to_half_open(): Transition to HALF_OPEN state.
        _transition_to_closed(): Transition to CLOSED state.
        call(): Execute function call with circuit breaker protection.
        call_async(): Execute async function call with protection.
        get_status(): Get current status and metrics.
        reset(): Reset circuit breaker to initial state.
    """

    # -------------------
    # --- Constructor ---
    # -------------------
    
    # ------------------------------------------------------------------------- __init__()
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None) -> None:
        """Initialize circuit breaker with configuration.

        Creates a circuit breaker instance with the specified name and configuration.
        The circuit breaker starts in the CLOSED state allowing normal operation.

        Args:
            name (str): Unique name for this circuit breaker instance.
            config (Optional[CircuitBreakerConfig]): Configuration settings.
                                                   If None, uses default configuration.
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.metrics = CircuitBreakerMetrics()
        self.lock = Lock()
        self._last_failure_time = None
        self._current_timeout = self.config.timeout_duration
        
        logger.info(f"Circuit breaker '{name}' initialized with config: {self.config}")
    # ------------------------------------------------------------------------- end __init__()

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # ------------------------------------------------------------------------- _should_allow_request()
    def _should_allow_request(self) -> bool:
        """Determine if a request should be allowed based on current state.

        This internal method implements the core circuit breaker logic for
        determining whether to allow or block requests based on the current
        state and timing considerations.

        Returns:
            bool: True if request should be allowed, False if blocked.
        """
        current_time = time.time()
        
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if self._last_failure_time and (current_time - self._last_failure_time) >= self._current_timeout:
                # Timeout expired, transition to HALF_OPEN
                self._transition_to_half_open()
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return True
        
        return False
    # ------------------------------------------------------------------------- end _should_allow_request()
    
    # ------------------------------------------------------------------------- _record_success()
    def _record_success(self) -> None:
        """Record a successful operation.

        This method updates metrics and potentially transitions the circuit breaker
        state when a successful operation is recorded. It handles the transition
        from HALF_OPEN to CLOSED state based on success threshold.
        """
        current_time = time.time()
        
        with self.lock:
            self.metrics.total_requests += 1
            self.metrics.successful_requests += 1
            self.metrics.consecutive_successes += 1
            self.metrics.consecutive_failures = 0
            self.metrics.last_success_time = current_time
            
            if self.state == CircuitState.HALF_OPEN:
                if self.metrics.consecutive_successes >= self.config.success_threshold:
                    self._transition_to_closed()
            elif self.state == CircuitState.OPEN:
                # Direct transition from OPEN to CLOSED (shouldn't happen normally)
                self._transition_to_closed()
    # ------------------------------------------------------------------------- end _record_success()
    
    # ------------------------------------------------------------------------- _record_failure()
    def _record_failure(self, error: Exception) -> None:
        """Record a failed operation.

        This method updates metrics and potentially transitions the circuit breaker
        to the OPEN state when failure threshold is exceeded. It implements
        exponential backoff for timeout duration.

        Args:
            error (Exception): The exception that caused the failure.
        """
        current_time = time.time()
        
        with self.lock:
            self.metrics.total_requests += 1
            self.metrics.failed_requests += 1
            self.metrics.consecutive_failures += 1
            self.metrics.consecutive_successes = 0
            self.metrics.last_failure_time = current_time
            self._last_failure_time = current_time
            
            logger.warning(
                f"Circuit breaker '{self.name}' recorded failure: {error}. "
                f"Consecutive failures: {self.metrics.consecutive_failures}"
            )
            
            if self.state in [CircuitState.CLOSED, CircuitState.HALF_OPEN]:
                if self.metrics.consecutive_failures >= self.config.failure_threshold:
                    self._transition_to_open()
    # ------------------------------------------------------------------------- end _record_failure()
    
    # ------------------------------------------------------------------------- _transition_to_open()
    def _transition_to_open(self) -> None:
        """Transition circuit breaker to OPEN state.

        This method transitions the circuit breaker to the OPEN state, implementing
        exponential backoff for the timeout duration and resetting counters.
        """
        old_state = self.state
        self.state = CircuitState.OPEN
        self.metrics.state_changes += 1
        self.metrics.reset_counts()
        
        # Implement exponential backoff
        self._current_timeout = min(
            self._current_timeout * self.config.backoff_multiplier,
            self.config.max_timeout_duration
        )
        
        logger.warning(
            f"Circuit breaker '{self.name}' transitioned: {old_state.value} -> OPEN. "
            f"Timeout: {self._current_timeout:.1f}s"
        )
    # ------------------------------------------------------------------------- end _transition_to_open()
    
    # ------------------------------------------------------------------------- _transition_to_half_open()
    def _transition_to_half_open(self) -> None:
        """Transition circuit breaker to HALF_OPEN state.

        This method transitions the circuit breaker to the HALF_OPEN state
        for testing service recovery. It resets counters and logs the transition.
        """
        old_state = self.state
        self.state = CircuitState.HALF_OPEN
        self.metrics.state_changes += 1
        self.metrics.reset_counts()
        
        logger.info(
            f"Circuit breaker '{self.name}' transitioned: {old_state.value} -> HALF_OPEN. "
            "Testing service recovery..."
        )
    # ------------------------------------------------------------------------- end _transition_to_half_open()
    
    # ------------------------------------------------------------------------- _transition_to_closed()
    def _transition_to_closed(self) -> None:
        """Transition circuit breaker to CLOSED state.

        This method transitions the circuit breaker to the CLOSED state indicating
        successful service recovery. It resets the timeout duration and counters.
        """
        old_state = self.state
        self.state = CircuitState.CLOSED
        self.metrics.state_changes += 1
        self.metrics.reset_counts()
        
        # Reset timeout duration on successful recovery
        self._current_timeout = self.config.timeout_duration
        
        logger.info(
            f"Circuit breaker '{self.name}' transitioned: {old_state.value} -> CLOSED. "
            "Service recovered!"
        )
    # ------------------------------------------------------------------------- end _transition_to_closed()

    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # ------------------------------------------------------------------------- call()
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function call protected by the circuit breaker.

        This method executes a function call with circuit breaker protection,
        recording success or failure and managing state transitions accordingly.

        Args:
            func (Callable): Function to execute.
            *args: Function arguments.
            **kwargs: Function keyword arguments.

        Returns:
            Any: Function result if successful.

        Raises:
            CircuitBreakerError: If circuit is open and requests are blocked.
            Exception: Original function exception if call fails.

        Examples:
            >>> breaker = CircuitBreaker("api_service")
            >>> result = breaker.call(some_api_function, param1, param2=value)
        """
        if not self._should_allow_request():
            timeout_remaining = 0
            if self._last_failure_time:
                timeout_remaining = max(0, self._current_timeout - (time.time() - self._last_failure_time))
            raise CircuitBreakerError(self.name, timeout_remaining)
        
        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            self._record_failure(e)
            raise
    # ------------------------------------------------------------------------- end call()
    
    # ------------------------------------------------------------------------- call_async()
    async def call_async(self, func: Callable, *args, **kwargs) -> Any:
        """Execute an async function call protected by the circuit breaker.

        This method executes an asynchronous function call with circuit breaker
        protection, recording success or failure and managing state transitions.

        Args:
            func (Callable): Async function to execute.
            *args: Function arguments.
            **kwargs: Function keyword arguments.

        Returns:
            Any: Function result if successful.

        Raises:
            CircuitBreakerError: If circuit is open and requests are blocked.
            Exception: Original function exception if call fails.

        Examples:
            >>> breaker = CircuitBreaker("async_service")
            >>> result = await breaker.call_async(some_async_function, param1)
        """
        if not self._should_allow_request():
            timeout_remaining = 0
            if self._last_failure_time:
                timeout_remaining = max(0, self._current_timeout - (time.time() - self._last_failure_time))
            raise CircuitBreakerError(self.name, timeout_remaining)
        
        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            self._record_failure(e)
            raise
    # ------------------------------------------------------------------------- end call_async()
    
    # ------------------------------------------------------------------------- reset()
    def reset(self) -> None:
        """Reset circuit breaker to initial state.

        This method resets the circuit breaker to its initial CLOSED state,
        clearing all metrics and resetting timeout duration. Useful for
        testing or manual recovery scenarios.
        """
        with self.lock:
            self.state = CircuitState.CLOSED
            self.metrics = CircuitBreakerMetrics()
            self._last_failure_time = None
            self._current_timeout = self.config.timeout_duration
            
        logger.info(f"Circuit breaker '{self.name}' reset to initial state")
    # ------------------------------------------------------------------------- end reset()

    # ---------------------------------------------------------------------
    # --- Class Information Methods (Optional, but highly recommended) ---
    # ---------------------------------------------------------------------
    
    # ------------------------------------------------------------------------- get_status()
    def get_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status and metrics.

        This method returns a comprehensive status report including current state,
        timing information, and all tracked metrics for monitoring and debugging.

        Returns:
            Dict[str, Any]: Dictionary containing status and metrics information.

        Examples:
            >>> breaker = CircuitBreaker("test_service")
            >>> status = breaker.get_status()
            >>> print(f"State: {status['state']}, Success rate: {status['metrics']['success_rate']:.1f}%")
        """
        current_time = time.time()
        timeout_remaining = 0
        
        if self.state == CircuitState.OPEN and self._last_failure_time:
            timeout_remaining = max(0, self._current_timeout - (current_time - self._last_failure_time))
        
        return {
            "name": self.name,
            "state": self.state.value,
            "timeout_remaining": timeout_remaining,
            "current_timeout": self._current_timeout,
            "metrics": {
                "total_requests": self.metrics.total_requests,
                "successful_requests": self.metrics.successful_requests,
                "failed_requests": self.metrics.failed_requests,
                "success_rate": (
                    self.metrics.successful_requests / max(1, self.metrics.total_requests) * 100
                ),
                "consecutive_failures": self.metrics.consecutive_failures,
                "consecutive_successes": self.metrics.consecutive_successes,
                "state_changes": self.metrics.state_changes,
                "last_failure_time": self.metrics.last_failure_time,
                "last_success_time": self.metrics.last_success_time,
            }
        }
    # ------------------------------------------------------------------------- end get_status()

# ------------------------------------------------------------------------- end class CircuitBreaker

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# --------------------------
# --- Utility Functions ---
# --------------------------

# ------------------------------------------------------------------------- circuit_breaker()
def circuit_breaker(name: str, config: Optional[CircuitBreakerConfig] = None):
    """Decorator to wrap functions with circuit breaker protection.

    This decorator provides an easy way to apply circuit breaker protection
    to any function or coroutine. It automatically handles both synchronous
    and asynchronous functions.

    Args:
        name (str): Circuit breaker name for identification.
        config (Optional[CircuitBreakerConfig]): Optional configuration.

    Returns:
        Decorator function that wraps the target function.

    Examples:
        >>> @circuit_breaker("api_service")
        ... def call_external_api():
        ...     return requests.get("https://api.example.com")
        
        >>> @circuit_breaker("async_service", CircuitBreakerConfig(failure_threshold=3))
        ... async def call_async_service():
        ...     return await aiohttp.get("https://async.example.com")
    """
    breaker = CircuitBreaker(name, config)
    
    # -----------------------
    # -- Embedded Function --
    # -----------------------
    
    # ------------------------------------------------------------------------- decorator()
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await breaker.call_async(func, *args, **kwargs)
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper
    # ------------------------------------------------------------------------- end decorator()
    
    return decorator
# ------------------------------------------------------------------------- end circuit_breaker()

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# ------------------------------------------------------------------------- get_circuit_breaker()
def get_circuit_breaker(name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
    """Get or create a circuit breaker by name.

    This function implements a registry pattern for circuit breakers, ensuring
    that circuit breakers with the same name return the same instance. This
    allows sharing circuit breaker state across different parts of the application.

    Args:
        name (str): Circuit breaker name for identification.
        config (Optional[CircuitBreakerConfig]): Configuration for new circuit breakers.
                                               Ignored if circuit breaker already exists.

    Returns:
        CircuitBreaker: Circuit breaker instance for the specified name.

    Examples:
        >>> breaker1 = get_circuit_breaker("database")
        >>> breaker2 = get_circuit_breaker("database")  # Same instance
        >>> assert breaker1 is breaker2
    """
    with _registry_lock:
        if name not in _circuit_breakers:
            _circuit_breakers[name] = CircuitBreaker(name, config)
        return _circuit_breakers[name]
# ------------------------------------------------------------------------- end get_circuit_breaker()

# ------------------------------------------------------------------------- get_all_circuit_breakers()
def get_all_circuit_breakers() -> Dict[str, CircuitBreaker]:
    """Get all registered circuit breakers.

    This function returns a copy of all circuit breakers in the global registry,
    useful for monitoring and management purposes.

    Returns:
        Dict[str, CircuitBreaker]: Dictionary mapping names to circuit breaker instances.

    Examples:
        >>> all_breakers = get_all_circuit_breakers()
        >>> for name, breaker in all_breakers.items():
        ...     status = breaker.get_status()
        ...     print(f"{name}: {status['state']}")
    """
    with _registry_lock:
        return _circuit_breakers.copy()
# ------------------------------------------------------------------------- end get_all_circuit_breakers()

# ------------------------
# --- Helper Functions ---
# ------------------------

# ------------------------------------------------------------------------- reset_all_circuit_breakers()
def reset_all_circuit_breakers() -> None:
    """Reset all circuit breakers to initial state.

    This function resets all circuit breakers in the global registry to their
    initial CLOSED state, clearing all metrics and state. Useful for testing
    or recovery scenarios.

    Examples:
        >>> reset_all_circuit_breakers()
        >>> # All circuit breakers are now in CLOSED state with reset metrics
    """
    with _registry_lock:
        for breaker in _circuit_breakers.values():
            breaker.reset()
    logger.info("All circuit breakers reset")
# ------------------------------------------------------------------------- end reset_all_circuit_breakers()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This module is designed to be imported, not executed directly.
# No main execution guard is needed. 

# =========================================================================
# End of File
# =========================================================================