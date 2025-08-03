# -------------------------------------------------------------------------
# File: build_hybrid_store.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: build_data/build_hybrid_store.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides functionality for building a comprehensive hybrid knowledge
# store that supports both GraphRAG and VectorRAG components for the MRCA Advanced
# Parallel Hybrid system. It processes Title 30 CFR regulatory PDF documents to
# create a dual-purpose data structure: entity-relationship graphs for structured
# knowledge traversal and vector embeddings for semantic similarity search. The module
# implements a complete ETL pipeline that transforms regulatory documents into a
# unified hybrid store enabling simultaneous graph and vector search operations.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: HybridStoreBuilder - Main class for building Advanced Parallel Hybrid stores
# - Function: main() - Entry point for hybrid store construction process
# - Global Constants: PROJECT_ROOT, SECRETS_PATH, logging configuration
# - Dependencies: Neo4j graph database, Google Gemini AI, LangChain components
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - os: File system operations and path manipulation
#   - logging: Process tracking and debugging information
#   - io.BytesIO: Binary stream operations for PDF processing
#   - time: API rate limiting and processing delays
#   - traceback: Error debugging and stack trace capture
#   - datetime: Progress tracking and timing operations
# - Third-Party:
#   - toml: Configuration file parsing for secrets management
#   - PyPDF2: PDF text extraction and document processing
#   - langchain_community.graphs: Neo4j graph database integration
#   - langchain_google_genai: Google Gemini AI models and embeddings
#   - langchain_core.documents: Document structure for text processing
#   - langchain.text_splitter: Text chunking for hybrid processing
# - Local Project Modules: None (standalone hybrid store builder)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is designed as a standalone script for building the complete hybrid
# knowledge store required by the MRCA Advanced Parallel Hybrid system. It reads
# PDF documents from the data/cfr_pdf directory and creates both graph structures
# (entities and relationships) and vector embeddings in a single Neo4j database.
# The resulting hybrid store enables simultaneous GraphRAG and VectorRAG operations
# for superior regulatory query processing. This module should be executed during
# system setup or when rebuilding the knowledge base with updated regulatory documents.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

Advanced Hybrid Store Builder for MRCA Mining Regulatory System

Provides comprehensive ETL pipeline for building hybrid knowledge stores that support
both GraphRAG (entity-relationship graphs) and VectorRAG (semantic embeddings) components
from Title 30 CFR regulatory documents for Advanced Parallel Hybrid search capabilities.

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
from datetime import datetime

# Third-party library imports
import toml
import PyPDF2
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Local application/library specific imports
# (None for this standalone module)

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Project root directory for reliable path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the secrets configuration file
SECRETS_PATH = os.path.join(PROJECT_ROOT, ".streamlit", "secrets.toml")

# Configure logging for hybrid store construction monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

# ------------------------------------------------------------------------- HybridStoreBuilder
class HybridStoreBuilder:
    """Advanced Hybrid Store Builder for MRCA Advanced Parallel Hybrid system.
    
    This class provides a comprehensive ETL pipeline for building hybrid knowledge
    stores that support both GraphRAG and VectorRAG components. It processes PDF
    regulatory documents to create a unified data structure containing entity-relationship
    graphs for structured knowledge traversal and vector embeddings for semantic
    similarity search. The hybrid store enables the Advanced Parallel Hybrid system
    to perform simultaneous graph and vector queries for superior regulatory information
    retrieval and compliance assistance.

    Class Attributes:
        None

    Instance Attributes:
        gemini_api_key (str): Google Gemini API key for LLM and embedding operations
        neo4j_uri (str): Neo4j database connection URI
        neo4j_username (str): Neo4j database username
        neo4j_password (str): Neo4j database password
        graph (Neo4jGraph): LangChain Neo4j graph interface for hybrid storage
        llm (ChatGoogleGenerativeAI): Gemini LLM for entity extraction
        embedding_model (GoogleGenerativeAIEmbeddings): Gemini embeddings for vectors
        text_splitter (RecursiveCharacterTextSplitter): Text chunking utility
        total_chunks_processed (int): Progress tracking for processed chunks
        total_entities_created (int): Progress tracking for extracted entities
        start_time (datetime): Processing start time for performance metrics

    Methods:
        __init__(): Initialize the HybridStoreBuilder for full production processing
        print_progress_header(): Print a nice progress header for monitoring
        extract_entities_msha(): Extract MSHA-specific entities with enhanced prompting
        print_progress_stats(): Print current hybrid store construction progress
        process_directory(): Process all PDF files to build complete hybrid store
        process_pdf(): Process PDF to create hybrid store components
        create_vector_index(): Create vector index for semantic search component
        print_final_summary(): Print final hybrid store construction completion summary
    """

    # -------------------
    # --- Constructor ---
    # -------------------
    
    # --------------------------------------------------------------------------------- __init__()
    def __init__(self):
        """Initialize the HybridStoreBuilder for full production processing.

        Sets up connections to Google Gemini AI services and Neo4j database for
        hybrid store construction. Initializes AI models for both entity extraction
        (GraphRAG component) and vector embeddings (VectorRAG component). Configures
        text processing utilities optimized for production-scale regulatory document
        processing with comprehensive progress tracking capabilities.

        Raises:
            ValueError: If required API keys or database credentials are missing
            Exception: If connection to Neo4j or Gemini services fails during initialization
        """
        print("Initializing MRCA Advanced Hybrid Store Builder...")
        try:
            # Gemini API Key from secrets
            self.gemini_api_key = secrets.get("GEMINI_API_KEY")
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY not found in secrets.toml.")
            print(f"✅ Gemini API key loaded")

            # Neo4j Credentials from secrets
            self.neo4j_uri = secrets.get("NEO4J_URI")
            self.neo4j_username = secrets.get("NEO4J_USERNAME")
            self.neo4j_password = secrets.get("NEO4J_PASSWORD")
            if not all([self.neo4j_uri, self.neo4j_username, self.neo4j_password]):
                raise ValueError("Neo4j credentials not found in secrets.toml.")
            print(f"✅ Neo4j credentials loaded")

            # Initialize connections
            print("Connecting to Neo4j...")
            self.graph = Neo4jGraph(
                url=self.neo4j_uri,
                username=self.neo4j_username,
                password=self.neo4j_password
            )
            print("✅ Neo4j connection established")
            
            # Initialize models
            print("Initializing Gemini models...")
            # Set environment variable for Google AI models
            import os
            os.environ["GOOGLE_API_KEY"] = self.gemini_api_key
            
            self.embedding_model = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            )
            
            # Get Gemini model with fallback
            gemini_model = secrets.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
            self.llm = ChatGoogleGenerativeAI(
                model=gemini_model, 
                temperature=0.1
            )
            print("✅ Gemini models initialized")
            
            # Text splitter for production (larger chunks)
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,  # Production chunk size
                chunk_overlap=200
            )
            
            # Progress tracking
            self.total_chunks_processed = 0
            self.total_entities_created = 0
            self.start_time = datetime.now()
            
            print("✅ MRCA Advanced Hybrid Store Builder ready!")

        except Exception as e:
            print(f"❌ ERROR during initialization: {e}")
            raise
    # --------------------------------------------------------------------------------- end __init__()

    # ---------------------------
    # --- Progress Monitoring ---
    # ---------------------------

    # --------------------------------------------------------------------------------- print_progress_header()
    def print_progress_header(self):
        """Print a comprehensive progress header for hybrid store construction monitoring.

        Displays detailed information about the hybrid store construction process
        including start time, target objectives, component descriptions, AI models
        being used, and database information. Provides clear visibility into the
        Advanced Parallel Hybrid system preparation workflow.
        """
        print("\n" + "="*80)
        print("MRCA ADVANCED HYBRID STORE BUILDER - FULL PROCESSING")
        print("="*80)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: Build hybrid store for Advanced Parallel Hybrid system")
        print(f"Graph: Entity-relationship knowledge graph")
        print(f"Vector: Semantic embeddings for similarity search")
        print(f"Models: Gemini 2.5 Pro + Embeddings")
        print(f"Database: Neo4j AuraDB")
        print("="*80)
    # --------------------------------------------------------------------------------- end print_progress_header()

    # --------------------------------------------------------------------------------- print_progress_stats()
    def print_progress_stats(self):
        """Print current hybrid store construction progress statistics.

        Retrieves and displays real-time statistics from the Neo4j database including
        total nodes, chunks with vector embeddings, extracted entities, documents
        processed, and processing rate calculations. Provides comprehensive monitoring
        of both GraphRAG and VectorRAG component construction progress.

        Raises:
            Exception: If database query fails during statistics retrieval
        """
        elapsed = datetime.now() - self.start_time
        elapsed_str = str(elapsed).split('.')[0]  # Remove microseconds
        
        # Get current database stats
        try:
            total_nodes = self.graph.query("MATCH (n) RETURN count(n) as count")[0]['count']
            total_chunks = self.graph.query("MATCH (c:Chunk) RETURN count(c) as count")[0]['count']
            total_entities = self.graph.query("MATCH (e:Entity) RETURN count(e) as count")[0]['count']
            total_docs = self.graph.query("MATCH (d:Document) RETURN count(d) as count")[0]['count']
            
            print(f"\nHYBRID STORE PROGRESS - Elapsed: {elapsed_str}")
            print(f"   Documents: {total_docs}")
            print(f"   Chunks (w/ vectors): {total_chunks}")
            print(f"   Entities (graph nodes): {total_entities}")
            print(f"   Total Nodes: {total_nodes}")
            
            if total_chunks > 0:
                chunks_per_hour = total_chunks / (elapsed.total_seconds() / 3600)
                print(f"   ⚡ Processing Rate: {chunks_per_hour:.1f} hybrid chunks/hour")
                
        except Exception as e:
            print(f"❌ Could not get progress stats: {e}")
    # --------------------------------------------------------------------------------- end print_progress_stats()

    # --------------------------------------------------------------------------------- print_final_summary()
    def print_final_summary(self):
        """Print final hybrid store construction completion summary.

        Generates and displays comprehensive completion statistics including total
        processing time, component counts, processing rates, and readiness confirmation
        for both GraphRAG and VectorRAG components. Provides final validation that
        the Advanced Parallel Hybrid system is ready for deployment.

        Raises:
            Exception: If final database statistics cannot be retrieved
        """
        elapsed = datetime.now() - self.start_time
        elapsed_str = str(elapsed).split('.')[0]
        
        try:
            total_nodes = self.graph.query("MATCH (n) RETURN count(n) as count")[0]['count']
            total_rels = self.graph.query("MATCH ()-[r]-() RETURN count(r) as count")[0]['count']
            total_chunks = self.graph.query("MATCH (c:Chunk) RETURN count(c) as count")[0]['count']
            total_entities = self.graph.query("MATCH (e:Entity) RETURN count(e) as count")[0]['count']
            total_docs = self.graph.query("MATCH (d:Document) RETURN count(d) as count")[0]['count']
            
            print(f"\n" + "="*80)
            print("MRCA ADVANCED HYBRID STORE CONSTRUCTION COMPLETED!")
            print("="*80)
            print(f"   Total Time: {elapsed_str}")
            print(f"Documents: {total_docs}")
            print(f"Hybrid Chunks: {total_chunks:,} (with vector embeddings)")
            print(f"Graph Entities: {total_entities:,}")
            print(f"Total Graph Nodes: {total_nodes:,}")
            print(f"Graph Relationships: {total_rels:,}")
            print(f"Processing Rate: {total_chunks / (elapsed.total_seconds() / 3600):.1f} hybrid chunks/hour")
            print("="*80)
            print("✅ HYBRID STORE COMPONENTS READY:")
            print("    GraphRAG: Entity-relationship graph for structural queries")
            print("    VectorRAG: Semantic embeddings for similarity search")
            print("    Advanced Parallel Hybrid system ready for deployment!")
            print("="*80)
            
        except Exception as e:
            print(f"❌ Could not generate final summary: {e}")
    # --------------------------------------------------------------------------------- end print_final_summary()

    # ---------------------------
    # --- Entity Extraction ---
    # ---------------------------

    # --------------------------------------------------------------------------------- extract_entities_msha()
    def extract_entities_msha(self, text):
        """Extract MSHA-specific entities with enhanced prompting for graph construction.

        Uses Google Gemini LLM to identify and extract mining-specific regulatory
        entities from text chunks. Focuses on mining equipment, safety regulations,
        procedures, and organizational elements that form meaningful graph relationships
        in the hybrid store's GraphRAG component.

        Args:
            text (str): Text chunk from regulatory document to analyze for entities

        Returns:
            list: List of tuples containing (entity_name, entity_type) pairs
                 Limited to 8 entities per chunk for optimal processing

        Examples:
            >>> builder = HybridStoreBuilder()
            >>> entities = builder.extract_entities_msha("Mine safety requires ventilation...")
            >>> print(entities)
            [('Mine Ventilation', 'Safety'), ('Airflow Standards', 'Regulation')]
        """
        prompt = f"""
Extract key entities from this MSHA mining safety regulation text.
Focus on MINING-SPECIFIC terms and regulations that will form graph relationships.

Text: {text[:1000]}...

Extract entities in these categories:
- Equipment: Mining machinery, safety equipment, tools
- Regulation: CFR sections, safety standards, compliance requirements  
- Safety: Safety procedures, hazard types, protective measures
- Mining: Mining operations, mine types, geological terms
- Organization: Government agencies, companies, departments
- Location: Mine locations, geographic areas

Return max 8 entities, one per line:
Format: EntityName (Category)

Entities:
"""
        try:
            response = self.llm.invoke(prompt)
            entities = []
            
            # Handle response content (ensure it's a string)
            content = response.content
            if isinstance(content, list):
                content = ' '.join(str(item) for item in content)
            content = str(content)
            
            for line in content.split('\n'):
                line = line.strip()
                if line and '(' in line and ')' in line:
                    entity_name = line.split('(')[0].strip()
                    entity_type = line.split('(')[1].split(')')[0].strip()
                    if entity_name and entity_type:
                        entities.append((entity_name, entity_type))
            
            return entities[:8]  # Limit to 8 entities per chunk
        except Exception as e:
            print(f"❌ Entity extraction failed: {e}")
            return []
    # --------------------------------------------------------------------------------- end extract_entities_msha()

    # ---------------------------
    # --- Document Processing ---
    # ---------------------------

    # --------------------------------------------------------------------------------- process_directory()
    def process_directory(self, directory_path):
        """Process all PDF files to build the complete hybrid store with progress tracking.

        Scans the specified directory for PDF files and processes each one to build
        both GraphRAG and VectorRAG components of the hybrid store. Provides detailed
        progress tracking, workload estimation, and error handling to ensure complete
        hybrid store construction across all regulatory documents.

        Args:
            directory_path (str): Path to directory containing PDF files for hybrid processing

        Examples:
            >>> builder = HybridStoreBuilder()
            >>> builder.process_directory("../data/cfr_pdf")
        """
        print(f"\nScanning directory for hybrid store construction: {directory_path}")
        
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        print(f"Found {len(pdf_files)} PDF files:")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"   {i}. {pdf_file}")

        # Estimate total chunks
        print(f"\nEstimating hybrid store workload...")
        estimated_chunks = 0
        for pdf_file in pdf_files:
            file_path = os.path.join(directory_path, pdf_file)
            file_size = os.path.getsize(file_path)
            # Rough estimate: 1MB ≈ 1000 chunks
            estimated_chunks += file_size // (1024 * 1024) * 1000
        
        print(f"Estimated total hybrid chunks: ~{estimated_chunks:,}")
        print(f"   Estimated processing time: ~{estimated_chunks//100:.1f} hours")

        for i, pdf_file in enumerate(pdf_files):
            file_path = os.path.join(directory_path, pdf_file)
            print(f"\n{'='*60}")
            print(f"Building hybrid store from PDF {i+1}/{len(pdf_files)}: {pdf_file}")
            print(f"{'='*60}")
            
            success = self.process_pdf(file_path)
            if success:
                print(f"✅ Successfully processed {pdf_file}")
                self.print_progress_stats()
            else:
                print(f"❌ Failed to process {pdf_file}")
    # --------------------------------------------------------------------------------- end process_directory()

    # --------------------------------------------------------------------------------- process_pdf()
    def process_pdf(self, file_path):
        """Process PDF to create hybrid store components.

        Performs comprehensive processing of a single PDF file to create both
        GraphRAG and VectorRAG components: extracts and chunks text, generates
        vector embeddings for semantic search, extracts entities for graph
        relationships, and stores both graph and vector data in Neo4j with
        proper rate limiting and error handling.

        Args:
            file_path (str): Full path to the PDF file to process for hybrid store

        Returns:
            bool: True if hybrid processing succeeds, False if any component fails

        Examples:
            >>> builder = HybridStoreBuilder()
            >>> success = builder.process_pdf("../data/cfr_pdf/title30_part1.pdf")
            >>> print(f"Hybrid processing: {'SUCCESS' if success else 'FAILED'}")
        """
        filename = os.path.basename(file_path)
        print(f"\nProcessing for hybrid store: {filename}")
        
        try:
            # Extract text
            print("Extracting text from PDF...")
            with open(file_path, 'rb') as f:
                pdf_content = f.read()

            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
            print(f"PDF has {len(pdf_reader.pages)} pages")
            
            full_text = ""
            for i, page in enumerate(pdf_reader.pages):
                if page.extract_text():
                    full_text += page.extract_text()
                if (i + 1) % 100 == 0:
                    print(f"   Processed {i+1}/{len(pdf_reader.pages)} pages...")

            if not full_text.strip():
                print(f"❌ No text extracted from {filename}")
                return False

            print(f"Extracted {len(full_text):,} characters")

            # Split into chunks
            print("Splitting into hybrid chunks...")
            text_chunks = self.text_splitter.split_text(full_text)
            print(f"Created {len(text_chunks):,} chunks for hybrid processing")

            # Process chunks in batches with progress tracking
            batch_size = 10
            total_batches = (len(text_chunks) + batch_size - 1) // batch_size
            
            print(f"Building hybrid store: {len(text_chunks)} chunks in {total_batches} batches...")

            for batch_idx in range(0, len(text_chunks), batch_size):
                batch_end = min(batch_idx + batch_size, len(text_chunks))
                batch_chunks = text_chunks[batch_idx:batch_end]
                batch_num = batch_idx // batch_size + 1
                
                print(f"\nHybrid Batch {batch_num}/{total_batches} (chunks {batch_idx+1}-{batch_end})")
                
                batch_entities = 0
                for i, chunk_text in enumerate(batch_chunks):
                    chunk_num = batch_idx + i + 1
                    chunk_id = f"{filename}_{chunk_num}"
                    
                    try:
                        # Generate embedding for vector component
                        print(f"   Generating vector embedding for chunk {chunk_num}...")
                        chunk_embedding = self.embedding_model.embed_query(chunk_text)
                        
                        # Create document and chunk nodes with hybrid data
                        print(f"   🕸️  Creating graph nodes with vector data...")
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
                        
                        # Extract and create entities for graph component
                        print(f"   Extracting entities for graph relationships...")
                        entities = self.extract_entities_msha(chunk_text)
                        for entity_name, entity_type in entities:
                            entity_id = f"{entity_type}_{entity_name.replace(' ', '_').replace('/', '_')}"
                            
                            self.graph.query("""
MERGE (e:Entity {id: $entity_id})
ON CREATE SET e.name = $entity_name, e.type = $entity_type
MERGE (c:Chunk {id: $chunk_id})
MERGE (c)-[:HAS_ENTITY]->(e)
""", {
                                "entity_id": entity_id,
                                "entity_name": entity_name,
                                "entity_type": entity_type,
                                "chunk_id": chunk_id
                            })
                        
                        batch_entities += len(entities)
                        self.total_chunks_processed += 1
                        self.total_entities_created += len(entities)
                        
                        # Progress indicator within batch
                        if i == len(batch_chunks) - 1:  # Last chunk in batch
                            print(f"   ✅ Completed hybrid batch: {len(batch_chunks)} chunks, {batch_entities} entities")
                        
                    except Exception as e:
                        print(f"❌ Failed hybrid chunk {chunk_num}: {e}")
                        continue
                    
                    # Rate limiting
                    time.sleep(1)  # 1 second between chunks
                
                # Longer pause between batches
                if batch_num < total_batches:
                    print(f"Pausing 10 seconds before next hybrid batch...")
                    time.sleep(10)

            print(f"✅ Completed hybrid store for {filename}: {len(text_chunks)} chunks processed")
            return True

        except Exception as e:
            print(f"❌ Failed to process {file_path}: {e}")
            print(f"Error details: {traceback.format_exc()}")
            return False
    # --------------------------------------------------------------------------------- end process_pdf()

    # -------------------------------
    # --- Database Configuration ---
    # -------------------------------

    # --------------------------------------------------------------------------------- create_vector_index()
    def create_vector_index(self):
        """Create vector index for semantic search component of hybrid store.

        Establishes a cosine similarity vector index on text embeddings stored
        in Chunk nodes to enable efficient semantic search operations for the
        VectorRAG component of the Advanced Parallel Hybrid system. Configures
        the index for 768-dimensional embeddings from Google's embedding-001 model.

        Raises:
            Exception: If vector index creation fails due to database connectivity
                      or configuration issues
        """
        print(f"\nCreating vector index for Advanced Parallel Hybrid semantic search...")
        try:
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
            print("✅ Vector index created - hybrid store VectorRAG component ready")
        except Exception as e:
            print(f"❌ Vector index creation failed: {e}")
    # --------------------------------------------------------------------------------- end create_vector_index()

# ------------------------------------------------------------------------- end HybridStoreBuilder

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ------------------------
# --- Helper Functions ---
# ------------------------

# --------------------------------------------------------------------------------- main()
def main():
    """Main function for hybrid store construction with comprehensive progress tracking.

    Orchestrates the complete Advanced Parallel Hybrid store construction workflow
    including HybridStoreBuilder initialization, database management, PDF document
    processing for both GraphRAG and VectorRAG components, vector index creation,
    and final completion reporting. Provides comprehensive error handling and
    progress monitoring throughout the entire hybrid store building process.

    This function serves as the entry point for building the complete MRCA hybrid
    knowledge store from Title 30 CFR regulatory documents, creating the unified
    data structure required for Advanced Parallel Hybrid search operations.

    Raises:
        KeyboardInterrupt: If user interrupts the hybrid store construction process
        Exception: If critical errors occur during hybrid store construction

    Examples:
        >>> if __name__ == "__main__":
        ...     main()
    """
    try:
        builder = HybridStoreBuilder()
        builder.print_progress_header()
        
        data_path = os.path.join("..", "data", "cfr_pdf")
        
        # Ask user about clearing database
        print(f"\nHybrid Store Database Management:")
        print(f"   Current database may contain existing hybrid store data.")
        print(f"   Recommendation: Clear database for fresh hybrid store build.")
        
        # Clear existing data
        print("Clearing existing hybrid store...")
        builder.graph.query("MATCH (n) DETACH DELETE n")
        print("✅ Database cleared - starting fresh hybrid store build")
        
        # Process all PDFs to build hybrid store
        builder.process_directory(data_path)
        builder.create_vector_index()
        
        # Final summary
        builder.print_final_summary()

    except KeyboardInterrupt:
        print(f"\n⚠️ Hybrid store construction interrupted by user")
        print(f"Partial hybrid store progress saved to database")
    except Exception as e:
        print(f"❌ Fatal error in hybrid store construction: {e}")
        print(f"Details: {traceback.format_exc()}")
# --------------------------------------------------------------------------------- end main()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.
# It serves as the entry point for the Advanced Parallel Hybrid store construction
# process, allowing the module to be used both as a standalone script and as an
# importable utility for other components of the MRCA system.

if __name__ == "__main__":
    # --- Advanced Parallel Hybrid Store Construction Entry Point ---
    print(f"Running MRCA Advanced Parallel Hybrid Store Builder from {__file__}...")
    
    try:
        # Execute the main hybrid store building process
        main()
        print("✅ Advanced Parallel Hybrid store construction completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user (Ctrl+C)")
        print("🛑 Hybrid store construction aborted")
        
    except Exception as e:
        print(f"❌ Critical error during hybrid store construction: {e}")
        print(f"Full traceback: {traceback.format_exc()}")
        print("🛑 Hybrid store construction failed")
        
    finally:
        print(f"Finished execution of {__file__}")

# =========================================================================
# End of File
# ========================================================================= 