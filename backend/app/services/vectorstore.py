import chromadb
from ..core.config import settings

class VectorStore:
    def __init__(self):
        # persistent directory for production durability
        # Connect to Chroma server
        self.client = chromadb.HttpClient(
            host=settings.chroma_server_host,
            port=settings.chroma_server_http_port
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

    def count(self):
        return self.collection.count()

    def clear(self):
        try:
            self.client.delete_collection(self.collection_name)
            print("DEBUG: Collection deleted.")
        except Exception as e:
            print(f"DEBUG: Collection delete failed (maybe didn't exist): {e}")
        
        # Always ensure we have a fresh collection
        try:
            self.collection = self.client.get_or_create_collection(self.collection_name)
            print("DEBUG: Vector store recreated/reset.")
        except Exception as e:
            print(f"CRITICAL: Failed to recreate collection: {e}")
            raise e

vectorstore = VectorStore()

vectorstore = VectorStore()


        
