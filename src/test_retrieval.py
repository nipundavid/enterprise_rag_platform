from retriever import create_query_embedding, run_retrieval
from config.load_config import config

query = "Why does Ruskin Bond choose to live in Mussoorie?"

query_vector = create_query_embedding(query)

results = run_retrieval(
    query_vector=query_vector,
    db_path=config.vector_store.persist_directory,
    collection_name=config.vector_store.collection_name,
    k=3
)

print(results["metadatas"])
print(results["documents"])