import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from qdrant_client.models import Filter, SearchParams 
from app.services.session_manager import get_all_collections

# Connect to local Qdrant instance
client = QdrantClient(host="localhost", port=6333)

# Load sentence-transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dimensional

def create_collection(collection_name="documents"):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def embed_text(text: str):
    return model.encode(text).tolist()

def add_document(text: str, metadata: dict, collection_name="documents"):
    vector = embed_text(text)
    doc_id = str(uuid.uuid4())
    
    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=doc_id,
                vector=vector,
                payload={**metadata, "text": text}
            )
        ]
    )
    return doc_id

def search_similar(query: str, top_k=3, collection_name="documents"):
    query_vector = embed_text(query)
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    return [hit.payload["text"] for hit in results if "text" in hit.payload]


def search_similar_documents(query: str, collection_name: str, top_k=3):
    query_vector = embed_text(query)
    
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    
    return search_result


def search_across_collections(query: str, top_k=3):
    query_vector = embed_text(query)
    all_collections = get_all_collections()

    matches = []

    for collection in all_collections:
        try:
            results = client.search(
                collection_name=collection,
                query_vector=query_vector,
                limit=top_k,
                with_payload=True
            )
            for r in results:
                if "text" in r.payload:
                    matches.append({
                        "text": r.payload["text"],
                        "collection": collection,
                        "score": r.score
                    })
        except Exception as e:
            print(f"Skipping collection {collection}: {e}")

    # Sort matches by score and return top overall
    return sorted(matches, key=lambda x: -x["score"])[:top_k]
