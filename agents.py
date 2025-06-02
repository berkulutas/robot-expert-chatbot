import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,  # TODO experiment
)

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import AzureChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


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
text_splitter = CharacterTextSplitter(
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


qa_prompt = PromptTemplate(
    input_variables=["input", "history", "context"],
    template=(
        "You are a helpful assistant for robots.\n"
        "Only answer using the provided context. Be concise.\n"
        "If the answer is not in the context, say: 'I don’t have that information in my documentation.'\n\n"
        "Previous Conversation:\n{history}\n\n"
        "Question: {input}\n\n"
        "Context:\n{context}"
    ),
)


def format_history(history: list[dict]) -> str:
    if not history:
        return "None"

    formatted = []
    for turn in history:
        user = turn.get("user", "").strip()
        assistant = turn.get("assistant", "").strip()
        if user:
            formatted.append(f"User: {user}\n")
        if assistant:
            formatted.append(f"Assistant: {assistant}\n")
    return "\n".join(formatted).strip() if formatted else "None"


def kuka_agent(question: str, history: list = None):
    if history is None:
        history = []
    history_text = format_history(history)

    document_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt)

    retrieval_chain = create_retrieval_chain(
        retriever=kuka_db.as_retriever(search_kwargs={"k": 3}),
        combine_docs_chain=document_chain,
    )

    result = retrieval_chain.invoke({"input": question, "history": history_text})[
        "answer"
    ]

    if not result.strip() or "I don’t have" in result.lower():
        return "I don’t have that information in my documentation."

    return result.strip()


def fanuc_agent(question: str, history: list = None):
    if history is None:
        history = []
    history_text = format_history(history)

    document_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt)

    retrieval_chain = create_retrieval_chain(
        retriever=fanuc_db.as_retriever(search_kwargs={"k": 3}),
        combine_docs_chain=document_chain,
    )

    result = retrieval_chain.invoke({"input": question, "history": history_text})[
        "answer"
    ]

    if not result.strip() or "I don’t have" in result.lower():
        return "I don’t have that information in my documentation."

    return result.strip()


def route_with_llm(question: str, history: list = None) -> str:
    history_text = format_history(history) if history else ""
    full_prompt = (
        f"Conversation so far:\n{history_text}\n\nNew user question:\n{question}"
    )

    system_msg = SystemMessage(
        content=(
            "You are a router for an industrial robot assistant system.\n"
            "Your job is to determine which robot brand the user is asking about.\n"
            "Respond with only one of the following: KUKA, FANUC, ABB, UR, YASKAWA, OTHER.\n"
            "Do not explain. Do not say anything else. Respond with a single brand name only."
        )
    )

    user_msg = HumanMessage(content=full_prompt)

    response = llm.invoke([system_msg, user_msg])
    return response.content.strip().upper()


def orchestrator(question: str, history: list[dict] = None):
    brand = route_with_llm(question, history)

    if brand == "KUKA":
        return kuka_agent(question, history), "KUKA"
    elif brand == "FANUC":
        return fanuc_agent(question, history), "FANUC"
    else:
        return (
            f"Sorry, I only support KUKA and FANUC robots. You asked about: {brand}",
            "Orchestrator",
        )
