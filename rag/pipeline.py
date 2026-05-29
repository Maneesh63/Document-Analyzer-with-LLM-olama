import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from django.shortcuts import get_object_or_404
from .models import Document, QueryHistory

CHROMA_DB_PATH = "./chroma_db"

RAG_PROMPT = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question in detail using ONLY the context below.

Guidelines:
- Give a well-structured answer
- Use bullet points                       
- If the answer is not in the context, say "I don't know"

Context:
{context}

Question:
{question}

Answer in detail:
""")


def get_embedding_model():
    return OllamaEmbeddings(
        model="nomic-embed-text"
    )


def get_llm():
    return ChatOllama(
        model="llama3.2",
        temperature=0.3
    )


class HandleLLM:

   
    @classmethod
    def index_pdf(cls, file_path, document_id):
        try:
             
            loader = PyPDFLoader(file_path)
            pages  = loader.load()

            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            chunks = splitter.split_documents(pages)

            
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "document_id":  str(document_id),
                    "chunk_index":  i,
                    "total_chunks": len(chunks),
                })

             
            Chroma.from_documents(
                documents=chunks,
                embedding=get_embedding_model(),
                persist_directory=CHROMA_DB_PATH,
                collection_name=f"doc_{str(document_id).replace('-', '_')}"
            )

            return None, len(chunks)    

        except Exception as e:
            return str(e), None        


     
    @classmethod
    def query_document(cls, question, document_id):
        try:
            embeddings  = get_embedding_model()
            vectorstore = Chroma(
                persist_directory=CHROMA_DB_PATH,
                embedding_function=embeddings,
                collection_name=f"doc_{str(document_id).replace('-', '_')}"
            )

            retriever = vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )

            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            chain = (
                {
                    "context":  retriever | format_docs,
                    "question": RunnablePassthrough()
                }
                | RAG_PROMPT
                | get_llm()
                | StrOutputParser()
            )

            answer      = chain.invoke(question)
            source_docs = retriever.invoke(question)

            return None, {
                "answer": answer,
                # "source_chunks": [
                #     {
                #         "content":     doc.page_content,
                #         "page_number": doc.metadata.get("page", "N/A"),
                #         "chunk_index": doc.metadata.get("chunk_index", "N/A"),
                #     }
                #     for doc in source_docs
                #]
            }

        except Exception as e:
            return str(e), None