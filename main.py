import argparse
from record import record_meeting
from transcribe import transcribe
from summarize import main as summarize_main
from search import build_faiss_index, query_faiss

def main():
    parser = argparse.ArgumentParser(description="Meeting Assistant Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("record", help="Record a meeting and transcribe it")
    
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe an audio file")
    transcribe_parser.add_argument("input_path", help="Path to the input audio file")

    subparsers.add_parser("summarize", help="Summarize a transcribed meeting file")

    subparsers.add_parser("index", help="Build FAISS index from summaries")

    search_parser = subparsers.add_parser("search", help="Search meeting summaries")
    search_parser.add_argument("query", help="Search query")

    args = parser.parse_args()

    if args.command == "record":
        record_meeting()
    elif args.command == "transcribe":
        transcribe(args.input_path)
    elif args.command == "summarize":
        summarize_main()
    elif args.command == "index":
        build_faiss_index()
    elif args.command == "search":
        results = query_faiss(args.query)
        print("\nTop Results:")
        for i, r in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Date: {r['date']}")
            print(f"Path: {r['path']}")
            print(f"Score: {r['score']:.2f}")
            print(f"Content:\n{r['content']}\n")

if __name__ == "__main__":
    main()
