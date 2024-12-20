import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from pypdf.errors import PdfReadError, PdfStreamError


# Load env vars
api_grok = "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"
api_langchain = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = api_langchain
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = api_grok

# Initialize language model, embeddings and text splitter
@st.cache_resource()
def initialize_models():
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7, max_tokens=2048)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2",
                                       model_kwargs={'device': 'cpu'})
    return llm, embeddings

llm, embeddings = initialize_models()
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
              all_documents.append(document)
            except (PdfReadError, PdfStreamError) as e:
              print(f"Error loading file {document.metadata['source']}: {e}")
    else:
        loader = PyPDFLoader(pdf_path)
        try:
            all_documents = loader.load()
        except (PdfReadError, PdfStreamError) as e:
            print(f"Error loading file {pdf_path}: {e}")
    return all_documents

@st.cache_resource()
def create_vectorstore(documents, persist_directory, _embeddings):  # Changed embeddings to _embeddings
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=_embeddings,  # Changed embeddings to _embeddings
        persist_directory=persist_directory
    )
    return vectorstore

@st.cache_resource()
def load_vectorstore(persist_directory, _embeddings):  # Changed embeddings to _embeddings
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=_embeddings)  # Changed embeddings to _embeddings
    return vectorstore

def setup_chain(vectorstore, llm, memory):
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
    )
    return chain

def query_documents(chain, question):
    arabic_prompt = f"يرجى الإجابة على السؤال التالي باللغة العربية: {question}"
    response = chain.invoke({"question": arabic_prompt})
    return {
        "answer": response["answer"],
        "source_documents": response["source_documents"]
    }

def main():
    st.markdown("""
       <style>
           body {
               direction: rtl;
           }
       </style>
       """, unsafe_allow_html=True)

    st.title("واجهة نموذج لغوي كبير")

    pdf_path = "/home/updog/ragllm/downloaded_pdfs"
    persist_directory = os.path.join("chroma_db", os.path.basename(pdf_path))

    if not os.path.exists(persist_directory):
        st.warning("No vector store exists. Please run `init_db.py` to create one.")
        return
    else:
        with st.spinner("جارٍ تحميل قاعدة البيانات المتجهة..."):
            vectorstore = load_vectorstore(persist_directory, embeddings)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ConversationBufferMemory(memory_key="chat_history", return_messages=True,
                                                                output_key="answer")
    chain = setup_chain(vectorstore, llm, st.session_state.chat_history)

    question = st.text_input("اطرح سؤالاً حول المستند:", placeholder="اكتب سؤالك هنا")

    if question:
        with st.spinner("جارٍ إنشاء الإجابة..."):
            response = query_documents(chain, question)
            st.write("الإجابة:", response["answer"])

            with st.expander("المصادر"):
                for doc in response["source_documents"]:
                    source = doc.metadata.get('source', 'N/A')  # Get the file source, set N/A if not found
                    st.write(f"- المصدر: {source}") # Display source
                    st.write(f"   - {doc.page_content[:200]}...") # Show the content snippet

if __name__ == "__main__":
    main()