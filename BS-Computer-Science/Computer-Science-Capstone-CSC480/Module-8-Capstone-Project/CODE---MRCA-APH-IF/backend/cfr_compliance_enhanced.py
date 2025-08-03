# -------------------------------------------------------------------------
# File: stop_services.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: stop_services.py
# ------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Enhanced CFR Regulatory Compliance System for MRCA
Comprehensive improvements to CFR structure awareness, citation handling, and mining-specific compliance features.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class CFRHierarchyLevel(Enum):
    """CFR document hierarchy levels"""
    TITLE = "title"
    PART = "part"
    SUBPART = "subpart"
    SECTION = "section"
    PARAGRAPH = "paragraph"
    SUBSECTION = "subsection"

class MSHAMineType(Enum):
    """MSHA mine classification types"""
    UNDERGROUND_COAL = "underground_coal"
    SURFACE_COAL = "surface_coal"
    UNDERGROUND_METAL = "underground_metal"
    SURFACE_METAL = "surface_metal"
    MILL_OPERATIONS = "mill_operations"
    INDEPENDENT_CONTRACTOR = "independent_contractor"

class ComplianceUrgency(Enum):
    """Compliance requirement urgency levels"""
    IMMEDIATE = "immediate"           # Safety-critical, immediate action required
    HIGH = "high"                    # Must comply within 30 days
    MEDIUM = "medium"                # Must comply within 90 days
    LOW = "low"                      # Ongoing compliance requirement
    INFORMATIONAL = "informational"  # Guidance only

@dataclass
class CFRCitation:
    """Enhanced CFR citation with full hierarchical structure"""
    title: int                                    # e.g., 30
    part: Optional[int] = None                   # e.g., 75
    subpart: Optional[str] = None                # e.g., "D"
    section: Optional[int] = None                # e.g., 1720
    paragraph: Optional[str] = None              # e.g., "(a)(1)(i)"
    full_citation: str = ""                      # Complete formatted citation
    mine_type_applicability: Optional[List[MSHAMineType]] = None
    compliance_urgency: ComplianceUrgency = ComplianceUrgency.INFORMATIONAL
    
    def __post_init__(self):
        if self.mine_type_applicability is None:
            self.mine_type_applicability = []
        if not self.full_citation:
            self.full_citation = self._build_citation()
    
    def _build_citation(self) -> str:
        """Build properly formatted CFR citation"""
        citation = f"{self.title} CFR"
        if self.part:
            citation += f" Part {self.part}"
        if self.section:
            citation += f" § {self.section}"
        if self.paragraph:
            citation += f"{self.paragraph}"
        return citation

@dataclass
class ComplianceRequirement:
    """Enhanced compliance requirement with mining-specific context"""
    citation: CFRCitation
    requirement_text: str
    compliance_actions: List[str]
    applicable_mine_types: List[MSHAMineType]
    enforcement_authority: str
    penalty_range: Optional[str] = None
    related_citations: List[CFRCitation] = None
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        if self.related_citations is None:
            self.related_citations = []

class EnhancedCFRParser:
    """
    Advanced CFR citation parser and structure analyzer
    Handles complex CFR references and hierarchical relationships
    """
    
    def __init__(self):
        """Initialize enhanced CFR parser with comprehensive patterns"""
        
        # Enhanced CFR citation patterns
        self.cfr_patterns = {
            # Complete citations: "30 CFR § 75.1720(a)(1)"
            'complete': r'(?P<title>\d+)\s+CFR\s+(?:Part\s+(?P<part>\d+)\s+)?§\s*(?P<section>\d+)(?P<paragraph>(?:\([a-zA-Z0-9]+\))*)',
            
            # Part references: "30 CFR Part 75"
            'part_only': r'(?P<title>\d+)\s+CFR\s+Part\s+(?P<part>\d+)',
            
            # Section references: "§ 75.1720"
            'section_only': r'§\s*(?P<section>\d+(?:\.\d+)?)',
            
            # Cross-references: "section 75.1720(a)"
            'cross_ref': r'section\s+(?P<section>\d+(?:\.\d+)?)(?P<paragraph>(?:\([a-zA-Z0-9]+\))*)',
            
            # Subpart references: "Subpart D"
            'subpart': r'Subpart\s+(?P<subpart>[A-Z]+)',
            
            # Multiple citations: "30 CFR §§ 75.1720 and 75.1721"
            'multiple': r'(?P<title>\d+)\s+CFR\s+§§\s*(?P<sections>[\d\.,\s]+(?:and\s+[\d\.]+)?)'
        }
        
        # MSHA-specific mining terminology with enhanced categories
        self.msha_terminology = {
            'safety_equipment': [
                'personal protective equipment', 'PPE', 'hard hat', 'safety glasses', 
                'steel-toed boots', 'respirator', 'self-rescue device', 'safety harness',
                'methane detector', 'carbon monoxide detector', 'flame safety lamp',
                'permissible equipment', 'intrinsically safe equipment'
            ],
            'mining_operations': [
                'underground mining', 'surface mining', 'coal mining', 'metal mining',
                'strip mining', 'longwall mining', 'room and pillar', 'continuous miner',
                'roof bolting', 'shot firing', 'blasting operations', 'conveyor systems'
            ],
            'ventilation_systems': [
                'mine ventilation', 'air quality', 'methane monitoring', 'air flow',
                'ventilation plan', 'auxiliary fan', 'main fan', 'air course',
                'return air', 'intake air', 'air measurement', 'ventilation survey'
            ],
            'emergency_procedures': [
                'mine rescue', 'emergency evacuation', 'escape route', 'refuge chamber',
                'emergency response plan', 'accident reporting', 'mine emergency',
                'self-rescue training', 'emergency communication', 'mine fire protocol'
            ],
            'electrical_systems': [
                'electrical equipment', 'grounding', 'circuit protection', 'electrical safety',
                'permissible electrical equipment', 'trailing cable', 'power center',
                'electrical examination', 'electrical standards', 'hazardous area classification'
            ],
            'regulatory_terms': [
                'operator', 'mine operator', 'responsible person', 'competent person',
                'certified person', 'qualified person', 'authorized representative',
                'MSHA inspector', 'compliance officer', 'mine safety committee'
            ]
        }
        
        # Mining hazard classifications
        self.hazard_classifications = {
            'high_risk': ['methane', 'carbon monoxide', 'roof fall', 'electrical shock', 'explosion'],
            'medium_risk': ['noise exposure', 'dust exposure', 'machinery accidents', 'slips and falls'],
            'regulatory_risk': ['non-compliance', 'citation', 'violation', 'penalty', 'enforcement']
        }
    
    def parse_cfr_citations(self, text: str) -> List[CFRCitation]:
        """
        Parse CFR citations from text with enhanced pattern recognition
        
        Args:
            text: Text containing CFR citations
            
        Returns:
            List of parsed CFRCitation objects
        """
        citations = []
        
        for pattern_name, pattern in self.cfr_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                try:
                    citation = self._create_citation_from_match(match, pattern_name)
                    if citation:
                        # Determine mine type applicability
                        citation.mine_type_applicability = self._determine_mine_type_applicability(citation, text)
                        # Determine compliance urgency
                        citation.compliance_urgency = self._determine_compliance_urgency(text)
                        citations.append(citation)
                except Exception as e:
                    logger.warning(f"Failed to parse CFR citation: {str(e)}")
                    continue
        
        return self._deduplicate_citations(citations)
    
    def _create_citation_from_match(self, match: re.Match, pattern_name: str) -> Optional[CFRCitation]:
        """Create CFRCitation from regex match"""
        groups = match.groupdict()
        
        try:
            # Parse section with proper null checking
            section_str = groups.get('section')
            section_int = None
            if section_str:
                section_int = int(section_str.replace('.', ''))
            
            citation = CFRCitation(
                title=int(groups.get('title', 30)),  # Default to Title 30 for MSHA
                part=int(groups.get('part')) if groups.get('part') else None,
                subpart=groups.get('subpart'),
                section=section_int,
                paragraph=groups.get('paragraph')
            )
            return citation
        except (ValueError, TypeError) as e:
            logger.warning(f"Error creating citation from match: {str(e)}")
            return None
    
    def _determine_mine_type_applicability(self, citation: CFRCitation, context_text: str) -> List[MSHAMineType]:
        """Determine which mine types this citation applies to"""
        applicable_types = []
        context_lower = context_text.lower()
        
        # Part-based determination
        if citation.part:
            if citation.part in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:  # General parts
                applicable_types = list(MSHAMineType)
            elif citation.part in range(70, 80):  # Coal mine safety parts
                applicable_types = [MSHAMineType.UNDERGROUND_COAL, MSHAMineType.SURFACE_COAL]
            elif citation.part in range(56, 58):  # Metal/nonmetal parts
                applicable_types = [MSHAMineType.UNDERGROUND_METAL, MSHAMineType.SURFACE_METAL]
            
        # Context-based determination
        if 'underground' in context_lower:
            if 'coal' in context_lower:
                applicable_types.append(MSHAMineType.UNDERGROUND_COAL)
            else:
                applicable_types.append(MSHAMineType.UNDERGROUND_METAL)
        
        if 'surface' in context_lower:
            if 'coal' in context_lower:
                applicable_types.append(MSHAMineType.SURFACE_COAL)
            else:
                applicable_types.append(MSHAMineType.SURFACE_METAL)
        
        return list(set(applicable_types)) if applicable_types else [MSHAMineType.UNDERGROUND_COAL]  # Default
    
    def _determine_compliance_urgency(self, text: str) -> ComplianceUrgency:
        """Determine compliance urgency based on content analysis"""
        text_lower = text.lower()
        
        # Safety-critical terms
        if any(term in text_lower for term in ['immediate', 'immediately', 'emergency', 'danger', 'fatal']):
            return ComplianceUrgency.IMMEDIATE
        
        # High priority terms
        if any(term in text_lower for term in ['shall', 'must', 'required', 'mandatory']):
            return ComplianceUrgency.HIGH
        
        # Medium priority terms
        if any(term in text_lower for term in ['should', 'recommend', 'compliance']):
            return ComplianceUrgency.MEDIUM
        
        # Default to informational
        return ComplianceUrgency.INFORMATIONAL
    
    def _deduplicate_citations(self, citations: List[CFRCitation]) -> List[CFRCitation]:
        """Remove duplicate citations while preserving the most complete ones"""
        unique_citations = {}
        
        for citation in citations:
            key = f"{citation.title}_{citation.part}_{citation.section}"
            if key not in unique_citations:
                unique_citations[key] = citation
            else:
                # Keep the more complete citation
                existing = unique_citations[key]
                if (citation.paragraph and not existing.paragraph) or \
                   (citation.subpart and not existing.subpart):
                    unique_citations[key] = citation
        
        return list(unique_citations.values())
    
    def analyze_regulatory_density(self, content: str) -> Dict[str, float]:
        """
        Enhanced regulatory density analysis with mining-specific scoring
        
        Args:
            content: Text content to analyze
            
        Returns:
            Dictionary with detailed regulatory analysis scores
        """
        analysis = {
            'cfr_citation_density': 0.0,
            'msha_terminology_density': 0.0,
            'safety_emphasis_score': 0.0,
            'compliance_language_score': 0.0,
            'hazard_awareness_score': 0.0,
            'overall_regulatory_score': 0.0
        }
        
        content_lower = content.lower()
        word_count = len(content.split())
        
        if word_count == 0:
            return analysis
        
        # CFR citation density
        citations = self.parse_cfr_citations(content)
        analysis['cfr_citation_density'] = min(1.0, len(citations) / (word_count / 100))
        
        # MSHA terminology density
        msha_term_count = 0
        for category, terms in self.msha_terminology.items():
            msha_term_count += sum(1 for term in terms if term.lower() in content_lower)
        analysis['msha_terminology_density'] = min(1.0, msha_term_count / (word_count / 50))
        
        # Safety emphasis score
        safety_terms = ['safety', 'hazard', 'risk', 'protection', 'secure', 'accident', 'injury']
        safety_count = sum(content_lower.count(term) for term in safety_terms)
        analysis['safety_emphasis_score'] = min(1.0, safety_count / (word_count / 100))
        
        # Compliance language score
        compliance_terms = ['shall', 'must', 'required', 'mandatory', 'compliance', 'violation']
        compliance_count = sum(content_lower.count(term) for term in compliance_terms)
        analysis['compliance_language_score'] = min(1.0, compliance_count / (word_count / 100))
        
        # Hazard awareness score
        hazard_count = 0
        for risk_level, hazards in self.hazard_classifications.items():
            hazard_count += sum(1 for hazard in hazards if hazard in content_lower)
        analysis['hazard_awareness_score'] = min(1.0, hazard_count / (word_count / 200))
        
        # Overall regulatory score (weighted combination)
        analysis['overall_regulatory_score'] = (
            analysis['cfr_citation_density'] * 0.25 +
            analysis['msha_terminology_density'] * 0.20 +
            analysis['safety_emphasis_score'] * 0.20 +
            analysis['compliance_language_score'] * 0.20 +
            analysis['hazard_awareness_score'] * 0.15
        )
        
        return analysis

class EnhancedComplianceTemplateSystem:
    """
    Advanced template system for different regulatory compliance scenarios
    Replaces the basic regulatory compliance template with specialized versions
    """
    
    def __init__(self, cfr_parser: EnhancedCFRParser):
        """Initialize with CFR parser for citation analysis"""
        self.cfr_parser = cfr_parser
    
    def create_specialized_compliance_template(
        self,
        user_query: str,
        fusion_result: Any,  # FusionResult from context_fusion.py
        mine_type: MSHAMineType = MSHAMineType.UNDERGROUND_COAL,
        compliance_focus: str = "general"
    ) -> str:
        """
        Create specialized compliance template based on query type and mine classification
        
        Args:
            user_query: Original user question
            fusion_result: Result from context fusion
            mine_type: Type of mining operation
            compliance_focus: Focus area (safety, equipment, emergency, electrical, etc.)
            
        Returns:
            Specialized compliance template
        """
        
        # Analyze regulatory content
        reg_analysis = self.cfr_parser.analyze_regulatory_density(fusion_result.fused_content)
        citations = self.cfr_parser.parse_cfr_citations(fusion_result.fused_content)
        
        # Select appropriate template based on focus
        if compliance_focus == "safety":
            return self._create_safety_compliance_template(user_query, fusion_result, mine_type, citations, reg_analysis)
        elif compliance_focus == "equipment":
            return self._create_equipment_compliance_template(user_query, fusion_result, mine_type, citations, reg_analysis)
        elif compliance_focus == "emergency":
            return self._create_emergency_compliance_template(user_query, fusion_result, mine_type, citations, reg_analysis)
        elif compliance_focus == "electrical":
            return self._create_electrical_compliance_template(user_query, fusion_result, mine_type, citations, reg_analysis)
        else:
            return self._create_general_compliance_template(user_query, fusion_result, mine_type, citations, reg_analysis)
    
    def _create_safety_compliance_template(
        self, 
        user_query: str, 
        fusion_result: Any, 
        mine_type: MSHAMineType,
        citations: List[CFRCitation],
        reg_analysis: Dict[str, float]
    ) -> str:
        """Specialized template for safety compliance queries"""
        
        mine_type_context = self._get_mine_type_context(mine_type)
        citation_summary = self._format_citation_summary(citations)
        urgency_assessment = self._assess_compliance_urgency(citations)
        
        template = f"""You are a certified MSHA safety compliance specialist with expertise in {mine_type_context} safety regulations.

SAFETY COMPLIANCE QUERY: {user_query}

MINE CLASSIFICATION: {mine_type.value.replace('_', ' ').title()}

REGULATORY SAFETY ANALYSIS:
{self._truncate_content(fusion_result.fused_content)}

CITATION ANALYSIS:
{citation_summary}

REGULATORY DENSITY ASSESSMENT:
- CFR Citation Density: {reg_analysis['cfr_citation_density']:.2f}/1.0
- Safety Emphasis Score: {reg_analysis['safety_emphasis_score']:.2f}/1.0
- Hazard Awareness Score: {reg_analysis['hazard_awareness_score']:.2f}/1.0

{urgency_assessment}

SAFETY COMPLIANCE FRAMEWORK:
Your response must prioritize mine worker safety and follow these requirements:

**IMMEDIATE SAFETY REQUIREMENTS:**
- Identify any immediate safety hazards or risks
- Cite specific CFR sections that apply to {mine_type_context}
- Use precise safety terminology ("shall", "must", "immediately required")
- Highlight life-safety critical requirements

**HAZARD IDENTIFICATION & MITIGATION:**
- Specific hazards addressed by the regulation
- Required protective measures and equipment
- Monitoring and inspection requirements
- Training and certification needs

**COMPLIANCE IMPLEMENTATION:**
- Step-by-step compliance procedures
- Required documentation and record-keeping
- Inspection schedules and monitoring protocols
- Responsible parties and accountability measures

**ENFORCEMENT & CONSEQUENCES:**
- MSHA enforcement standards and inspection priorities
- Potential citations and penalty ranges
- Corrective action requirements
- Appeal processes and timelines

Please structure your response as:
1. **IMMEDIATE SAFETY ASSESSMENT**
2. **SPECIFIC REGULATORY REQUIREMENTS** (with complete CFR citations)
3. **IMPLEMENTATION PROCEDURES** (with timelines)
4. **COMPLIANCE VERIFICATION** (inspection and documentation)
5. **ENFORCEMENT CONSIDERATIONS**

SAFETY COMPLIANCE EXPERT RESPONSE:"""
        
        return template
    
    def _create_equipment_compliance_template(
        self, 
        user_query: str, 
        fusion_result: Any, 
        mine_type: MSHAMineType,
        citations: List[CFRCitation],
        reg_analysis: Dict[str, float]
    ) -> str:
        """Specialized template for equipment compliance queries"""
        
        mine_type_context = self._get_mine_type_context(mine_type)
        citation_summary = self._format_citation_summary(citations)
        
        template = f"""You are a certified MSHA equipment compliance specialist with expertise in {mine_type_context} equipment regulations.

EQUIPMENT COMPLIANCE QUERY: {user_query}

MINE CLASSIFICATION: {mine_type.value.replace('_', ' ').title()}

EQUIPMENT REGULATORY CONTEXT:
{self._truncate_content(fusion_result.fused_content)}

APPLICABLE CFR CITATIONS:
{citation_summary}

EQUIPMENT COMPLIANCE FRAMEWORK:

**EQUIPMENT SPECIFICATIONS & STANDARDS:**
- Required equipment specifications and performance standards
- Permissible equipment certifications (where applicable)
- Installation and setup requirements
- Compatibility with mine conditions

**INSPECTION & MAINTENANCE REQUIREMENTS:**
- Pre-shift, weekly, and periodic inspection schedules
- Maintenance procedures and documentation
- Record-keeping requirements and retention periods
- Qualified person requirements for inspections

**OPERATIONAL COMPLIANCE:**
- Proper operation procedures and limitations
- Operator training and certification requirements
- Safety interlocks and protective systems
- Emergency shutdown and isolation procedures

**REGULATORY APPROVAL & CERTIFICATION:**
- MSHA approval requirements (if applicable)
- Third-party certification needs
- Modification approval processes
- Recall and retrofit requirements

Please structure your response as:
1. **EQUIPMENT REGULATORY REQUIREMENTS**
2. **SPECIFICATION COMPLIANCE** (with CFR citations)
3. **INSPECTION & MAINTENANCE PROCEDURES**
4. **OPERATIONAL REQUIREMENTS**
5. **CERTIFICATION & APPROVAL PROCESSES**

EQUIPMENT COMPLIANCE EXPERT RESPONSE:"""
        
        return template
    
    def _create_emergency_compliance_template(
        self, 
        user_query: str, 
        fusion_result: Any, 
        mine_type: MSHAMineType,
        citations: List[CFRCitation],
        reg_analysis: Dict[str, float]
    ) -> str:
        """Specialized template for emergency procedure compliance"""
        
        mine_type_context = self._get_mine_type_context(mine_type)
        citation_summary = self._format_citation_summary(citations)
        
        template = f"""You are a certified MSHA emergency response specialist with expertise in {mine_type_context} emergency procedures.

EMERGENCY COMPLIANCE QUERY: {user_query}

MINE CLASSIFICATION: {mine_type.value.replace('_', ' ').title()}

EMERGENCY REGULATORY REQUIREMENTS:
{self._truncate_content(fusion_result.fused_content)}

EMERGENCY-RELATED CFR CITATIONS:
{citation_summary}

EMERGENCY COMPLIANCE FRAMEWORK:

**EMERGENCY PREPAREDNESS REQUIREMENTS:**
- Required emergency response plans and procedures
- Emergency equipment and supplies requirements
- Communication system requirements
- Evacuation route planning and marking

**TRAINING & COMPETENCY REQUIREMENTS:**
- Emergency response training requirements
- Mine rescue team requirements and training
- Self-rescue device training and certification
- Emergency drill frequency and documentation

**RESPONSE PROCEDURES:**
- Immediate response protocols for different emergency types
- Chain of command and notification requirements
- Coordination with external emergency services
- Post-emergency investigation and reporting

**REGULATORY COMPLIANCE & DOCUMENTATION:**
- Required emergency plan approvals and updates
- Training documentation and certification records
- Emergency drill records and evaluation reports
- MSHA notification and reporting requirements

Please structure your response as:
1. **EMERGENCY PREPAREDNESS REQUIREMENTS**
2. **TRAINING & COMPETENCY STANDARDS** (with CFR citations)
3. **RESPONSE PROTOCOLS**
4. **DOCUMENTATION & REPORTING**
5. **REGULATORY OVERSIGHT & COMPLIANCE**

EMERGENCY RESPONSE EXPERT RESPONSE:"""
        
        return template
    
    def _create_electrical_compliance_template(
        self, 
        user_query: str, 
        fusion_result: Any, 
        mine_type: MSHAMineType,
        citations: List[CFRCitation],
        reg_analysis: Dict[str, float]
    ) -> str:
        """Specialized template for electrical safety compliance"""
        
        mine_type_context = self._get_mine_type_context(mine_type)
        citation_summary = self._format_citation_summary(citations)
        
        template = f"""You are a certified MSHA electrical safety specialist with expertise in {mine_type_context} electrical regulations.

ELECTRICAL COMPLIANCE QUERY: {user_query}

MINE CLASSIFICATION: {mine_type.value.replace('_', ' ').title()}

ELECTRICAL REGULATORY REQUIREMENTS:
{self._truncate_content(fusion_result.fused_content)}

ELECTRICAL CFR CITATIONS:
{citation_summary}

ELECTRICAL COMPLIANCE FRAMEWORK:

**ELECTRICAL EQUIPMENT STANDARDS:**
- Permissible electrical equipment requirements
- Intrinsically safe equipment specifications
- Grounding and bonding requirements
- Circuit protection and overcurrent devices

**INSTALLATION & MAINTENANCE:**
- Qualified electrician requirements
- Installation standards and procedures
- Testing and inspection protocols
- Maintenance documentation requirements

**OPERATIONAL SAFETY:**
- Lockout/tagout procedures
- Electrical hazard identification and control
- Personal protective equipment for electrical work
- Electrical safety training requirements

**REGULATORY COMPLIANCE:**
- MSHA electrical equipment approvals
- Electrical examination requirements
- Record-keeping and documentation
- Violation consequences and corrective actions

Please structure your response as:
1. **ELECTRICAL EQUIPMENT REQUIREMENTS**
2. **INSTALLATION & MAINTENANCE STANDARDS** (with CFR citations)
3. **OPERATIONAL SAFETY PROCEDURES**
4. **INSPECTION & DOCUMENTATION**
5. **REGULATORY APPROVAL & COMPLIANCE**

ELECTRICAL SAFETY EXPERT RESPONSE:"""
        
        return template
    
    def _create_general_compliance_template(
        self, 
        user_query: str, 
        fusion_result: Any, 
        mine_type: MSHAMineType,
        citations: List[CFRCitation],
        reg_analysis: Dict[str, float]
    ) -> str:
        """Enhanced general compliance template with comprehensive analysis"""
        
        mine_type_context = self._get_mine_type_context(mine_type)
        citation_summary = self._format_citation_summary(citations)
        urgency_assessment = self._assess_compliance_urgency(citations)
        
        template = f"""You are a certified MSHA compliance specialist with comprehensive expertise in {mine_type_context} regulations.

COMPLIANCE QUERY: {user_query}

MINE CLASSIFICATION: {mine_type.value.replace('_', ' ').title()}

COMPREHENSIVE REGULATORY ANALYSIS:
{self._truncate_content(fusion_result.fused_content)}

CFR CITATION ANALYSIS:
{citation_summary}

REGULATORY QUALITY ASSESSMENT:
- Overall Regulatory Score: {reg_analysis['overall_regulatory_score']:.2f}/1.0
- MSHA Terminology Density: {reg_analysis['msha_terminology_density']:.2f}/1.0
- Compliance Language Score: {reg_analysis['compliance_language_score']:.2f}/1.0

{urgency_assessment}

COMPREHENSIVE COMPLIANCE FRAMEWORK:

**REGULATORY REQUIREMENTS ANALYSIS:**
- Specific CFR sections applicable to {mine_type_context}
- Mandatory vs. recommended compliance measures
- Cross-referenced requirements and dependencies
- Recent regulatory updates and interpretations

**IMPLEMENTATION STRATEGY:**
- Step-by-step compliance procedures
- Resource requirements and cost considerations
- Timeline for implementation and ongoing compliance
- Training and competency development needs

**VERIFICATION & MONITORING:**
- Self-assessment tools and checklists
- Required inspections and documentation
- Performance metrics and compliance indicators
- Third-party audit and certification requirements

**ENFORCEMENT & RISK MANAGEMENT:**
- MSHA inspection priorities and enforcement trends
- Potential violations and penalty structures
- Mitigation strategies for compliance risks
- Best practices for regulatory relationship management

Please structure your response as:
1. **REGULATORY REQUIREMENTS SUMMARY**
2. **SPECIFIC COMPLIANCE OBLIGATIONS** (with complete CFR citations)
3. **IMPLEMENTATION GUIDANCE** (with priorities and timelines)
4. **VERIFICATION & DOCUMENTATION**
5. **ENFORCEMENT & RISK CONSIDERATIONS**

COMPREHENSIVE COMPLIANCE EXPERT RESPONSE:"""
        
        return template
    
    def _get_mine_type_context(self, mine_type: MSHAMineType) -> str:
        """Get descriptive context for mine type"""
        contexts = {
            MSHAMineType.UNDERGROUND_COAL: "underground coal mining",
            MSHAMineType.SURFACE_COAL: "surface coal mining",
            MSHAMineType.UNDERGROUND_METAL: "underground metal/nonmetal mining",
            MSHAMineType.SURFACE_METAL: "surface metal/nonmetal mining",
            MSHAMineType.MILL_OPERATIONS: "mill operations and processing",
            MSHAMineType.INDEPENDENT_CONTRACTOR: "independent contractor operations"
        }
        return contexts.get(mine_type, "mining operations")
    
    def _format_citation_summary(self, citations: List[CFRCitation]) -> str:
        """Format CFR citations into readable summary"""
        if not citations:
            return "No specific CFR citations identified in the regulatory content."
        
        summary = "Identified CFR Citations:\n"
        for citation in citations:
            mine_types = ", ".join([mt.value.replace('_', ' ').title() for mt in citation.mine_type_applicability])
            urgency = citation.compliance_urgency.value.title()
            summary += f"• {citation.full_citation} - {urgency} Priority - Applies to: {mine_types}\n"
        
        return summary
    
    def _assess_compliance_urgency(self, citations: List[CFRCitation]) -> str:
        """Assess overall compliance urgency from citations"""
        if not citations:
            return ""
        
        urgency_levels = [citation.compliance_urgency for citation in citations]
        
        if ComplianceUrgency.IMMEDIATE in urgency_levels:
            return "\n⚠️ IMMEDIATE ACTION REQUIRED: This query involves safety-critical regulations requiring immediate compliance."
        elif ComplianceUrgency.HIGH in urgency_levels:
            return "\n🔴 HIGH PRIORITY: This involves mandatory compliance requirements with strict enforcement."
        elif ComplianceUrgency.MEDIUM in urgency_levels:
            return "\n🟡 MEDIUM PRIORITY: This involves compliance requirements with established timelines."
        else:
            return "\n🟢 INFORMATIONAL: This involves general regulatory guidance and best practices."
    
    def _truncate_content(self, content: str, max_length: int = 2000) -> str:
        """Truncate content while preserving regulatory structure"""
        if len(content) <= max_length:
            return content
        
        # Try to end at a sentence boundary
        truncated = content[:max_length]
        last_period = truncated.rfind('.')
        
        if last_period > max_length * 0.8:
            return truncated[:last_period + 1] + "\n\n[Content truncated for length - full regulatory text available for detailed analysis]"
        else:
            return truncated + "...\n\n[Content truncated for length - full regulatory text available for detailed analysis]"

# Integration functions for existing system
def get_enhanced_cfr_parser() -> EnhancedCFRParser:
    """Get singleton instance of enhanced CFR parser"""
    if not hasattr(get_enhanced_cfr_parser, '_cfr_parser'):
        get_enhanced_cfr_parser._cfr_parser = EnhancedCFRParser()
    return get_enhanced_cfr_parser._cfr_parser

def get_enhanced_template_system() -> EnhancedComplianceTemplateSystem:
    """Get singleton instance of enhanced template system"""
    global _template_system
    if not hasattr(get_enhanced_template_system, '_template_system'):
        parser = get_enhanced_cfr_parser()
        get_enhanced_template_system._template_system = EnhancedComplianceTemplateSystem(parser)
    return get_enhanced_template_system._template_system

def enhance_regulatory_quality_scoring(content: str) -> Dict[str, float]:
    """
    Enhanced regulatory quality scoring that replaces the basic version
    
    Args:
        content: Text content to analyze
        
    Returns:
        Comprehensive regulatory quality scores
    """
    parser = get_enhanced_cfr_parser()
    return parser.analyze_regulatory_density(content)

# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced CFR system
    parser = get_enhanced_cfr_parser() 
    template_system = get_enhanced_template_system()
    
    # Test CFR citation parsing
    sample_text = """According to 30 CFR § 75.1720(a)(1), underground coal mines must maintain proper ventilation. 
    Additionally, 30 CFR Part 75 Subpart D covers ventilation requirements, and section 75.1721 specifies air flow measurements."""
    
    citations = parser.parse_cfr_citations(sample_text)
    print(f"Found {len(citations)} citations:")
    for citation in citations:
        print(f"  - {citation.full_citation} ({citation.compliance_urgency.value})")
    
    # Test regulatory analysis
    analysis = parser.analyze_regulatory_density(sample_text)
    print(f"\nRegulatory Analysis:")
    for metric, score in analysis.items():
        print(f"  - {metric}: {score:.2f}") 