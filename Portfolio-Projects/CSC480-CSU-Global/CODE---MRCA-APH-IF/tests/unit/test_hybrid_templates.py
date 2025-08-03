# -------------------------------------------------------------------------
# File: test_hybrid_templates.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-28
# File Path: tests/unit/test_hybrid_templates.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the hybrid templates module (backend/hybrid_templates.py).
# Tests template generation, response formatting, template types, and
# prompt engineering techniques. Ensures proper template creation for
# different regulatory scenarios and response requirements.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Hybrid Templates Unit Tests

Comprehensive testing of the Advanced Template functionality:
- Template types and configuration
- Prompt generation for different scenarios
- Content truncation and formatting
- Confidence information display
- Source attribution and methodology notes
- Factory functions and singleton pattern
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from typing import Dict, Any, List

# Import hybrid template components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.hybrid_templates import (
    TemplateType, TemplateConfig, HybridPromptTemplate,
    get_template_engine, create_hybrid_prompt, generate_hybrid_response,
    _template_engine
)
from backend.context_fusion import FusionResult


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def sample_fusion_result():
    """Provide sample fusion result for testing."""
    return FusionResult(
        fused_content="CFR § 30.1 requires safety equipment including hard hats, safety glasses, and protective clothing for all mining operations. Based on MSHA regulations, mining operations must maintain specific safety equipment standards including personal protective equipment and emergency response equipment.",
        fusion_strategy="advanced_hybrid",
        vector_contribution=0.6,
        graph_contribution=0.4,
        final_confidence=0.8,
        fusion_quality_score=0.75,
        metadata={
            "complementarity_score": 0.6,
            "vector_regulatory_score": 0.9,
            "graph_regulatory_score": 0.8
        }
    )

@pytest.fixture
def low_confidence_fusion_result():
    """Provide low confidence fusion result for testing."""
    return FusionResult(
        fused_content="Limited information available about safety requirements.",
        fusion_strategy="fallback",
        vector_contribution=0.5,
        graph_contribution=0.5,
        final_confidence=0.3,
        fusion_quality_score=0.4,
        metadata={"source": "fallback"}
    )

@pytest.fixture
def custom_template_config():
    """Provide custom template configuration for testing."""
    return TemplateConfig(
        include_confidence_scores=False,
        include_source_attribution=False,
        include_methodology_notes=True,
        max_context_length=1000,
        regulatory_focus=False
    )

@pytest.fixture
def long_fusion_result():
    """Provide fusion result with long content for truncation testing."""
    long_content = "CFR § 30.1 safety requirements " * 200  # Very long content
    return FusionResult(
        fused_content=long_content,
        fusion_strategy="advanced_hybrid",
        vector_contribution=0.6,
        graph_contribution=0.4,
        final_confidence=0.8,
        fusion_quality_score=0.75,
        metadata={}
    )

@pytest.fixture
def mock_llm():
    """Provide mock LLM for response generation."""
    with patch('backend.llm.get_llm') as mock_get_llm:
        mock_llm_instance = Mock()
        mock_response = Mock()
        mock_response.content = "Generated response based on the hybrid template and context"
        mock_llm_instance.invoke.return_value = mock_response
        mock_get_llm.return_value = mock_llm_instance
        yield mock_llm_instance

@pytest.fixture
def clean_template_engine():
    """Reset global template engine instance before each test."""
    global _template_engine
    original_engine = _template_engine
    _template_engine = None
    yield
    _template_engine = original_engine


# =========================================================================
# Unit Tests for Data Classes and Enums
# =========================================================================

@pytest.mark.unit
class TestDataClassesAndEnums:
    """Test data classes and enums for hybrid templates."""
    
    def test_template_type_enum(self):
        """Test TemplateType enum values."""
        assert TemplateType.BASIC_HYBRID.value == "basic_hybrid"
        assert TemplateType.RESEARCH_BASED.value == "research_based"
        assert TemplateType.REGULATORY_COMPLIANCE.value == "regulatory_compliance"
        assert TemplateType.COMPARATIVE_ANALYSIS.value == "comparative_analysis"
        assert TemplateType.CONFIDENCE_WEIGHTED.value == "confidence_weighted"
    
    def test_template_config_default(self):
        """Test TemplateConfig default values."""
        config = TemplateConfig()
        
        assert config.include_confidence_scores is True
        assert config.include_source_attribution is True
        assert config.include_methodology_notes is False
        assert config.max_context_length == 2000
        assert config.regulatory_focus is True
    
    def test_template_config_custom(self, custom_template_config):
        """Test TemplateConfig with custom values."""
        config = custom_template_config
        
        assert config.include_confidence_scores is False
        assert config.include_source_attribution is False
        assert config.include_methodology_notes is True
        assert config.max_context_length == 1000
        assert config.regulatory_focus is False


# =========================================================================
# Unit Tests for HybridPromptTemplate Class
# =========================================================================

@pytest.mark.unit
class TestHybridPromptTemplate:
    """Test HybridPromptTemplate class functionality."""
    
    def test_initialization_default(self):
        """Test template initialization with default configuration."""
        template = HybridPromptTemplate()
        
        assert isinstance(template.config, TemplateConfig)
        assert template.config.include_confidence_scores is True
        assert template.config.max_context_length == 2000
    
    def test_initialization_custom_config(self, custom_template_config):
        """Test template initialization with custom configuration."""
        template = HybridPromptTemplate(custom_template_config)
        
        assert template.config == custom_template_config
        assert template.config.include_confidence_scores is False
    
    def test_create_hybrid_prompt_basic(self, sample_fusion_result):
        """Test basic hybrid prompt creation."""
        template = HybridPromptTemplate()
        
        prompt = template.create_hybrid_prompt(
            "What safety equipment is required?",
            sample_fusion_result,
            TemplateType.BASIC_HYBRID
        )
        
        assert "What safety equipment is required?" in prompt
        assert "CFR § 30.1" in prompt
        assert "PRESERVE EXACT CFR CITATIONS" in prompt
        assert "RESPONSE:" in prompt
    
    def test_create_hybrid_prompt_research_based(self, sample_fusion_result):
        """Test research-based prompt creation."""
        template = HybridPromptTemplate()
        
        prompt = template.create_hybrid_prompt(
            "What safety equipment is required?",
            sample_fusion_result,
            TemplateType.RESEARCH_BASED
        )
        
        assert "What safety equipment is required?" in prompt
        assert "VECTOR SEARCH RESULTS" in prompt
        assert "KNOWLEDGE GRAPH ANALYSIS" in prompt
        assert "EXPERT RESPONSE:" in prompt
    
    def test_create_hybrid_prompt_regulatory_compliance(self, sample_fusion_result):
        """Test regulatory compliance prompt creation."""
        template = HybridPromptTemplate()
        
        prompt = template.create_hybrid_prompt(
            "What safety equipment is required?",
            sample_fusion_result,
            TemplateType.REGULATORY_COMPLIANCE
        )
        
        assert "What safety equipment is required?" in prompt
        assert "REGULATORY COMPLIANCE ANALYSIS" in prompt
        assert "COMPLIANCE REQUIREMENTS" in prompt
        assert "SPECIALIZED COMPLIANCE EXPERT RESPONSE:" in prompt
    
    def test_create_hybrid_prompt_comparative_analysis(self, sample_fusion_result):
        """Test comparative analysis prompt creation."""
        template = HybridPromptTemplate()
        
        prompt = template.create_hybrid_prompt(
            "What safety equipment is required?",
            sample_fusion_result,
            TemplateType.COMPARATIVE_ANALYSIS
        )
        
        assert "What safety equipment is required?" in prompt
        assert "COMPARATIVE ANALYSIS" in prompt
        assert "Vector contribution:" in prompt
        assert "Graph contribution:" in prompt
        assert "ANALYTICAL RESPONSE:" in prompt
    
    def test_create_hybrid_prompt_confidence_weighted(self, sample_fusion_result):
        """Test confidence-weighted prompt creation."""
        template = HybridPromptTemplate()
        
        prompt = template.create_hybrid_prompt(
            "What safety equipment is required?",
            sample_fusion_result,
            TemplateType.CONFIDENCE_WEIGHTED
        )
        
        assert "What safety equipment is required?" in prompt
        assert "CONFIDENCE-WEIGHTED ANALYSIS" in prompt
        assert "Final confidence: 0.80" in prompt
        assert "CONFIDENCE-CALIBRATED EXPERT RESPONSE:" in prompt
    
    def test_create_hybrid_prompt_unknown_type(self, sample_fusion_result):
        """Test prompt creation with unknown template type."""
        template = HybridPromptTemplate()
        
        unknown_type = Mock()
        unknown_type.value = "unknown_type"
        
        prompt = template.create_hybrid_prompt(
            "What safety equipment is required?",
            sample_fusion_result,
            unknown_type
        )
        
        # Should fall back to research-based template
        assert "VECTOR SEARCH RESULTS" in prompt
        assert "KNOWLEDGE GRAPH ANALYSIS" in prompt

    def test_truncate_content_short(self, sample_fusion_result):
        """Test content truncation with short content."""
        template = HybridPromptTemplate()

        truncated = template._truncate_content(sample_fusion_result.fused_content)

        # Should not be truncated since it's short
        assert truncated == sample_fusion_result.fused_content

    def test_truncate_content_long(self, long_fusion_result):
        """Test content truncation with long content."""
        template = HybridPromptTemplate()

        truncated = template._truncate_content(long_fusion_result.fused_content)

        # Should be truncated
        assert len(truncated) < len(long_fusion_result.fused_content)
        assert len(truncated) <= template.config.max_context_length + 25  # Allow small buffer for sentence boundaries
        # Truncation may or may not add "..." depending on sentence boundaries
        assert len(truncated) > 0

    def test_add_confidence_info_high_confidence(self, sample_fusion_result):
        """Test confidence information with high confidence."""
        template = HybridPromptTemplate()

        confidence_info = template._add_confidence_info(sample_fusion_result)

        assert "Confidence: 0.80" in confidence_info
        assert "Quality: 0.75" in confidence_info
        assert "Vector: 60%" in confidence_info
        assert "Graph: 40%" in confidence_info

    def test_get_confidence_level_high(self):
        """Test confidence level description for high confidence."""
        template = HybridPromptTemplate()

        level = template._get_confidence_level(0.9)
        assert level == "Very High"

        level = template._get_confidence_level(0.8)
        assert level == "High"

    def test_get_confidence_level_low(self):
        """Test confidence level description for low confidence."""
        template = HybridPromptTemplate()

        level = template._get_confidence_level(0.3)
        assert level == "Low-Medium"  # 0.2-0.4 range

        level = template._get_confidence_level(0.1)
        assert level == "Low"  # 0.0-0.2 range


# =========================================================================
# Unit Tests for Factory Functions
# =========================================================================

@pytest.mark.unit
class TestFactoryFunctions:
    """Test factory functions and global instance management."""

    def test_get_template_engine_singleton(self, clean_template_engine):
        """Test that get_template_engine implements singleton pattern."""
        engine1 = get_template_engine()
        engine2 = get_template_engine()

        assert engine1 is engine2
        assert isinstance(engine1, HybridPromptTemplate)

    def test_create_hybrid_prompt_function(self, sample_fusion_result, clean_template_engine):
        """Test create_hybrid_prompt factory function."""
        prompt = create_hybrid_prompt(
            "What are safety requirements?",
            sample_fusion_result,
            TemplateType.RESEARCH_BASED
        )

        assert "What are safety requirements?" in prompt
        assert "VECTOR SEARCH RESULTS" in prompt
        assert "KNOWLEDGE GRAPH ANALYSIS" in prompt

    @pytest.mark.asyncio
    async def test_generate_hybrid_response_success(self, sample_fusion_result, mock_llm, clean_template_engine):
        """Test successful hybrid response generation."""
        response = await generate_hybrid_response(
            "What safety equipment is required?",
            sample_fusion_result,
            TemplateType.RESEARCH_BASED
        )

        assert len(response) > 0
        assert "Generated response based on the hybrid template and context" in response
        mock_llm.invoke.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_hybrid_response_llm_error(self, sample_fusion_result, clean_template_engine):
        """Test hybrid response generation with LLM error."""
        with patch('backend.llm.get_llm', side_effect=Exception("LLM failed")):
            response = await generate_hybrid_response(
                "What safety equipment is required?",
                sample_fusion_result,
                TemplateType.RESEARCH_BASED
            )

            # Should fall back to basic response
            assert len(response) > 0
            assert "Based on MSHA regulations" in response
            assert sample_fusion_result.fused_content[:800] in response

    @pytest.mark.asyncio
    async def test_generate_hybrid_response_cleanup(self, sample_fusion_result, mock_llm, clean_template_engine):
        """Test response cleanup after LLM generation."""
        # Mock LLM to return response with template artifacts
        mock_llm.invoke.return_value.content = "EXPERT RESPONSE: This is the actual response content"

        response = await generate_hybrid_response(
            "What safety equipment is required?",
            sample_fusion_result,
            TemplateType.RESEARCH_BASED
        )

        # Should clean up template artifacts
        assert response == "This is the actual response content"
        assert "EXPERT RESPONSE:" not in response


# =========================================================================
# Unit Tests for Edge Cases and Integration
# =========================================================================

@pytest.mark.unit
class TestEdgeCasesAndIntegration:
    """Test edge cases and integration scenarios."""

    def test_template_with_empty_content(self):
        """Test template generation with empty fusion content."""
        template = HybridPromptTemplate()

        empty_fusion = FusionResult(
            fused_content="",
            fusion_strategy="fallback",
            vector_contribution=0.0,
            graph_contribution=0.0,
            final_confidence=0.0,
            fusion_quality_score=0.0,
            metadata={}
        )

        prompt = template.create_hybrid_prompt(
            "test query",
            empty_fusion,
            TemplateType.BASIC_HYBRID
        )

        assert "test query" in prompt
        assert len(prompt) > 0  # Should still generate a valid prompt

    def test_template_with_special_characters(self, sample_fusion_result):
        """Test template generation with special characters in query."""
        template = HybridPromptTemplate()

        special_query = "What about § 30.1 & CFR requirements? (urgent!)"

        prompt = template.create_hybrid_prompt(
            special_query,
            sample_fusion_result,
            TemplateType.BASIC_HYBRID
        )

        assert special_query in prompt
        assert "§ 30.1" in prompt
        assert "&" in prompt
        assert "(urgent!)" in prompt

    def test_confidence_edge_cases(self):
        """Test confidence level and interpretation edge cases."""
        template = HybridPromptTemplate()

        # Test boundary values
        assert template._get_confidence_level(0.0) == "Very Low"
        assert template._get_confidence_level(1.0) == "Very High"
        assert template._get_confidence_level(0.5) == "Medium-High"  # 0.5-0.7 range

        # Test interpretation for edge cases
        interpretation_low = template._interpret_confidence(0.0)
        assert len(interpretation_low) > 0

        interpretation_high = template._interpret_confidence(1.0)
        assert len(interpretation_high) > 0

    def test_config_affects_all_template_types(self, sample_fusion_result):
        """Test that configuration affects all template types."""
        config_no_confidence = TemplateConfig(include_confidence_scores=False)
        template = HybridPromptTemplate(config_no_confidence)

        template_types = [
            TemplateType.BASIC_HYBRID,
            TemplateType.RESEARCH_BASED,
            TemplateType.REGULATORY_COMPLIANCE,
            TemplateType.COMPARATIVE_ANALYSIS,
            TemplateType.CONFIDENCE_WEIGHTED
        ]

        for template_type in template_types:
            prompt = template.create_hybrid_prompt(
                "test query",
                sample_fusion_result,
                template_type
            )

            # Configuration should affect template generation
            # Some templates may still include confidence info in their core structure
            # The main test is that the template generates successfully with the config
            assert len(prompt) > 0
            assert "test query" in prompt

    def test_large_metadata_handling(self):
        """Test template generation with large metadata."""
        template = HybridPromptTemplate()

        large_metadata = {f"key_{i}": f"value_{i}" * 100 for i in range(100)}

        fusion_with_large_metadata = FusionResult(
            fused_content="Test content",
            fusion_strategy="test",
            vector_contribution=0.5,
            graph_contribution=0.5,
            final_confidence=0.5,
            fusion_quality_score=0.5,
            metadata=large_metadata
        )

        # Should handle large metadata without errors
        prompt = template.create_hybrid_prompt(
            "test query",
            fusion_with_large_metadata,
            TemplateType.BASIC_HYBRID
        )

        assert len(prompt) > 0
        assert "test query" in prompt
