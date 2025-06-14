#!/usr/bin/env python3
"""
MemoryVault AI - Document Vault
==============================
Handles document processing, indexing, and querying.
Single Responsibility: Document processing only.

Architecture: Domain service for document management
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict

# LangChain imports
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    CSVLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA


class DocumentVault:
    """Manages document processing and querying"""

    def __init__(
        self,
        docs_folder: str = "LocalDocs",
        model_name: str = "deepseek-r1-distill-8b",
    ):
        self.docs_folder = Path(docs_folder)
        self.docs_folder.mkdir(exist_ok=True)

        self.model_name = model_name
        self.vector_db_path = "vectorstores/documents"
        Path(self.vector_db_path).parent.mkdir(exist_ok=True)

        # Initialize AI components
        self.embeddings = None
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None

        self._initialize_ai_components()
        self._load_existing_vectorstore()

    def _initialize_ai_components(self):
        """Initialize AI model and embeddings with actual connectivity test"""
        try:
            # Create the objects (these don't fail for non-existent models)
            temp_embeddings = OllamaEmbeddings(model=self.model_name)
            temp_llm = OllamaLLM(model=self.model_name)

            # TEST ACTUAL FUNCTIONALITY - this will fail for
            # non-existent models
            try:
                # Test embeddings with a simple query
                test_result = temp_embeddings.embed_query("test")
                if test_result and len(test_result) > 0:
                    # If we get here, embeddings actually work
                    self.embeddings = temp_embeddings
                    self.llm = temp_llm
                    print(
                        f"✅ Document vault initialized with "
                        f"model: {self.model_name}"
                    )
                else:
                    raise Exception("Embeddings returned empty result")

            except Exception as connectivity_error:
                # Actual connection/model test failed
                print(
                    f"⚠️  Warning: Model {self.model_name} not "
                    f"available: {connectivity_error}"
                )
                print(
                    "  Document indexing will not be available until "
                    "AI model is connected"
                )
                self.embeddings = None
                self.llm = None

        except Exception as e:
            print(f"⚠️  Warning: Could not initialize AI components: {e}")
            print(
                "  Document indexing will not be available until "
                "AI model is connected"
            )
            self.embeddings = None
            self.llm = None

    def _load_existing_vectorstore(self):
        """Load existing vectorstore if available"""
        try:
            if os.path.exists(self.vector_db_path) and self.embeddings:
                self.vectorstore = Chroma(
                    persist_directory=self.vector_db_path,
                    embedding_function=self.embeddings,
                )
                self._create_qa_chain()
                print("✅ Existing document database loaded")
        except Exception as e:
            print(f"⚠️  Could not load existing vectorstore: {e}")

    def _create_qa_chain(self):
        """Create QA chain for document querying"""
        if self.vectorstore and self.llm:
            try:
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
                    return_source_documents=True,
                )
            except Exception as e:
                print(f"⚠️  Could not create QA chain: {e}")

    def _get_file_hash(self, file_path: Path) -> str:
        """Get hash of file for change detection"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def scan_documents(self) -> Dict:
        """Scan documents folder and return comprehensive file info"""
        supported_extensions = [
            ".pdf",
            ".txt",
            ".docx",
            ".csv",
            ".md",
            ".py",
            ".js",
            ".html",
            ".css",
            ".json",
            ".tsx",
            ".jsx",
            ".ts",
            ".yaml",
            ".yml",
        ]

        files_info = []
        total_size = 0

        for file_path in self.docs_folder.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                file_stat = file_path.stat()
                file_size = file_stat.st_size
                total_size += file_size

                files_info.append(
                    {
                        "name": file_path.name,
                        "path": str(file_path),
                        "relative_path": (str(file_path.relative_to(self.docs_folder))),
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "modified": datetime.fromtimestamp(
                            file_stat.st_mtime
                        ).isoformat(),
                        "type": file_path.suffix.lower(),
                        "hash": self._get_file_hash(file_path),
                    }
                )

        return {
            "total_files": len(files_info),
            "total_size_mb": round(total_size / (1024 * 1024), 4),
            "files": files_info,
            "supported_types": supported_extensions,
            "scan_time": datetime.now().isoformat(),
        }

    def index_documents(self, force_reindex: bool = False) -> Dict:
        """Index all documents in the folder"""

        if not self.embeddings:
            return {
                "success": False,
                "error": ("AI embeddings not available - " "check model connection"),
            }

        try:
            documents = []
            indexed_files = []
            skipped_files = []
            errors = []

            # File loader mapping
            file_loaders = {
                ".pdf": PyPDFLoader,
                ".txt": TextLoader,
                ".docx": UnstructuredWordDocumentLoader,
                ".csv": CSVLoader,
                ".md": TextLoader,
                ".py": TextLoader,
                ".js": TextLoader,
                ".html": TextLoader,
                ".css": TextLoader,
                ".json": TextLoader,
                ".tsx": TextLoader,
                ".jsx": TextLoader,
                ".ts": TextLoader,
                ".yaml": TextLoader,
                ".yml": TextLoader,
            }

            # Process each supported file
            for file_path in self.docs_folder.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in file_loaders:
                    try:
                        # Skip if file is too large (>10MB)
                        if file_path.stat().st_size > 10 * 1024 * 1024:
                            skipped_files.append(f"{file_path.name} (too large)")
                            continue

                        loader_class = file_loaders[file_path.suffix.lower()]
                        loader = loader_class(str(file_path))
                        docs = loader.load()

                        # Add comprehensive metadata
                        for doc in docs:
                            doc.metadata.update(
                                {
                                    "source_file": file_path.name,
                                    "file_path": str(file_path),
                                    "relative_path": (
                                        str(file_path.relative_to(self.docs_folder))
                                    ),
                                    "file_type": file_path.suffix.lower(),
                                    "file_size": file_path.stat().st_size,
                                    "indexed_time": datetime.now().isoformat(),
                                    "file_hash": self._get_file_hash(file_path),
                                }
                            )

                        documents.extend(docs)
                        indexed_files.append(file_path.name)

                    except Exception as e:
                        errors.append(f"{file_path.name}: {str(e)}")

            if not documents:
                return {
                    "success": False,
                    "error": "No documents could be processed",
                    "indexed_files": indexed_files,
                    "skipped_files": skipped_files,
                    "errors": errors,
                }

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""],
            )
            splits = text_splitter.split_documents(documents)

            # Create or update vectorstore
            if self.vectorstore and not force_reindex:
                # Add to existing vectorstore
                self.vectorstore.add_documents(splits)
            else:
                # Create new vectorstore
                self.vectorstore = Chroma.from_documents(
                    documents=splits,
                    embedding=self.embeddings,
                    persist_directory=self.vector_db_path,
                )

            # Update QA chain
            self._create_qa_chain()

            # Persist the vectorstore
            if hasattr(self.vectorstore, "persist"):
                self.vectorstore.persist()

            return {
                "success": True,
                "indexed_files": indexed_files,
                "skipped_files": skipped_files,
                "total_chunks": len(splits),
                "errors": errors,
                "reindexed": force_reindex,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def query_documents(
        self, question: str, context: str = "", max_results: int = 5
    ) -> Dict:
        """Query documents with optional conversation context"""
        if not self.qa_chain:
            return {
                "success": False,
                "error": "Documents not indexed or QA chain not available",
            }

        try:
            # Enhance question with conversation context if provided
            if context:
                enhanced_question = f"""
Previous conversation context:
{context}

Current question: {question}

Please answer the current question using the documents,\
considering our conversation history.
"""
            else:
                enhanced_question = question

            # Query the documents
            result = self.qa_chain({"query": enhanced_question})

            # Extract and format source information
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"][:max_results]:
                    sources.append(
                        {
                            "file": doc.metadata.get("source_file", "Unknown"),
                            "path": (doc.metadata.get("relative_path", "Unknown")),
                            "type": doc.metadata.get("file_type", "Unknown"),
                            "size": doc.metadata.get("file_size", 0),
                            "content_preview": (
                                doc.page_content[:200] + "..."
                                if len(doc.page_content) > 200
                                else doc.page_content
                            ),
                            "indexed_time": doc.metadata.get("indexed_time"),
                        }
                    )

            return {
                "success": True,
                "answer": result["result"],
                "sources": sources,
                "question": question,
                "enhanced_question": enhanced_question if context else None,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_vault_status(self) -> Dict:
        """Get comprehensive document vault status"""
        scan_result = self.scan_documents()

        return {
            "model_name": self.model_name,
            "ai_available": (self.llm is not None and self.embeddings is not None),
            "vectorstore_available": self.vectorstore is not None,
            "qa_chain_available": self.qa_chain is not None,
            "docs_folder": str(self.docs_folder),
            "vector_db_path": self.vector_db_path,
            "total_files": scan_result["total_files"],
            "total_size_mb": scan_result["total_size_mb"],
            "supported_types": scan_result["supported_types"],
            "last_scan": scan_result["scan_time"],
        }

    def clear_index(self) -> bool:
        """Clear the document index/vectorstore"""
        try:
            if os.path.exists(self.vector_db_path):
                import shutil

                shutil.rmtree(self.vector_db_path)

            self.vectorstore = None
            self.qa_chain = None
            return True
        except Exception as e:
            print(f"Error clearing index: {e}")
            return False
