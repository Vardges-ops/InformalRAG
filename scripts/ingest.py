import pandas as pd
from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# df = pd.read_parquet("hf://datasets/rahular/simple-wikipedia/data/train-00000-of-00001-090b52ccb189d47a.parquet")
df = pd.DataFrame({})

docs = []
current_title = None
current_text = []

def is_title(text):
    text = text.strip()
    return (
        len(text) < 50 and
        text[0].isupper() and
        "." not in text
    )

for row in df["text"]:
    if is_title(row):
        # save previous doc
        if current_title:
            docs.append({
                "title": current_title,
                "content": " ".join(current_text)
            })
        # start new doc
        current_title = row.strip()
        current_text = []
    else:
        current_text.append(row.strip())


if current_title:
    docs.append({
        "title": current_title,
        "content": " ".join(current_text)
    })

docs_df = pd.DataFrame(docs)
docs_df2 = docs_df[docs_df.content.str.strip() != '']

def is_valid_title(t):
    t = t.strip()
    return not (
        t.endswith(":") or         # section headers
        len(t.split()) > 6 or      # too long → likely sentence
        t.islower()                # not a proper title
    )

docs_df2 = docs_df2[docs_df2["title"].apply(is_valid_title)]

df["doc_id"] = range(len(df))


def chunk_text(text, chunk_size=250, overlap=40):
    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        if chunk_words:
            chunks.append(" ".join(chunk_words))

    return chunks


rows = []

for doc_id, row in df.iterrows():
    title = row["title"].strip()
    content = row["content"].strip()

    chunks = chunk_text(content, chunk_size=250, overlap=40)

    for chunk_id, chunk in enumerate(chunks):
        rows.append({
            "doc_id": doc_id,
            "title": title,
            "chunk_id": chunk_id,
            "text": f"{title}. {chunk}"
        })


chunks_df = pd.DataFrame(rows)

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = chunks_df["text"].tolist()
embeddings = model.encode(
    texts,
    batch_size=32,
    normalize_embeddings=True,
    show_progress_bar=True
)

client = QdrantClient(url="http://localhost:6333")  # persists on disk

collection_name = "wiki_chunks"

collections = client.get_collections().collections
names = [c.name for c in collections]

if collection_name not in names:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=embeddings.shape[1],
            distance=Distance.COSINE
        )
    )

batch_size = 1000

for i in range(0, len(embeddings), batch_size):
    batch = []

    for j in range(i, min(i + batch_size, len(embeddings))):
        batch.append(PointStruct(
            id=j,
            vector=embeddings[j].tolist(),
            payload={
                "doc_id": int(chunks_df.iloc[j]["doc_id"]),
                "title": chunks_df.iloc[j]["title"],
                "chunk_id": int(chunks_df.iloc[j]["chunk_id"]),
                "text": chunks_df.iloc[j]["text"]
            }
        ))

    client.upsert(
        collection_name=collection_name,
        points=batch
    )