from langgraph.graph import START, StateGraph, MessagesState
from typing import List
from langchain_core.documents import Document
from model import prompt, llm,format_chat_history
from create_db import db
from conversation_store import get_history, save_message
from dotenv import load_dotenv

load_dotenv()

class State(MessagesState):
    thread_id: str
    question: str
    context: List[Document]
    answer: str

# 1. Retrieve relevant documents
def retrieve(state: State):
    retrieved_docs = db.similarity_search(state["question"])
    return {"context": retrieved_docs}

# 2. Generate answer with history 
def generate(state: State):
    thread_id = state["thread_id"]
    question = state["question"]
    context_docs = state["context"]

    # Get conversation history from MongoDB
    past_messages = get_history(thread_id)
    formatted_history = format_chat_history(past_messages)

    docs_content = "\n\n".join(doc.page_content for doc in context_docs)

    # Build prompt input
    messages = prompt.invoke({
        "context": docs_content,
        "question": question,
        "chat_history": formatted_history
    })

    # Get model response
    response = llm.invoke(messages)

    # Save user and assistant messages to MongoDB
    save_message(thread_id, "user", question)
    save_message(thread_id, "assistant", response.content)

    return {
        "answer": response.content
    }

# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)
graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "generate")
graph = graph_builder.compile()
