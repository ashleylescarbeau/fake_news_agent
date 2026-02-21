import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma


# Create embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Sample documents
documents = [
    "Fake news spreads misinformation on social media platforms.",
    "Machine learning models can classify news articles.",
    "The sky appears blue due to Rayleigh scattering."
]

# Create vector store
vectorstore = Chroma.from_texts(
    texts=documents,
    embedding=embeddings,
    persist_directory="chroma_db"
)

# Query
query = "How does misinformation spread?"
results = vectorstore.similarity_search(query, k=2)

print("Query Results:")
for r in results:
    print("-", r.page_content)