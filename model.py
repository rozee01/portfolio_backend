from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import config

# Load RAG prompt
with open(config.PROMPT_HUB_PATH, "r", encoding="utf-8") as f:
    prompt_template = f.read()

prompt = PromptTemplate.from_template(prompt_template)
# LLM client
llm = ChatGroq(
    temperature=0,
    model=config.LLM_MODEL,
    api_key=config.GROQ_API_KEY
)
def format_chat_history(messages):
    formatted_history = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted_history.append(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            formatted_history.append(f"Assistant: {msg.content}")
        else:
            formatted_history.append(str(msg))
    return "\n".join(formatted_history)