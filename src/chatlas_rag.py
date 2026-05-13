"""
Example: Integrating raghilda RAG with chatlas

This example demonstrates how to:
1. Build a RAG index from the chatlas documentation
2. Register a search tool with chatlas
3. Use the chat to answer questions about chatlas using RAG

Requirements:
    pip install chatlas raghilda sentence-transformers

Usage:
    python examples/chatlas_rag.py
"""

from pathlib import Path
import inspect

from dotenv import load_dotenv
import torch

from raghilda.store import DuckDBStore
from raghilda.embedding import EmbeddingSentenceTransformers
from raghilda.chunker import MarkdownChunker
from raghilda.read import read_as_markdown
from raghilda.scrape import find_links

load_dotenv()

# Path to store the RAG database
DB_PATH = Path(__file__).parent / "chatlas_docs.db"


def get_best_device() -> torch.device:
    """Select the best available compute device: CUDA, then MPS, then CPU."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def get_device_name(device: torch.device) -> str:
    if device.type == "cuda":
        try:
            return torch.cuda.get_device_name(device.index or 0)
        except Exception:
            return "cuda"
    return device.type


def build_embedder(device: torch.device) -> EmbeddingSentenceTransformers:
    embed_kwargs = {"model": "all-MiniLM-L6-v2"}
    try:
        signature = inspect.signature(EmbeddingSentenceTransformers)
        if "device" in signature.parameters:
            embed_kwargs["device"] = str(device)
        elif "device_name" in signature.parameters:
            embed_kwargs["device_name"] = str(device)
        else:
            print(
                "Warning: EmbeddingSentenceTransformers does not expose a device parameter; "
                "it may default to CPU or infer the device automatically."
            )
    except Exception:
        print(
            "Warning: Unable to inspect EmbeddingSentenceTransformers signature. "
            "Attempting to instantiate without explicit device override."
        )

    return EmbeddingSentenceTransformers(**embed_kwargs)


def build_rag_index():
    """Build a RAG index from the chatlas documentation."""
    print("Finding links from chatlas documentation...")
    links = find_links(
        "https://posit-dev.github.io/chatlas/",
        depth=1,
        children_only=True,
        validate=True,
        progress=True,
    )
    # Filter out image and non-document files
    excluded_extensions = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp")
    links = [link for link in links if not link.lower().endswith(excluded_extensions)]
    print(f"Found {len(links)} pages to index.")

    device = get_best_device()
    device_name = get_device_name(device)
    print(f"Using device: {device_name}")

    print("Creating RAG store and indexing documents...")
    store = DuckDBStore.create(
        location=str(DB_PATH),
        embed=build_embedder(device),
        overwrite=True,
        name="chatlas_docs",
        title="Chatlas Documentation",
    )
    chunker = MarkdownChunker()
    for link in links:
        store.upsert(chunker.chunk(read_as_markdown(link)))

    # Build indexes for faster retrieval
    print("Building search indexes...")
    store.build_index()

    print(f"RAG index built successfully! Stored at: {DB_PATH}")
    print(f"Total documents: {store.size()}")
    return store


def create_chat_with_rag():
    """Create a chatlas chat with RAG tool registered."""
    from chatlas import ChatOllama  # type: ignore[reportMissingImports]

    device = get_best_device()
    device_name = get_device_name(device)
    print(f"Detected best device: {device_name}")

    # Connect to existing store or build if it doesn't exist
    if DB_PATH.exists():
        print(f"Connecting to existing RAG store at {DB_PATH}")
        print("If you want to rebuild the index using the detected accelerator, rerun with --rebuild.")
        store = DuckDBStore.connect(str(DB_PATH), read_only=True)
    else:
        print("RAG store not found. Building index first...")
        store = build_rag_index()

    # Define the RAG search tool
    def search_chatlas_docs(query: str, num_results: int = 5) -> str:
        """
        Search the chatlas documentation for relevant information.

        Use this tool when the user asks questions about chatlas, such as:
        - How to create a chat
        - How to use different models
        - How to register tools
        - How to stream responses
        - Any other chatlas-related questions

        Args:
            query: The search query describing what information to find.
            num_results: Number of relevant chunks to return (default: 5).

        Returns:
            JSON array of relevant excerpts from the chatlas documentation.
        """
        import json

        chunks = store.retrieve(query, top_k=num_results, deoverlap=True)
        return json.dumps(
            [{"text": chunk.text, "context": chunk.context} for chunk in chunks]
        )

    # Create the chat with system prompt
    chat = ChatOllama(
        model="gemma4:e4b",
        system_prompt="""You are a helpful assistant that answers questions about the chatlas Python library.

You have access to a search tool that can find relevant information from the chatlas documentation.
Always use the search tool when answering questions about chatlas to ensure accurate information.

When providing code examples, make sure they are correct and follow chatlas best practices.
If you're not sure about something, say so rather than making things up.""",
    )

    # Register the RAG tool
    chat.register_tool(search_chatlas_docs)

    # Show tool requests but not results
    def handle_tool_request(request):
        print(f"🔍 Searching: {request.arguments.get('query', '')}")

    chat.on_tool_request(handle_tool_request)

    return chat


def main():
    import sys

    # Check if we need to rebuild the index
    if "--rebuild" in sys.argv:
        build_rag_index()

    # Create the chat
    chat = create_chat_with_rag()

    print("\n" + "=" * 60)
    print("Chatlas RAG Assistant")
    print("=" * 60)
    print("Ask questions about the chatlas library.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("=" * 60 + "\n")

    # Interactive chat loop
    while True:
        try:
            user_input = input("❯ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        chat.chat(user_input, echo="text")


if __name__ == "__main__":
    main()
