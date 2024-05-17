import lib_llm
import lib_embeddings
import lib_vectordb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Question(BaseModel):
    q: str

topic = "Elastic"
index_name = "book_wookieepedia_mpnet"

hf = lib_embeddings.setup_embeddings()
db, url = lib_vectordb.setup_vectordb(hf, index_name)
llm_chain_informed = lib_llm.make_the_llm()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": f"I am a chatbot developed by Planom Technology. You can ask me about {topic}"}

@app.post("/ask")
def ask_a_question(question: Question):
    similar_docs = db.similarity_search(question.q)
    if not similar_docs:
        raise HTTPException(status_code=404, detail="No similar documents found")
    response = ask_llm(similar_docs, question.q)
    return {"question": question.q, "answer": response}

def ask_llm(similar_docs, question):
    informed_context = similar_docs[0].page_content
    informed_response = llm_chain_informed.run(context=informed_context, question=question)
    return informed_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
