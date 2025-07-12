"""
Tests for the chat engine module.

ChatEngine handles AI conversation logic, including response
generation and orchestration with memory management.
"""

from unittest.mock import Mock
from chat_engine import ChatEngine
from memory_manager import MemoryManager


def test_generate_response_reference_topic():
    # Arrange
    mock_memory_manager = Mock(spec=MemoryManager)
    chat_engine = ChatEngine(mock_memory_manager)
    user_message = "I want to learn Python"

    # Act
    response = chat_engine.generate_response(user_message)

    # Assert
    assert "Python" in response
    assert "understand" in response.lower()
