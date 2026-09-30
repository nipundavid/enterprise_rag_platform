from retriever import create_query_embedding, run_retrieval
from pathlib import Path
from config.load_config import config

def generate_answer(query:str):
    from openai import OpenAI
    client = OpenAI()

    query_embedding = create_query_embedding(query)
    results = run_retrieval(query_vector=query_embedding, db_path=config.vector_store.persist_directory, collection_name=config.vector_store.collection_name)
    retrieved_chunks = results["documents"][0]
    print(f"Retrieved Chunks: {retrieved_chunks}")
    
    context = "\n\n".join(retrieved_chunks)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer based only on the provided context. If unsure, say I don't know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    
    return response.choices[0].message.content 

def ask_query():
    # How old is Mukesh's child?
    # input_query = input("Enter your query: ")
    
    answer = generate_answer("How old is Mukesh's child?") 
    
    print("Answer:", answer)

if __name__ == "__main__":
    ask_query()
    