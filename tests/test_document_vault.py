#!/usr/bin/env python3
"""
MemoryVault AI - Document Vault Tests
====================================
Unit tests for the document vault functionality.
Tests document scanning, indexing, and querying capabilities.
"""

from document_vault import DocumentVault
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import document_vault
sys.path.append(str(Path(__file__).parent.parent))


def setup_test_environment():
    """Setup isolated test environment with sample documents"""
    # Create temporary directory for test
    test_dir = tempfile.mkdtemp(prefix="documentvault_test_")
    test_docs_dir = os.path.join(test_dir, "TestDocs")
    test_vector_dir = os.path.join(test_dir, "vectorstores")

    os.makedirs(test_docs_dir, exist_ok=True)
    os.makedirs(test_vector_dir, exist_ok=True)

    # Create sample documents
    sample_files = {
        "sample.txt": (
            "This is a sample text document for testing "
            "MemoryVault AI document processing."
        ),
        "readme.md": (
            "# Test Document\n\n"
            "This is a markdown document for testing purposes.\n\n"
            "## Features\n"
            "- Document scanning\n"
            "- Text processing"
        ),
        "script.py": (
            "#!/usr/bin/env python3\n"
            "# Sample Python script\n"
            "def hello_world():\n"
            "    print('Hello from test script!')"
        ),
        "data.json": (
            '{"test": true, "purpose": "document vault testing", '
            '"features": ["scanning", "indexing"]}'
        ),
        "config.yaml": (
            "app:\n"
            "  name: MemoryVault AI\n"
            "  version: 1.0\n"
            "  features:\n"
            "    - memory\n"
            "    - documents"
        ),
    }

    created_files = []
    for filename, content in sample_files.items():
        file_path = os.path.join(test_docs_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
        created_files.append(filename)

    return test_dir, test_docs_dir, test_vector_dir, created_files


def cleanup_test_environment(test_dir):
    """Clean up test environment"""
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def test_document_vault_initialization():
    """Test document vault initialization"""
    print("🧪 Testing Document Vault Initialization...")

    test_dir, test_docs_dir, test_vector_dir, _ = setup_test_environment()

    try:
        # Test initialization (without AI model - should still work)
        vault = DocumentVault(docs_folder=test_docs_dir, model_name="test-model")
        assert vault is not None, "Document vault should initialize"
        assert vault.docs_folder.exists(), "Docs folder should be created"

        print("  ✅ Initialization successful")

        # Test folder creation
        assert os.path.exists(test_docs_dir), "Test docs folder should exist"
        print("  ✅ Folder structure created")

    finally:
        cleanup_test_environment(test_dir)


def test_document_scanning():
    """Test document scanning functionality"""
    print("🧪 Testing Document Scanning...")

    test_dir, test_docs_dir, test_vector_dir, created_files = setup_test_environment()

    try:
        vault = DocumentVault(docs_folder=test_docs_dir)

        # Test document scanning
        scan_result = vault.scan_documents()

        assert scan_result["total_files"] == len(created_files), (
            f"Should find {len(created_files)} files, "
            f"found {scan_result['total_files']}"
        )
        assert scan_result["total_size_mb"] > 0, "Should calculate total size"
        assert len(scan_result["files"]) == len(created_files), "Should list all files"

        print(f"  ✅ Scanned {scan_result['total_files']} files")
        print(f"  ✅ Total size: {scan_result['total_size_mb']} MB")

        # Test file details
        file_names = [f["name"] for f in scan_result["files"]]
        for expected_file in created_files:
            assert expected_file in file_names, f"Should find {expected_file}"

        print("  ✅ All expected files found")

        # Test file metadata
        for file_info in scan_result["files"]:
            assert "name" in file_info, "File should have name"
            assert "size" in file_info, "File should have size"
            assert "type" in file_info, "File should have type"
            assert "hash" in file_info, "File should have hash"

        print("  ✅ File metadata complete")

    finally:
        cleanup_test_environment(test_dir)


def test_vault_status():
    """Test vault status reporting"""
    print("🧪 Testing Vault Status...")

    test_dir, test_docs_dir, test_vector_dir, created_files = setup_test_environment()

    try:
        vault = DocumentVault(docs_folder=test_docs_dir)

        # Test status reporting
        status = vault.get_vault_status()

        assert "model_name" in status, "Status should include model name"
        assert "ai_available" in status, "Status should include AI availability"
        assert "total_files" in status, "Status should include file count"
        assert "docs_folder" in status, "Status should include docs folder"

        print(f"  ✅ Model: {status['model_name']}")
        print(f"  ✅ AI Available: {status['ai_available']}")
        print(f"  ✅ Files Found: {status['total_files']}")
        print(f"  ✅ Docs Folder: {status['docs_folder']}")

        # Verify file count matches scan
        assert status["total_files"] == len(
            created_files
        ), "Status should match scan results"

        print("  ✅ Status reporting accurate")

    finally:
        cleanup_test_environment(test_dir)


def test_indexing_without_ai():
    """Test indexing behavior when AI is not available"""
    print("🧪 Testing Indexing Without AI...")

    test_dir, test_docs_dir, test_vector_dir, created_files = setup_test_environment()

    try:
        # Create vault without AI model (will fail to connect)
        vault = DocumentVault(
            docs_folder=test_docs_dir, model_name="non-existent-model"
        )

        # Test indexing without AI
        index_result = vault.index_documents()

        assert not index_result["success"], "Indexing should fail without AI"
        assert (
            "AI embeddings not available" in index_result["error"]
        ), "Should indicate AI unavailable"

        print("  ✅ Graceful failure when AI unavailable")
        print(f"  ✅ Error message: {index_result['error']}")

    finally:
        cleanup_test_environment(test_dir)


def test_file_type_support():
    """Test support for different file types"""
    print("🧪 Testing File Type Support...")

    test_dir, test_docs_dir, test_vector_dir, _ = setup_test_environment()

    try:
        # Create additional file types
        additional_files = {
            "style.css": "body { font-family: Arial; }",
            "component.jsx": "const Component = () => <div>Hello</div>;",
            "types.ts": "interface User { name: string; }",
            "unsupported.xyz": "This file type is not supported",
        }

        for filename, content in additional_files.items():
            file_path = os.path.join(test_docs_dir, filename)
            with open(file_path, "w") as f:
                f.write(content)

        vault = DocumentVault(docs_folder=test_docs_dir)
        scan_result = vault.scan_documents()

        # Check supported types are found
        file_names = [f["name"] for f in scan_result["files"]]
        assert "style.css" in file_names, "Should support CSS files"
        assert "component.jsx" in file_names, "Should support JSX files"
        assert "types.ts" in file_names, "Should support TypeScript files"

        # Check unsupported type is ignored
        assert (
            "unsupported.xyz" not in file_names
        ), "Should ignore unsupported file types"

        print("  ✅ Supported file types detected")
        print("  ✅ Unsupported file types ignored")

        # Verify supported types list
        supported = scan_result["supported_types"]
        assert ".css" in supported, "CSS should be in supported types"
        assert ".jsx" in supported, "JSX should be in supported types"
        assert ".ts" in supported, "TypeScript should be in supported types"

        print(f"  ✅ Total supported types: {len(supported)}")

    finally:
        cleanup_test_environment(test_dir)


def test_large_file_handling():
    """Test handling of large files"""
    print("🧪 Testing Large File Handling...")

    test_dir, test_docs_dir, test_vector_dir, _ = setup_test_environment()

    try:
        # Create a large file (simulate - don't actually create 10MB)
        vault = DocumentVault(docs_folder=test_docs_dir)

        # Create a moderately sized file
        large_content = "Large file content. " * 1000  # ~20KB
        large_file_path = os.path.join(test_docs_dir, "large_file.txt")
        with open(large_file_path, "w") as f:
            f.write(large_content)

        scan_result = vault.scan_documents()

        # Should find the large file
        large_files = [f for f in scan_result["files"] if f["name"] == "large_file.txt"]
        assert len(large_files) == 1, "Should find large file"

        large_file = large_files[0]
        assert large_file["size"] > 10000, "Should detect large file size"

        print(f"  ✅ Large file detected: {large_file['size_mb']} MB")

        # Test indexing behavior (would skip very large files)
        # Note: This tests the scanning, actual indexing would skip 10MB+ files

    finally:
        cleanup_test_environment(test_dir)


def test_index_clearing():
    """Test index clearing functionality"""
    print("🧪 Testing Index Clearing...")

    test_dir, test_docs_dir, test_vector_dir, _ = setup_test_environment()

    try:
        vault = DocumentVault(docs_folder=test_docs_dir)

        # Create a mock vector store directory
        mock_vector_path = os.path.join(test_dir, "vectorstores", "documents")
        os.makedirs(mock_vector_path, exist_ok=True)

        # Create a test file in the vector store
        test_index_file = os.path.join(mock_vector_path, "test_index.db")
        with open(test_index_file, "w") as f:
            f.write("mock index data")

        # Verify the file exists
        assert os.path.exists(test_index_file), "Test index file should exist"

        # Override the vector_db_path for testing
        vault.vector_db_path = mock_vector_path

        # Test clearing index
        success = vault.clear_index()
        assert success, "Index clearing should succeed"

        # Verify the directory is gone
        assert not os.path.exists(
            mock_vector_path
        ), "Vector store directory should be removed"

        print("  ✅ Index cleared successfully")

    finally:
        cleanup_test_environment(test_dir)


def run_all_tests():
    """Run all document vault tests"""
    print("🧠🔒 MEMORYVAULT AI - DOCUMENT VAULT TESTS")
    print("=" * 50)

    tests = [
        test_document_vault_initialization,
        test_document_scanning,
        test_vault_status,
        test_indexing_without_ai,
        test_file_type_support,
        test_large_file_handling,
        test_index_clearing,
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
        print("✅ Document Vault is working correctly")
    else:
        print(f"\n⚠️  {failed} TESTS FAILED")
        print("Please fix the issues before proceeding")


if __name__ == "__main__":
    run_all_tests()
