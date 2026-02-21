import os
import requests
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma


NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in environment variables.")


def fetch_trusted_articles():
    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "sources": "bbc-news,reuters",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        raise ValueError(f"NewsAPI error: {data}")

    return data["articles"]


def load_into_chroma():
    articles = fetch_trusted_articles()

    documents = []

    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")

        content = f"{title}\n\n{description}"
        documents.append(Document(page_content=content))

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    vectorstore = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory="chroma_db",
    )

    vectorstore.persist()

    print(f"Loaded {len(documents)} articles into Chroma.")


if __name__ == "__main__":
    load_into_chroma()