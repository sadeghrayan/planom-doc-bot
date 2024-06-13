import lib_llm
import lib_embeddings
import lib_vectordb
from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

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

# Dictionary to store session data
sessions = {}

@app.middleware("http")
async def add_session_id(request: Request, call_next):
    # Generate a unique session ID for each request
    session_id = request.cookies.get("session_id", str(uuid4()))
    request.state.session_id = session_id
    response = await call_next(request)
    # Set session ID as a cookie in the response
    response.set_cookie("session_id", session_id)
    return response

@app.get("/")
def read_root():
    return {"message": f"I am a chatbot developed by Planom Technology. You can ask me about {topic}"}

@app.post("/ask")
def ask_a_question(request: Request, question: Question):
    session_id = request.state.session_id
    # Retrieve or create session data for the current session ID
    session_data = sessions.setdefault(session_id, {"context": {}})
    
    similar_docs = db.similarity_search(question.q)
    if not similar_docs:
        raise HTTPException(status_code=404, detail="No similar documents found")
    response = ask_llm(similar_docs, question.q, session_data["context"])
    return {"question": question.q, "answer": response}

def ask_llm(similar_docs, question, session_context):
    informed_context = similar_docs[0].page_content
    # Pass session context to LLM for informed response
    informed_response = llm_chain_informed.run(context=informed_context, question=question, session_context=session_context)
    return informed_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
