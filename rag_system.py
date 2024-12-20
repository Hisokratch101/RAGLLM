#!/usr/bin/env python3
import os
import argparse
from typing import List, Dict, Any
import logging
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_groq(api_key: str) -> ChatGroq:
    """Initialize the Groq LLM."""
    try:
        return ChatGroq(
            groq_api_key=api_key,
            model_name="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=2048
        )
    except Exception as e:
        logger.error(f"Failed to initialize Groq: {e}")
        raise

def load_documents(pdf_path: str) -> List[Any]:
    """Load documents from a file or directory."""
    path = Path(pdf_path)
    try:
        if path.is_dir():
            logger.info(f"Loading PDFs from directory: {pdf_path}")
            loader = DirectoryLoader(
                pdf_path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader
            )
        else:
            logger.info(f"Loading single PDF: {pdf_path}")
            loader = PyPDFLoader(str(path))
        
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} document segments")
        return documents
    
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        raise

def create_vectorstore(documents: List[Any], embeddings: HuggingFaceEmbeddings) -> Chroma:
    """Create vector store from documents."""
    try:
        logger.info("Creating text chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        texts = text_splitter.split_documents(documents)
        
        logger.info("Creating vector store...")
        return Chroma.from_documents(
            documents=texts,
            embedding=embeddings
        )
    
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise

def setup_rag_system(pdf_path: str, api_key: str) -> ConversationalRetrievalChain:
    """Set up the complete RAG system."""
    try:
        # Initialize Groq
        llm = setup_groq(api_key)
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Load documents
        documents = load_documents(pdf_path)
        
        # Create vector store
        vectorstore = create_vectorstore(documents, embeddings)
        
        # Initialize memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create chain
        logger.info("Setting up conversation chain...")
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            return_source_documents=True
        )
        
        return chain
    
    except Exception as e:
        logger.error(f"Error setting up RAG system: {e}")
        raise

def interactive_qa(chain: ConversationalRetrievalChain):
    """Run interactive Q&A session."""
    logger.info("Starting interactive Q&A session. Type 'exit' to quit.")
    
    while True:
        question = input("\nEnter your question: ").strip()
        
        if question.lower() == 'exit':
            break
            
        if not question:
            continue
            
        try:
            response = chain({"question": question})
            
            print("\nAnswer:", response["answer"])
            print("\nSources:")
            for i, doc in enumerate(response["source_documents"], 1):
                print(f"\n{i}. {doc.page_content[:200]}...")
                
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            print("An error occurred. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="RAG System with Groq and PDF support")
    parser.add_argument(
        "pdf_path",
        help="Path to PDF file or directory containing PDFs"
    )
    parser.add_argument(
        "--api-key",
        help="Groq API key (or set GROQ_API_KEY environment variable)",
        default=os.getenv("GROQ_API_KEY")
    )
    
    args = parser.parse_args()
    
    if not args.api_key:
        logger.error("No Groq API key provided. Set it via --api-key or GROQ_API_KEY environment variable")
        return
    
    try:
        chain = setup_rag_system(args.pdf_path, args.api_key)
        interactive_qa(chain)
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        return

if __name__ == "__main__":
    main()