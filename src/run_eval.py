import csv
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

eval_dataset = "/workspaces/enterprise_rag_platform/eval_dataset/rag_baseline_questions.csv"

eval_data = [{}]

with open(eval_dataset, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        id=row["id"]
        question = row["question"]
        expected_answer = row["expected_answer"]
        eval_data.append({"id": id, "question": question, "expected_answer": expected_answer})

from generation import create_query_embedding, run_retrieval, generate_answer

for data in eval_data[1:]:
    id = data["id"]
    question = data["question"]
    expected_answer = data["expected_answer"]
    query_embedding = create_query_embedding(question)
    db_path = "/workspaces/enterprise_rag_platform/src/my_chroma_db"
    collection_name = "my_collection_short_stories"
    results = run_retrieval(query_vector=query_embedding, db_path=db_path, collection_name=collection_name)
    retrieved_chunks = results["documents"][0]
    answer = generate_answer(question, retrieved_chunks, source=results["metadatas"][0]) 
    logger.info(f"Question {id}: {question}")
    logger.info(f"Answer: {answer}")
    logger.info(f"Expected Answer: {expected_answer}")