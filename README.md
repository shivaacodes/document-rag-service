# Document RAG Service 🤖📄

A production-ready **Retrieval-Augmented Generation (RAG)** microservice built with **FastAPI**, **Next.js**, and **ChromaDB**.

Upload PDF/TXT documents and chat with them using a local LLM (Ollama).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.0-blue.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)

## ✨ Features

- **📄 Multi-Format Support**: Ingest PDF and TXT files with automatic text extraction and chunking.
- **🔍 Semantic Search**: Powered by `SentenceTransformers` and `ChromaDB` for accurate context retrieval.
- **🤖 Local LLM Integration**: Uses **Ollama** for privacy-focused, offline inference.
- **⚡ Modern UI**: Built with **Next.js 14**, **Tailwind CSS**, and **Framer Motion** for a smooth chat experience.
- **🐳 Dockerized**: One-command setup with `docker-compose`.
- **🧪 Robust Testing**: Comprehensive Unit, Integration, and E2E tests with 90%+ coverage.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Vector DB**: ChromaDB
- **Embeddings**: `all-MiniLM-L6-v2`
- **PDF Processing**: `pdfminer.six`
- **Testing**: Pytest, Pytest-Asyncio

### Frontend
- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS
- **State**: React Hooks
- **PDF Viewer**: `react-pdf`

## 🚀 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) & Docker Compose
- [Ollama](https://ollama.ai/) (running locally)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/document-rag-service.git
   cd document-rag-service
   ```

2. **Start the services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000/docs`

## 🧪 Running Tests

The project includes a robust test suite running inside Docker.

```bash
# Run all tests
docker-compose exec backend pytest app/tests

# Run specific test category
docker-compose exec backend pytest app/tests/unit
docker-compose exec backend pytest app/tests/integration
docker-compose exec backend pytest app/tests/e2e
```

## 📂 Project Structure

```
├── backend/             # FastAPI application
│   ├── app/
│   │   ├── api/         # API Routes
│   │   ├── core/        # Config & Settings
│   │   ├── services/    # Business Logic (Ingestion, Retrieval, LLM)
│   │   └── tests/       # Pytest Suite
│   └── Dockerfile
├── frontend/            # Next.js application
│   ├── src/
│   │   ├── components/  # React Components
│   │   └── app/         # Pages & Layouts
│   └── Dockerfile
├── docs/                # Documentation
└── docker-compose.yml   # Orchestration
```

## 🤝 Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` (coming soon) for details.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
