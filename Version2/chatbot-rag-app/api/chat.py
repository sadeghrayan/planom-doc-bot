from langchain_elasticsearch import ElasticsearchStore
from llm_integrations import get_llm
from elasticsearch_client import (
    elasticsearch_client,
    get_elasticsearch_chat_message_history,
)
from flask import render_template, stream_with_context, current_app
import json
import os

INDEX = os.getenv("ES_INDEX", "workplace-app-docs")
INDEX_CHAT_HISTORY = os.getenv(
    "ES_INDEX_CHAT_HISTORY", "workplace-app-docs-chat-history"
)
ELSER_MODEL = os.getenv("ELSER_MODEL", ".elser_model_2")
SESSION_ID_TAG = "[SESSION_ID]"
SOURCE_TAG = "[SOURCE]"
DONE_TAG = "[DONE]"

store = ElasticsearchStore(
    es_connection=elasticsearch_client,
    index_name=INDEX,
    strategy=ElasticsearchStore.SparseVectorRetrievalStrategy(model_id=ELSER_MODEL),
)

@stream_with_context
def ask_question(question, session_id):
    yield f"data: {SESSION_ID_TAG} {session_id}\n\n"
    current_app.logger.debug("Chat session ID: %s", session_id)

    chat_history = get_elasticsearch_chat_message_history(
        INDEX_CHAT_HISTORY, session_id
    )

    if len(chat_history.messages) > 0:
        # create a condensed question
        condense_question_prompt = render_template(
            "condense_question_prompt.txt",
            question=question,
            chat_history=chat_history.messages,
        )
        #condensed_question = get_llm().invoke(condense_question_prompt)
        content = []
        context = ""
        for logs_entry in get_llm().stream(condense_question_prompt):
            content = logs_entry['response']
            context += content
        condensed_question = context    
    else:
        condensed_question = question

    current_app.logger.debug("Condensed question: %s", condensed_question)
    current_app.logger.debug("Question: %s", question)

    docs = store.as_retriever().invoke(condensed_question)
    for doc in docs:
        doc_source = {**doc.metadata, "page_content": doc.page_content}
        current_app.logger.debug(
            "Retrieved document passage from: %s", doc.metadata["name"]
        )
        yield f"data: {SOURCE_TAG} {json.dumps(doc_source)}\n\n"

    qa_prompt = render_template(
        "rag_prompt.txt",
        question=question,
        docs=docs,
        chat_history=chat_history.messages,
    )

    answer = ""
    content = []
    for log_entry in get_llm().stream(qa_prompt):
       content = log_entry['response']
       yield f"data: {content}\n\n"
       answer += content
       #content.append(response_data)
    #yield f"data: {content}\n\n" 
#        #content = chunk.replace(
#        #    "\n", " "
#        #)  # the stream can get messed up with newlines
#        #yield f"data: {content}\n\n"
#        answer += chunk

#    yield f"data: {DONE_TAG}\n\n"
#    current_app.logger.debug("Answer: %s", answer)
    #answer = log_entry

    chat_history.add_user_message(question)
    chat_history.add_ai_message(answer)

#    current_app.logger.debug(get_llm().stream(qa_prompt))
#    for chunk in get_llm().stream(qa_prompt):
#        current_app.logger.debug(chunk)
#        if isinstance(chunk, dict):
#            content = chunk.get("text", "")  # Assuming "text" is the key containing the string
#            if content:
#                content = content.replace("\n", " ")
#                yield f"data: {content}\n\n"
#                answer += content
#        elif isinstance(chunk, str):
#            content = chunk.replace("\n", " ")
#            yield f"data: {content}\n\n"
#            answer += content
    #yield f"data: {content}\n\n"
    yield f"data: {DONE_TAG}\n\n"
    current_app.logger.debug("Answer: %s", answer)
