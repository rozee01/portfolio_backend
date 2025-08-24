from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import MarkdownTextSplitter
import config

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
    loader = DirectoryLoader(config.DOCS_PATH, glob="**/*.md")
    docs = loader.load()

    # Split into chunks for markdown
    splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
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
