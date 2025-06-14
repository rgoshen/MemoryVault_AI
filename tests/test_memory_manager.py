"""
MemoryVault AI - Memory Manager Tests
====================================
Unit tests for the memory manager functionality.
Separate from implementation for clean architecture.
"""

from memory_manager import MemoryManager
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import memory_manager
sys.path.append(str(Path(__file__).parent.parent))


def setup_test_environment():
    """Setup isolated test environment"""
    # Create temporary directory for test
    test_dir = tempfile.mkdtemp(prefix="memoryvault_test_")
    test_memory_file = os.path.join(test_dir, "test_memory.json")
    return test_dir, test_memory_file


def cleanup_test_environment(test_dir):
    """Clean up test environment"""
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def test_memory_initialization():
    """Test memory manager initialization"""
    print("🧪 Testing Memory Manager Initialization...")

    test_dir, test_memory_file = setup_test_environment()

    try:
        # Test initialization
        memory = MemoryManager(memory_file=test_memory_file)
        assert memory is not None, "Memory manager should initialize"
        assert memory.current_session is not None, "Should create current session"

        print("  ✅ Initialization successful")

        # Test memory file creation
        assert os.path.exists(test_memory_file), "Memory file should be created"
        print("  ✅ Memory file created")

    finally:
        cleanup_test_environment(test_dir)


def test_message_storage():
    """Test adding and retrieving messages"""
    print("🧪 Testing Message Storage...")

    test_dir, test_memory_file = setup_test_environment()

    try:
        memory = MemoryManager(memory_file=test_memory_file)

        # Test adding messages
        success1 = memory.add_message("user", "Hello, this is a test!")
        success2 = memory.add_message("assistant", "Hello! I received your message.")

        assert success1, "Should successfully add user message"
        assert success2, "Should successfully add assistant message"
        print("  ✅ Messages added successfully")

        # Test retrieving context
        context = memory.get_recent_context(5)
        assert len(context) == 2, f"Should retrieve 2 messages, got {len(context)}"
        assert context[0]["role"] == "user", "First message should be from user"
        assert (
            context[1]["role"] == "assistant"
        ), "Second message should be from assistant"
        print("  ✅ Context retrieved correctly")

    finally:
        cleanup_test_environment(test_dir)


def test_memory_persistence():
    """Test that memory persists across instances"""
    print("🧪 Testing Memory Persistence...")

    test_dir, test_memory_file = setup_test_environment()

    try:
        # Create first instance and add messages
        memory1 = MemoryManager(memory_file=test_memory_file)
        memory1.add_message("user", "Persistent test message")

        # Create second instance and check if message exists
        memory2 = MemoryManager(memory_file=test_memory_file)
        context = memory2.get_recent_context(5)

        assert len(context) > 0, "Should load existing messages"
        assert (
            "Persistent test message" in context[0]["content"]
        ), "Should load the exact message"
        print("  ✅ Memory persisted across instances")

    finally:
        cleanup_test_environment(test_dir)


def test_conversation_search():
    """Test searching through conversations"""
    print("🧪 Testing Conversation Search...")

    test_dir, test_memory_file = setup_test_environment()

    try:
        memory = MemoryManager(memory_file=test_memory_file)

        # Add test messages
        memory.add_message("user", "I love pizza and pasta")
        memory.add_message("assistant", "Great! Italian food is delicious.")
        memory.add_message("user", "What about sushi?")
        memory.add_message("assistant", "Sushi is also wonderful!")

        # Test search functionality
        pizza_results = memory.search_conversations("pizza")
        assert (
            len(pizza_results) == 1
        ), f"Should find 1 pizza message, got {len(pizza_results)}"

        food_results = memory.search_conversations("food")
        assert (
            len(food_results) == 1
        ), f"Should find 1 food message, got {len(food_results)}"

        print("  ✅ Search functionality working")

    finally:
        cleanup_test_environment(test_dir)


def test_memory_statistics():
    """Test memory statistics functionality"""
    print("🧪 Testing Memory Statistics...")

    test_dir, test_memory_file = setup_test_environment()

    try:
        memory = MemoryManager(memory_file=test_memory_file)

        # Add some messages
        memory.add_message("user", "Test message 1")
        memory.add_message("assistant", "Response 1")
        memory.add_message("user", "Test message 2")

        # Get statistics
        stats = memory.get_memory_stats()

        assert stats["total_sessions"] >= 1, "Should have at least 1 session"
        assert (
            stats["total_messages"] == 3
        ), f"Should have 3 messages, got {stats['total_messages']}"
        assert stats["current_session"] is not None, "Should have current session"

        print("  ✅ Statistics calculated correctly")
        print(f"     Sessions: {stats['total_sessions']}")
        print(f"     Messages: {stats['total_messages']}")

    finally:
        cleanup_test_environment(test_dir)


def test_memory_clearing():
    """Test clearing memory functionality"""
    print("🧪 Testing Memory Clearing...")

    test_dir, test_memory_file = setup_test_environment()

    try:
        memory = MemoryManager(memory_file=test_memory_file)

        # Add messages
        memory.add_message("user", "This will be cleared")
        memory.add_message("assistant", "This will also be cleared")

        # Verify messages exist
        stats_before = memory.get_memory_stats()
        assert (
            stats_before["total_messages"] == 2
        ), "Should have messages before clearing"

        # Clear memory
        success = memory.clear_memory()
        assert success, "Clear memory should succeed"

        # Verify messages are cleared
        stats_after = memory.get_memory_stats()
        assert (
            stats_after["total_messages"] == 0
        ), "Should have no messages after clearing"

        print("  ✅ Memory cleared successfully")

    finally:
        cleanup_test_environment(test_dir)


def test_explicit_new_session():
    """Test starting new session explicitly"""
    print("🧪 Testing Explicit New Session Creation...")

    test_dir, test_memory_file = setup_test_environment()

    try:
        memory = MemoryManager(memory_file=test_memory_file)

        # Add message to first session
        memory.add_message("user", "Message in first session")
        first_session_id = memory.current_session

        # Explicitly start new session
        new_session_id = memory.start_new_session()

        # Verify new session was created
        assert new_session_id != first_session_id, "Should create different session ID"
        assert memory.current_session == new_session_id, "Should switch to new session"

        # Add message to new session
        memory.add_message("user", "Message in second session")

        # Verify messages are in separate sessions
        stats = memory.get_memory_stats()
        assert (
            stats["total_sessions"] == 2
        ), f"Should have 2 sessions, got {stats['total_sessions']}"

        # Verify current context is from new session only
        context = memory.get_recent_context(5)
        assert (
            len(context) == 1
        ), f"Should have 1 message in new session, got {len(context)}"
        assert (
            "second session" in context[0]["content"]
        ), "Should have message from new session"

        print("  ✅ New session created successfully")
        print(f"     First session: {first_session_id}")
        print(f"     New session: {new_session_id}")
        print(f"     Total sessions: {stats['total_sessions']}")

    finally:
        cleanup_test_environment(test_dir)


def run_all_tests():
    """Run all memory manager tests"""
    print("🧠🔒 MEMORYVAULT AI - MEMORY MANAGER TESTS")
    print("=" * 50)

    tests = [
        test_memory_initialization,
        test_message_storage,
        test_memory_persistence,
        test_conversation_search,
        test_memory_statistics,
        test_memory_clearing,
        test_explicit_new_session,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  ❌ {test_func.__name__} FAILED: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {passed/(passed+failed)*100:.1f}%")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Memory Manager is working correctly")
    else:
        print(f"\n⚠️  {failed} TESTS FAILED")
        print("Please fix the issues before proceeding")


if __name__ == "__main__":
    run_all_tests()
