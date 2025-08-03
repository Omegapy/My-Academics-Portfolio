# -------------------------------------------------------------------------
# File: context_fusion.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/context_fusion.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module implements advanced context fusion algorithms for the MRCA Advanced
# Parallel Hybrid system. It provides sophisticated techniques for combining
# VectorRAG and GraphRAG results using research-based fusion strategies including
# weighted linear combination, maximum confidence selection, advanced hybrid fusion,
# and adaptive dynamic weighting. The module is designed to optimize the quality
# and relevance of combined retrieval results for enhanced regulatory query processing.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Enum: FusionStrategy - Available fusion strategies (weighted_linear, max_confidence, etc.)
# - Class: FusionWeights - Weight configuration dataclass for fusion algorithms
# - Class: FusionResult - Result dataclass containing fusion output and metadata
# - Class: HybridContextFusion - Main fusion engine implementing multiple strategies
# - Function: get_fusion_engine() - Factory function for fusion engine instances
# - Various private methods implementing specific fusion algorithms and quality metrics
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - logging: For fusion operation logging and debugging
#   - math: For mathematical calculations in fusion algorithms
#   - re: For regular expression pattern matching in content analysis
#   - asyncio: For asynchronous fusion operations
#   - typing: For type hints (Dict, List, Any, Optional, Tuple)
#   - dataclasses: For fusion configuration and result data structures
#   - enum: For fusion strategy enumeration
# - Third-Party: None
# - Local Project Modules:
#   - .parallel_hybrid: RetrievalResult, ParallelRetrievalResponse data structures
#   - .llm: get_llm function for LLM-based fusion enhancement
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is used by the parallel hybrid system for intelligent context combination:
# - parallel_hybrid.py: Uses fusion engines to combine VectorRAG and GraphRAG results
# - main.py: Configures fusion strategies through API endpoints
# - hybrid_templates.py: Works with fusion results for response generation
# The fusion strategies implement research-based techniques for optimizing
# the quality and relevance of combined retrieval contexts in regulatory AI systems.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Advanced Context Fusion for MRCA Parallel Hybrid System

Implements sophisticated fusion algorithms for combining VectorRAG and GraphRAG results
using research-based strategies including weighted linear combination, maximum confidence
selection, advanced hybrid fusion, and adaptive dynamic weighting for regulatory AI systems.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging
import math
import re
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Third-party library imports
# (None for this module)

# Local application/library specific imports
try:
    # Try relative imports first (when run as module)
    from .parallel_hybrid import RetrievalResult, ParallelRetrievalResponse
    from .llm import get_llm
except ImportError:
    # Fall back to absolute imports (when run directly from backend directory)
    from parallel_hybrid import RetrievalResult, ParallelRetrievalResponse
    from llm import get_llm

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)
# Global instance for reuse
_fusion_engine = None

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class FusionStrategy 
class FusionStrategy(Enum):
    """Available fusion strategies.

    This enumeration defines the available context fusion strategies that can be
    used to combine VectorRAG and GraphRAG results. Each strategy implements
    a different approach to optimizing the combination of retrieval contexts.

    Class Attributes:
        WEIGHTED_LINEAR: Basic weighted linear combination strategy.
        MAX_CONFIDENCE: Maximum confidence selection strategy.
        ADVANCED_HYBRID: Research-based advanced hybrid fusion strategy.
        ADAPTIVE_FUSION: Dynamic adaptive weighting strategy.

    Instance Attributes:
        Inherits from Enum

    Methods:
        Inherits from Enum
    """
    WEIGHTED_LINEAR = "weighted_linear"
    MAX_CONFIDENCE = "max_confidence"
    ADVANCED_HYBRID = "advanced_hybrid"
    ADAPTIVE_FUSION = "adaptive_fusion"
# ------------------------------------------------------------------------- end class FusionStrategy

# ------------------------------------------------------------------------- class FusionWeights 
@dataclass
class FusionWeights:
    """Weight configuration for fusion algorithms.

    This dataclass defines the weight parameters used by various fusion strategies
    to control the contribution of different retrieval sources and apply various
    bonuses and penalties during the fusion process.

    Class Attributes:
        None

    Instance Attributes:
        vector_weight (float): Base weight for vector retrieval results. Defaults to 0.6.
        graph_weight (float): Base weight for graph retrieval results. Defaults to 0.4.
        confidence_boost (float): Boost factor for high-confidence results. Defaults to 0.1.
        length_penalty (float): Penalty factor for overly long results. Defaults to 0.05.
        regulatory_bonus (float): Bonus factor for regulatory-specific content. Defaults to 0.15.

    Methods:
        None (dataclass with default values)
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    vector_weight: float = 0.6
    graph_weight: float = 0.4
    confidence_boost: float = 0.1
    length_penalty: float = 0.05
    regulatory_bonus: float = 0.15
    
    # ------------------------------------------------------------------------- end class FusionWeights

# ------------------------------------------------------------------------- class FusionResult 
@dataclass
class FusionResult:
    """Result of context fusion operation.

    This dataclass contains the output of a context fusion operation including
    the fused content, metadata about the fusion process, and quality metrics
    for evaluation and optimization.

    Class Attributes:
        None

    Instance Attributes:
        fused_content (str): The combined content from fusion operation.
        fusion_strategy (str): Name of the fusion strategy used.
        vector_contribution (float): Relative contribution of vector retrieval.
        graph_contribution (float): Relative contribution of graph retrieval.
        final_confidence (float): Final confidence score of fused result.
        fusion_quality_score (float): Quality metric for fusion evaluation.
        metadata (Dict[str, Any]): Additional metadata about the fusion process.

    Methods:
        None (dataclass for data storage)
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    fused_content: str
    fusion_strategy: str
    vector_contribution: float
    graph_contribution: float
    final_confidence: float
    fusion_quality_score: float
    metadata: Dict[str, Any]
    
    # ------------------------------------------------------------------------- end class FusionResult

# ------------------------------------------------------------------------- class HybridContextFusion 
class HybridContextFusion:
    """Hybrid Context Fusion Engine.

    This class implements various context fusion strategies from research literature
    for combining VectorRAG and GraphRAG results. It provides multiple algorithms
    including weighted linear combination, maximum confidence selection, advanced
    hybrid fusion, and adaptive dynamic weighting techniques.

    Class Attributes:
        None

    Instance Attributes:
        weights (FusionWeights): Default fusion weights configuration.
        llm: Lazy-initialized LLM instance for advanced fusion operations.

    Methods:
        fuse_contexts(): Main fusion method implementing strategy selection.
        _weighted_linear_fusion(): Basic weighted linear combination implementation.
        _max_confidence_fusion(): Maximum confidence selection implementation.
        _advanced_hybrid_fusion(): Research-based advanced hybrid implementation.
        _adaptive_fusion(): Dynamic adaptive weighting implementation.
        Various private helper methods for quality scoring and content analysis.
    """

    # -------------------
    # --- Constructor ---
    # -------------------
    
    # ------------------------------------------------------------------------- __init__()
    def __init__(self, default_weights: Optional[FusionWeights] = None) -> None:
        """Initialize the context fusion engine.

        Creates a context fusion engine with the specified default weights configuration.
        The LLM is initialized lazily to improve startup performance.

        Args:
            default_weights (Optional[FusionWeights]): Default fusion weights configuration.
                                                     If None, uses default FusionWeights.
        """
        self.weights = default_weights or FusionWeights()
        self.llm = None  # Lazy initialization
    # ------------------------------------------------------------------------- end __init__()

    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # ------------------------------------------------------------------------- fuse_contexts()
    async def fuse_contexts(
        self, 
        parallel_response: ParallelRetrievalResponse,
        strategy: FusionStrategy = FusionStrategy.ADVANCED_HYBRID,
        custom_weights: Optional[FusionWeights] = None
    ) -> FusionResult:
        """Fuse the parallel retrieval results using specified strategy.

        This is the main fusion method that combines VectorRAG and GraphRAG results
        using the specified fusion strategy. It handles strategy selection and
        delegates to appropriate specialized fusion methods.

        Args:
            parallel_response (ParallelRetrievalResponse): Results from parallel retrieval.
            strategy (FusionStrategy): Fusion strategy to use. Defaults to ADVANCED_HYBRID.
            custom_weights (Optional[FusionWeights]): Optional custom weights for this fusion.

        Returns:
            FusionResult: Combined context with fusion metadata and quality metrics.

        Examples:
            >>> fusion_engine = HybridContextFusion()
            >>> result = await fusion_engine.fuse_contexts(parallel_response)
            >>> print(f"Fusion confidence: {result.final_confidence}")
        """
        if not parallel_response.fusion_ready:
            logger.warning("Parallel response not fusion ready, using fallback")
            return self._create_fallback_fusion(parallel_response)
            
        weights = custom_weights or self.weights
        
        logger.info(f"Starting context fusion using {strategy.value} strategy")
        
        if strategy == FusionStrategy.WEIGHTED_LINEAR:
            result = await self._weighted_linear_fusion(parallel_response, weights)
            result.fusion_strategy = strategy.value
            return result
        elif strategy == FusionStrategy.MAX_CONFIDENCE:
            result = await self._max_confidence_fusion(parallel_response)
            result.fusion_strategy = strategy.value
            return result
        elif strategy == FusionStrategy.ADVANCED_HYBRID:
            result = await self._advanced_hybrid_fusion(parallel_response, weights)
            result.fusion_strategy = strategy.value
            return result
        elif strategy == FusionStrategy.ADAPTIVE_FUSION:
            result = await self._adaptive_fusion(parallel_response, weights)
            result.fusion_strategy = strategy.value
            return result
        else:
            logger.error(f"❌ Unknown fusion strategy: {strategy}")
            return self._create_fallback_fusion(parallel_response)
    # ------------------------------------------------------------------------- end fuse_contexts()

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # ------------------------------------------------------------------------- _weighted_linear_fusion()
    async def _weighted_linear_fusion(
        self, 
        response: ParallelRetrievalResponse, 
        weights: FusionWeights
    ) -> FusionResult:
        """Basic weighted linear combination of contexts.

        This is the simplest fusion approach where both contexts are combined
        with fixed weights based on their confidence scores. It implements
        dynamic weight adjustment based on relative confidence levels.

        Args:
            response (ParallelRetrievalResponse): Parallel retrieval results to fuse.
            weights (FusionWeights): Weight configuration for fusion algorithm.

        Returns:
            FusionResult: Weighted linear combination of input contexts.
        """
        vector_result = response.vector_result
        graph_result = response.graph_result
        
        # Calculate dynamic weights based on confidence
        vector_conf = vector_result.confidence
        graph_conf = graph_result.confidence
        
        # Normalize weights based on confidence
        total_conf = vector_conf + graph_conf
        if total_conf > 0:
            dynamic_vector_weight = (vector_conf / total_conf) * weights.vector_weight
            dynamic_graph_weight = (graph_conf / total_conf) * weights.graph_weight
        else:
            dynamic_vector_weight = weights.vector_weight
            dynamic_graph_weight = weights.graph_weight

        # Normalize contributions to sum to 1.0
        total_weight = dynamic_vector_weight + dynamic_graph_weight
        if total_weight > 0:
            dynamic_vector_weight = dynamic_vector_weight / total_weight
            dynamic_graph_weight = dynamic_graph_weight / total_weight
            
        # Create weighted combination
        fused_content = self._create_weighted_content(
            vector_result.content, 
            graph_result.content,
            dynamic_vector_weight,
            dynamic_graph_weight
        )
        
        # Calculate final confidence
        final_confidence = (vector_conf * dynamic_vector_weight + 
                          graph_conf * dynamic_graph_weight)
        
        return FusionResult(
            fused_content=fused_content,
            fusion_strategy="weighted_linear",
            vector_contribution=dynamic_vector_weight,
            graph_contribution=dynamic_graph_weight,
            final_confidence=final_confidence,
            fusion_quality_score=self._calculate_quality_score(fused_content),
            metadata={
                "original_vector_conf": vector_conf,
                "original_graph_conf": graph_conf,
                "fusion_method": "linear_combination"
            }
        )
    # ------------------------------------------------------------------------- end _weighted_linear_fusion()

    # ------------------------------------------------------------------------- _max_confidence_fusion()
    async def _max_confidence_fusion(self, response: ParallelRetrievalResponse) -> FusionResult:
        """
        Select the result with maximum confidence
        
        Simple strategy that picks the retrieval method with higher confidence
        but includes some context from the other method.
        """
        vector_result = response.vector_result
        graph_result = response.graph_result
        
        if vector_result.confidence >= graph_result.confidence:
            primary_result = vector_result
            secondary_result = graph_result
            primary_method = "vector_rag"
            vector_contrib = 0.8
            graph_contrib = 0.2
        else:
            primary_result = graph_result
            secondary_result = vector_result
            primary_method = "graph_rag"
            vector_contrib = 0.2
            graph_contrib = 0.8
            
        # Create content with primary result and secondary context
        fused_content = f"{primary_result.content}\n\nAdditional Context:\n{secondary_result.content[:200]}..."
        
        return FusionResult(
            fused_content=fused_content,
            fusion_strategy="max_confidence",
            vector_contribution=vector_contrib,
            graph_contribution=graph_contrib,
            final_confidence=primary_result.confidence,
            fusion_quality_score=self._calculate_quality_score(fused_content),
            metadata={
                "primary_method": primary_method,
                "confidence_diff": abs(vector_result.confidence - graph_result.confidence)
            }
        )
    # ------------------------------------------------------------------------- end _max_confidence_fusion()

    # ------------------------------------------------------------------------- _advanced_hybrid_fusion()
    async def _advanced_hybrid_fusion(
        self, 
        response: ParallelRetrievalResponse, 
        weights: FusionWeights
    ) -> FusionResult:
        """
        Advanced hybrid fusion based on research literature
        
        This implements the approach described in research papers that uses:
        1. Complementary information identification
        2. Regulatory domain-specific fusion
        3. Quality-based weighting
        4. Semantic coherence optimization
        """
        vector_result = response.vector_result
        graph_result = response.graph_result
        
        # Step 1: Analyze complementary information
        complementarity_score = self._calculate_complementarity(
            vector_result.content, 
            graph_result.content
        )
        
        # Step 2: Calculate domain-specific weights
        vector_regulatory_score = self._calculate_regulatory_quality(vector_result.content)
        graph_regulatory_score = self._calculate_regulatory_quality(graph_result.content)
        
        # Step 3: Adaptive weighting based on content quality
        adaptive_vector_weight = self._calculate_adaptive_weight(
            vector_result, vector_regulatory_score, complementarity_score
        )
        adaptive_graph_weight = self._calculate_adaptive_weight(
            graph_result, graph_regulatory_score, complementarity_score
        )
        
        # Normalize weights
        total_weight = adaptive_vector_weight + adaptive_graph_weight
        if total_weight > 0:
            adaptive_vector_weight /= total_weight
            adaptive_graph_weight /= total_weight
        
        # Step 4: Create semantically coherent fusion
        if self.llm is None:
            self.llm = get_llm()
            
        fused_content = await self._create_semantic_fusion(
            vector_result.content,
            graph_result.content,
            adaptive_vector_weight,
            adaptive_graph_weight,
            response.query
        )
        
        # Step 5: Calculate advanced fusion confidence
        final_confidence = self._calculate_advanced_confidence(
            vector_result.confidence,
            graph_result.confidence,
            complementarity_score,
            vector_regulatory_score,
            graph_regulatory_score
        )
        
        # DEBUGGING: Show fused content before template processing
        logger.info(f"\nCONTEXT FUSION RESULT:")
        logger.info(f"{'─'*60}")
        logger.info(f"Strategy: advanced_hybrid")
        logger.info(f"Vector contribution: {adaptive_vector_weight:.2f}")
        logger.info(f"Graph contribution: {adaptive_graph_weight:.2f}")
        logger.info(f"Final confidence: {final_confidence:.2f}")
        logger.info(f"Quality score: {self._calculate_quality_score(fused_content):.2f}")
        logger.info(f"\nFUSED CONTENT (before template processing):")
        logger.info(f"{'─'*60}")
        logger.info(f"{fused_content}")
        logger.info(f"{'─'*60}")
        
        return FusionResult(
            fused_content=fused_content,
            fusion_strategy="advanced_hybrid",
            vector_contribution=adaptive_vector_weight,
            graph_contribution=adaptive_graph_weight,
            final_confidence=final_confidence,
            fusion_quality_score=self._calculate_quality_score(fused_content),
            metadata={
                "complementarity_score": complementarity_score,
                "vector_regulatory_score": vector_regulatory_score,
                "graph_regulatory_score": graph_regulatory_score,
                "fusion_method": "advanced_semantic_coherence"
            }
        )
    # ------------------------------------------------------------------------- end _advanced_hybrid_fusion()

    # ------------------------------------------------------------------------- _adaptive_fusion()
    async def _adaptive_fusion(
        self, 
        response: ParallelRetrievalResponse, 
        weights: FusionWeights
    ) -> FusionResult:
        """
        Adaptive fusion that dynamically adjusts strategy based on content analysis
        
        This method analyzes the retrieval results and chooses the best fusion
        approach based on the specific characteristics of the content.
        """
        vector_result = response.vector_result
        graph_result = response.graph_result
        
        # Analyze content characteristics
        vector_analysis = self._analyze_content_characteristics(vector_result.content)
        graph_analysis = self._analyze_content_characteristics(graph_result.content)
        
        # Decide on best strategy based on analysis
        if vector_analysis["complexity"] > 0.7 and graph_analysis["complexity"] > 0.7:
            # Both are complex, use advanced hybrid
            return await self._advanced_hybrid_fusion(response, weights)
        elif abs(vector_result.confidence - graph_result.confidence) > 0.3:
            # Large confidence difference, use max confidence
            return await self._max_confidence_fusion(response)
        else:
            # Use weighted linear for balanced cases
            return await self._weighted_linear_fusion(response, weights)
    # ------------------------------------------------------------------------- end _adaptive_fusion()

    # ------------------------------------------------------------------------- _create_weighted_content()
    def _create_weighted_content(
        self, 
        vector_content: str, 
        graph_content: str,
        vector_weight: float,
        graph_weight: float
    ) -> str:
        """Create weighted combination of content"""
        
        # Simple template-based fusion
        if vector_weight > graph_weight:
            primary_content = vector_content
            secondary_content = graph_content
            primary_label = "Semantic Search Results"
            secondary_label = "Related Regulatory Information"
        else:
            primary_content = graph_content
            secondary_content = vector_content
            primary_label = "Regulatory Structure Analysis"
            secondary_label = "Supporting Documentation"
        
        fused = f"""## {primary_label}
{primary_content}

## {secondary_label}
{secondary_content}"""
        
        return fused
    # ------------------------------------------------------------------------- end _create_weighted_content()

    # ------------------------------------------------------------------------- _create_semantic_fusion()
    async def _create_semantic_fusion(
        self,
        vector_content: str,
        graph_content: str,
        vector_weight: float,
        graph_weight: float,
        original_query: str
    ) -> str:
        """Create semantically coherent fusion using LLM"""
        
        fusion_prompt = f"""You are an expert at combining regulatory information from multiple sources.

Original Question: {original_query}

Vector Search Results (Weight: {vector_weight:.2f}):
{vector_content}

Graph Analysis Results (Weight: {graph_weight:.2f}):
{graph_content}

Please combine these results into a comprehensive, coherent response that:
1. Prioritizes information based on the given weights
2. Eliminates redundancy while preserving important details
3. Maintains regulatory accuracy and proper CFR citations
   🚨 CRITICAL INSTRUCTION: PRESERVE EXACT CFR CITATIONS
   You MUST preserve all CFR section references EXACTLY as they appear in the regulatory context above. 
   🚨 DO NOT change, modify, or "correct" any CFR citations (e.g., § 75.1720(a), § 57.15030, etc.). 
Preserve the exact section numbers and letters such as (a), subsections, and formatting from the source material.
4. Provides a clear, structured answer to the original question
5. Uses professional regulatory compliance language

Combined Response:"""
        
        try:
            if self.llm is None:
                self.llm = get_llm()
            
            # Ensure llm is properly initialized before calling invoke
            if self.llm is None:
                logger.error("❌ LLM initialization failed in semantic fusion")
                raise ValueError("LLM not available for semantic fusion")
                
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.llm.invoke(fusion_prompt) if self.llm else None
            )
            
            # Handle different response types properly
            if response is not None and hasattr(response, 'content'):
                result = response.content
                return str(result) if not isinstance(result, str) else result
            elif response is not None:
                return str(response)
            else:
                raise ValueError("LLM returned None response")
            
        except Exception as e:
            logger.error(f"❌ Semantic fusion failed: {str(e)}")
            # Fallback to template-based fusion
            return self._create_weighted_content(
                vector_content, graph_content, vector_weight, graph_weight
            )
    # ------------------------------------------------------------------------- end _create_semantic_fusion()

    # ------------------------------------------------------------------------- _calculate_complementarity()
    def _calculate_complementarity(self, content1: str, content2: str) -> float:
        """Calculate how complementary two pieces of content are"""
        
        # Simple complementarity based on unique information
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        intersection = words1 & words2
        union = words1 | words2
        
        if len(union) == 0:
            return 0.0
            
        # Jaccard similarity
        similarity = len(intersection) / len(union)
        
        # Complementarity is inverse of similarity
        complementarity = 1.0 - similarity
        
        return max(0.0, min(1.0, complementarity))
    # ------------------------------------------------------------------------- end _calculate_complementarity()

    # ------------------------------------------------------------------------- _calculate_regulatory_quality()
    def _calculate_regulatory_quality(self, content: str) -> float:
        """Calculate regulatory quality score for content"""
        
        quality_score = 0.0
        
        # Enhanced CFR citations with hierarchical awareness
        # Basic CFR citations (existing) - fixed to handle decimal sections
        cfr_matches = len(re.findall(r'\b\d+\s+CFR\s+§\s*\d+(?:\.\d+)*', content))
        quality_score += min(0.3, cfr_matches * 0.1)
        
        # ENHANCEMENT: Advanced CFR citation patterns
        # Complete citations with parts and subparts
        complete_citations = len(re.findall(r'\b\d+\s+CFR\s+Part\s+\d+\s+§\s*\d+', content))
        quality_score += min(0.15, complete_citations * 0.15)
        
        # Cross-references and related sections
        cross_refs = len(re.findall(r'section\s+\d+(?:\.\d+)?(?:\([a-zA-Z0-9]+\))*', content, re.IGNORECASE))
        quality_score += min(0.1, cross_refs * 0.05)
        
        # Enhanced regulatory keywords with mining-specific terms
        regulatory_terms = [
            'shall', 'must', 'required', 'compliance', 'standard',
            'regulation', 'safety', 'equipment', 'operator', 'mine'
        ]
        
        # ENHANCEMENT: MSHA-specific terminology
        msha_terms = [
            'underground coal', 'surface coal', 'metal mine', 'mine operator',
            'competent person', 'qualified person', 'permissible equipment',
            'methane monitoring', 'ventilation plan', 'self-rescue device',
            'mine rescue', 'electrical examination', 'roof control'
        ]
        
        term_count = sum(1 for term in regulatory_terms if term.lower() in content.lower())
        msha_term_count = sum(1 for term in msha_terms if term.lower() in content.lower())
        
        quality_score += min(0.25, term_count * 0.03)
        quality_score += min(0.15, msha_term_count * 0.05)  # Higher weight for MSHA-specific terms
        
        # ENHANCEMENT: Safety urgency indicators
        safety_critical_terms = ['immediate', 'emergency', 'danger', 'fatal', 'explosion', 'methane']
        safety_count = sum(1 for term in safety_critical_terms if term.lower() in content.lower())
        quality_score += min(0.1, safety_count * 0.1)  # Higher penalty for safety-critical content
        
        # Length and structure (existing)
        if len(content) > 200:
            quality_score += 0.15  # Reduced from 0.2 to accommodate new scoring
        if len(content) > 500:
            quality_score += 0.05  # Reduced from 0.1
            
        # Enhanced specific details with mining measurements
        detail_patterns = [
            r'\d+\s*(feet|foot|ft)', r'\d+\s*(percent|%)', r'\d+\s*psi',
            r'\d+\s*cfm', r'\d+\s*rpm', r'\d+\s*(volt|amp)', r'\d+\s*degree'
        ]
        detail_count = sum(len(re.findall(pattern, content, re.IGNORECASE)) for pattern in detail_patterns)
        quality_score += min(0.1, detail_count * 0.02)
        
        return min(1.0, quality_score)
    # ------------------------------------------------------------------------- end _calculate_regulatory_quality()

    # ------------------------------------------------------------------------- _calculate_adaptive_weight()
    def _calculate_adaptive_weight(
        self, 
        result: RetrievalResult, 
        regulatory_score: float, 
        complementarity: float
    ) -> float:
        """Calculate adaptive weight for a retrieval result"""
        
        base_weight = result.confidence
        regulatory_boost = regulatory_score * self.weights.regulatory_bonus
        complementarity_boost = complementarity * self.weights.confidence_boost
        
        # Response time penalty (slower = lower weight)
        time_penalty = min(0.1, result.response_time_ms / 10000.0)
        
        adaptive_weight = base_weight + regulatory_boost + complementarity_boost - time_penalty
        
        return max(0.1, min(1.0, adaptive_weight))
    # ------------------------------------------------------------------------- end _calculate_adaptive_weight()

    # ------------------------------------------------------------------------- _calculate_advanced_confidence()
    def _calculate_advanced_confidence(
        self,
        vector_conf: float,
        graph_conf: float,
        complementarity: float,
        vector_reg_score: float,
        graph_reg_score: float
    ) -> float:
        """Calculate confidence using advanced fusion formula"""
        
        # Base confidence is weighted average
        base_confidence = (vector_conf + graph_conf) / 2.0
        
        # Complementarity bonus
        comp_bonus = complementarity * 0.15
        
        # Regulatory quality bonus
        reg_bonus = max(vector_reg_score, graph_reg_score) * 0.1
        
        # Consistency bonus (similar confidence scores)
        consistency_bonus = (1.0 - abs(vector_conf - graph_conf)) * 0.05
        
        final_confidence = base_confidence + comp_bonus + reg_bonus + consistency_bonus
        
        return min(1.0, final_confidence)
    # ------------------------------------------------------------------------- end _calculate_advanced_confidence()

    # ------------------------------------------------------------------------- _analyze_content_characteristics()
    def _analyze_content_characteristics(self, content: str) -> Dict[str, float]:
        """Analyze content characteristics for adaptive fusion"""
        
        characteristics = {
            "complexity": 0.0,
            "regulatory_density": 0.0,
            "specificity": 0.0,
            "length_score": 0.0
        }
        
        # Complexity based on sentence structure and vocabulary
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        characteristics["complexity"] = min(1.0, avg_sentence_length / 25.0)
        
        # Regulatory density
        characteristics["regulatory_density"] = self._calculate_regulatory_quality(content)
        
        # Specificity based on numbers and technical terms
        technical_patterns = [r'\d+', r'CFR', r'§', r'percent', r'psi', r'feet']
        tech_count = sum(len(re.findall(pattern, content, re.IGNORECASE)) for pattern in technical_patterns)
        characteristics["specificity"] = min(1.0, tech_count / 10.0)
        
        # Length score
        characteristics["length_score"] = min(1.0, len(content) / 1000.0)
        
        return characteristics
    # ------------------------------------------------------------------------- end _analyze_content_characteristics()

    # ------------------------------------------------------------------------- _calculate_quality_score()
    def _calculate_quality_score(self, content: str) -> float:
        """Calculate overall quality score for fused content"""
        
        # Combine multiple quality metrics
        reg_quality = self._calculate_regulatory_quality(content)
        characteristics = self._analyze_content_characteristics(content)
        
        quality_score = (
            reg_quality * 0.4 +
            characteristics["complexity"] * 0.2 +
            characteristics["specificity"] * 0.3 +
            characteristics["length_score"] * 0.1
        )
        
        return min(1.0, quality_score)
    # ------------------------------------------------------------------------- end _calculate_quality_score()

    # ------------------------------------------------------------------------- _create_fallback_fusion()
    def _create_fallback_fusion(self, response: ParallelRetrievalResponse) -> FusionResult:
        """Create fallback fusion when parallel response is not fusion ready"""
        
        # Use whichever result is available and better
        if response.vector_result.error is None and response.graph_result.error is not None:
            # Only vector succeeded
            return FusionResult(
                fused_content=response.vector_result.content,
                fusion_strategy="fallback_vector",
                vector_contribution=1.0,
                graph_contribution=0.0,
                final_confidence=response.vector_result.confidence,
                fusion_quality_score=self._calculate_quality_score(response.vector_result.content),
                metadata={"fallback_reason": "graph_failed"}
            )
        elif response.graph_result.error is None and response.vector_result.error is not None:
            # Only graph succeeded
            return FusionResult(
                fused_content=response.graph_result.content,
                fusion_strategy="fallback_graph",
                vector_contribution=0.0,
                graph_contribution=1.0,
                final_confidence=response.graph_result.confidence,
                fusion_quality_score=self._calculate_quality_score(response.graph_result.content),
                metadata={"fallback_reason": "vector_failed"}
            )
        else:
            # Both failed or other issue
            fallback_content = f"Both retrieval methods encountered issues:\nVector: {response.vector_result.error or 'Unknown error'}\nGraph: {response.graph_result.error or 'Unknown error'}"
            return FusionResult(
                fused_content=fallback_content,
                fusion_strategy="fallback_error",
                vector_contribution=0.0,
                graph_contribution=0.0,
                final_confidence=0.0,
                fusion_quality_score=0.0,
                metadata={"fallback_reason": "both_failed"}
            )
    # ------------------------------------------------------------------------- end _create_fallback_fusion()

# ------------------------------------------------------------------------- end class HybridContextFusion

# ------------------------------------------------------------------------- get_fusion_engine() 
def get_fusion_engine() -> HybridContextFusion:
    """Get or create the global context fusion engine"""
    global _fusion_engine
    if _fusion_engine is None:
        _fusion_engine = HybridContextFusion()
    return _fusion_engine
# ------------------------------------------------------------------------- end get_fusion_engine()

# ------------------------------------------------------------------------- test_context_fusion()
import pytest

@pytest.mark.asyncio
async def test_context_fusion():
    """Test the context fusion engine"""
    logger.info("Testing Advanced Context Fusion Engine...")
    
    # This would normally come from parallel retrieval
    # For testing, we'll create mock results
    from .parallel_hybrid import RetrievalResult, ParallelRetrievalResponse
    
    mock_vector = RetrievalResult(
        content="According to 30 CFR § 57.15030, safety equipment including hard hats, safety glasses, and steel-toed boots are required in underground mines.",
        method="vector_rag",
        confidence=0.8,
        response_time_ms=1200
    )
    
    mock_graph = RetrievalResult(
        content="Mine safety regulations specify that operators must provide personal protective equipment. Related entities include Equipment, Safety, and Regulation nodes in the knowledge graph.",
        method="graph_rag", 
        confidence=0.7,
        response_time_ms=1500
    )
    
    mock_response = ParallelRetrievalResponse(
        vector_result=mock_vector,
        graph_result=mock_graph,
        query="What safety equipment is required in underground mines?",
        total_time_ms=2000,
        success=True,
        fusion_ready=True
    )
    
    fusion_engine = get_fusion_engine()
    
    # Test all fusion strategies
    strategies = [
        FusionStrategy.WEIGHTED_LINEAR,
        FusionStrategy.MAX_CONFIDENCE,
        FusionStrategy.ADVANCED_HYBRID,
        FusionStrategy.ADAPTIVE_FUSION
    ]
    
    for strategy in strategies:
        logger.info(f"\nTesting {strategy.value} fusion...")
        
        result = await fusion_engine.fuse_contexts(mock_response, strategy)
        
        logger.info(f"✅ Fusion completed")
        logger.info(f"Vector contribution: {result.vector_contribution:.2f}")
        logger.info(f"Graph contribution: {result.graph_contribution:.2f}")
        logger.info(f"Final confidence: {result.final_confidence:.2f}")
        logger.info(f"Quality score: {result.fusion_quality_score:.2f}")
    
    logger.info("\nContext fusion testing complete!")
# ------------------------------------------------------------------------- end test_context_fusion() 

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.

if __name__ == "__main__":
    # --- Testing Entry Point ---
    # Run the context fusion testing function when executed directly
    asyncio.run(test_context_fusion())

# =========================================================================
# End of File
# =========================================================================