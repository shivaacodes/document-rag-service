# API Reference

The backend exposes a RESTful API built with FastAPI.

## Base URL
`http://localhost:8000`

## Authentication
Currently, the API uses a simple API key mechanism for demonstration purposes.
- **Header**: `X-API-Key`
- **Value**: `local-dev-key` (default for development)

## Endpoints

### 1. Upload Document
Uploads a PDF or TXT file for ingestion. The file is processed, chunked, and stored in the vector database.

- **URL**: `/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

#### Request
| Field | Type | Description |
|-------|------|-------------|
| `file` | File | The PDF or TXT file to upload. |

#### Response
```json
{
  "filename": "example.pdf",
  "chunks": 15,
  "status": "ingested"
}
```

---

### 2. Query (Retrieval Only)
Retrieves the most relevant text chunks for a given query without generating an answer. Useful for debugging retrieval.

- **URL**: `/api/query`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request
```json
{
  "query": "What is the summary of the document?",
  "top_k": 5
}
```

#### Response
```json
{
  "results": [
    {
      "text": "Extracted text chunk...",
      "metadata": { "source": "example.pdf", "page": 1 },
      "score": 0.85
    }
  ]
}
```

---

### 3. Generate Answer (RAG)
Performs the full RAG workflow: retrieves relevant context and generates an answer using the LLM.

- **URL**: `/api/generate`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request
```json
{
  "query": "Explain the main concept.",
  "top_k": 5
}
```

#### Response
```json
{
  "answer": "The main concept is...",
  "chunks": [
    {
      "text": "Relevant context chunk...",
      "score": 0.85
    }
  ]
}
```

## Health Check
- **URL**: `/healthz`
- **Method**: `GET`
- **Response**: `{"status": "ok"}`
