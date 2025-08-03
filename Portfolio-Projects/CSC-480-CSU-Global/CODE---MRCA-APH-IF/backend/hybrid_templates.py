# -------------------------------------------------------------------------
# File: hybrid_templates.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25 
# File Path: backend/hybrid_templates.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module implements advanced prompt templates for the MRCA Advanced Parallel
# Hybrid system. It provides research-based prompt engineering techniques specifically
# designed for combining vector and graph retrieval results in regulatory compliance
# scenarios. The module includes multiple template types optimized for different
# use cases including basic hybrid, research-based, regulatory compliance, comparative
# analysis, and confidence-weighted response generation.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Enum: TemplateType - Available hybrid template types (basic_hybrid, research_based, etc.)
# - Class: TemplateConfig - Configuration dataclass for template customization
# - Class: HybridPromptTemplate - Main template engine for hybrid prompt generation
# - Function: get_template_engine() - Factory function for template engine instances
# - Function: create_hybrid_prompt() - Factory function for prompt creation
# - Function: generate_hybrid_response() - Response generation using templates
# - Various specialized template methods for different regulatory scenarios
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - logging: For template operation logging and debugging
#   - re: For regular expression pattern matching in template processing
#   - typing: For type hints (Dict, List, Any, Optional)
#   - dataclasses: For template configuration data structures
#   - enum: For template type enumeration
# - Third-Party: None
# - Local Project Modules:
#   - .context_fusion: FusionResult data structure from context fusion operations
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is used by the parallel hybrid system for intelligent response generation:
# - parallel_hybrid.py: Uses templates to generate responses from fused contexts
# - main.py: Configures template types through API endpoints
# - context_fusion.py: Provides fusion results that are processed by templates
# The templates implement research-based prompt engineering for optimizing
# the quality and structure of regulatory AI responses.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Third-party library imports
# (None for this module)

# Local application/library specific imports
try:
    # Try relative imports first (when run as module)
    from .context_fusion import FusionResult
except ImportError:
    # Fall back to absolute imports (when run directly from backend directory)
    from context_fusion import FusionResult

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)
# Global template instance for singleton pattern
_template_engine = None

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class TemplateType
class TemplateType(Enum):
    """Available hybrid template types.

    This enumeration defines the available template types for hybrid prompt
    generation. Each template type is optimized for specific regulatory
    use cases and response requirements.

    Class Attributes:
        BASIC_HYBRID: Simple hybrid template for general use cases.
        RESEARCH_BASED: Research-optimized template for detailed analysis.
        REGULATORY_COMPLIANCE: Compliance-focused template for regulatory queries.
        COMPARATIVE_ANALYSIS: Comparative template for multi-source analysis.
        CONFIDENCE_WEIGHTED: Confidence-based template with quality metrics.

    Instance Attributes:
        Inherits from Enum

    Methods:
        Inherits from Enum
    """
    BASIC_HYBRID = "basic_hybrid"
    RESEARCH_BASED = "research_based"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    COMPARATIVE_ANALYSIS = "comparative_analysis"
    CONFIDENCE_WEIGHTED = "confidence_weighted"
# ------------------------------------------------------------------------- end class TemplateType

# ------------------------------------------------------------------------- class TemplateConfig
@dataclass
class TemplateConfig:
    """Configuration for hybrid templates.

    This dataclass defines configuration parameters for customizing template
    behavior including confidence display, source attribution, methodology
    notes, and regulatory focus settings.

    Class Attributes:
        None

    Instance Attributes:
        include_confidence_scores (bool): Include confidence scores in output. Defaults to True.
        include_source_attribution (bool): Include source attribution information. Defaults to True.
        include_methodology_notes (bool): Include methodology explanations. Defaults to False.
        max_context_length (int): Maximum context length for templates. Defaults to 2000.
        regulatory_focus (bool): Enable regulatory-specific optimizations. Defaults to True.

    Methods:
        None (dataclass with default values)
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    include_confidence_scores: bool = True
    include_source_attribution: bool = True
    include_methodology_notes: bool = False
    max_context_length: int = 2000
    regulatory_focus: bool = True
    
# ------------------------------------------------------------------------- end class TemplateConfig

# ------------------------------------------------------------------------- class HybridPromptTemplate
class HybridPromptTemplate:
    """Advanced Prompt Templates for HybridRAG.

    This class implements research-based prompt engineering techniques specifically
    designed for combining vector and graph retrieval results in regulatory compliance
    scenarios. It provides multiple template types optimized for different use cases
    and response requirements.

    Class Attributes:
        None

    Instance Attributes:
        config (TemplateConfig): Template configuration settings.

    Methods:
        create_hybrid_prompt(): Main method for generating hybrid prompts.
        _create_basic_hybrid_template(): Basic hybrid template implementation.
        _create_research_based_template(): Research-optimized template implementation.
        _create_regulatory_compliance_template(): Compliance-focused template implementation.
        _create_comparative_analysis_template(): Comparative analysis template implementation.
        _create_confidence_weighted_template(): Confidence-based template implementation.
        _truncate_content(): Content truncation with sentence boundary preservation.
        _add_confidence_info(): Confidence information formatting.
        _add_source_attribution(): Source attribution information formatting.
        _add_detailed_confidence_breakdown(): Detailed confidence analysis formatting.
        _get_confidence_level(): Numeric to descriptive confidence conversion.
        _interpret_confidence(): Confidence score interpretation explanations.
    """

    # -------------------
    # --- Constructor ---
    # -------------------
    
    # --------------------------------------------------------------------------------- __init__()
    def __init__(self, config: Optional[TemplateConfig] = None) -> None:
        """Initialize advanced prompt templates.

        Creates a prompt template engine with the specified configuration settings.
        The templates are optimized for regulatory compliance scenarios and hybrid
        context processing.

        Args:
            config (Optional[TemplateConfig]): Template configuration options.
                                             If None, uses default TemplateConfig.
        """
        self.config = config or TemplateConfig()
    # --------------------------------------------------------------------------------- end __init__()

    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # --------------------------------------------------------------------------------- create_hybrid_prompt()
    def create_hybrid_prompt(
        self,
        user_query: str,
        fusion_result: FusionResult,
        template_type: TemplateType = TemplateType.RESEARCH_BASED
    ) -> str:
        """Create advanced hybrid prompt from fusion result.

        This method generates specialized prompts optimized for different use cases
        by combining user queries with fused context from VectorRAG and GraphRAG
        using research-based template engineering techniques.

        Args:
            user_query (str): Original user question.
            fusion_result (FusionResult): Result from context fusion.
            template_type (TemplateType): Type of advanced template to use.

        Returns:
            str: Formatted prompt string for LLM processing.

        Examples:
            >>> template = HybridPromptTemplate()
            >>> prompt = template.create_hybrid_prompt("What are safety rules?", fusion_result)
            >>> print(prompt[:100])
        """
        logger.info(f"Creating {template_type.value} template for query: {user_query[:50]}...")
        
        if template_type == TemplateType.BASIC_HYBRID:
            return self._create_basic_hybrid_template(user_query, fusion_result)
        elif template_type == TemplateType.RESEARCH_BASED:
            return self._create_research_based_template(user_query, fusion_result)
        elif template_type == TemplateType.REGULATORY_COMPLIANCE:
            return self._create_regulatory_compliance_template(user_query, fusion_result)
        elif template_type == TemplateType.COMPARATIVE_ANALYSIS:
            return self._create_comparative_analysis_template(user_query, fusion_result)
        elif template_type == TemplateType.CONFIDENCE_WEIGHTED:
            return self._create_confidence_weighted_template(user_query, fusion_result)
        else:
            logger.warning(f"⚠️ Unknown template type: {template_type}, using research based")
            return self._create_research_based_template(user_query, fusion_result)
    # --------------------------------------------------------------------------------- end create_hybrid_prompt()

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # --------------------------------------------------------------------------------- _create_basic_hybrid_template()
    def _create_basic_hybrid_template(self, user_query: str, fusion_result: FusionResult) -> str:
        """Basic hybrid template for simple combination.

        This internal method creates a simple hybrid template that combines
        vector and graph contexts with basic formatting for general use cases.

        Args:
            user_query (str): Original user question.
            fusion_result (FusionResult): Result from context fusion.

        Returns:
            str: Basic hybrid prompt template.
        """
        
        template = f"""You are an expert assistant specialized in mining safety and regulatory compliance.

USER QUESTION: {user_query}

HYBRID CONTEXT INFORMATION:
{self._truncate_content(fusion_result.fused_content)}

{self._add_confidence_info(fusion_result) if self.config.include_confidence_scores else ""}

🚨 CRITICAL INSTRUCTION: PRESERVE EXACT CFR CITATIONS
You MUST preserve all CFR section references EXACTLY as they appear in the context above. 
🚨 DO NOT change, modify, or "correct" any CFR citations (e.g., § 75.1720(a), § 57.15030, etc.).

Please provide a comprehensive answer based on the hybrid context above. Ensure your response:
1. Directly addresses the user's question
2. Includes specific regulatory citations EXACTLY as provided in the context
3. Maintains professional regulatory compliance language
4. Is accurate and well-structured
5. Preserves all CFR section references exactly as written in the context

RESPONSE:"""
        
        return template
    # --------------------------------------------------------------------------------- end _create_basic_hybrid_template()
    
    # --------------------------------------------------------------------------------- _create_research_based_template()
    def _create_research_based_template(self, user_query: str, fusion_result: FusionResult) -> str:
        """Research-based template based on HybridRAG literature.

        This template implements findings from research papers showing that
        explicit instruction about information sources improves response quality
        and enhances the effectiveness of hybrid retrieval systems.

        Args:
            user_query (str): Original user question.
            fusion_result (FusionResult): Result from context fusion.

        Returns:
            str: Research-optimized hybrid prompt template.
        """
        
        methodology_note = ""
        if self.config.include_methodology_notes:
            methodology_note = f"""
METHODOLOGY NOTE:
This response combines information from vector similarity search (semantic) and graph traversal (structural) approaches using {fusion_result.fusion_strategy} fusion with quality score {fusion_result.fusion_quality_score:.2f}.
"""
        
        template = f"""You are a regulatory compliance expert with access to hybrid information retrieval results.

QUERY ANALYSIS:
Original Question: {user_query}
Information Processing: Combined Vector Search + Knowledge Graph Analysis
Fusion Strategy: {fusion_result.fusion_strategy.replace('_', ' ').title()}

VECTOR SEARCH RESULTS:
{self._truncate_content(fusion_result.fused_content)}

KNOWLEDGE GRAPH ANALYSIS:
Structural relationships and regulatory connections identified through graph traversal.

{self._add_source_attribution(fusion_result) if self.config.include_source_attribution else ""}
{self._add_confidence_info(fusion_result) if self.config.include_confidence_scores else ""}
{methodology_note}

🚨 CRITICAL INSTRUCTION: PRESERVE EXACT CFR CITATIONS
You MUST preserve all CFR section references EXACTLY as they appear in the hybrid context above. 
🚨 DO NOT change, modify, or "correct" any CFR citations (e.g., § 75.1720(a), § 57.15030, etc.).
Copy the exact section numbers, subsections, and formatting from the source material.
Regulatory compliance requires precise citation accuracy.

RESPONSE INSTRUCTIONS:
As an expert in mining safety regulations, analyze the hybrid context above and provide a response that:

1. **Direct Answer**: Provide a clear, direct answer to the user's question
2. **Regulatory Precision**: Include specific CFR citations EXACTLY as provided in the context
3. **Source Integration**: Seamlessly integrate information from both semantic and structural sources
4. **Professional Tone**: Use appropriate regulatory compliance language
5. **Completeness**: Ensure all relevant aspects of the question are addressed
6. **Accuracy**: Maintain strict adherence to regulatory requirements and exact citations

Begin your response with a direct answer, then provide supporting details and citations.
REMEMBER: Preserve all CFR section references EXACTLY as written in the context above.

EXPERT RESPONSE:"""
        
        return template
    # --------------------------------------------------------------------------------- end _create_research_based_template()
    
    # --------------------------------------------------------------------------------- _create_regulatory_compliance_template()
    def _create_regulatory_compliance_template(self, user_query: str, fusion_result: FusionResult) -> str:
        """Enhanced specialized template for regulatory compliance queries with mine-type awareness"""
        
        # CHECK FOR OUT-OF-SCOPE QUERIES FIRST
        query_lower = user_query.lower()
        content_lower = fusion_result.fused_content.lower()

        # Check if the user query itself is off-domain
        off_domain_query_indicators = [
            "dog", "cat", "animal", "pet", "sound", "noise", "bark", "meow",
            "weather", "cooking", "recipe", "sports", "music", "movie", "book",
            "car", "travel", "vacation", "restaurant", "food", "clothing",
            "computer", "software", "programming", "internet", "social media",
            "politics", "election", "government", "tax", "finance", "stock",
            "health", "medicine", "doctor", "hospital", "disease", "symptom"
        ]

        # Check if query contains obvious off-domain terms
        query_is_off_domain = any(term in query_lower for term in off_domain_query_indicators)

        # Also check if the retrieved content indicates off-scope
        content_out_of_scope_indicators = [
            "does not directly relate", "does not pertain to", "i don't know",
            "does not include information about", "outside the mining",
            "not related to mining", "about dogs", "about cats", "about animals"
        ]

        content_indicates_off_scope = any(indicator in content_lower for indicator in content_out_of_scope_indicators)

        # If query is clearly out of scope, return appropriate redirection
        if query_is_off_domain or content_indicates_off_scope:
            from backend.tools.general import handle_out_of_scope_questions
            return f"""You are an MSHA regulatory compliance assistant.

USER QUERY: {user_query}

RESPONSE: {handle_out_of_scope_questions(user_query)}

Please ask me about mining safety, MSHA regulations, or related topics instead."""
        
        # ENHANCEMENT: Analyze query for mine type and compliance focus
        query_lower = user_query.lower()
        
        # Determine mine type context
        mine_type_context = "mining operations"
        if "underground" in query_lower and "coal" in query_lower:
            mine_type_context = "underground coal mining"
        elif "surface" in query_lower and "coal" in query_lower:
            mine_type_context = "surface coal mining"
        elif "underground" in query_lower:
            mine_type_context = "underground metal/nonmetal mining"
        elif "surface" in query_lower:
            mine_type_context = "surface metal/nonmetal mining"
        
        # Determine compliance focus area
        compliance_focus = "general compliance"
        if any(term in query_lower for term in ["equipment", "machinery", "tool"]):
            compliance_focus = "equipment compliance"
        elif any(term in query_lower for term in ["safety", "ppe", "protective"]):
            compliance_focus = "safety compliance"
        elif any(term in query_lower for term in ["emergency", "evacuation", "rescue"]):
            compliance_focus = "emergency preparedness"
        elif any(term in query_lower for term in ["electrical", "power", "circuit"]):
            compliance_focus = "electrical safety"
        elif any(term in query_lower for term in ["ventilation", "air", "methane"]):
            compliance_focus = "ventilation compliance"
        
        # ENHANCEMENT: Assess compliance urgency from content
        content_lower = fusion_result.fused_content.lower()
        urgency_assessment = ""
        if any(term in content_lower for term in ["immediate", "emergency", "danger", "fatal"]):
            urgency_assessment = "\nIMMEDIATE ACTION REQUIRED: This query involves safety-critical regulations requiring immediate compliance."
        elif any(term in content_lower for term in ["shall", "must", "required", "mandatory"]):
            urgency_assessment = "\nHIGH PRIORITY: This involves mandatory compliance requirements with strict enforcement."
        elif any(term in content_lower for term in ["should", "recommend", "compliance"]):
            urgency_assessment = "\nMEDIUM PRIORITY: This involves compliance requirements with established timelines."
        else:
            urgency_assessment = "\nINFORMATIONAL: This involves general regulatory guidance and best practices."
        
        # ENHANCEMENT: Enhanced CFR citation analysis
        cfr_citations = re.findall(r'\b\d+\s+CFR\s+(?:Part\s+\d+\s+)?§\s*\d+(?:\([a-zA-Z0-9]+\))*', fusion_result.fused_content)
        citation_summary = ""
        if cfr_citations:
            citation_summary = f"\nIDENTIFIED CFR CITATIONS:\n"
            for citation in cfr_citations[:5]:  # Limit to first 5 citations
                citation_summary += f"• {citation}\n"
        
        template = f"""You are a certified MSHA compliance specialist with expertise in {mine_type_context} regulations.

COMPLIANCE QUERY: {user_query}

COMPLIANCE FOCUS AREA: {compliance_focus.title()}
MINE TYPE CONTEXT: {mine_type_context.title()}

REGULATORY COMPLIANCE ANALYSIS:
{self._truncate_content(fusion_result.fused_content)}

{citation_summary}
{self._add_confidence_info(fusion_result) if self.config.include_confidence_scores else ""}
{urgency_assessment}

🚨 CRITICAL INSTRUCTION: PRESERVE EXACT CFR CITATIONS
You MUST preserve all CFR section references EXACTLY as they appear in the regulatory context above. 
🚨 DO NOT change, modify, or "correct" any CFR citations (e.g., § 75.1720(a), § 57.15030, etc.). 
Preserve the exact section numbers and letters such as (a), subsections, and formatting from the source material.
Copy the exact section numbers, subsections, and formatting from the source material.
Regulatory compliance requires precise citation accuracy.

ENHANCED COMPLIANCE RESPONSE FRAMEWORK:
Your response must follow regulatory compliance standards for {mine_type_context}:

**COMPLIANCE REQUIREMENTS:**
- Cite specific CFR sections EXACTLY as provided in the context above
- Use precise regulatory language ("shall", "must", "required")
- Distinguish between mandatory and recommended practices
- Include compliance deadlines or timeframes if relevant
- Note any mine-type-specific exceptions or conditions

REMEMBER: Preserve all CFR section references EXACTLY as written in the context above.

SPECIALIZED COMPLIANCE EXPERT RESPONSE:"""
        
        return template
    # --------------------------------------------------------------------------------- end _create_regulatory_compliance_template()
    
    # --------------------------------------------------------------------------------- _create_comparative_analysis_template()
    def _create_comparative_analysis_template(self, user_query: str, fusion_result: FusionResult) -> str:
        """Template for comparative analysis showing different information sources"""
        
        # Extract information about vector and graph contributions
        vector_contrib = fusion_result.vector_contribution
        graph_contrib = fusion_result.graph_contribution
        
        template = f"""You are an information analysis expert specializing in regulatory research methodologies.

RESEARCH QUESTION: {user_query}

COMPARATIVE INFORMATION ANALYSIS:
This response combines two complementary research approaches:

**Vector Search Results** (Semantic Similarity - Weight: {vector_contrib:.1%}):
Provides contextually relevant documents and passages based on semantic meaning.

**Knowledge Graph Analysis** (Structural Relationships - Weight: {graph_contrib:.1%}):
Reveals regulatory relationships and structured knowledge connections.

COMBINED CONTEXT:
{self._truncate_content(fusion_result.fused_content)}

FUSION METHODOLOGY:
- Strategy: {fusion_result.fusion_strategy.replace('_', ' ').title()}
- Quality Score: {fusion_result.fusion_quality_score:.2f}/1.0
- Final Confidence: {fusion_result.final_confidence:.2f}/1.0
- Vector contribution: {vector_contrib:.1%}
- Graph contribution: {graph_contrib:.1%}

🚨 CRITICAL INSTRUCTION: PRESERVE EXACT CFR CITATIONS
You MUST preserve all CFR section references EXACTLY as they appear in the context above. 
DO NOT change, modify, or "correct" any CFR citations (e.g., § 75.1720(a), § 57.15030, etc.).

ANALYTICAL RESPONSE INSTRUCTIONS:
Provide a comprehensive answer that:
1. Synthesizes information from both methodological approaches
2. Highlights how different sources complement each other
3. Maintains regulatory accuracy and precision with EXACT CFR citations
4. Acknowledges the strength of the combined approach
5. Preserves all CFR section references exactly as written in the context

Your response should demonstrate the value of hybrid information retrieval in regulatory compliance.

ANALYTICAL RESPONSE:
COMPARATIVE ANALYSIS RESPONSE:"""
        
        return template
    # --------------------------------------------------------------------------------- end _create_comparative_analysis_template()
    
    # --------------------------------------------------------------------------------- _create_confidence_weighted_template()
    def _create_confidence_weighted_template(self, user_query: str, fusion_result: FusionResult) -> str:
        """Template that explicitly incorporates confidence weighting"""
        
        confidence_level = self._get_confidence_level(fusion_result.final_confidence)
        
        template = f"""You are a regulatory expert with access to confidence-scored information retrieval.

QUERY: {user_query}

CONFIDENCE-WEIGHTED ANALYSIS:
- Overall Confidence Level: {confidence_level} ({fusion_result.final_confidence:.2f}/1.0)
- Information Quality Score: {fusion_result.fusion_quality_score:.2f}/1.0
- Fusion Strategy: {fusion_result.fusion_strategy.replace('_', ' ').title()}
- Final confidence: {fusion_result.final_confidence:.2f}

RETRIEVED CONTEXT:
{self._truncate_content(fusion_result.fused_content)}

{self._add_detailed_confidence_breakdown(fusion_result)}

🚨 CRITICAL INSTRUCTION: PRESERVE EXACT CFR CITATIONS
You MUST preserve all CFR section references EXACTLY as they appear in the context above. 
DO NOT change, modify, or "correct" any CFR citations (e.g., § 75.1720(a), § 57.15030, etc.).

CONFIDENCE-AWARE RESPONSE GUIDELINES:
Based on the confidence assessment above, your response should:

**High Confidence (>0.8)**: Provide definitive regulatory guidance with strong citations (EXACT as provided)
**Medium Confidence (0.5-0.8)**: Provide guidance with appropriate caveats and verification recommendations  
**Lower Confidence (<0.5)**: Acknowledge limitations and suggest additional verification

Your response tone and certainty should match the confidence level. Always maintain regulatory accuracy and preserve exact CFR citations.

CONFIDENCE-CALIBRATED EXPERT RESPONSE:"""
        
        return template
    # --------------------------------------------------------------------------------- end _create_confidence_weighted_template()
    
    # --------------------------------------------------------------------------------- _truncate_content()
    def _truncate_content(self, content: str) -> str:
        """Truncate content to fit within template limits.

        This internal method intelligently truncates content to fit within the
        configured maximum context length while attempting to preserve sentence
        boundaries for better readability.

        Args:
            content (str): Original content text to be truncated.

        Returns:
            str: Truncated content with appropriate truncation indicators.
        """
        if len(content) <= self.config.max_context_length:
            return content

        # Truncate but try to end at a sentence boundary
        truncated = content[:self.config.max_context_length]
        last_period = truncated.rfind('.')

        if last_period > self.config.max_context_length * 0.8:  # If period is reasonably close to end
            return truncated[:last_period + 1] + "\n\n[Content truncated for length]"
        else:
            return truncated + "...\n\n[Content truncated for length]"
    # --------------------------------------------------------------------------------- end _truncate_content()
    
    # --------------------------------------------------------------------------------- _add_confidence_info()
    def _add_confidence_info(self, fusion_result: FusionResult) -> str:
        """Add confidence information to template.

        This internal method generates formatted confidence information including
        retrieval confidence scores and quality metrics for template inclusion.

        Args:
            fusion_result (FusionResult): Result from context fusion containing confidence data.

        Returns:
            str: Formatted confidence information block for template insertion.
        """
        confidence_level = self._get_confidence_level(fusion_result.final_confidence)
        
        return f"""
INFORMATION CONFIDENCE:
- Retrieval Confidence: {fusion_result.final_confidence:.2f}/1.0 ({confidence_level})
- Quality: {fusion_result.fusion_quality_score:.2f}/1.0
- Vector: {fusion_result.vector_contribution:.0%}
- Graph: {fusion_result.graph_contribution:.0%}
"""
    # --------------------------------------------------------------------------------- end _add_confidence_info()
    
    # --------------------------------------------------------------------------------- _add_source_attribution()
    def _add_source_attribution(self, fusion_result: FusionResult) -> str:
        """Add source attribution information to template.

        This internal method generates formatted source composition information
        showing the contribution percentages from vector and graph sources.

        Args:
            fusion_result (FusionResult): Result from context fusion containing source data.

        Returns:
            str: Formatted source attribution block for template insertion.
        """
        return f"""
SOURCE COMPOSITION:
- Vector Search Contribution: {fusion_result.vector_contribution:.1%}
- Knowledge Graph Contribution: {fusion_result.graph_contribution:.1%}
- Fusion Method: {fusion_result.fusion_strategy.replace('_', ' ').title()}
"""
    # --------------------------------------------------------------------------------- end _add_source_attribution()
    
    # --------------------------------------------------------------------------------- _add_detailed_confidence_breakdown()
    def _add_detailed_confidence_breakdown(self, fusion_result: FusionResult) -> str:
        """Add detailed confidence breakdown to template.

        This internal method generates comprehensive confidence analysis including
        contribution percentages, quality scores, and interpretive explanations.

        Args:
            fusion_result (FusionResult): Result from context fusion containing detailed metrics.

        Returns:
            str: Formatted detailed confidence analysis block for template insertion.
        """
        return f"""
DETAILED CONFIDENCE ANALYSIS:
- Vector Search Contribution: {fusion_result.vector_contribution:.1%}
- Knowledge Graph Contribution: {fusion_result.graph_contribution:.1%}
- Combined Confidence: {fusion_result.final_confidence:.2f}/1.0
- Information Quality: {fusion_result.fusion_quality_score:.2f}/1.0
- Fusion Strategy: {fusion_result.fusion_strategy.replace('_', ' ').title()}

CONFIDENCE INTERPRETATION:
{self._interpret_confidence(fusion_result.final_confidence)}
"""
    # --------------------------------------------------------------------------------- end _add_detailed_confidence_breakdown()
    
    # --------------------------------------------------------------------------------- _get_confidence_level()
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert numeric confidence to descriptive level.

        This internal method converts numerical confidence scores into
        human-readable descriptive confidence levels for template display.

        Args:
            confidence (float): Numerical confidence score between 0.0 and 1.0.

        Returns:
            str: Descriptive confidence level (High, Medium-High, Medium, Low-Medium, Low).
        """
        if confidence >= 0.9:
            return "Very High"
        elif confidence >= 0.7:
            return "High"
        elif confidence >= 0.5:
            return "Medium-High"
        elif confidence >= 0.4:
            return "Medium"
        elif confidence >= 0.2:
            return "Low-Medium"
        elif confidence > 0.0:
            return "Low"
        else:
            return "Very Low"
    # --------------------------------------------------------------------------------- end _get_confidence_level()
    
    # --------------------------------------------------------------------------------- _interpret_confidence()
    def _interpret_confidence(self, confidence: float) -> str:
        """Provide interpretation of confidence score.

        This internal method generates detailed explanations of what different
        confidence score ranges mean in terms of information quality and reliability.

        Args:
            confidence (float): Numerical confidence score between 0.0 and 1.0.

        Returns:
            str: Detailed interpretation explaining the meaning of the confidence level.
        """
        if confidence >= 0.8:
            return "High confidence indicates strong agreement between sources and high-quality regulatory information."
        elif confidence >= 0.6:
            return "Medium-high confidence suggests good information quality with minor uncertainties."
        elif confidence >= 0.4:
            return "Medium confidence indicates adequate information with some limitations or inconsistencies."
        elif confidence >= 0.2:
            return "Low-medium confidence suggests information may be incomplete or have conflicting elements."
        else:
            return "Low confidence indicates significant limitations in available information - additional verification recommended."
    # --------------------------------------------------------------------------------- end _interpret_confidence()
    
# ------------------------------------------------------------------------- end class HybridPromptTemplate


# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# --------------------------------------------------------------------------------- get_template_engine()
def get_template_engine(config: Optional[TemplateConfig] = None) -> HybridPromptTemplate:
    """Get or create the global template engine instance.

    This function implements a singleton pattern to provide global access to
    the template engine instance with optional configuration override.

    Args:
        config (Optional[TemplateConfig]): Template configuration settings.
                                         If provided, creates new instance with config.

    Returns:
        HybridPromptTemplate: The global template engine instance.

    Examples:
        >>> engine = get_template_engine()
        >>> prompt = engine.create_hybrid_prompt("safety question", fusion_result)
    """
    global _template_engine
    if _template_engine is None or config is not None:
        _template_engine = HybridPromptTemplate(config)
    return _template_engine
# --------------------------------------------------------------------------------- end get_template_engine()

# --------------------------
# --- Utility Functions ---
# --------------------------

# --------------------------------------------------------------------------------- create_hybrid_prompt()
def create_hybrid_prompt(
    user_query: str,
    fusion_result: FusionResult,
    template_type: TemplateType = TemplateType.RESEARCH_BASED,
    config: Optional[TemplateConfig] = None
) -> str:
    """Quick utility function to create hybrid prompts.

    This function provides a convenient interface for creating hybrid prompts
    without directly instantiating the template engine. It handles engine
    creation and template generation in a single call.

    Args:
        user_query (str): Original user question.
        fusion_result (FusionResult): Result from context fusion.
        template_type (TemplateType): Type of template to use. Defaults to RESEARCH_BASED.
        config (Optional[TemplateConfig]): Optional template configuration.

    Returns:
        str: Formatted prompt string ready for LLM processing.

    Examples:
        >>> prompt = create_hybrid_prompt("safety rules", fusion_result)
        >>> print(prompt[:100])
    """
    template_engine = get_template_engine(config)
    return template_engine.create_hybrid_prompt(user_query, fusion_result, template_type)
# --------------------------------------------------------------------------------- end create_hybrid_prompt()

# ------------------------
# --- Helper Functions ---
# ------------------------

# --------------------------------------------------------------------------------- generate_hybrid_response()
async def generate_hybrid_response(
    user_query: str,
    fusion_result: FusionResult,
    template_type: TemplateType = TemplateType.RESEARCH_BASED,
    config: Optional[TemplateConfig] = None
) -> str:
    """Generate complete Advanced Parallel Hybrid response.

    This function provides end-to-end response generation by creating an advanced
    research template, invoking the LLM with the template, and returning a clean
    final response with proper formatting and error handling.

    Args:
        user_query (str): Original user question.
        fusion_result (FusionResult): Result from context fusion.
        template_type (TemplateType): Type of template to use. Defaults to RESEARCH_BASED.
        config (Optional[TemplateConfig]): Optional template configuration.

    Returns:
        str: Final clean response from LLM processing.

    Examples:
        >>> response = await generate_hybrid_response("safety rules", fusion_result)
        >>> print(f"Response length: {len(response)}")
    """
    import asyncio
    try:
        # Try relative imports first (when run as module)
        from .llm import get_llm
    except ImportError:
        # Fall back to absolute imports (when run directly from backend directory)
        from llm import get_llm
    
    try:
        # Step 1: Generate the advanced prompt
        template_engine = get_template_engine(config)
        advanced_prompt = template_engine.create_hybrid_prompt(user_query, fusion_result, template_type)
        
        # Step 2: Invoke LLM with the advanced prompt
        llm = get_llm()
        
        # Run LLM invocation in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: llm.invoke(advanced_prompt)
        )
        
        # Step 3: Extract clean response
        if hasattr(response, 'content'):
            final_response = str(response.content)
        else:
            final_response = str(response)
        
        # Clean up any residual template artifacts
        if "EXPERT RESPONSE:" in final_response:
            final_response = final_response.split("EXPERT RESPONSE:")[-1].strip()
        
        # DEBUGGING: Show final response after template processing
        logger.info(f"\nTEMPLATE PROCESSING COMPLETE:")
        logger.info(f"{'─'*60}")
        logger.info(f"Template type: {template_type.value}")
        logger.info(f"Response length: {len(final_response)} chars")
        logger.info(f"\nFINAL RESPONSE (after template processing):")
        logger.info(f"{'─'*60}")
        logger.info(f"{final_response}")
        logger.info(f"\n" + "="*80)
        logger.info(f"ADVANCED PARALLEL HYBRID PROCESSING COMPLETE")
        logger.info(f"="*80)
        
        return final_response
        
    except Exception as e:
        logger.error(f"❌ Error generating hybrid response: {str(e)}")
        
        # Fallback to basic response without LLM
        return f"""Based on MSHA regulations regarding "{user_query}":

{fusion_result.fused_content[:800]}

This information combines vector search (semantic similarity) and knowledge graph analysis to provide comprehensive regulatory guidance. For specific compliance requirements, please consult the complete CFR documentation.

*Note: Response generated with {fusion_result.fusion_strategy.replace('_', ' ')} fusion strategy with {fusion_result.final_confidence:.2f} confidence.*""" 
# --------------------------------------------------------------------------------- end generate_hybrid_response()

# =========================================================================
# End of File
# =========================================================================