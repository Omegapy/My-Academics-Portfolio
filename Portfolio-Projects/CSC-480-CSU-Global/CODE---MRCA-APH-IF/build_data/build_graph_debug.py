# -------------------------------------------------------------------------
# File: build_graph_debug.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: build_data/build_graph_debug.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides functionality for building and populating a Neo4j knowledge graph
# from mining regulatory PDF documents using AI-powered entity extraction. It processes
# Title 30 CFR documents by extracting text, creating vector embeddings, and using
# Google's Gemini LLM to identify regulatory entities and relationships. The module
# implements a complete ETL pipeline for transforming regulatory documents into a
# structured knowledge graph with semantic search capabilities.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: GraphBuilder - Main class for building knowledge graphs from PDFs
# - Function: main() - Entry point for the graph building process
# - Global Constants: PROJECT_ROOT, SECRETS_PATH, logging configuration
# - Dependencies: Neo4j graph database, Google Gemini AI, LangChain transformers
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - os: File system operations and path manipulation
#   - logging: Debug logging and process tracking
#   - io.BytesIO: Binary stream operations for PDF processing
#   - time: API rate limiting and sleep operations
#   - traceback: Error debugging and stack trace capture
# - Third-party:
#   - toml: Configuration file parsing for secrets
#   - PyPDF2: PDF text extraction and processing
#   - langchain_community.graphs: Neo4j graph integration
#   - langchain_google_genai: Google Gemini AI models and embeddings
#   - langchain_experimental.graph_transformers: LLM-based entity extraction
#   - langchain_core.documents: Document structure for text processing
#   - langchain.text_splitter: Text chunking for vector processing
#   - langchain_community.graphs.graph_document: Graph entity definitions
# - Local Project Modules: None (standalone utility)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is designed to be run as a standalone script for initial knowledge graph
# construction. It reads PDF documents from the data/cfr_pdf directory and populates
# a Neo4j database with extracted entities and relationships. The resulting knowledge
# graph is then used by the main MRCA application for Advanced Parallel Hybrid search.
# This module should be executed during system setup or when adding new regulatory
# documents to the knowledge base.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

Knowledge Graph Builder for Mining Regulatory Documents

Provides ETL pipeline for transforming Title 30 CFR PDF documents into a Neo4j
knowledge graph using AI-powered entity extraction and vector embeddings for
semantic search capabilities in the MRCA system.

"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import os
import logging
from io import BytesIO
import time
import traceback

# Third-party library imports
import toml
import PyPDF2
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.graphs.graph_document import Node, Relationship

# Local application/library specific imports
# (None for this standalone module)

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Project root directory for reliable path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the secrets configuration file
SECRETS_PATH = os.path.join(PROJECT_ROOT, ".streamlit", "secrets.toml")

# Configure comprehensive logging for debugging and monitoring
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('build_graph_debug.log')  # File output
    ]
)

# Logger for this module
logger = logging.getLogger(__name__)

# Load secrets from the .streamlit/secrets.toml file
if os.path.exists(SECRETS_PATH):
    secrets = toml.load(SECRETS_PATH)
    print(f"✅ Loaded secrets from {SECRETS_PATH}")
else:
    print(f"❌ Secrets file not found at {SECRETS_PATH}")
    secrets = {}

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- GraphBuilder
class GraphBuilder:
    """AI-powered knowledge graph builder for mining regulatory documents.

    This class provides a complete ETL pipeline for transforming PDF regulatory
    documents into a structured Neo4j knowledge graph. It uses Google's Gemini LLM
    for entity extraction, creates vector embeddings for semantic search, and
    establishes relationships between regulatory concepts, procedures, and requirements.
    The class handles PDF text extraction, chunk processing, entity identification,
    and graph database population with proper error handling and rate limiting.

    Class Attributes:
        None

    Instance Attributes:
        gemini_api_key (str): Google Gemini API key for LLM operations
        neo4j_uri (str): Neo4j database connection URI
        neo4j_username (str): Neo4j database username
        neo4j_password (str): Neo4j database password
        graph (Neo4jGraph): LangChain Neo4j graph interface
        llm (ChatGoogleGenerativeAI): Gemini LLM for entity extraction
        embedding_model (GoogleGenerativeAIEmbeddings): Gemini embeddings model
        llm_transformer (LLMGraphTransformer): LLM-based graph transformer
        text_splitter (RecursiveCharacterTextSplitter): Text chunking utility

    Methods:
        __init__(): Initialize the GraphBuilder with API keys and database credentials
        test_llm_transformer(): Test the LLM transformer with a simple example
        create_vector_index(): Create a vector index on Chunk nodes for semantic search
        process_directory(): Process all PDF files in a given directory
        process_pdf(): Extract text, chunk it, create nodes, and build the graph
    """

    # -------------------
    # --- Constructor ---
    # -------------------
    
    # --------------------------------------------------------------------------------- __init__()
    def __init__(self):
        """Initialize the GraphBuilder with API keys and database credentials.

        Sets up connections to Google Gemini AI services and Neo4j database,
        initializes the LLM graph transformer with regulatory entity types,
        and configures text processing utilities. Performs connection testing
        to ensure all services are accessible before processing begins.

        Raises:
            ValueError: If required API keys or database credentials are missing
            Exception: If connection to Neo4j or Gemini services fails
        """
        print("Initializing GraphBuilder...")
        try:
            # Gemini API Key from secrets
            self.gemini_api_key = secrets.get("GEMINI_API_KEY")
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY not found in secrets.toml.")
            print(f"✅ Gemini API key loaded (starts with: {self.gemini_api_key[:10]}...)")

            # Neo4j Credentials from secrets
            self.neo4j_uri = secrets.get("NEO4J_URI")
            self.neo4j_username = secrets.get("NEO4J_USERNAME")
            self.neo4j_password = secrets.get("NEO4J_PASSWORD")
            if not all([self.neo4j_uri, self.neo4j_username, self.neo4j_password]):
                raise ValueError("Neo4j credentials not found in secrets.toml.")
            print(f"✅ Neo4j credentials loaded: {self.neo4j_uri}")

            # Test Neo4j connection first
            print("🔌 Testing Neo4j connection...")
            self.graph = Neo4jGraph(
                url=self.neo4j_uri,
                username=self.neo4j_username,
                password=self.neo4j_password
            )
            # Test the connection
            test_result = self.graph.query("RETURN 'Connection successful' as status")
            print(f"✅ Neo4j connection successful: {test_result}")

            # Initialize the LLM - Using gemini-2.5-pro
            print("Initializing Gemini LLM...")
            # Set environment variable for Google AI models
            import os
            os.environ["GOOGLE_API_KEY"] = self.gemini_api_key
            
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro", 
                temperature=0.1
            )
            print("✅ Gemini LLM initialized")

            # Initialize the Embedding Model
            print("Initializing Gemini embeddings...")
            self.embedding_model = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            )
            print("✅ Gemini embeddings initialized")

            # Initialize the Graph Transformer with explicit node and relationship types
            print("Initializing LLM Graph Transformer...")
            allowed_nodes = ["Person", "Organization", "Location", "Equipment", "Regulation", "Safety", "Procedure", "Chemical", "Mining", "Concept", "Component"]
            allowed_relationships = ["REQUIRES", "RELATES_TO", "PART_OF", "MANAGES", "USES", "LOCATED_IN", "GOVERNS", "APPLIES_TO", "CONTAINS", "SPECIFIES"]
            
            try:
                self.llm_transformer = LLMGraphTransformer(
                    llm=self.llm,
                    allowed_nodes=allowed_nodes,
                    allowed_relationships=allowed_relationships,
                    strict_mode=False
                )
                print("✅ LLM Graph Transformer initialized with allowed types")
            except Exception as transformer_error:
                print(f"❌ LLM Graph Transformer failed: {transformer_error}")
                print("Trying basic LLM Graph Transformer...")
                self.llm_transformer = LLMGraphTransformer(llm=self.llm)
                print("✅ Basic LLM Graph Transformer initialized")

            # Initialize Text Splitter
            print("Initializing text splitter...")
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,  # Smaller chunks for testing
                chunk_overlap=100
            )
            print("✅ Text splitter initialized")

            print("✅ Graph Builder initialized successfully!")

        except Exception as e:
            print(f"❌ ERROR during GraphBuilder initialization: {e}")
            print(f"Full traceback: {traceback.format_exc()}")
            raise
    # --------------------------------------------------------------------------------- end __init__()

    # ---------------------------
    # --- Testing / Validation ---
    # ---------------------------

    # --------------------------------------------------------------------------------- test_llm_transformer()
    def test_llm_transformer(self):
        """Test the LLM transformer with a simple regulatory example.

        Validates that the LLM graph transformer can successfully extract
        entities and relationships from a sample mining safety text. This
        serves as a health check before processing large document collections.

        Returns:
            bool: True if the transformer test passes, False if it fails

        Examples:
            >>> builder = GraphBuilder()
            >>> success = builder.test_llm_transformer()
            >>> print(f"Transformer test: {'PASS' if success else 'FAIL'}")
        """
        print("Testing LLM Graph Transformer...")
        try:
            test_doc = Document(
                page_content="Mine safety requires proper ventilation systems in underground coal mines.",
                metadata={'source': 'test', 'chunk_num': 1}
            )
            
            print("Test document created, converting to graph...")
            graph_documents = self.llm_transformer.convert_to_graph_documents([test_doc])
            print(f"✅ LLM Transformer test successful! Generated {len(graph_documents)} graph documents")
            
            for i, graph_doc in enumerate(graph_documents):
                print(f" Graph doc {i+1}: {len(graph_doc.nodes)} nodes, {len(graph_doc.relationships)} relationships")
                
            return True
        except Exception as e:
            print(f"❌ LLM Transformer test failed: {e}")
            print(f"Full traceback: {traceback.format_exc()}")
            return False
    # --------------------------------------------------------------------------------- end test_llm_transformer()

    # -------------------------------
    # --- Database Configuration ---
    # -------------------------------

    # --------------------------------------------------------------------------------- create_vector_index()
    def create_vector_index(self):
        """Create a vector index on the Chunk nodes for semantic search.

        Establishes a cosine similarity vector index on text embeddings stored
        in Chunk nodes to enable efficient semantic search operations. The index
        is configured for 768-dimensional embeddings from Google's embedding-001 model.

        Raises:
            Exception: If vector index creation fails due to database connectivity
                      or configuration issues
        """
        print("Creating vector index...")
        try:
            # The dimension depends on the embedding model, embedding-001 is 768
            dimension = 768 
            index_query = f"""
CREATE VECTOR INDEX `chunkVector` IF NOT EXISTS
FOR (c:Chunk) ON (c.textEmbedding)
OPTIONS {{
  indexConfig: {{
    `vector.dimensions`: {dimension},
    `vector.similarity_function`: 'cosine'
  }}
}}
"""
            self.graph.query(index_query)
            print("✅ Vector index `chunkVector` created or already exists")
        except Exception as e:
            print(f"❌ Failed to create vector index: {e}")
            print(f"Full traceback: {traceback.format_exc()}")
    # --------------------------------------------------------------------------------- end create_vector_index()

    # ---------------------------
    # --- Document Processing ---
    # ---------------------------

    # --------------------------------------------------------------------------------- process_directory()
    def process_directory(self, directory_path):
        """Process all PDF files in a given directory.

        Scans the specified directory for PDF files and processes each one
        to extract regulatory entities and build the knowledge graph. Provides
        error handling to continue processing remaining files if individual
        files fail.

        Args:
            directory_path (str): Path to directory containing PDF files to process

        Examples:
            >>> builder = GraphBuilder()
            >>> builder.process_directory("../data/cfr_pdf")
        """
        print(f"Processing directory: {directory_path}")
        
        if not os.path.exists(directory_path):
            print(f"❌ Directory does not exist: {directory_path}")
            return
            
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        print(f"Found {len(pdf_files)} PDF files: {pdf_files}")

        for pdf_file in pdf_files:
            file_path = os.path.join(directory_path, pdf_file)
            print(f"\nProcessing: {pdf_file}")
            success = self.process_pdf(file_path)
            if not success:
                print(f"❌ Failed to process {pdf_file}, continuing with next file...")
                continue
    # --------------------------------------------------------------------------------- end process_directory()

    # --------------------------------------------------------------------------------- process_pdf()
    def process_pdf(self, file_path):
        """Extract text, chunk it, create nodes, and build the graph.

        Performs complete ETL processing for a single PDF file including text
        extraction, chunking, vector embedding generation, entity extraction
        using Gemini LLM, and graph database population. Implements rate limiting
        to respect API quotas and provides detailed logging for debugging.

        Args:
            file_path (str): Full path to the PDF file to process

        Returns:
            bool: True if processing succeeds, False if any step fails

        Examples:
            >>> builder = GraphBuilder()
            >>> success = builder.process_pdf("../data/cfr_pdf/title30_part1.pdf")
            >>> print(f"Processing result: {'SUCCESS' if success else 'FAILED'}")
        """
        print(f"Processing PDF: {file_path}")
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"❌ File does not exist: {file_path}")
                return False

            print(f"File size: {os.path.getsize(file_path)} bytes")
            
            with open(file_path, 'rb') as f:
                pdf_content = f.read()

            print("Reading PDF content...")
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
            print(f"PDF has {len(pdf_reader.pages)} pages")
            
            full_text = ""
            for i, page in enumerate(pdf_reader.pages):
                if page.extract_text():
                    page_text = page.extract_text()
                    full_text += page_text
                    if i < 3:  # Show first few pages
                        print(f"Page {i+1} extracted: {len(page_text)} characters")

            if not full_text.strip():
                print(f"❌ No text extracted from {os.path.basename(file_path)}")
                return False

            print(f"Total text extracted: {len(full_text)} characters")

            # Chunk the extracted text
            print("✂Splitting text into chunks...")
            text_chunks = self.text_splitter.split_text(full_text)
            print(f"Split into {len(text_chunks)} chunks")

            # Process only first 2 chunks for testing
            test_chunks = text_chunks[:2]
            print(f"Processing first {len(test_chunks)} chunks for testing...")

            for i, chunk_text in enumerate(test_chunks):
                chunk_num = i + 1
                filename = os.path.basename(file_path)
                chunk_id = f"{filename}_{chunk_num}"

                print(f"\nProcessing Chunk {chunk_num}/{len(test_chunks)} of {filename}")
                print(f"Chunk length: {len(chunk_text)} characters")
                print(f"Chunk preview: {chunk_text[:200]}...")

                # Step 1: Create Document and Chunk nodes with vector embeddings
                print("Generating embeddings...")
                try:
                    chunk_embedding = self.embedding_model.embed_query(chunk_text)
                    print(f"✅ Embedding generated: {len(chunk_embedding)} dimensions")
                except Exception as embed_error:
                    print(f"❌ Embedding generation failed: {embed_error}")
                    continue

                # Create nodes and relationships in Neo4j
                print("Creating nodes in Neo4j...")
                try:
                    self.graph.query("""
MERGE (d:Document {id: $filename})
MERGE (c:Chunk {id: $chunk_id})
ON CREATE SET c.text = $text, c.textEmbedding = $embedding
MERGE (d)<-[:PART_OF]-(c)
""", {
                        "filename": filename,
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                        "embedding": chunk_embedding
                    })
                    print("✅ Nodes created successfully")
                except Exception as node_error:
                    print(f"❌ Node creation failed: {node_error}")
                    continue

                # Step 2: Extract entities and link them to the chunk
                print("🔍 Extracting entities with LLM Graph Transformer...")
                try:
                    doc = Document(
                        page_content=chunk_text,
                        metadata={
                            'source': filename,
                            'chunk_num': chunk_num
                        }
                    )

                    print("Converting to graph documents...")
                    graph_documents = self.llm_transformer.convert_to_graph_documents([doc])
                    print(f"✅ Generated {len(graph_documents)} graph documents")

                    for j, graph_doc in enumerate(graph_documents):
                        print(f"  Graph doc {j+1}: {len(graph_doc.nodes)} nodes, {len(graph_doc.relationships)} relationships")

                    # Get a reference to the chunk node to link entities to it
                    chunk_node = Node(id=chunk_id, type="Chunk")

                    # Add HAS_ENTITY relationships
                    for graph_doc in graph_documents:
                        for node in graph_doc.nodes:
                            graph_doc.relationships.append(
                                Relationship(source=chunk_node, target=node, type="HAS_ENTITY")
                            )

                    print("Adding graph documents to Neo4j...")
                    # Add the graph documents (including new links) to Neo4j
                    self.graph.add_graph_documents(graph_documents)
                    print(f"✅ Successfully processed and linked Chunk {chunk_num}")

                except Exception as entity_error:
                    print(f"❌ Entity extraction failed: {entity_error}")
                    print(f"Full traceback: {traceback.format_exc()}")
                    continue

                # Respect API rate limits
                print("⏱Waiting 5 seconds for API rate limiting...")
                time.sleep(5)

            return True

        except Exception as e:
            print(f"❌ Failed to process {file_path}: {e}")
            print(f"Full traceback: {traceback.format_exc()}")
            return False
    # --------------------------------------------------------------------------------- end process_pdf()

# ------------------------------------------------------------------------- end GraphBuilder

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ------------------------
# --- Helper Functions ---
# ------------------------

# --------------------------------------------------------------------------------- main()
def main():
    """Main function to run the graph building process.

    Orchestrates the complete knowledge graph construction workflow including
    GraphBuilder initialization, LLM transformer testing, PDF document processing,
    and vector index creation. Provides comprehensive error handling and logging
    for the entire pipeline.

    This function serves as the entry point for building the MRCA knowledge graph
    from Title 30 CFR regulatory documents. It processes all PDF files in the
    configured data directory and populates the Neo4j database with extracted
    entities and relationships.

    Raises:
        Exception: If GraphBuilder initialization fails or critical errors occur
                  during the graph construction process

    Examples:
        >>> if __name__ == "__main__":
        ...     main()
    """
    print("Starting MRCA Knowledge Graph Builder")
    print("=" * 50)
    
    try:
        # Initialize builder
        builder = GraphBuilder()

        # Test the LLM transformer first
        if not builder.test_llm_transformer():
            print("❌ LLM Transformer test failed, aborting...")
            return

        # Define the path to the PDF data
        data_path = os.path.join("..", "data", "cfr_pdf")
        print(f"Data path: {data_path}")

        # Process the directory to build the graph
        builder.process_directory(data_path)

        # After processing, create the vector index
        builder.create_vector_index()

        print("✅ Knowledge graph construction process completed!")

    except Exception as e:
        print(f"❌ An error occurred during main execution: {e}")
        print(f"Full traceback: {traceback.format_exc()}")
# --------------------------------------------------------------------------------- end main()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.
# It serves as the entry point for the knowledge graph construction process,
# allowing the module to be used both as a standalone script and as an importable
# utility for other components of the MRCA system.

if __name__ == "__main__":
    # --- Knowledge Graph Construction Entry Point ---
    print(f"Running MRCA Knowledge Graph Builder from {__file__}...")
    
    try:
        # Execute the main graph building process
        main()
        print("Knowledge graph construction completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user (Ctrl+C)")
        print("🛑 Knowledge graph construction aborted")
        
    except Exception as e:
        print(f"❌ Critical error during knowledge graph construction: {e}")
        print(f"Full traceback: {traceback.format_exc()}")
        print("🛑 Knowledge graph construction failed")
        
    finally:
        print(f"Finished execution of {__file__}")

# =========================================================================
# End of File
# ========================================================================= 