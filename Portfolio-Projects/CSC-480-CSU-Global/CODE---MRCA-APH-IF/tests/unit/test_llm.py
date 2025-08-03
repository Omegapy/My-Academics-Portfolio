# -------------------------------------------------------------------------
# File: test_llm.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-28
# File Path: tests/unit/test_llm.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the LLM management module (backend/llm.py).
# Tests LLM factory functions, lazy loading patterns, configuration validation,
# and integration with OpenAI and Gemini services. Ensures proper resource
# management and error handling for language model components.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
LLM Management Unit Tests

Comprehensive testing of LLM and embeddings functionality:
- Configuration validation for OpenAI and Gemini APIs
- Factory functions for LLM and embeddings creation
- Lazy loading patterns and resource management
- Error handling and resilience testing
- Integration with configuration management
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Any

# Import LLM components
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.llm import (
    validate_openai_config, validate_gemini_config,
    get_llm, get_embeddings,
    LazyLLM, LazyEmbeddings,
    llm, embeddings
)


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def mock_config():
    """Provide mock configuration for testing."""
    config = Mock()
    config.openai_api_key = "sk-test-openai-key"
    config.openai_model = "gpt-4o"
    config.gemini_api_key = "test-gemini-key"
    config.gemini_model = "models/embedding-001"
    return config

@pytest.fixture
def invalid_config():
    """Provide invalid configuration for testing."""
    config = Mock()
    config.openai_api_key = None
    config.openai_model = "gpt-4o"
    config.gemini_api_key = None
    config.gemini_model = "models/embedding-001"
    return config

@pytest.fixture
def invalid_openai_key_config():
    """Provide configuration with invalid OpenAI key format."""
    config = Mock()
    config.openai_api_key = "invalid-key-format"
    config.openai_model = "gpt-4o"
    config.gemini_api_key = "test-gemini-key"
    config.gemini_model = "models/embedding-001"
    return config


# =========================================================================
# Unit Tests for Configuration Validation
# =========================================================================

# ------------------------------------------------------------------------- TestConfigurationValidation
@pytest.mark.unit
class TestConfigurationValidation:
    """Test configuration validation functions."""
    
    def test_validate_openai_config_success(self, mock_config):
        """Test successful OpenAI configuration validation."""
        with patch('backend.llm.init_config', return_value=mock_config):
            api_key, model = validate_openai_config()
            
            assert api_key == "sk-test-openai-key"
            assert model == "gpt-4o"
    
    def test_validate_openai_config_missing_key(self, invalid_config):
        """Test OpenAI validation failure for missing API key."""
        with patch('backend.llm.init_config', return_value=invalid_config):
            with pytest.raises(ValueError) as exc_info:
                validate_openai_config()
            
            assert "Missing OpenAI API key in configuration" in str(exc_info.value)
    
    def test_validate_openai_config_invalid_format(self, invalid_openai_key_config):
        """Test OpenAI validation failure for invalid key format."""
        with patch('backend.llm.init_config', return_value=invalid_openai_key_config):
            with pytest.raises(ValueError) as exc_info:
                validate_openai_config()
            
            assert "Invalid OpenAI API key format" in str(exc_info.value)
    
    def test_validate_gemini_config_success(self, mock_config):
        """Test successful Gemini configuration validation."""
        with patch('backend.llm.init_config', return_value=mock_config):
            api_key = validate_gemini_config()
            
            assert api_key == "test-gemini-key"
    
    def test_validate_gemini_config_missing_key(self, invalid_config):
        """Test Gemini validation failure for missing API key."""
        with patch('backend.llm.init_config', return_value=invalid_config):
            with pytest.raises(ValueError) as exc_info:
                validate_gemini_config()
            
            assert "GEMINI_API_KEY not found in configuration" in str(exc_info.value)
    
    def test_validate_gemini_config_empty_key(self):
        """Test Gemini validation failure for empty API key."""
        config = Mock()
        config.gemini_api_key = ""

        with patch('backend.llm.init_config', return_value=config):
            with pytest.raises(ValueError) as exc_info:
                validate_gemini_config()

            assert "GEMINI_API_KEY not found in configuration" in str(exc_info.value)


# =========================================================================
# Unit Tests for Factory Functions
# =========================================================================

@pytest.mark.unit
class TestFactoryFunctions:
    """Test LLM and embeddings factory functions."""
    
    @patch('backend.llm.ChatOpenAI')
    @patch('backend.llm.os.environ', {})
    def test_get_llm_success(self, mock_chat_openai, mock_config):
        """Test successful LLM creation."""
        mock_llm_instance = Mock()
        mock_chat_openai.return_value = mock_llm_instance
        
        with patch('backend.llm.validate_openai_config', return_value=("sk-test-key", "gpt-4o")):
            result = get_llm()
            
            assert result == mock_llm_instance
            mock_chat_openai.assert_called_once_with(
                model="gpt-4o",
                temperature=0,
                max_completion_tokens=4096,
                timeout=60
            )
            # Check that environment variable was set
            assert os.environ.get("OPENAI_API_KEY") == "sk-test-key"
    
    @patch('backend.llm.validate_openai_config')
    def test_get_llm_validation_failure(self, mock_validate):
        """Test LLM creation failure due to validation error."""
        mock_validate.side_effect = ValueError("Invalid configuration")
        
        with pytest.raises(ValueError):
            get_llm()
    
    @patch('backend.llm.ChatOpenAI')
    def test_get_llm_initialization_failure(self, mock_chat_openai):
        """Test LLM creation failure during initialization."""
        mock_chat_openai.side_effect = Exception("Connection failed")
        
        with patch('backend.llm.validate_openai_config', return_value=("sk-test-key", "gpt-4o")):
            with pytest.raises(Exception) as exc_info:
                get_llm()
            
            assert "Connection failed" in str(exc_info.value)
    
    @patch('backend.llm.GoogleGenerativeAIEmbeddings')
    @patch('backend.llm.os.environ', {})
    def test_get_embeddings_success(self, mock_embeddings_class):
        """Test successful embeddings creation."""
        mock_embeddings_instance = Mock()
        mock_embeddings_class.return_value = mock_embeddings_instance
        
        with patch('backend.llm.validate_gemini_config', return_value="test-gemini-key"):
            result = get_embeddings()
            
            assert result == mock_embeddings_instance
            mock_embeddings_class.assert_called_once_with(
                model="models/embedding-001"
            )
            # Check that environment variable was set
            assert os.environ.get("GOOGLE_API_KEY") == "test-gemini-key"
    
    @patch('backend.llm.validate_gemini_config')
    def test_get_embeddings_validation_failure(self, mock_validate):
        """Test embeddings creation failure due to validation error."""
        mock_validate.side_effect = ValueError("Invalid Gemini configuration")
        
        with pytest.raises(ValueError):
            get_embeddings()
    
    @patch('backend.llm.GoogleGenerativeAIEmbeddings')
    def test_get_embeddings_initialization_failure(self, mock_embeddings_class):
        """Test embeddings creation failure during initialization."""
        mock_embeddings_class.side_effect = Exception("Gemini API error")
        
        with patch('backend.llm.validate_gemini_config', return_value="test-key"):
            with pytest.raises(Exception) as exc_info:
                get_embeddings()
            
            assert "Gemini API error" in str(exc_info.value)


# =========================================================================
# Unit Tests for Lazy Loading Classes
# =========================================================================

@pytest.mark.unit
class TestLazyLoadingClasses:
    """Test lazy loading wrapper classes."""
    
    def test_lazy_llm_initialization(self):
        """Test LazyLLM initialization."""
        lazy_llm = LazyLLM()
        
        assert lazy_llm._llm is None
    
    @patch('backend.llm.get_llm')
    def test_lazy_llm_attribute_access(self, mock_get_llm):
        """Test LazyLLM attribute access triggers initialization."""
        mock_llm_instance = Mock()
        mock_llm_instance.invoke = Mock(return_value="test response")
        mock_get_llm.return_value = mock_llm_instance
        
        lazy_llm = LazyLLM()
        
        # First access should trigger initialization
        result = lazy_llm.invoke("test query")
        
        mock_get_llm.assert_called_once()
        mock_llm_instance.invoke.assert_called_once_with("test query")
        assert result == "test response"
        assert lazy_llm._llm == mock_llm_instance
    
    @patch('backend.llm.get_llm')
    def test_lazy_llm_subsequent_access(self, mock_get_llm):
        """Test LazyLLM subsequent access doesn't reinitialize."""
        mock_llm_instance = Mock()
        mock_get_llm.return_value = mock_llm_instance
        
        lazy_llm = LazyLLM()
        
        # First access
        _ = lazy_llm.model
        # Second access
        _ = lazy_llm.temperature
        
        # get_llm should only be called once
        mock_get_llm.assert_called_once()
    
    def test_lazy_embeddings_initialization(self):
        """Test LazyEmbeddings initialization."""
        lazy_embeddings = LazyEmbeddings()
        
        assert lazy_embeddings._embeddings is None
    
    @patch('backend.llm.get_embeddings')
    def test_lazy_embeddings_attribute_access(self, mock_get_embeddings):
        """Test LazyEmbeddings attribute access triggers initialization."""
        mock_embeddings_instance = Mock()
        mock_embeddings_instance.embed_documents = Mock(return_value=[[0.1, 0.2, 0.3]])
        mock_get_embeddings.return_value = mock_embeddings_instance
        
        lazy_embeddings = LazyEmbeddings()
        
        # First access should trigger initialization
        result = lazy_embeddings.embed_documents(["test document"])
        
        mock_get_embeddings.assert_called_once()
        mock_embeddings_instance.embed_documents.assert_called_once_with(["test document"])
        assert result == [[0.1, 0.2, 0.3]]
        assert lazy_embeddings._embeddings == mock_embeddings_instance

    @patch('backend.llm.get_embeddings')
    def test_lazy_embeddings_subsequent_access(self, mock_get_embeddings):
        """Test LazyEmbeddings subsequent access doesn't reinitialize."""
        mock_embeddings_instance = Mock()
        mock_get_embeddings.return_value = mock_embeddings_instance

        lazy_embeddings = LazyEmbeddings()

        # First access
        _ = lazy_embeddings.model
        # Second access
        _ = lazy_embeddings.embed_query

        # get_embeddings should only be called once
        mock_get_embeddings.assert_called_once()


# =========================================================================
# Unit Tests for Global Instances
# =========================================================================

@pytest.mark.unit
class TestGlobalInstances:
    """Test global LLM and embeddings instances."""

    def test_global_llm_instance_type(self):
        """Test that global llm instance is LazyLLM."""
        from backend.llm import llm as global_llm

        assert isinstance(global_llm, LazyLLM)
        # Note: _llm may be initialized if accessed elsewhere during test setup

    def test_global_embeddings_instance_type(self):
        """Test that global embeddings instance is LazyEmbeddings."""
        from backend.llm import embeddings as global_embeddings

        assert isinstance(global_embeddings, LazyEmbeddings)
        # Note: _embeddings may be initialized if accessed elsewhere during test setup

    @patch('backend.llm.get_llm')
    def test_global_llm_lazy_loading(self, mock_get_llm):
        """Test that global llm instance uses lazy loading."""
        mock_llm_instance = Mock()
        mock_get_llm.return_value = mock_llm_instance

        from backend.llm import llm as global_llm

        # Reset the lazy loading state for this test
        global_llm._llm = None

        # Access an attribute to trigger lazy loading
        _ = global_llm.model_name

        mock_get_llm.assert_called_once()
        assert global_llm._llm == mock_llm_instance

    @patch('backend.llm.get_embeddings')
    def test_global_embeddings_lazy_loading(self, mock_get_embeddings):
        """Test that global embeddings instance uses lazy loading."""
        mock_embeddings_instance = Mock()
        mock_get_embeddings.return_value = mock_embeddings_instance

        from backend.llm import embeddings as global_embeddings

        # Reset the lazy loading state for this test
        global_embeddings._embeddings = None

        # Access an attribute to trigger lazy loading
        _ = global_embeddings.model

        mock_get_embeddings.assert_called_once()
        assert global_embeddings._embeddings == mock_embeddings_instance


# =========================================================================
# Unit Tests for Error Handling and Edge Cases
# =========================================================================

@pytest.mark.unit
class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge cases."""

    @patch('backend.llm.get_llm')
    def test_lazy_llm_initialization_error(self, mock_get_llm):
        """Test LazyLLM handles initialization errors."""
        mock_get_llm.side_effect = Exception("LLM initialization failed")

        lazy_llm = LazyLLM()

        with pytest.raises(Exception) as exc_info:
            _ = lazy_llm.model

        assert "LLM initialization failed" in str(exc_info.value)

    @patch('backend.llm.get_embeddings')
    def test_lazy_embeddings_initialization_error(self, mock_get_embeddings):
        """Test LazyEmbeddings handles initialization errors."""
        mock_get_embeddings.side_effect = Exception("Embeddings initialization failed")

        lazy_embeddings = LazyEmbeddings()

        with pytest.raises(Exception) as exc_info:
            _ = lazy_embeddings.model

        assert "Embeddings initialization failed" in str(exc_info.value)

    def test_validate_openai_config_with_none_key(self):
        """Test OpenAI validation with None API key."""
        config = Mock()
        config.openai_api_key = None
        config.openai_model = "gpt-4o"

        with patch('backend.llm.init_config', return_value=config):
            with pytest.raises(ValueError) as exc_info:
                validate_openai_config()

            assert "Missing OpenAI API key in configuration" in str(exc_info.value)

    def test_validate_openai_config_with_empty_string_key(self):
        """Test OpenAI validation with empty string API key."""
        config = Mock()
        config.openai_api_key = ""
        config.openai_model = "gpt-4o"

        with patch('backend.llm.init_config', return_value=config):
            with pytest.raises(ValueError) as exc_info:
                validate_openai_config()

            assert "Missing OpenAI API key in configuration" in str(exc_info.value)

    def test_validate_gemini_config_with_none_key(self):
        """Test Gemini validation with None API key."""
        config = Mock()
        config.gemini_api_key = None

        with patch('backend.llm.init_config', return_value=config):
            with pytest.raises(ValueError) as exc_info:
                validate_gemini_config()

            assert "GEMINI_API_KEY not found in configuration" in str(exc_info.value)

    @patch('backend.llm.ChatOpenAI')
    def test_get_llm_environment_variable_setting(self, mock_chat_openai):
        """Test that get_llm properly sets environment variables."""
        mock_llm_instance = Mock()
        mock_chat_openai.return_value = mock_llm_instance

        # Clear environment first
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        with patch('backend.llm.validate_openai_config', return_value=("sk-test-key", "gpt-4o")):
            get_llm()

            assert os.environ.get("OPENAI_API_KEY") == "sk-test-key"

    @patch('backend.llm.GoogleGenerativeAIEmbeddings')
    def test_get_embeddings_environment_variable_setting(self, mock_embeddings_class):
        """Test that get_embeddings properly sets environment variables."""
        mock_embeddings_instance = Mock()
        mock_embeddings_class.return_value = mock_embeddings_instance

        # Clear environment first
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]

        with patch('backend.llm.validate_gemini_config', return_value="test-gemini-key"):
            get_embeddings()

            assert os.environ.get("GOOGLE_API_KEY") == "test-gemini-key"

    def test_lazy_llm_attribute_error_propagation(self):
        """Test that LazyLLM properly propagates AttributeError."""
        mock_llm_instance = Mock()
        # Remove an attribute to trigger AttributeError
        del mock_llm_instance.nonexistent_attribute

        with patch('backend.llm.get_llm', return_value=mock_llm_instance):
            lazy_llm = LazyLLM()

            with pytest.raises(AttributeError):
                _ = lazy_llm.nonexistent_attribute

    def test_lazy_embeddings_attribute_error_propagation(self):
        """Test that LazyEmbeddings properly propagates AttributeError."""
        mock_embeddings_instance = Mock()
        # Remove an attribute to trigger AttributeError
        del mock_embeddings_instance.nonexistent_attribute

        with patch('backend.llm.get_embeddings', return_value=mock_embeddings_instance):
            lazy_embeddings = LazyEmbeddings()

            with pytest.raises(AttributeError):
                _ = lazy_embeddings.nonexistent_attribute


# =========================================================================
# Integration Tests
# =========================================================================

@pytest.mark.unit
class TestIntegration:
    """Test integration scenarios."""

    @patch('backend.llm.ChatOpenAI')
    @patch('backend.llm.GoogleGenerativeAIEmbeddings')
    def test_concurrent_initialization(self, mock_embeddings_class, mock_chat_openai):
        """Test concurrent initialization of LLM and embeddings."""
        mock_llm_instance = Mock()
        mock_embeddings_instance = Mock()
        mock_chat_openai.return_value = mock_llm_instance
        mock_embeddings_class.return_value = mock_embeddings_instance

        with patch('backend.llm.validate_openai_config', return_value=("sk-test-key", "gpt-4o")):
            with patch('backend.llm.validate_gemini_config', return_value="test-gemini-key"):
                llm_result = get_llm()
                embeddings_result = get_embeddings()

                assert llm_result == mock_llm_instance
                assert embeddings_result == mock_embeddings_instance

    def test_configuration_consistency(self):
        """Test that configuration is consistent across function calls."""
        config = Mock()
        config.openai_api_key = "sk-consistent-key"
        config.openai_model = "gpt-4o"
        config.gemini_api_key = "consistent-gemini-key"

        with patch('backend.llm.init_config', return_value=config):
            # Multiple calls should return same configuration
            api_key1, model1 = validate_openai_config()
            api_key2, model2 = validate_openai_config()

            assert api_key1 == api_key2 == "sk-consistent-key"
            assert model1 == model2 == "gpt-4o"

            gemini_key1 = validate_gemini_config()
            gemini_key2 = validate_gemini_config()

            assert gemini_key1 == gemini_key2 == "consistent-gemini-key"
# ------------------------------------------------------------------------- end TestIntegration

# =========================================================================
# End of File
# =========================================================================
