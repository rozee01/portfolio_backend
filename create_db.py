from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import glob
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownTextSplitter
import config

def simple_md_loader(folder_path):
    docs = []
    for filepath in glob.glob(os.path.join(folder_path, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            docs.append(Document(page_content=content, metadata={"source": filepath}))
    return docs

def load_and_index():
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    db = Chroma(
        persist_directory=config.VECTOR_DB_PATH,
        embedding_function=embeddings
    )
    return db


db = load_and_index()

#this function is only used to create the vector store
def create_vector_store():
    # Load all .md files from DOCS_PATH
    docs = simple_md_loader(config.DOCS_PATH)

    # Split into chunks for markdown
    splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
    all_splits = splitter.split_documents(docs)

    # Create embeddings
    embedding_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    # Create Chroma vector store (persistent)
    os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)
    vector_store = Chroma.from_documents(
        documents=all_splits,
        embedding=embedding_model,
        persist_directory=config.VECTOR_DB_PATH
    )

    print(f" Chroma vector store saved to '{config.VECTOR_DB_PATH}'")

# if __name__ == "__main__":
#     create_vector_store()
