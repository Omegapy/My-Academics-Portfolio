# -------------------------------------------------------------------------
# File: config.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/config.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides centralized configuration management for the MRCA backend system
# using Pydantic settings with support for environment variables, .env files, and
# Streamlit secrets. It handles all configuration aspects including API settings,
# database connections, LLM configurations, CORS policies, logging, and performance
# parameters. The module implements a singleton pattern for global configuration
# access and provides validation and helper functions for specific configuration domains.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: BackendConfig - Main configuration class with Pydantic settings validation
# - Function: init_config() - Initialize and return global configuration instance
# - Function: get_config() - Get current configuration instance
# - Function: validate_config() - Validate critical configuration settings
# - Function: get_database_config() - Get database configuration as dictionary
# - Function: get_llm_config() - Get LLM configuration as dictionary  
# - Function: get_logging_config() - Get logging configuration as dictionary
# - Global Variables: _config_instance, config - Singleton configuration management
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - os: For file system operations and environment variable access
#   - logging: For configuration logging and debug information
#   - typing: For type hints (Optional, Dict, Any)
# - Third-Party:
#   - pydantic_settings.BaseSettings: Base class for settings management
#   - pydantic.Field: Field definition and validation for configuration parameters
#   - toml: For parsing Streamlit secrets.toml configuration files
# - Local Project Modules: None
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is imported throughout the MRCA backend for configuration access:
# - llm.py: Uses get_config() for OpenAI and Gemini API configuration
# - graph.py: Uses get_config() for Neo4j database connection parameters
# - database.py: Uses get_config() for enhanced database configuration
# - main.py: Uses get_config() for API server settings and CORS configuration
# The singleton pattern ensures consistent configuration across all components
# while supporting multiple configuration sources (env vars, .env files, secrets).
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Centralized Configuration Management for MRCA Backend System

Provides comprehensive configuration management using Pydantic settings with
support for environment variables, .env files, and Streamlit secrets for
the Mining Regulatory Compliance Assistant backend system.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import os
import logging
from typing import Optional, Dict, Any

# Third-party library imports
from pydantic_settings import BaseSettings
from pydantic import Field
import toml

# Local application/library specific imports
# (None for this module)

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# Global configuration instance for singleton pattern
_config_instance = None

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class BackendConfig
class BackendConfig(BaseSettings):
    """Backend configuration management using Pydantic settings.

    This class provides comprehensive configuration management for the MRCA backend
    system with automatic loading from environment variables, .env files, and
    Streamlit secrets. It includes validation, type checking, and helper methods
    for accessing configuration from multiple sources.

    Class Attributes:
        Config: Pydantic configuration class defining env file settings.

    Instance Attributes:
        app_name (str): Application name for identification.
        app_version (str): Application version string.
        debug (bool): Debug mode flag for development.
        host (str): Host address to bind the server.
        port (int): Port number for server binding.
        cors_origins (list[str]): CORS allowed origins list.
        cors_methods (list[str]): CORS allowed HTTP methods.
        cors_headers (list[str]): CORS allowed headers.
        neo4j_uri (Optional[str]): Neo4j database URI.
        neo4j_username (Optional[str]): Neo4j database username.
        neo4j_password (Optional[str]): Neo4j database password.
        openai_api_key (Optional[str]): OpenAI API key for LLM access.
        openai_model (str): OpenAI model identifier.
        gemini_api_key (Optional[str]): Google Gemini API key.
        gemini_model (str): Gemini embedding model identifier.
        agent_timeout (int): Agent response timeout in seconds.
        agent_max_iterations (int): Maximum agent iteration limit.
        agent_verbose (bool): Agent verbose logging flag.
        session_timeout (int): Session timeout duration.
        max_sessions (int): Maximum concurrent sessions limit.
        rate_limit_requests (int): Rate limit requests per minute.
        rate_limit_window (int): Rate limit window duration.
        log_level (str): Logging level setting.
        log_format (str): Log format string template.
        request_timeout (int): Request timeout duration.
        agent_max_execution_time (int): Agent maximum execution time.
        health_check_interval (int): Health check interval duration.

    Methods:
        load_streamlit_secrets(): Load configuration from Streamlit secrets files.
        update_from_secrets(): Update configuration values from Streamlit secrets.
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    
    # API Configuration
    app_name: str = Field(default="MRCA Backend API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Host to bind")
    port: int = Field(default=8000, description="Port to bind")
    
    # CORS Configuration
    cors_origins: list[str] = Field(default=["*"], description="CORS allowed origins")
    cors_methods: list[str] = Field(default=["GET", "POST"], description="CORS allowed methods")
    cors_headers: list[str] = Field(default=["*"], description="CORS allowed headers")
    
    # Neo4j Database Configuration
    neo4j_uri: Optional[str] = Field(default=None, description="Neo4j database URI")
    neo4j_username: Optional[str] = Field(default=None, description="Neo4j username")
    neo4j_password: Optional[str] = Field(default=None, description="Neo4j password")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o", description="OpenAI model to use")
    
    # Gemini Configuration  
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API key")
    gemini_model: str = Field(default="models/embedding-001", description="Gemini embedding model")
    
    # Agent Configuration
    agent_timeout: int = Field(default=90, description="Agent response timeout in seconds (increased for Advanced Parallel Hybrid)")
    agent_max_iterations: int = Field(default=5, description="Maximum agent iterations")
    agent_verbose: bool = Field(default=True, description="Agent verbose logging")
    
    # Session Configuration (Persistent sessions while frontend is active)
    session_timeout: int = Field(default=86400, description="Session timeout in seconds - 24 hours for long-running sessions")
    max_sessions: int = Field(default=1000, description="Maximum concurrent sessions")
    
    # API Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Requests per minute per IP")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    # Performance Configuration - Enhanced for Advanced Parallel Hybrid Operations
    request_timeout: int = Field(default=120, description="Request timeout in seconds (increased for complex queries)")
    agent_max_execution_time: int = Field(default=90, description="Agent max execution time (increased for Parallel Hybrid)")
    
    # Server Configuration - Uvicorn timeout settings (No disconnection for active sessions)
    server_timeout_keep_alive: int = Field(default=3600, description="Uvicorn keep-alive timeout - 1 hour for persistent sessions")
    server_timeout_graceful_shutdown: int = Field(default=30, description="Uvicorn graceful shutdown timeout")
    
    # Health Check Configuration
    health_check_interval: int = Field(default=30, description="Health check interval in seconds")
    health_check_timeout: int = Field(default=60, description="Health check timeout in seconds (increased for complex operations)")

    def __str__(self) -> str:
        """Custom string representation that hides sensitive information."""
        # Get all field values
        values = {}
        for field_name, field_info in self.model_fields.items():
            value = getattr(self, field_name)
            # Hide sensitive fields
            if any(sensitive in field_name.lower() for sensitive in ['password', 'key', 'secret']):
                if value:
                    values[field_name] = f"***{value[-4:]}" if len(str(value)) > 4 else "***"
                else:
                    values[field_name] = value
            else:
                values[field_name] = value

        # Format as key=value pairs
        field_strs = [f"{k}={v!r}" for k, v in values.items()]
        return f"{self.__class__.__name__}({', '.join(field_strs)})"

    def __repr__(self) -> str:
        """Custom repr that uses the same logic as __str__."""
        return self.__str__()
    
    # ---------------------------------------------------------------------------------
    
    # -----------------------
    # -- Embedded Classes --
    # ----------------------

    # --------------------------------------------------------------------------------- Config
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    # --------------------------------------------------------------------------------- end Config
    
    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
        
    # --------------------------------------------------------------------------------- load_streamlit_secrets()
    def load_streamlit_secrets(self) -> Dict[str, Any]:
        """Load configuration from Streamlit secrets.toml files.

        This method searches for and loads configuration from Streamlit secrets files
        in multiple potential locations. It supports the standard Streamlit secrets
        format and provides fallback locations for different deployment scenarios.

        Returns:
            Dict[str, Any]: Dictionary containing loaded secrets configuration.

        Examples:
            >>> config = BackendConfig()
            >>> secrets = config.load_streamlit_secrets()
            >>> print("NEO4J_URI" in secrets)
            True
        """
        secrets = {}
        
        # Try different locations for secrets.toml
        secrets_paths = [
            ".streamlit/secrets.toml",
            "../.streamlit/secrets.toml", 
            "frontend/.streamlit/secrets.toml"
        ]
        
        for secrets_path in secrets_paths:
            if os.path.exists(secrets_path):
                try:
                    with open(secrets_path, 'r') as f:
                        secrets.update(toml.load(f))
                    logger.info(f"Loaded secrets from {secrets_path}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load secrets from {secrets_path}: {e}")
                    
        return secrets
    # --------------------------------------------------------------------------------- end load_streamlit_secrets()
        
    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # --------------------------------------------------------------------------------- update_from_secrets()
    def update_from_secrets(self) -> None:
        """Update configuration values from Streamlit secrets.

        This method loads secrets from Streamlit configuration files and updates
        the current configuration instance with values that are not already set.
        It provides a mapping between secret keys and configuration field names.

        Examples:
            >>> config = BackendConfig()
            >>> config.update_from_secrets()
            >>> # Configuration updated with values from secrets.toml
        """
        secrets = self.load_streamlit_secrets()
        
        if secrets:
            # Map secrets to configuration fields
            secret_mappings = {
                "NEO4J_URI": "neo4j_uri",
                "NEO4J_USERNAME": "neo4j_username", 
                "NEO4J_PASSWORD": "neo4j_password",
                "OPENAI_API_KEY": "openai_api_key",
                "OPENAI_MODEL": "openai_model",
                "GEMINI_API_KEY": "gemini_api_key"
            }
            
            for secret_key, config_field in secret_mappings.items():
                if secret_key in secrets and not getattr(self, config_field):
                    setattr(self, config_field, secrets[secret_key])
                    logger.debug(f"Updated {config_field} from secrets")
    # --------------------------------------------------------------------------------- end update_from_secrets()

# ------------------------------------------------------------------------- end class BackendConfig

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# --------------------------
# --- Factory Functions ---
# --------------------------

# --------------------------------------------------------------------------------- init_config()
def init_config() -> BackendConfig:
    """Initialize and return the global configuration instance.

    This function implements a singleton pattern for configuration management,
    creating the global configuration instance on first call and returning
    the existing instance on subsequent calls. It loads configuration from
    all available sources (environment variables, .env files, secrets).

    Returns:
        BackendConfig: The initialized configuration instance.

    Examples:
        >>> config = init_config()
        >>> print(config.app_name)
        MRCA Backend API
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = BackendConfig()
        # Automatically load secrets from Streamlit configuration
        _config_instance.update_from_secrets()
        logger.info("Configuration initialized successfully with secrets loaded")
        
    return _config_instance
# --------------------------------------------------------------------------------- end init_config()

# --------------------------------------------------------------------------------- get_config()
def get_config() -> BackendConfig:
    """Get the current configuration instance.

    This function returns the current global configuration instance, 
    initializing it if it hasn't been created yet. This provides
    convenient access to configuration throughout the application.

    Returns:
        BackendConfig: The current configuration instance.

    Examples:
        >>> config = get_config()
        >>> print(config.debug)
        False
    """
    return init_config()
# --------------------------------------------------------------------------------- end get_config()

# -------------------------------------------
# --- Configuration Domain Helper Functions ---
# -------------------------------------------

# --------------------------------------------------------------------------------- get_database_config()
def get_database_config() -> dict:
    """Get database configuration as a dictionary.

    This function extracts database-specific configuration into a dictionary
    format suitable for Neo4j driver initialization and connection management.
    It includes all necessary parameters for database connectivity.

    Returns:
        dict: Dictionary containing database configuration parameters.

    Examples:
        >>> db_config = get_database_config()
        >>> print("neo4j_uri" in db_config)
        True
        >>> print("neo4j_username" in db_config)
        True
    """
    config = init_config()
    
    return {
        "neo4j_uri": config.neo4j_uri,
        "neo4j_username": config.neo4j_username,
        "neo4j_password": config.neo4j_password,
    }
# --------------------------------------------------------------------------------- end get_database_config()

# --------------------------------------------------------------------------------- get_llm_config()
def get_llm_config() -> dict:
    """Get LLM configuration for OpenAI and Gemini services.

    This function extracts LLM-specific configuration into a dictionary
    format suitable for language model and embedding service initialization.
    It includes API keys, model specifications, and performance parameters.

    Returns:
        dict: Dictionary containing LLM configuration parameters.

    Examples:
        >>> llm_config = get_llm_config()
        >>> print(llm_config["model"])
        gpt-4o
        >>> print(llm_config["temperature"])
        0.0
    """
    config = init_config()
    
    return {
        "openai_api_key": config.openai_api_key,
        "gemini_api_key": config.gemini_api_key,
        "model": config.openai_model,
        "embedding_model": config.gemini_model,
        "temperature": 0.0,  # Default temperature for consistent results
        "timeout": config.agent_timeout,
    }
# --------------------------------------------------------------------------------- end get_llm_config()

# --------------------------------------------------------------------------------- get_logging_config()
def get_logging_config() -> dict:
    """Get logging configuration for the application.

    This function extracts logging-specific configuration into a dictionary
    format suitable for logging configuration and setup.

    Returns:
        dict: Dictionary containing logging configuration parameters.

    Examples:
        >>> log_config = get_logging_config()
        >>> print(log_config["level"])
        INFO
        >>> print("%(asctime)s" in log_config["format"])
        True
    """
    config = init_config()
    
    return {
        "level": config.log_level,
        "format": config.log_format,
    }
# --------------------------------------------------------------------------------- end get_logging_config()

# ------------------------
# --- Helper Functions ---
# ------------------------

# --------------------------------------------------------------------------------- validate_config()
def validate_config(config: BackendConfig) -> None:
    """Validate critical configuration settings.

    This function performs comprehensive validation of configuration settings
    to ensure all required components are properly configured. It checks for
    missing required values, validates formats, and ensures performance
    settings are within acceptable ranges.

    Args:
        config (BackendConfig): The configuration instance to validate.

    Raises:
        ValueError: If any critical configuration validation fails.

    Examples:
        >>> config = get_config()
        >>> validate_config(config)
        >>> # Raises ValueError if validation fails
    """
    errors = []
    
    # Validate Neo4j configuration
    if not config.neo4j_uri:
        errors.append("NEO4J_URI is required")
    if not config.neo4j_username:
        errors.append("NEO4J_USERNAME is required")
    if not config.neo4j_password:
        errors.append("NEO4J_PASSWORD is required")
    
    # Validate OpenAI configuration
    if not config.openai_api_key:
        errors.append("OPENAI_API_KEY is required")
    elif not config.openai_api_key.startswith("sk-"):
        errors.append("OPENAI_API_KEY must start with 'sk-'")
    
    # Validate Gemini configuration
    if not config.gemini_api_key:
        errors.append("GEMINI_API_KEY is required")
    
    # Validate performance settings
    if config.agent_timeout <= 0:
        errors.append("agent_timeout must be positive")
    if config.agent_max_iterations <= 0:
        errors.append("agent_max_iterations must be positive")
    
    if errors:
        error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("Configuration validation passed")
# --------------------------------------------------------------------------------- end validate_config()

# =========================================================================
# Module Initialization / Global Variables
# =========================================================================
# Export the configuration for easy access throughout the application

# Global configuration instance for module-level access
config = init_config()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This module is designed to be imported, not executed directly.
# No main execution guard is needed.

# =========================================================================
# End of File
# =========================================================================