import os
from dotenv import load_dotenv
import chromadb

def create_query_embedding(query: str):
    from openai import OpenAI
    client = OpenAI()
    response = client.embeddings.create(
        input=query, model="text-embedding-3-small"
    )
    return response.data[0].embedding

def run_retrieval(query_vector:list, db_path:str, collection_name:str):
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name=collection_name)

    # Query using the pre-generated vector
    results = collection.query(
        query_embeddings=[query_vector], 
        n_results=3
    )

    return results

