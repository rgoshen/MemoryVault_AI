#!/usr/bin/env python3
"""
MemoryVault AI - Setup Verification
==================================
Verifies your system is ready to run MemoryVault AI.
Checks dependencies, Ollama connection, and creates project folders.

Run with: python setup_verification.py
"""

import sys
import requests
from datetime import datetime
from pathlib import Path


class MemoryVaultSetupVerifier:
    def __init__(self):
        self.all_tests_passed = True
        self.results = []

    def log_result(self, test_name, passed, details=""):
        """Log test result"""
        self.results.append(
            {
                "test": test_name,
                "passed": passed,
                "details": details,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if not passed:
            self.all_tests_passed = False

    def test_python_version(self):
        """Test Python version compatibility"""
        print("🐍 Testing Python version...")

        version = sys.version_info
        if version.major == 3 and version.minor >= 13:
            print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
            self.log_result(
                "Python Version",
                True,
                f"{version.major}.{version.minor}.{version.micro}",
            )
            return True
        else:
            print(
                f"  ❌ Python {version.major}.{version.minor}."
                f"{version.micro} - Need Python 3.13+"
            )
            self.log_result(
                "Python Version",
                False,
                f"Need 3.13+, got {version.major}.{version.minor}",
            )
            return False

    def test_required_packages(self):
        """Test if required packages are installed"""
        print("📦 Testing required packages...")

        required_packages = [
            ("langchain", "Core LangChain framework"),
            ("streamlit", "Web interface"),
            ("requests", "Web functionality"),
            ("chromadb", "Document storage"),
            ("pypdf", "PDF processing"),
            ("bs4", "Web scraping"),
            ("fastapi", "API server"),
            ("uvicorn", "ASGI server"),
        ]

        missing_packages = []

        for package, description in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"  ✅ {package}")
            except ImportError:
                print(f"  ❌ {package} - MISSING")
                missing_packages.append(package)

        if missing_packages:
            self.log_result(
                "Required Packages", False, f"Missing: {', '.join(missing_packages)}"
            )
            return False
        else:
            self.log_result("Required Packages", True, "All packages installed")
            return True

    def test_ollama_connection(self):
        """Test Ollama connection"""
        print("🔧 Testing Ollama connection...")

        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                print("  ✅ Ollama is running")

                models = response.json()
                if models.get("models"):
                    print("  📋 Available models:")
                    model_names = []
                    for model in models["models"]:
                        name = model.get("name", "Unknown")
                        print(f"    • {name}")
                        model_names.append(name)

                    self.log_result(
                        "Ollama Connection", True, f"Models: {', '.join(model_names)}"
                    )
                    return True
                else:
                    print("  ❌ No models found")
                    self.log_result("Ollama Connection", False, "No models available")
                    return False
            else:
                print(f"  ❌ Ollama returned status {response.status_code}")
                return False

        except requests.exceptions.RequestException:
            print("  ❌ Cannot connect to Ollama")
            print("  💡 Make sure GPT4All is running")
            self.log_result("Ollama Connection", False, "Connection failed")
            return False

    def create_project_folders(self):
        """Create necessary project folders"""
        print("📁 Creating project folders...")

        folders = ["LocalDocs", "memory", "vectorstores", "exports"]
        created = []

        for folder in folders:
            try:
                Path(folder).mkdir(exist_ok=True)
                print(f"  ✅ {folder}/")
                created.append(folder)
            except Exception as e:
                print(f"  ❌ Failed to create {folder}/: {e}")

        self.log_result(
            "Project Folders", len(created) == len(folders), f"Created: {created}"
        )
        return len(created) == len(folders)

    def generate_report(self):
        """Generate verification report"""
        print("\n" + "=" * 60)
        print("📊 MEMORYVAULT AI SETUP VERIFICATION")
        print("=" * 60)

        passed_tests = [r for r in self.results if r["passed"]]
        failed_tests = [r for r in self.results if not r["passed"]]

        print(f"✅ Passed: {len(passed_tests)}")
        print(f"❌ Failed: {len(failed_tests)}")
        print(f"📊 Success Rate: " f"{len(passed_tests)/(len(self.results))*100:.1f}%")

        if failed_tests:
            print("\n⚠️  ISSUES TO FIX:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['details']}")

        if self.all_tests_passed:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Your system is ready for MemoryVault AI")
            print("\n🚀 Next step: Create core_components.py")
        else:
            print("\n⚠️  SETUP INCOMPLETE")
            print("Please fix the failed tests before proceeding")

    def run_all_tests(self):
        """Run all verification tests"""
        print("🧠🔒 MEMORYVAULT AI SETUP VERIFICATION")
        print("=" * 50)

        tests = [
            self.test_python_version,
            self.test_required_packages,
            self.test_ollama_connection,
            self.create_project_folders,
        ]

        for test_func in tests:
            print()
            test_func()

        self.generate_report()


if __name__ == "__main__":
    verifier = MemoryVaultSetupVerifier()
    verifier.run_all_tests()
