import os
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

models = client.models.list()

for model in models:
    print(model.name)