from app.rag.retriever import build_index
if __name__ == "__main__":
    print(f"Built FAISS index with {build_index()} chunks.")
