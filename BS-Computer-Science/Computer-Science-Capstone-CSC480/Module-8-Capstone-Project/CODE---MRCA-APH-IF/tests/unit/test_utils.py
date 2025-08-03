# -------------------------------------------------------------------------
# File: test_utils.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-28
# File Path: tests/unit/test_utils.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the utils module (backend/utils.py).
# Tests session management, utility functions, message storage,
# and response formatting. Ensures proper session tracking and
# regulatory response formatting with comprehensive error handling.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Utils Unit Tests

Comprehensive testing of the utility functionality:
- Session ID generation and management
- Session data storage and retrieval
- Message saving and conversation tracking
- Regulatory response formatting
- In-memory session storage operations
- Error handling and edge cases
"""

import pytest
import uuid
from unittest.mock import Mock, patch
from typing import Dict, Any, List

# Import utils components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.utils import (
    get_session_id, get_session_data, save_message,
    format_regulatory_response, _backend_sessions
)


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def clean_sessions():
    """Reset global session storage before each test."""
    global _backend_sessions
    original_sessions = _backend_sessions.copy()
    _backend_sessions.clear()
    yield
    _backend_sessions.clear()
    _backend_sessions.update(original_sessions)

@pytest.fixture
def sample_session_id():
    """Provide a sample session ID for testing."""
    return "test-session-12345"

@pytest.fixture
def sample_result_dict():
    """Provide sample regulatory query result for formatting."""
    return {
        "answer": "CFR § 30.1 requires safety equipment including hard hats, safety glasses, and protective clothing for all mining operations. Compliance with these requirements is mandatory.",
        "cypher_query": "MATCH (r:Regulation)-[:REQUIRES]->(e:Equipment) WHERE r.section = '30.1' RETURN r.text, e.name"
    }

@pytest.fixture
def minimal_result_dict():
    """Provide minimal regulatory query result for testing."""
    return {
        "answer": "Safety regulations apply to mining operations."
    }

@pytest.fixture
def empty_result_dict():
    """Provide empty regulatory query result for testing."""
    return {}


# =========================================================================
# Unit Tests for Session Management
# =========================================================================

# ------------------------------------------------------------------------- TestSessionManagement
@pytest.mark.unit
class TestSessionManagement:
    """Test session management functionality."""
    
    # ------------------------------------------------------------------------- test_get_session_id_new_generation()
    def test_get_session_id_new_generation(self, clean_sessions):
        """Test generation of new session ID."""
        session_id = get_session_id()
        
        assert session_id is not None
        assert len(session_id) > 0
        assert isinstance(session_id, str)
        
        # Should be a valid UUID format
        try:
            uuid.UUID(session_id)
        except ValueError:
            pytest.fail("Generated session ID is not a valid UUID")
    # ------------------------------------------------------------------------- end test_get_session_id_new_generation()
    
    # ------------------------------------------------------------------------- test_get_session_id_existing_session()
    def test_get_session_id_existing_session(self, clean_sessions, sample_session_id):
        """Test returning existing session ID."""
        returned_id = get_session_id(sample_session_id)
        
        assert returned_id == sample_session_id
    
    def test_get_session_id_none_input(self, clean_sessions):
        """Test session ID generation with None input."""
        session_id = get_session_id(None)
        
        assert session_id is not None
        assert len(session_id) > 0
        
        # Should be a valid UUID
        try:
            uuid.UUID(session_id)
        except ValueError:
            pytest.fail("Generated session ID is not a valid UUID")
    # ------------------------------------------------------------------------- end test_get_session_id_none_input()
    
    # ------------------------------------------------------------------------- test_get_session_id_empty_string()
    def test_get_session_id_empty_string(self, clean_sessions):
        """Test session ID with empty string input."""
        session_id = get_session_id("")
        
        assert session_id == ""
    
    def test_get_session_id_uniqueness(self, clean_sessions):
        """Test that generated session IDs are unique."""
        session_ids = [get_session_id() for _ in range(10)]
        
        # All session IDs should be unique
        assert len(set(session_ids)) == len(session_ids)
    
    def test_get_session_data_new_session(self, clean_sessions, sample_session_id):
        """Test getting data for a new session."""
        session_data = get_session_data(sample_session_id)
        
        assert isinstance(session_data, dict)
        assert "messages" in session_data
        assert "created" in session_data
        assert isinstance(session_data["messages"], list)
        assert len(session_data["messages"]) == 0
        assert session_data["created"] is not None
    # ------------------------------------------------------------------------- end test_get_session_data_new_session()
    
    # ------------------------------------------------------------------------- test_get_session_data_existing_session()
    def test_get_session_data_existing_session(self, clean_sessions, sample_session_id):
        """Test getting data for an existing session."""
        # Create session first
        first_call = get_session_data(sample_session_id)
        first_call["messages"].append({"role": "user", "content": "test"})
        
        # Get session data again
        second_call = get_session_data(sample_session_id)
        
        assert first_call is second_call
        assert len(second_call["messages"]) == 1
        assert second_call["messages"][0]["content"] == "test"
    # ------------------------------------------------------------------------- end test_get_session_data_existing_session()
    
    # ------------------------------------------------------------------------- test_get_session_data_multiple_sessions()
    def test_get_session_data_multiple_sessions(self, clean_sessions):
        """Test managing multiple sessions."""
        session1_id = "session-1"
        session2_id = "session-2"
        
        session1_data = get_session_data(session1_id)
        session2_data = get_session_data(session2_id)
        
        assert session1_data is not session2_data
        assert session1_data["created"] != session2_data["created"]
        
        # Modify one session
        session1_data["messages"].append({"role": "user", "content": "session1 message"})
        
        # Other session should be unaffected
        assert len(session2_data["messages"]) == 0
        assert len(session1_data["messages"]) == 1
    # ------------------------------------------------------------------------- end test_get_session_data_multiple_sessions()
    
    # ------------------------------------------------------------------------- test_save_message_new_session()
    def test_save_message_new_session(self, clean_sessions, sample_session_id):
        """Test saving message to a new session."""
        save_message(sample_session_id, "user", "Hello, what are safety requirements?")
        
        session_data = get_session_data(sample_session_id)
        
        assert len(session_data["messages"]) == 1
        assert session_data["messages"][0]["role"] == "user"
        assert session_data["messages"][0]["content"] == "Hello, what are safety requirements?"
    # ------------------------------------------------------------------------- end test_save_message_new_session()
    
    # ------------------------------------------------------------------------- test_save_message_existing_session()
    def test_save_message_existing_session(self, clean_sessions, sample_session_id):
        """Test saving message to an existing session."""
        # Save first message
        save_message(sample_session_id, "user", "First message")
        
        # Save second message
        save_message(sample_session_id, "assistant", "Second message")
        
        session_data = get_session_data(sample_session_id)
        
        assert len(session_data["messages"]) == 2
        assert session_data["messages"][0]["role"] == "user"
        assert session_data["messages"][0]["content"] == "First message"
        assert session_data["messages"][1]["role"] == "assistant"
        assert session_data["messages"][1]["content"] == "Second message"
    
    def test_save_message_conversation_flow(self, clean_sessions, sample_session_id):
        """Test saving a complete conversation flow."""
        conversation = [
            ("user", "What safety equipment is required?"),
            ("assistant", "CFR § 30.1 requires hard hats and safety glasses."),
            ("user", "What about underground mines?"),
            ("assistant", "Underground mines have additional requirements...")
        ]
        
        for role, content in conversation:
            save_message(sample_session_id, role, content)
        
        session_data = get_session_data(sample_session_id)
        
        assert len(session_data["messages"]) == 4
        
        for i, (expected_role, expected_content) in enumerate(conversation):
            assert session_data["messages"][i]["role"] == expected_role
            assert session_data["messages"][i]["content"] == expected_content
    
    def test_save_message_empty_content(self, clean_sessions, sample_session_id):
        """Test saving message with empty content."""
        save_message(sample_session_id, "user", "")
        
        session_data = get_session_data(sample_session_id)
        
        assert len(session_data["messages"]) == 1
        assert session_data["messages"][0]["content"] == ""
    
    def test_save_message_special_characters(self, clean_sessions, sample_session_id):
        """Test saving message with special characters."""
        special_content = "What about § 30.1 & CFR requirements? (urgent!) 🚨"
        
        save_message(sample_session_id, "user", special_content)
        
        session_data = get_session_data(sample_session_id)
        
        assert len(session_data["messages"]) == 1
        assert session_data["messages"][0]["content"] == special_content
# ------------------------------------------------------------------------- end TestSessionManagement


# =========================================================================
# Unit Tests for Response Formatting
# =========================================================================

# ------------------------------------------------------------------------- TestResponseFormatting
@pytest.mark.unit
class TestResponseFormatting:
    """Test regulatory response formatting functionality."""
    
    # ------------------------------------------------------------------------- test_format_regulatory_response_complete()
    def test_format_regulatory_response_complete(self, sample_result_dict):
        """Test formatting complete regulatory response."""
        formatted = format_regulatory_response(sample_result_dict)
        
        assert "**Regulatory Information:**" in formatted
        assert sample_result_dict["answer"] in formatted
        assert "**Query Details:**" in formatted
        assert sample_result_dict["cypher_query"] in formatted
        assert "**Disclaimer:**" in formatted
        assert "```cypher" in formatted
        assert "```" in formatted
    
    def test_format_regulatory_response_minimal(self, minimal_result_dict):
        """Test formatting minimal regulatory response."""
        formatted = format_regulatory_response(minimal_result_dict)
        
        assert "**Regulatory Information:**" in formatted
        assert minimal_result_dict["answer"] in formatted
        assert "**Disclaimer:**" in formatted
        
        # Should not include query details section
        assert "**Query Details:**" not in formatted
        assert "```cypher" not in formatted
    
    def test_format_regulatory_response_empty(self, empty_result_dict):
        """Test formatting empty regulatory response."""
        formatted = format_regulatory_response(empty_result_dict)
        
        assert "**Regulatory Information:**" in formatted
        assert "No answer found" in formatted
        assert "**Disclaimer:**" in formatted
        
        # Should not include query details
        assert "**Query Details:**" not in formatted
    
    def test_format_regulatory_response_no_answer(self):
        """Test formatting response with no answer key."""
        result_dict = {
            "cypher_query": "MATCH (n) RETURN n"
        }
        
        formatted = format_regulatory_response(result_dict)
        
        assert "No answer found" in formatted
        assert "**Query Details:**" in formatted
        assert result_dict["cypher_query"] in formatted
    
    def test_format_regulatory_response_structure(self, sample_result_dict):
        """Test the structure of formatted response."""
        formatted = format_regulatory_response(sample_result_dict)
        
        # Check order of sections
        regulatory_pos = formatted.find("**Regulatory Information:**")
        query_pos = formatted.find("**Query Details:**")
        disclaimer_pos = formatted.find("**Disclaimer:**")
        
        assert regulatory_pos < query_pos < disclaimer_pos
    
    def test_format_regulatory_response_disclaimer_content(self, sample_result_dict):
        """Test disclaimer content in formatted response."""
        formatted = format_regulatory_response(sample_result_dict)
        
        assert "guidance only" in formatted
        assert "official CFR documentation" in formatted
        assert "compliance requirements" in formatted
    
    def test_format_regulatory_response_long_content(self):
        """Test formatting response with very long content."""
        long_answer = "CFR § 30.1 safety requirements " * 100
        long_query = "MATCH (n:Regulation) WHERE n.section = '30.1' " * 10
        
        result_dict = {
            "answer": long_answer,
            "cypher_query": long_query
        }
        
        formatted = format_regulatory_response(result_dict)
        
        assert long_answer in formatted
        assert long_query in formatted
        assert "**Regulatory Information:**" in formatted
        assert "**Query Details:**" in formatted
        assert "**Disclaimer:**" in formatted
# ------------------------------------------------------------------------- end TestResponseFormatting


# =========================================================================
# Unit Tests for Edge Cases and Integration
# =========================================================================

# ------------------------------------------------------------------------- TestEdgeCasesAndIntegration
@pytest.mark.unit
class TestEdgeCasesAndIntegration:
    """Test edge cases and integration scenarios."""

    # ------------------------------------------------------------------------- test_session_persistence_across_operations()
    def test_session_persistence_across_operations(self, clean_sessions):
        """Test session persistence across multiple operations."""
        session_id = get_session_id()

        # Save multiple messages
        save_message(session_id, "user", "First question")
        save_message(session_id, "assistant", "First answer")
        save_message(session_id, "user", "Follow-up question")

        # Get session data multiple times
        data1 = get_session_data(session_id)
        data2 = get_session_data(session_id)

        assert data1 is data2
        assert len(data1["messages"]) == 3
        assert len(data2["messages"]) == 3

    def test_concurrent_session_operations(self, clean_sessions):
        """Test concurrent operations on different sessions."""
        session1 = get_session_id()
        session2 = get_session_id()

        # Interleave operations on different sessions
        save_message(session1, "user", "Session 1 message 1")
        save_message(session2, "user", "Session 2 message 1")
        save_message(session1, "assistant", "Session 1 message 2")
        save_message(session2, "assistant", "Session 2 message 2")

        data1 = get_session_data(session1)
        data2 = get_session_data(session2)

        assert len(data1["messages"]) == 2
        assert len(data2["messages"]) == 2
        assert data1["messages"][0]["content"] == "Session 1 message 1"
        assert data2["messages"][0]["content"] == "Session 2 message 1"

    def test_large_session_data(self, clean_sessions, sample_session_id):
        """Test handling of large session data."""
        # Save many messages
        for i in range(100):
            save_message(sample_session_id, "user", f"Message {i}")
            save_message(sample_session_id, "assistant", f"Response {i}")

        session_data = get_session_data(sample_session_id)

        assert len(session_data["messages"]) == 200
        assert session_data["messages"][0]["content"] == "Message 0"
        assert session_data["messages"][-1]["content"] == "Response 99"

    def test_unicode_content_handling(self, clean_sessions, sample_session_id):
        """Test handling of Unicode content in messages."""
        unicode_content = "Safety requirements: 安全要求 🚨 Sécurité ñ"

        save_message(sample_session_id, "user", unicode_content)
        session_data = get_session_data(sample_session_id)

        assert session_data["messages"][0]["content"] == unicode_content

    def test_format_response_with_none_values(self):
        """Test formatting response with None values."""
        result_dict = {
            "answer": None,
            "cypher_query": None
        }

        formatted = format_regulatory_response(result_dict)

        assert "None" in formatted or "No answer found" in formatted
        assert "**Query Details:**" not in formatted
        assert "**Disclaimer:**" in formatted

    def test_format_response_with_empty_strings(self):
        """Test formatting response with empty strings."""
        result_dict = {
            "answer": "",
            "cypher_query": ""
        }

        formatted = format_regulatory_response(result_dict)

        assert len(formatted) > 0  # Should have some content even if empty
        assert "**Disclaimer:**" in formatted

    def test_session_memory_usage(self, clean_sessions):
        """Test session storage memory usage patterns."""
        initial_session_count = len(_backend_sessions)

        # Create multiple sessions
        session_ids = [get_session_id() for _ in range(10)]

        for session_id in session_ids:
            save_message(session_id, "user", "Test message")

        assert len(_backend_sessions) == initial_session_count + 10

        # Verify all sessions are accessible
        for session_id in session_ids:
            session_data = get_session_data(session_id)
            assert len(session_data["messages"]) == 1

    def test_message_role_variations(self, clean_sessions, sample_session_id):
        """Test saving messages with various role types."""
        roles = ["user", "assistant", "system", "function", "tool", "custom_role"]

        for i, role in enumerate(roles):
            save_message(sample_session_id, role, f"Message from {role}")

        session_data = get_session_data(sample_session_id)

        assert len(session_data["messages"]) == len(roles)

        for i, role in enumerate(roles):
            assert session_data["messages"][i]["role"] == role
            assert session_data["messages"][i]["content"] == f"Message from {role}"

    def test_regulatory_response_formatting_edge_cases(self):
        """Test regulatory response formatting with various edge cases."""
        edge_cases = [
            {"answer": "CFR § 30.1", "cypher_query": "MATCH (n) RETURN n"},
            {"answer": "A" * 10000},  # Very long answer
            {"answer": "Short"},  # Very short answer
            {"cypher_query": "MATCH (n) RETURN n"},  # Only query
            {"other_field": "value"},  # Unexpected fields
        ]

        for case in edge_cases:
            formatted = format_regulatory_response(case)

            # All should have basic structure
            assert "**Regulatory Information:**" in formatted
            assert "**Disclaimer:**" in formatted
            assert len(formatted) > 0
# ------------------------------------------------------------------------- end TestEdgeCasesAndIntegration

# =========================================================================
# End of File
# =========================================================================
