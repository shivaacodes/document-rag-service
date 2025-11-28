# PDF→ text extraction → chunking → embeddings → metadata → insert into Chroma → persist

from .text_extraction import (
    extract_text_from_pdf,
    extract_text_from_txt
)
from .chunking import chunk_text
from .embeddings import embedding_service
from .vectorstore import vectorstore


class IngestionService:
    async def ingest(self, file_bytes: bytes, filename: str):
        # extract text based on extension
        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        elif filename.lower().endswith(".txt"):
            text = extract_text_from_txt(file_bytes)
        else:
            raise ValueError("Unsupported file type")

        # Clear existing documents to ensure fresh context
        vectorstore.clear()

        # 1. chunk text
        chunks = chunk_text(text)
        print(f"DEBUG: Generated {len(chunks)} chunks")
        if not chunks:
            print("DEBUG: No chunks generated! Text might be empty.")
        
        chunk_texts = [c["text"] for c in chunks]

        # 2. embed chunks
        embeddings = await embedding_service.embed_texts(chunk_texts)

        # 3. metadata
        ids = [f"{filename}::{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": filename,
                "chunk_index": c["chunk_index"],
                "start_token": c["start_token"],
                "end_token": c["end_token"],
            }
            for c in chunks
        ]

        # 4. store in Chroma
        vectorstore.add_documents(
            ids=ids,
            documents=chunk_texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

        # 5. return ingestion summary
        return {
            "filename": filename,
            "chunks": len(chunks),
            "status": "ingested"
        }


ingestion_service = IngestionService()

