import uvicorn
import ollama
import os
import faiss
import numpy as np

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama



from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel



class ChatQuery(BaseModel):
    query: str

app = FastAPI()

MODEL_OLLAMA = "deepseek-r1:1.5b"
MODEL_EMBEDDING = "all-MiniLM-L6-v2"

HOST = "0.0.0.0"
PORT = 5000

embedding_model = SentenceTransformerEmbeddings(model_name=MODEL_EMBEDDING)

# faiss_index =  faiss.IndexFlatL2(embedding_model.client.get_sentence_embedding_dimension())
# vector_store = FAISS.from_embeddings(faiss_index, embedding_model)
vector_store = FAISS.from_texts([""], embedding_model)  # Initialize FAISS with an empty document

retriever = vector_store.as_retriever()
llm = ChatOllama(model=MODEL_OLLAMA)
# qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())


@app.get("/chat/")
async def chat_init():
    response = "Hello to this mini chat-bot"
    return {
        "response": response
    }

@app.post("/chat/")
async def chat(chat_query: ChatQuery):
    try:
        
        response = qa.run(chat_query.query)
        return {"response":response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)