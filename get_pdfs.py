import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

# Load env vars
api_grok = "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"
api_langchain = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = api_langchain
if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = api_grok


# Initialize language model, embeddings and text splitter
llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0.7, max_tokens=2048)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={'device': 'cpu'})
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer") #  Set the output key
persist_directory = "chroma_db" # Path to save the vector store

def load_pdfs(pdf_path, is_directory=False):
    if is_directory:
        loader = DirectoryLoader(
            pdf_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
    else:
        loader = PyPDFLoader(pdf_path)
    return loader.load()


def create_vectorstore(documents, persist_directory):
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    #vectorstore.persist()  # No longer necessary
    return vectorstore

def load_vectorstore(persist_directory):
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectorstore


def setup_chain(vectorstore):
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
    )
    return chain


def query_documents(chain, question):
    response = chain.invoke({"question": question}) # Changed to chain.invoke
    return {
        "answer": response["answer"],
        "source_documents": response["source_documents"]
    }


if __name__ == "__main__":
    # Load documents
    pdf_path = "/home/updog/ragllm/downloaded_pdfs/تربية الأغنام : سلالة تمحضيت.pdf"  
    documents = load_pdfs(pdf_path, is_directory=False)
    
    # Check if a vector store exists in the directory, create it if it doesn't
    if not os.path.exists(persist_directory):
        print("Creating vectorstore...")
        vectorstore = create_vectorstore(documents, persist_directory)
    else:
        print("Loading vectorstore...")
        vectorstore = load_vectorstore(persist_directory)
    
    # Setup chain
    chain = setup_chain(vectorstore)
    
    # Query example
    question = "What is the main topic of the documents?"
    response = query_documents(chain, question)
    
    # Print results
    print("Answer:", response["answer"])
    print("\nSources:")
    for doc in response["source_documents"]:
        print(f"- {doc.page_content[:200]}...")