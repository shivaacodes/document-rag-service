# Ensures consistent token counts compatible with embedding and LLM context limits.

import tiktoken

def chunk_text(text: str,chunk_size: int = 1200,overlap: int = 300):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        sub_tokens = tokens[start:end]
        chunk_text = enc.decode(sub_tokens)
        chunks.append({
            "text": chunk_text
            "start_token": start,
            "end_token": end,
            "chunk_index": len(chunks)
        })
        start += chunk_size - overlap
    return chunks
