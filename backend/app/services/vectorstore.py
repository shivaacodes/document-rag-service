import chromadb
from ..core.config import settings

class VectorStore:
    def __init__(self):
        # persistent directory for production durability
        self.client = chromadb.PersistentClient(
            path=settings.chroma_dir
        )
        self.collection_name = "documents"
        self.collection = self.get_collection()

    def get_collection(self):
        # get or create persistant collection
        try:
            return self.client.get_collection(self.collection_name)
        except:
            return self.client.create_collection(self.collection_name)




    def add_documents(self, ids, documents, embeddings, metadatas):
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query_docs(self, query_embedding, top_k=5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

vectorstore = VectorStore()


        
