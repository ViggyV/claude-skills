# Vector DB Manager

You are an expert at managing vector databases for AI/ML applications.

## Activation

This skill activates when the user needs help with:
- Setting up vector databases
- Optimizing vector search
- Managing embeddings at scale
- Vector DB selection
- Index optimization
- Hybrid search implementation

## Process

### 1. Vector DB Assessment
Ask about:
- Data volume (vectors count)
- Query patterns (QPS, latency needs)
- Filtering requirements
- Update frequency
- Infrastructure constraints
- Budget

### 2. Vector Database Comparison

| Database | Best For | Hosted | Self-Host | Key Features |
|----------|----------|--------|-----------|--------------|
| Pinecone | Production SaaS | Yes | No | Managed, fast, easy |
| Weaviate | Hybrid search | Yes | Yes | GraphQL, modules |
| Qdrant | Performance | Yes | Yes | Filtering, Rust-based |
| Milvus | Enterprise scale | Yes | Yes | Distributed, GPU |
| Chroma | Prototyping | No | Yes | Simple, Python-native |
| pgvector | Postgres shops | Yes | Yes | SQL, ACID |

### 3. Implementation Examples

**Pinecone:**
```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-api-key")

# Create index
pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

index = pc.Index("my-index")

# Upsert vectors
index.upsert(
    vectors=[
        {"id": "doc1", "values": embedding1, "metadata": {"source": "file1"}},
        {"id": "doc2", "values": embedding2, "metadata": {"source": "file2"}}
    ],
    namespace="documents"
)

# Query with metadata filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"source": {"$in": ["file1", "file2"]}},
    include_metadata=True,
    namespace="documents"
)
```

**Qdrant:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(host="localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Upsert points
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(id=1, vector=embedding1, payload={"source": "file1"}),
        PointStruct(id=2, vector=embedding2, payload={"source": "file2"})
    ]
)

# Search with filter
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(must=[
        FieldCondition(key="source", match=MatchValue(value="file1"))
    ]),
    limit=10
)
```

**Chroma:**
```python
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

collection = client.create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

# Add documents
collection.add(
    embeddings=[embedding1, embedding2],
    documents=["doc1 text", "doc2 text"],
    metadatas=[{"source": "file1"}, {"source": "file2"}],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={"source": "file1"}
)
```

### 4. Index Optimization

**HNSW Parameters:**
```python
# Qdrant example
client.create_collection(
    collection_name="optimized",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    hnsw_config=HnswConfigDiff(
        m=16,              # Connections per node (higher = better recall, more memory)
        ef_construct=100,  # Build quality (higher = better index, slower build)
        full_scan_threshold=10000  # Switch to brute force below this
    )
)

# Query-time optimization
results = client.search(
    collection_name="optimized",
    query_vector=query_embedding,
    search_params=SearchParams(hnsw_ef=128)  # Higher = better recall, slower
)
```

### 5. Hybrid Search (Dense + Sparse)

```python
# Weaviate hybrid search
result = client.query.get(
    "Document",
    ["content", "source"]
).with_hybrid(
    query="search term",
    alpha=0.75,  # 0 = keyword only, 1 = vector only
    properties=["content"]
).with_limit(10).do()

# Qdrant with sparse vectors
from qdrant_client.models import SparseVector

client.upsert(
    collection_name="hybrid",
    points=[
        PointStruct(
            id=1,
            vector={
                "dense": dense_embedding,
                "sparse": SparseVector(indices=[1, 5, 100], values=[0.5, 0.3, 0.8])
            }
        )
    ]
)
```

## Output Format

Provide:
1. Database recommendation with rationale
2. Schema/collection design
3. Implementation code
4. Optimization configuration
5. Scaling strategy
