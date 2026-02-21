import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Make sure your Codespace secret is set
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key
)

response = llm.invoke("Explain what fake news is in 2 sentences.")

print(response.content)