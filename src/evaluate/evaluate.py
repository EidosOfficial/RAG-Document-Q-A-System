import time
import json
import argparse
from src.services.vector_service import retrieve_similar_chunks


def evaluate(top_k: int = 3):
    total_correct = 0
    total_questions = 0
    average_retrieval_latency = 0.0

    with open("eval_dataset.json", "r") as file:
        dataset = json.load(file)

    for entry in dataset:
        total_questions += 1
        start_time = time.perf_counter()
        question, expected_source = entry["question"], entry["expected_source"]
        retrieved_chunks = retrieve_similar_chunks(question, top_k=top_k)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # calculate average retrieval latency
        average_retrieval_latency += (
            execution_time - average_retrieval_latency
        ) / total_questions

        # check if expected source is in retrieved chunks
        did_source_match = any(
            expected_source.lower()
            in (chunk[1].get("source", "").lower() if chunk[1] else "")
            for chunk in retrieved_chunks
        )
        if did_source_match:
            total_correct += 1

    # calculate recall score
    recall_score = total_correct / total_questions

    print_results(
        top_k=top_k,
        total_questions=total_questions,
        total_hits=total_correct,
        recall_score=recall_score,
        avg_latency=average_retrieval_latency,
    )


def print_results(
    top_k: int,
    total_questions: int,
    total_hits: int,
    recall_score: float,
    avg_latency: float,
):
    print("=" * 60)
    print("RETRIEVAL EVALUATION REPORT")
    print("=" * 60)
    print(f"Top-K Value: {top_k}")
    print(f"Total Questions: {total_questions}")
    print(f"Total Hits: {total_hits}")
    print(f"Recall: {recall_score:.2%}")
    print(f"Avg Latency: {avg_latency * 1000:.2f} ms")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the RAG system")
    parser.add_argument(
        "--k",
        type=int,
        default=3,
        help="Number of chunks to retrieve",
    )
    args = parser.parse_args()
    evaluate(args.k)
