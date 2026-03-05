import json
from app.agent import FakeNewsAgent

DATA_PATH = "data/mock_news.json"


# TOOL FUNCTION
def tool_get_example(example_id: int):
    """
    Tool that retrieves an article from a local dataset.
    """
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    for item in data:
        if item["id"] == example_id:
            return item

    raise ValueError("Example not found")


def main():

    agent = FakeNewsAgent(use_retrieval=True)

    # Run 2 iterations (assignment requirement)
    for step, example_id in enumerate([1, 2], start=1):

        print("\n==============================")
        print(f"ITERATION {step}")
        print("==============================")

        print("Current internal state:", agent.source_trust)

        # ACTION: tool call
        try:
            example = tool_get_example(example_id)
            tool_ok = True
        except Exception as e:
            print("Tool error:", e)
            tool_ok = False
            example = {"source": "unknown", "article": "", "label": "Unable to Determine"}

        source = example["source"]
        article = example["article"]
        truth = example["label"]

        print("Tool returned article from:", source)

        # AGENT DECISION
        result = agent.analyze(article)

        predicted = result["label"]

        print("Agent prediction:", predicted)
        print("Ground truth:", truth)

        # LEARNING UPDATE
        agent.update_state(source, predicted, truth, tool_ok)

        print("Updated state:", agent.source_trust)
        print("Memory entry:", agent.memory[-1])


if __name__ == "__main__":
    main()