from retriever import create_query_embedding, run_retrieval

def generate_answer(query:str, retrieved_chunks:list, source:dict):
    from openai import OpenAI
    client = OpenAI()
    
    context = "\n\n".join(retrieved_chunks)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer based only on the provided context. If unsure, say I don't know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    
    return response.choices[0].message.content 

if __name__ == "__main__":
    query = "How old is Mukesh's infant?"
    query_embedding = create_query_embedding(query)
    results = run_retrieval(query_vector=query_embedding, db_path="./my_chroma_db", collection_name="my_collection_short_stories")
    retrieved_chunks = results["documents"][0]
    input_query = input("Enter your query: ")
    # How old is Mukesh's child?
    answer = generate_answer(input_query, retrieved_chunks, source=results["metadatas"][0])  # Pass the source metadata if needed 
    
    print("Answer:", answer)