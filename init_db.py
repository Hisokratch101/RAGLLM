import os
import logging
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from pypdf.errors import PdfReadError, PdfStreamError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load env vars
api_grok = "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"
api_langchain = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = api_langchain
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = api_grok

# Initialize language model, embeddings and text splitter
llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0.7, max_tokens=2048)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2",
                                   model_kwargs={'device': 'cpu'})
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)


def load_pdfs(pdf_path, is_directory=False):
    all_documents = []
    if is_directory:
        loader = DirectoryLoader(
            pdf_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        for document in loader.lazy_load():
            try:
                logging.info(f"Loading file: {document.metadata.get('source', 'unknown')}")
                all_documents.append(document)
            except (PdfReadError, PdfStreamError) as e:
                logging.error(f"Error loading file {document.metadata.get('source', 'unknown')}: {e}")
    else:
        loader = PyPDFLoader(pdf_path)
        try:
            logging.info(f"Loading file: {pdf_path}")
            all_documents = loader.load()
        except (PdfReadError, PdfStreamError) as e:
            logging.error(f"Error loading file {pdf_path}: {e}")
    if not all_documents:
        logging.warning("No documents were loaded.")
    return all_documents



def create_vectorstore(documents, persist_directory, _embeddings):  # Changed embeddings to _embeddings
    logging.info("Creating vector store")
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=_embeddings,  # Changed embeddings to _embeddings
        persist_directory=persist_directory
    )
    logging.info("Vector store created")
    return vectorstore


def main():
    pdf_path = "/home/updog/ragllm/downloaded_pdfs" # path to the folder where PDFs are stored
    persist_directory = os.path.join("chroma_db",  os.path.basename(pdf_path) ) # Changed folder path
    logging.info("Starting initialization of the database...")
    documents = load_pdfs(pdf_path, is_directory=True)
    
    if documents:
        if not os.path.exists(persist_directory):
            logging.info("Creating vectorstore...")
            vectorstore = create_vectorstore(documents, persist_directory, embeddings)  # Changed embeddings to embeddings
            logging.info(f"Vectorstore created and saved in: {persist_directory}")
        else:
            logging.info(f"Vectorstore already exists in: {persist_directory}")
    else:
        logging.warning("No documents were loaded, therefore no vectorstore will be created")
    logging.info("Finished initialization of the database.")


if __name__ == "__main__":
    main()