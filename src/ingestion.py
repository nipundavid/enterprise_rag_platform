import pymupdf4llm
import logging
import chromadb
from pathlib import Path as PATH
client = chromadb.Client()
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

CHUNK_SIZE = 512
OVERLAP = 50
COLLECTION_NAME = "my_collection_short_stories"

# Format: {"file_name": text}
texts_data = {} 

# Format: {"text": chunk, "source": source, "embedding": embedding}
chunks = [] 


def load_text(file):
    text = pymupdf4llm.to_markdown(file)
    texts_data[file.name] = text

def create_chunks(text_data:dict):
    
    for text, source in zip(text_data.values(), text_data.keys()):
        for i in range(0, len(text), CHUNK_SIZE - OVERLAP):
            chunk = text[i:i + CHUNK_SIZE]
            chunks.append({"text": chunk, "source": source})
    return chunks


def create_index(chunks:list):
    # Set up an OpenAI embedding function (requires your API key)
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    db_path = PATH(__file__).resolve().parent / "my_chroma_db"
    client = chromadb.PersistentClient(path=str(db_path))

    # Pass the embedding function during collection creation
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, 
        embedding_function=openai_ef
    )

    # Now, adding text automatically uses OpenAI to generate the embeddings
    collection.add(
        documents=[chunk["text"] for chunk in chunks],
        ids=[f"doc{i}" for i in range(len(chunks))],
        metadatas=[{"source": chunk["source"]} for chunk in chunks]
    )


def start_ingestion(data:str):
    # Ingest all the pdfs in the data folder and store them in a list
    try:
        dir_path = PATH(data)
        for pdf in dir_path.glob("*.pdf"):
            logging.info(f"Processing PDF: {pdf.name}")
            load_text(pdf)
        logging.info(f"Total PDFs processed: {len(texts_data)}")
    except Exception as e:
        logging.error(f"Error while reading pdf {e}")

    # Create chunks of the text
    try:
        chunks = create_chunks(texts_data)
        logging.info(f"Total chunks created: {len(chunks)}")
    except Exception as e:
        logging.error(f"Error while creating chunks {e}")

    # create index of the chunks and store in ChromaDB
    try:
        create_index(chunks)
        logging.info("Index created successfully.")
    except Exception:
        logging.exception("Error while creating index")



if __name__ == "__main__":
    start_ingestion("/workspaces/enterprise_rag_platform/data")


