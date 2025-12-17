# pre_push_check.py
import requests
from qdrant_client import QdrantClient
from cohere import Cohere

# ----------------------------
# Configuration
# ----------------------------
QDRANT_HOST = "https://281787b6-5564-4c55-87d6-5154fed685ac.us-east4-0.gcp.cloud.qdrant.io:6333"  # replace with your Qdrant URL
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.4_rnW0lalUEOOMmfcWxoYDuJUeBIE5WsrOylVRnqtbk"   # use env variable ideally
COLLECTION_NAME = "physical_ai_book"

FASTAPI_ENDPOINT = "http://localhost:8000/ask"  # backend endpoint

COHERE_API_KEY = "967F04h1ykuimrMRzFcWdH4NcGDGqEB9fN5BkB1O"  # for generating embeddings

# ----------------------------
# Initialize clients
# ----------------------------
qdrant_client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY
)
co = Cohere(api_key=COHERE_API_KEY)

# ----------------------------
# Test 1: Retrieval from Qdrant
# ----------------------------
print("Testing retrieval pipeline...")
sample_text = "Explain ROS2 architecture"
embedding = co.embed(texts=[sample_text], model="small")["embeddings"][0]

try:
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=3
    )
    if results:
        print(f"✅ Retrieval returned {len(results)} chunks.")
        for i, r in enumerate(results, 1):
            print(f"{i}: {r.payload.get('chapter')} - {r.payload.get('url')}")
    else:
        print("❌ Retrieval returned no results.")
except Exception as e:
    print("❌ Retrieval test failed:", e)

# ----------------------------
# Test 2: Backend Agent Endpoint
# ----------------------------
print("\nTesting backend agent...")
payload = {"query": sample_text, "selected_text": ""}

try:
    response = requests.post(FASTAPI_ENDPOINT, json=payload)
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "")
        metadata = data.get("metadata", {})
        if answer:
            print("✅ Agent returned answer successfully.")
            print("Answer snippet:", answer[:200], "...")
            print("Metadata:", metadata)
        else:
            print("❌ Agent returned empty answer.")
    else:
        print(f"❌ Backend returned status {response.status_code}")
except Exception as e:
    print("❌ Backend test failed:", e)

print("\nPre-push verification complete.")
