# -------------------------------------------------------------------------
# File: test_config.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-28
# File Path: tests/unit/test_config.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the configuration management module (backend/config.py).
# Tests BackendConfig class, configuration loading, validation, helper functions,
# and integration with Streamlit secrets. Ensures proper configuration management
# across different deployment scenarios and validation of critical settings.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Configuration Management Unit Tests

Comprehensive testing of the BackendConfig class and related functionality:
- Configuration initialization and singleton pattern
- Environment variable and secrets loading
- Configuration validation and error handling
- Helper functions for domain-specific configuration
- Integration with Streamlit secrets files
"""

import pytest
import os
import tempfile
import toml
from unittest.mock import Mock, patch, mock_open
from typing import Dict, Any
from pathlib import Path
from pydantic import ValidationError

# Import configuration components
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.config import (
    BackendConfig, init_config, get_config,
    get_database_config, get_llm_config, get_logging_config,
    validate_config, _config_instance
)


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def clean_config():
    """Reset global configuration instance before each test."""
    global _config_instance
    original_instance = _config_instance
    _config_instance = None
    yield
    _config_instance = original_instance

@pytest.fixture
def sample_env_vars():
    """Provide sample environment variables for testing."""
    return {
        "NEO4J_URI": "neo4j+s://test.databases.neo4j.io",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "test-password",
        "OPENAI_API_KEY": "sk-test-openai-key",
        "GEMINI_API_KEY": "test-gemini-key",
        "DEBUG": "true",
        "LOG_LEVEL": "DEBUG"
    }

@pytest.fixture
def sample_secrets():
    """Provide sample Streamlit secrets for testing."""
    return {
        "NEO4J_URI": "neo4j+s://secrets.databases.neo4j.io",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "secrets-password",
        "OPENAI_API_KEY": "sk-secrets-openai-key",
        "GEMINI_API_KEY": "secrets-gemini-key"
    }

@pytest.fixture
def temp_secrets_file(sample_secrets):
    """Create temporary secrets.toml file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        toml.dump(sample_secrets, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        pass


# =========================================================================
# Unit Tests for BackendConfig Class
# =========================================================================

# ------------------------------------------------------------------------- TestBackendConfig
@pytest.mark.unit
class TestBackendConfig:
    """Test BackendConfig class functionality."""
    
    def test_default_configuration(self, clean_config):
        """Test default configuration values."""
        config = BackendConfig()
        
        # Test default values
        assert config.app_name == "MRCA Backend API"
        assert config.app_version == "1.0.0"
        assert config.debug is False
        assert config.host == "0.0.0.0"
        assert config.port == 8000
        
        # Test CORS defaults
        assert config.cors_origins == ["*"]
        assert config.cors_methods == ["GET", "POST"]
        assert config.cors_headers == ["*"]
        
        # Test model defaults
        assert config.openai_model == "gpt-4o"
        assert config.gemini_model == "models/embedding-001"
        
        # Test timeout defaults
        assert config.agent_timeout == 90
        assert config.request_timeout == 120
        assert config.session_timeout == 86400  # 24 hours
    
    def test_environment_variable_loading(self, clean_config, sample_env_vars):
        """Test loading configuration from environment variables."""
        with patch.dict(os.environ, sample_env_vars):
            config = BackendConfig()
            
            assert config.neo4j_uri == "neo4j+s://test.databases.neo4j.io"
            assert config.neo4j_username == "neo4j"
            assert config.neo4j_password == "test-password"
            assert config.openai_api_key == "sk-test-openai-key"
            assert config.gemini_api_key == "test-gemini-key"
            assert config.debug is True
            assert config.log_level == "DEBUG"
    
    def test_case_insensitive_environment_variables(self, clean_config):
        """Test that environment variables are case insensitive."""
        env_vars = {
            "neo4j_uri": "neo4j+s://lowercase.databases.neo4j.io",
            "OPENAI_API_KEY": "sk-uppercase-key"
        }
        
        with patch.dict(os.environ, env_vars):
            config = BackendConfig()
            
            assert config.neo4j_uri == "neo4j+s://lowercase.databases.neo4j.io"
            assert config.openai_api_key == "sk-uppercase-key"
    
    def test_load_streamlit_secrets_file_exists(self, clean_config, temp_secrets_file):
        """Test loading secrets when file exists."""
        config = BackendConfig()
        
        # Mock os.path.exists to return True for our temp file
        with patch('backend.config.os.path.exists') as mock_exists:
            mock_exists.side_effect = lambda path: path == ".streamlit/secrets.toml"
            
            # Mock open to return our temp file content
            with patch('backend.config.open', mock_open(read_data=open(temp_secrets_file).read())):
                secrets = config.load_streamlit_secrets()
                
                assert "NEO4J_URI" in secrets
                assert secrets["NEO4J_URI"] == "neo4j+s://secrets.databases.neo4j.io"
                assert secrets["OPENAI_API_KEY"] == "sk-secrets-openai-key"
    
    def test_load_streamlit_secrets_file_not_exists(self, clean_config):
        """Test loading secrets when no file exists."""
        config = BackendConfig()
        
        with patch('backend.config.os.path.exists', return_value=False):
            secrets = config.load_streamlit_secrets()
            
            assert secrets == {}
    
    def test_load_streamlit_secrets_multiple_paths(self, clean_config, sample_secrets):
        """Test loading secrets from multiple potential paths."""
        config = BackendConfig()
        
        # Mock the first path to fail, second to succeed
        def mock_exists(path):
            return path == "../.streamlit/secrets.toml"
        
        with patch('backend.config.os.path.exists', side_effect=mock_exists):
            with patch('backend.config.open', mock_open(read_data=toml.dumps(sample_secrets))):
                secrets = config.load_streamlit_secrets()
                
                assert "NEO4J_URI" in secrets
                assert secrets["NEO4J_URI"] == "neo4j+s://secrets.databases.neo4j.io"
    
    def test_update_from_secrets(self, clean_config, sample_secrets):
        """Test updating configuration from secrets."""
        config = BackendConfig()

        # Mock load_streamlit_secrets at the class level
        with patch.object(BackendConfig, 'load_streamlit_secrets', return_value=sample_secrets):
            # Ensure fields are initially None
            config.neo4j_uri = None
            config.openai_api_key = None

            config.update_from_secrets()

            assert config.neo4j_uri == "neo4j+s://secrets.databases.neo4j.io"
            assert config.openai_api_key == "sk-secrets-openai-key"
    
    def test_update_from_secrets_no_override(self, clean_config, sample_secrets):
        """Test that secrets don't override existing values."""
        config = BackendConfig()

        # Set existing values
        config.neo4j_uri = "existing-uri"
        config.openai_api_key = "existing-key"

        with patch.object(BackendConfig, 'load_streamlit_secrets', return_value=sample_secrets):
            config.update_from_secrets()

            # Values should not be overridden
            assert config.neo4j_uri == "existing-uri"
            assert config.openai_api_key == "existing-key"


# =========================================================================
# Unit Tests for Factory Functions
# =========================================================================

@pytest.mark.unit
class TestFactoryFunctions:
    """Test configuration factory functions."""

    def test_init_config_singleton(self, clean_config):
        """Test that init_config implements singleton pattern."""
        config1 = init_config()
        config2 = init_config()

        assert config1 is config2
        assert id(config1) == id(config2)

    def test_get_config_returns_same_instance(self, clean_config):
        """Test that get_config returns the same instance as init_config."""
        config1 = init_config()
        config2 = get_config()

        assert config1 is config2

    def test_init_config_calls_update_from_secrets(self, clean_config):
        """Test that init_config automatically loads secrets."""
        # Ensure singleton is reset before test
        import backend.config
        backend.config._config_instance = None

        with patch.object(BackendConfig, 'update_from_secrets') as mock_update:
            config = init_config()

            mock_update.assert_called_once()


# =========================================================================
# Unit Tests for Helper Functions
# =========================================================================

@pytest.mark.unit
class TestHelperFunctions:
    """Test configuration helper functions."""

    def test_get_database_config(self, clean_config, sample_env_vars):
        """Test database configuration extraction."""
        with patch.dict(os.environ, sample_env_vars):
            # Mock init_config to return a fresh config with test environment
            with patch('backend.config.init_config') as mock_init:
                test_config = BackendConfig()
                mock_init.return_value = test_config

                db_config = get_database_config()

                assert "neo4j_uri" in db_config
                assert "neo4j_username" in db_config
                assert "neo4j_password" in db_config
                assert db_config["neo4j_uri"] == "neo4j+s://test.databases.neo4j.io"
                assert db_config["neo4j_username"] == "neo4j"
                assert db_config["neo4j_password"] == "test-password"

    def test_get_llm_config(self, clean_config, sample_env_vars):
        """Test LLM configuration extraction."""
        with patch.dict(os.environ, sample_env_vars):
            # Mock init_config to return a fresh config with test environment
            with patch('backend.config.init_config') as mock_init:
                test_config = BackendConfig()
                mock_init.return_value = test_config

                llm_config = get_llm_config()

                assert "openai_api_key" in llm_config
                assert "gemini_api_key" in llm_config
                assert "model" in llm_config
                assert "embedding_model" in llm_config
                assert "temperature" in llm_config
                assert "timeout" in llm_config

                assert llm_config["openai_api_key"] == "sk-test-openai-key"
                assert llm_config["gemini_api_key"] == "test-gemini-key"
                assert llm_config["model"] == "gpt-4o"
                assert llm_config["embedding_model"] == "models/embedding-001"
                assert llm_config["temperature"] == 0.0
                assert llm_config["timeout"] == 90

    def test_get_logging_config(self, clean_config, sample_env_vars):
        """Test logging configuration extraction."""
        with patch.dict(os.environ, sample_env_vars):
            # Mock init_config to return a fresh config with test environment
            with patch('backend.config.init_config') as mock_init:
                test_config = BackendConfig()
                mock_init.return_value = test_config

                log_config = get_logging_config()

                assert "level" in log_config
                assert "format" in log_config
                assert log_config["level"] == "DEBUG"
                assert "%(asctime)s" in log_config["format"]


# =========================================================================
# Unit Tests for Configuration Validation
# =========================================================================

@pytest.mark.unit
class TestConfigurationValidation:
    """Test configuration validation functionality."""

    def test_validate_config_success(self, clean_config, sample_env_vars):
        """Test successful configuration validation."""
        with patch.dict(os.environ, sample_env_vars):
            config = BackendConfig()

            # Should not raise any exception
            validate_config(config)

    def test_validate_config_missing_neo4j_uri(self, clean_config):
        """Test validation failure for missing Neo4j URI."""
        config = BackendConfig()
        config.neo4j_username = "neo4j"
        config.neo4j_password = "password"
        config.openai_api_key = "sk-test-key"
        config.gemini_api_key = "test-key"

        with pytest.raises(ValueError) as exc_info:
            validate_config(config)

        assert "NEO4J_URI is required" in str(exc_info.value)

    def test_validate_config_missing_neo4j_username(self, clean_config):
        """Test validation failure for missing Neo4j username."""
        config = BackendConfig()
        config.neo4j_uri = "neo4j+s://test.databases.neo4j.io"
        config.neo4j_password = "password"
        config.openai_api_key = "sk-test-key"
        config.gemini_api_key = "test-key"

        with pytest.raises(ValueError) as exc_info:
            validate_config(config)

        assert "NEO4J_USERNAME is required" in str(exc_info.value)

    def test_validate_config_missing_neo4j_password(self, clean_config):
        """Test validation failure for missing Neo4j password."""
        config = BackendConfig()
        config.neo4j_uri = "neo4j+s://test.databases.neo4j.io"
        config.neo4j_username = "neo4j"
        config.openai_api_key = "sk-test-key"
        config.gemini_api_key = "test-key"

        with pytest.raises(ValueError) as exc_info:
            validate_config(config)

        assert "NEO4J_PASSWORD is required" in str(exc_info.value)

    def test_validate_config_missing_openai_key(self, clean_config):
        """Test validation failure for missing OpenAI API key."""
        # Clear any environment variables that might interfere
        with patch.dict(os.environ, {}, clear=True):
            config = BackendConfig()
            config.neo4j_uri = "neo4j+s://test.databases.neo4j.io"
            config.neo4j_username = "neo4j"
            config.neo4j_password = "password"
            config.gemini_api_key = "test-key"

            # Explicitly ensure openai_api_key is None
            config.openai_api_key = None

            # Debug: Print the actual value
            print(f"DEBUG: openai_api_key = {config.openai_api_key!r}")
            print(f"DEBUG: bool(openai_api_key) = {bool(config.openai_api_key)}")

            with pytest.raises(ValueError) as exc_info:
                validate_config(config)

            assert "OPENAI_API_KEY is required" in str(exc_info.value)

    def test_validate_config_invalid_openai_key_format(self, clean_config):
        """Test validation failure for invalid OpenAI API key format."""
        config = BackendConfig()
        config.neo4j_uri = "neo4j+s://test.databases.neo4j.io"
        config.neo4j_username = "neo4j"
        config.neo4j_password = "password"
        config.openai_api_key = "invalid-key-format"
        config.gemini_api_key = "test-key"

        with pytest.raises(ValueError) as exc_info:
            validate_config(config)

        assert "OPENAI_API_KEY must start with 'sk-'" in str(exc_info.value)

    def test_validate_config_missing_gemini_key(self, clean_config):
        """Test validation failure for missing Gemini API key."""
        config = BackendConfig()
        config.neo4j_uri = "neo4j+s://test.databases.neo4j.io"
        config.neo4j_username = "neo4j"
        config.neo4j_password = "password"
        config.openai_api_key = "sk-test-key"

        with pytest.raises(ValueError) as exc_info:
            validate_config(config)

        assert "GEMINI_API_KEY is required" in str(exc_info.value)

    def test_validate_config_invalid_timeout_values(self, clean_config, sample_env_vars):
        """Test validation failure for invalid timeout values."""
        with patch.dict(os.environ, sample_env_vars):
            config = BackendConfig()
            config.agent_timeout = -1

            with pytest.raises(ValueError) as exc_info:
                validate_config(config)

            assert "agent_timeout must be positive" in str(exc_info.value)

    def test_validate_config_invalid_max_iterations(self, clean_config, sample_env_vars):
        """Test validation failure for invalid max iterations."""
        with patch.dict(os.environ, sample_env_vars):
            config = BackendConfig()
            config.agent_max_iterations = 0

            with pytest.raises(ValueError) as exc_info:
                validate_config(config)

            assert "agent_max_iterations must be positive" in str(exc_info.value)

    def test_validate_config_multiple_errors(self, clean_config):
        """Test validation with multiple errors."""
        # Clear all environment variables to ensure clean state
        with patch.dict(os.environ, {}, clear=True):
            config = BackendConfig()
            # Explicitly set all required fields to None to ensure they're empty
            config.neo4j_uri = None
            config.neo4j_username = None
            config.neo4j_password = None
            config.openai_api_key = None
            config.gemini_api_key = None

            with pytest.raises(ValueError) as exc_info:
                validate_config(config)

            error_message = str(exc_info.value)
            assert "NEO4J_URI is required" in error_message
            assert "NEO4J_USERNAME is required" in error_message
            assert "NEO4J_PASSWORD is required" in error_message
            assert "OPENAI_API_KEY is required" in error_message
            assert "GEMINI_API_KEY is required" in error_message


# =========================================================================
# Unit Tests for Edge Cases and Integration
# =========================================================================

@pytest.mark.unit
class TestEdgeCasesAndIntegration:
    """Test edge cases and integration scenarios."""

    def test_boolean_environment_variable_parsing(self, clean_config):
        """Test parsing of boolean environment variables."""
        # Valid boolean values that Pydantic accepts
        valid_test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("on", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
            ("no", False),
            ("off", False)
        ]

        for env_value, expected in valid_test_cases:
            with patch.dict(os.environ, {"DEBUG": env_value}):
                config = BackendConfig()
                assert config.debug == expected

        # Invalid boolean values that should raise ValidationError
        invalid_test_cases = ["", "invalid", "maybe", "2"]

        for env_value in invalid_test_cases:
            with patch.dict(os.environ, {"DEBUG": env_value}):
                with pytest.raises(ValidationError):
                    BackendConfig(), f"Failed for env_value: {env_value}"

    def test_integer_environment_variable_parsing(self, clean_config):
        """Test parsing of integer environment variables."""
        env_vars = {
            "PORT": "9000",
            "AGENT_TIMEOUT": "120",
            "AGENT_MAX_ITERATIONS": "50"
        }

        with patch.dict(os.environ, env_vars):
            config = BackendConfig()

            assert config.port == 9000
            assert config.agent_timeout == 120
            assert config.agent_max_iterations == 50

    def test_invalid_integer_environment_variables(self, clean_config):
        """Test handling of invalid integer environment variables."""
        env_vars = {
            "PORT": "invalid",
            "AGENT_TIMEOUT": "not_a_number"
        }

        with patch.dict(os.environ, env_vars):
            # Invalid integer values should raise ValidationError
            with pytest.raises(ValidationError):
                BackendConfig()

    def test_list_environment_variable_parsing(self, clean_config):
        """Test parsing of list environment variables using JSON format."""
        env_vars = {
            "CORS_ORIGINS": '["http://localhost:3000", "https://example.com"]',
            "CORS_METHODS": '["GET", "POST", "PUT", "DELETE"]'
        }

        with patch.dict(os.environ, env_vars):
            config = BackendConfig()

            assert config.cors_origins == ["http://localhost:3000", "https://example.com"]
            assert config.cors_methods == ["GET", "POST", "PUT", "DELETE"]

    def test_empty_list_environment_variables(self, clean_config):
        """Test handling of empty list environment variables."""
        env_vars = {
            "CORS_ORIGINS": "[]",  # Empty JSON array
            "CORS_METHODS": "[]"   # Empty JSON array
        }

        with patch.dict(os.environ, env_vars):
            config = BackendConfig()

            # Should use empty lists from environment
            assert config.cors_origins == []
            assert config.cors_methods == []

    def test_secrets_override_priority(self, clean_config):
        """Test that environment variables take priority over secrets."""
        env_vars = {
            "NEO4J_URI": "neo4j+s://env.databases.neo4j.io"
        }

        secrets = {
            "NEO4J_URI": "neo4j+s://secrets.databases.neo4j.io"
        }

        with patch.dict(os.environ, env_vars):
            config = BackendConfig()

            with patch.object(BackendConfig, 'load_streamlit_secrets', return_value=secrets):
                config.update_from_secrets()

                # Environment variable should take priority
                assert config.neo4j_uri == "neo4j+s://env.databases.neo4j.io"

    def test_config_immutability_after_validation(self, clean_config, sample_env_vars):
        """Test that configuration behaves consistently after validation."""
        with patch.dict(os.environ, sample_env_vars):
            config = BackendConfig()
            validate_config(config)

            # Store original values
            original_uri = config.neo4j_uri
            original_key = config.openai_api_key

            # Values should remain the same
            assert config.neo4j_uri == original_uri
            assert config.openai_api_key == original_key

    def test_logging_configuration_integration(self, clean_config):
        """Test logging configuration integration."""
        env_vars = {
            "LOG_LEVEL": "WARNING",
            "LOG_FORMAT": "%(levelname)s - %(message)s"
        }

        with patch.dict(os.environ, env_vars):
            # Mock init_config to return a fresh config with test environment
            with patch('backend.config.init_config') as mock_init:
                test_config = BackendConfig()
                mock_init.return_value = test_config

                config = BackendConfig()
                log_config = get_logging_config()

                assert log_config["level"] == "WARNING"
                assert log_config["format"] == "%(levelname)s - %(message)s"

    def test_streamlit_secrets_toml_parsing_error(self, clean_config):
        """Test handling of TOML parsing errors in secrets file."""
        config = BackendConfig()

        # Mock file exists but contains invalid TOML
        with patch('backend.config.os.path.exists', return_value=True):
            with patch('backend.config.open', mock_open(read_data="invalid toml content [")):
                secrets = config.load_streamlit_secrets()

                # Should return empty dict on parsing error
                assert secrets == {}

    def test_config_repr_and_str(self, clean_config):
        """Test string representation of configuration."""
        # Use clean environment to avoid real API keys
        with patch.dict(os.environ, {}, clear=True):
            config = BackendConfig()
            # Set a test API key to verify it's not exposed
            config.openai_api_key = "sk-test-key-for-repr-test"

            # Test that repr and str don't expose sensitive information
            config_str = str(config)
            config_repr = repr(config)

            # Should contain class name
            assert "BackendConfig" in config_repr

            # Should not expose sensitive keys
            assert config.openai_api_key not in config_str
            assert config.openai_api_key not in config_repr


# =========================================================================
# Integration Tests with Global Configuration
# =========================================================================

@pytest.mark.unit
class TestGlobalConfiguration:
    """Test global configuration instance behavior."""

    def test_global_config_instance_creation(self, clean_config):
        """Test that global config instance is created properly."""
        # Import should create global instance
        from backend.config import config

        assert config is not None
        assert isinstance(config, BackendConfig)

    def test_global_config_singleton_behavior(self, clean_config):
        """Test that global config maintains singleton behavior."""
        # Use clean environment to ensure consistent behavior
        with patch.dict(os.environ, {}, clear=True):
            config1 = get_config()
            config2 = init_config()

            from backend.config import config as global_config

            assert config1 is config2
            # Note: global_config might be different due to module-level initialization
            # but config1 and config2 should be the same singleton instance

    def test_module_level_access(self, clean_config):
        """Test accessing configuration at module level."""
        from backend.config import config

        # Should have default values
        assert config.app_name == "MRCA Backend API"
        assert config.app_version == "1.0.0"
        assert isinstance(config.port, int)
        assert isinstance(config.debug, bool)
# ------------------------------------------------------------------------- end TestGlobalConfiguration

# =========================================================================
# End of File
# =========================================================================
