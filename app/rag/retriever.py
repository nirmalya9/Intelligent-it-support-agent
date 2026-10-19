from pathlib import Path
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = ROOT / "data" / "knowledge"
INDEX_DIR = ROOT / "artifacts" / "rag"
INDEX_PATH = INDEX_DIR / "knowledge.faiss"
DOCS_PATH = INDEX_DIR / "documents.json"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def read_documents():
    docs = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        title = next((line[2:].strip() for line in content.splitlines() if line.startswith("# ")), path.stem)
        for i, chunk in enumerate([x.strip() for x in content.split("\n\n") if len(x.strip()) > 30]):
            docs.append({"title": title, "source": path.name, "text": chunk, "chunk": i})
    return docs


def build_index():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    docs = read_documents()
    if not docs:
        raise RuntimeError(f"No knowledge documents found in {KNOWLEDGE_DIR}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    vectors = np.asarray(model.encode([d["text"] for d in docs], normalize_embeddings=True), dtype="float32")
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, str(INDEX_PATH))
    DOCS_PATH.write_text(json.dumps(docs, indent=2), encoding="utf-8")
    return len(docs)


class KnowledgeRetriever:
    def __init__(self):
        self.model = self.index = self.docs = None

    def _load(self):
        if self.index is None:
            if not INDEX_PATH.exists() or not DOCS_PATH.exists():
                build_index()
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            self.index = faiss.read_index(str(INDEX_PATH))
            self.docs = json.loads(DOCS_PATH.read_text(encoding="utf-8"))

    def search(self, query: str, k: int = 3) -> list[dict]:
        self._load()
        vector = np.asarray(self.model.encode([query], normalize_embeddings=True), dtype="float32")
        scores, ids = self.index.search(vector, min(k, len(self.docs)))
        result = []
        for score, idx in zip(scores[0], ids[0]):
            if idx >= 0:
                d = self.docs[int(idx)]
                result.append({"title": d["title"], "source": d["source"], "excerpt": d["text"][:900],
                               "score": float(score), "text": d["text"]})
        return result
