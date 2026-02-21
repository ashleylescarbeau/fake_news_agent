# app/agent.py

import json
from typing import List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma


class FakeNewsAgent:
    def __init__(
        self,
        use_retrieval: bool = False,
        chroma_path: str = "chroma_db",
        temperature: float = 0.2,
    ):
        """
        Fake News Reasoning Agent

        Args:
            use_retrieval: Whether to use vector retrieval
            chroma_path: Path to Chroma DB
            temperature: LLM temperature (lower = more factual)
        """

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=temperature,
        )

        self.use_retrieval = use_retrieval
        self.retriever = None

        # Optional Retrieval Setup
        if self.use_retrieval:
            embeddings = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001"
            )

            vectorstore = Chroma(
                persist_directory=chroma_path,
                embedding_function=embeddings,
            )

            self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # Build Prompt Template
        self.prompt = ChatPromptTemplate.from_template(
            """
You are an AI fact-checking agent.

Your task is to analyze a news article and determine:

- Real
- Fake
- Unable to Determine

You must:
1. Carefully analyze factual claims.
2. Consider credibility, tone, and verifiability.
3. Provide EXACTLY three reasons.
4. Respond ONLY in valid JSON.

If context is provided, use it as supporting evidence.

Context:
{context}

Article:
{article}

Respond in this format:
{{
  "label": "Real | Fake | Unable to Determine",
  "reasons": [
    "Reason 1",
    "Reason 2",
    "Reason 3"
  ]
}}
"""
        )

        self.parser = StrOutputParser()

    def _retrieve_context(self, article: str) -> str:
        """
        Retrieve similar documents from vector store.
        """
        if not self.retriever:
            return ""

        docs = self.retriever.invoke(article)

        print("\n--- RETRIEVED DOCUMENTS ---")
        for d in docs:
            print(d.page_content[:200])
            print("-----")

        context_text = "\n\n".join([doc.page_content for doc in docs])
        return context_text

    def analyze(self, article: str) -> dict:
        """
        Main entry point for analyzing an article.
        Returns structured dict with label and reasons.
        """

        context = ""
        if self.use_retrieval:
            context = self._retrieve_context(article)

        chain = self.prompt | self.llm | self.parser

# Remove markdown code fences if present


        response = chain.invoke(
            {
                "article": article,
                "context": context,
            }
        )

        if "```" in response:
            response = response.strip()
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()


        # Attempt to parse JSON safely
        try:
            parsed = json.loads(response)
            return parsed
        except Exception:
            return {
                "label": "Error",
                "reasons": ["Model returned invalid JSON", response, ""],
            }