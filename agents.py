import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import AzureChatOpenAI

from langchain.chains import RetrievalQA


# Load environment variables from .env file
load_dotenv()

# Embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# Azure gpt-4o model for q&a
llm = AzureChatOpenAI(
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    deployment_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_BASE_URL"),
    model_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
)

# How to split pdf into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # TODO experiment with chunk size
    chunk_overlap=50,
)


# Load or create faiss index for pdf
def load_or_create_vectorstore(pdf_path: str, index_path: str):
    if os.path.exists(index_path):
        return FAISS.load_local(
            index_path, embedding_model, allow_dangerous_deserialization=True
        )
    else:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        chunks = text_splitter.split_documents(pages)
        vectorstore = FAISS.from_documents(chunks, embedding_model)
        vectorstore.save_local(index_path)
        return vectorstore


# Load dbs
kuka_db = load_or_create_vectorstore(
    pdf_path="docs/kuka_kr1000.pdf", index_path="faiss_index_kuka"
)
fanuc_db = load_or_create_vectorstore(
    pdf_path="docs/fanuc_robots.pdf", index_path="faiss_index_fanuc"
)


def kuka_agent(question: str):
    retriever = kuka_db.as_retriever(search_kwargs={"k": 1})
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa.invoke({"query": question})["result"]

    if not result.strip() or "I don't know" in result or "not sure" in result.lower():
        return "I don’t have that information in my documentation.", "KUKA"

    return result.strip(), "KUKA"


def fanuc_agent(question: str):
    retriever = fanuc_db.as_retriever(search_kwargs={"k": 1})
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa.invoke({"query": question})["result"]

    if not result.strip() or "I don't know" in result or "not sure" in result.lower():
        return "I don’t have that information in my documentation.", "FANUC"

    return result.strip(), "FANUC"


def orchestrator(question: str):
    q = question.lower()

    if "kuka" in q or "kr 10 r1100" in q:
        return kuka_agent(question)

    elif "fanuc" in q or "lr-mate" in q or "200id" in q:
        return fanuc_agent(question)

    elif any(
        brand in q for brand in ["abb", "ur", "yaskawa", "staubli", "kawasaki", "tm"]
    ):
        return (
            "Sorry, I only respond to questions about KUKA and FANUC robots.",
            "Orchestrator",
        )

    else:
        return (
            "Sorry, I only respond to questions about KUKA and FANUC robots.",
            "Orchestrator",
        )
