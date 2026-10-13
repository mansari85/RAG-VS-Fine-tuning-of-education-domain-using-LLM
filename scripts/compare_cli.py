"""
Interactive Side-by-Side Model Comparison CLI
==============================================
Runs both models (RAG and Fine-Tuning) in CMD on any question.
Loads only ONE base model instance in RAM for safe 16 GB CPU operation.

Usage:
    # Interactive mode:
    .\\backend\\.venv\\Scripts\\python.exe scripts/compare_cli.py

    # Single-question mode:
    .\\backend\\.venv\\Scripts\\python.exe scripts/compare_cli.py "What is electrochemistry?"
"""

import sys
import os
import time
from pathlib import Path

# Setup paths
ROOT_DIR = Path(__file__).resolve().parent.parent
FT_DIR = ROOT_DIR / "Fine-Tuning"
RAG_DIR = ROOT_DIR / "RAG"

for p in [str(ROOT_DIR), str(FT_DIR), str(RAG_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from evaluation.compare import EvaluationEngine
except ImportError:
    from Fine_Tuning.evaluation.compare import EvaluationEngine


def print_banner():
    print("\n" + "=" * 70)
    print("      DOMAIN LLM PLATFORM: DUAL MODEL RUNNER (CMD)")
    print("      Model 1: RAG (Base Model + FAISS Vector Retrieval)")
    print("      Model 2: Fine-Tuned (Qwen2.5-1.5B + LoRA Domain Adapter)")
    print("=" * 70)


def evaluate_question(engine: EvaluationEngine, question: str):
    print("\n" + "-" * 70)
    print(f"QUESTION: {question}")
    print("-" * 70)

    # 1. RAG
    print("\n[1] Running RAG (Base Model + Retrieval)...", flush=True)
    t0 = time.time()
    rag_res = engine.run_rag_inference(question)
    rag_time = round(time.time() - t0, 2)

    print("\n>>> RAG ANSWER:")
    print(rag_res.get("answer", "").strip())
    print(f"\n[RAG Sources]: {rag_res.get('retrieved_sources')}")
    print(f"[RAG Stats] Time: {rag_time}s | Tokens: {rag_res.get('generated_tokens')} | Speed: {rag_res.get('tokens_per_second')} tok/s")

    # 2. Fine-Tuning
    print("\n[2] Running Fine-Tuning (LoRA Adapter Without Retrieval)...", flush=True)
    t0 = time.time()
    ft_res = engine.run_finetuning_inference(question)
    ft_time = round(time.time() - t0, 2)

    print("\n>>> FINE-TUNED ANSWER:")
    print(ft_res.get("answer", "").strip())
    print(f"\n[Fine-Tuning Stats] Time: {ft_time}s | Tokens: {ft_res.get('generated_tokens')} | Speed: {ft_res.get('tokens_per_second')} tok/s")
    print("-" * 70 + "\n")


def main():
    print_banner()
    print("Initializing models and FAISS index on CPU (this takes ~10-15s)...", flush=True)
    engine = EvaluationEngine()
    print("✓ Models and index successfully loaded into memory!\n")

    # If argument provided, run once and exit
    if len(sys.argv) > 1 and sys.argv[1].strip():
        question = " ".join(sys.argv[1:]).strip()
        evaluate_question(engine, question)
        return

    # Interactive loop
    print("Enter any question to compare both models.")
    print("Type 'exit' or 'quit' to quit.\n")

    while True:
        try:
            q = input("\nEnter Question > ").strip()
            if not q:
                continue
            if q.lower() in ["exit", "quit", "q"]:
                print("Exiting...")
                break
            evaluate_question(engine, q)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
