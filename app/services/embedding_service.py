import os, pickle
from dotenv import load_dotenv
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from fastapi.responses import JSONResponse

load_dotenv()


class EmbeddingService:
    def __init__(self, embed_dir: str = "app/embeddings"):
        os.makedirs(embed_dir, exist_ok=True)
        self.embed_dir = embed_dir
        self.embeddings = OpenAIEmbeddings()

    def create_embedding(self, file_bytes: bytes, filename: str) -> str:
        """Convert text file to embeddings and save."""
        try:
            print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
            content = file_bytes.decode("utf-8")
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_text(content)
            docs = [Document(page_content=c, metadata={"source": filename}) for c in chunks]

            vector_store = FAISS.from_documents(docs, self.embeddings)

            output_path = os.path.join(self.embed_dir, filename.replace(".txt", ""))
            vector_store.save_local(output_path)  # <-- this actually writes files

            return output_path
        except Exception as e:
            print("Embedding creation error:", e)
            raise e

    def query_embedding(self, query: str, embed_filename: str):
        try:
            """Search the given embedding file for a query."""
            file_path = os.path.join(self.embed_dir, embed_filename)
            if not os.path.exists(file_path):
                return JSONResponse({"error": "Embedding file not found"}, status_code=404)

            # Load FAISS index from disk
            vector_store = FAISS.load_local(
                                file_path,
                                self.embeddings,
                                allow_dangerous_deserialization=True
                            )

            results = vector_store.similarity_search(query, k=3)
            output = [{"content": r.page_content, "metadata": r.metadata} for r in results]
            return {"query": query, "results": output}
        except Exception as e:
           print("Embedding Query error:", e)
           raise e
