# Enterprise RAG Platform

An enterprise-focused knowledge platform for turning organizational documents into searchable, answerable knowledge. The project explores a grounded RAG architecture: ingest source documents, retrieve relevant evidence, and generate answers constrained by that evidence.

This portfolio project is being developed toward an enterprise-scale platform. The current implementation establishes the core document-ingestion and question-answering flow; production concerns such as identity-aware access, tenant isolation, operational observability, and evaluation are part of the platform's growth path, not capabilities claimed by the current prototype.

## Platform Flow

```text
PDF documents -> text extraction -> overlapping chunks -> ChromaDB
														^
User question -> query embedding -> relevant chunks -----+-> grounded answer
```

## Current Capabilities

- Extracts PDF content as Markdown and splits it into overlapping text chunks.
- Stores document chunks and source metadata in a persistent ChromaDB collection.
- Embeds user questions and retrieves up to three relevant chunks.
- Generates answers with OpenAI `gpt-4o-mini`, instructing the model to use only retrieved context and acknowledge uncertainty.

## Enterprise Roadmap

The architecture is intended to grow toward the needs of enterprise knowledge systems, including:

- Identity-aware retrieval, authorization, and tenant isolation.
- Multiple document sources, incremental ingestion, and lifecycle management.
- Source-level citations and stronger answer-grounding controls.
- Retrieval and generation evaluation, observability, and cost controls.
- Service APIs, deployment automation, and scalable storage and processing.

These are forward-looking goals; they are not implemented by the current scripts.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key for embeddings and answer generation

Install the project dependencies from the repository root:

```sh
uv sync
```

Set the API key in the shell where you will run the scripts:

```sh
export OPENAI_API_KEY="your-api-key"
```

## Run Locally

Put PDF files in `data/`. The repository includes `GreatStoriesforChildrenRuskinBond.pdf` as a sample. Run both scripts from `src/`; this keeps ingestion and retrieval pointed at the same `src/my_chroma_db` database:

```sh
cd src
uv run ingestion.py
uv run generation.py
```

The generation script prompts for a question. It retrieves up to three text chunks from the `my_collection_short_stories` collection and asks `gpt-4o-mini` to answer using that context. Run ingestion before generation when creating or updating the index.

## Codebase

- `data/`: source PDF documents
- `src/ingestion.py`: document extraction, chunking, and indexing
- `src/retriever.py`: query embedding and similarity retrieval
- `src/generation.py`: context-grounded answer generation
- `src/my_chroma_db/`: local persistent ChromaDB index
