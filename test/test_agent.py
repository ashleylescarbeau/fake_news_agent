from app.agent import FakeNewsAgent

# agent = FakeNewsAgent(use_retrieval=False)
agent = FakeNewsAgent(use_retrieval=True)

article = """
BREAKING: Scientists confirm that drinking coffee cures all forms of cancer.
Researchers say pharmaceutical companies tried to hide this discovery.
"""

result = agent.analyze(article)

print(result)