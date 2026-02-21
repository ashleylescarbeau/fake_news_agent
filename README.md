# fake_news_agent
This project builds an agentic fake-news detection system that determines whether a news article or social media post contains real or fake information. The system will combine text classification, OCR (for image inputs), and evidence-based reasoning to produce a label on the introduced dataset, along with clear explanations as to why it was labeled real/fake/unverifiable.

The agent will operate in the domain of digital news and/or social media content. It will require knowledge of news (such as reputable news outlets and fact0checking databases). It also relies on NLP. ML classification models, and OCR technology for imae-based text extraction.

Target users for this project may include studemts, social media users, educators, and other people who want to verify the credibility of the content they are consuming. Users would be able to upload an article or screenshot and ask the system whether the information is real or fake. The agent would respond with a classification of the real/fakeness of the submission, and provide reasoning explaining how it got to that conclusion.

- **Generation:** Google Gemini
- **Embeddings:** Google Gemini
- **Vision (if needed):** Google Gemini
- **Why:** There are many reasons why I am choosing to work with Google Gemini for all the parts of this project. It has multimodal capabiities, and with this project, the system has to be able to handle text and images directly. Gemini has proven to be good for this. It would get a little confusing having to use multiple agents in my opinion, so development will be much easier using the same agent (subject to change, though). Also, Google AI Studio provides 1 million tokens per day and 15 requests per minute - this seems pretty suffiecient for the use cases that will be in this project.

**Design Architecture**

1. Input (text or image)

2. Text extraction (OCR if needed)

3. Claim analysis

4. (Optional) Retrieval from vector store

5. LLM reasoning

6. Structured output:

  - Label
  - 3 reasons
    
