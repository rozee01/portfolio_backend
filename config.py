import os
from dotenv import load_dotenv
load_dotenv()
# ---- General Settings ----
TIMEOUT_SECONDS = 3600  
VECTOR_DB_PATH = "vectorstore"
DOCS_PATH = "data"  

# ---- Embeddings ----
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---- LLM ----
LLM_MODEL = "llama3-8b-8192"  
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---- Prompt ----
PROMPT_HUB_PATH = "prompt.md"  
