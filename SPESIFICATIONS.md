# Multi-Agent Robot Expert Chatbot

## Project Description

This project is a simple multi-agent chatbot system built in Python with Flask.
The chatbot can answer engineering questions about two industrial robot families by routing each question to a specialised agent:
- KUKA Agent – expert on KUKA robots (e.g. KR AGILUS KR 10 R1100).
- FANUC Agent – expert on FANUC robots (e.g. LR-Mate 200iD).

Both agents rely **only** on the official PDF manual for their model using a Retrieval-Augmented Generation (RAG) pipeline. Two short (4 pager) PDFs are shared for both Kuka and Fanuc expertise.

A central **Orchestrator** decides which agent should answer or returns a fallback message when the question is out of scope.

A complete unit-test suite must verify the chatbot’s behaviour.

Key Features:
- **KUKA Expert Agent**: Responds to questions that mention the KUKA robots (only within the information provided in the PDF document).
- **FANUC Expert Agent**: Responds to questions that mention the FANUC robots (only within the information provided in the PDF document).
- **Unknown-Robot Handling**: If the user asks about any other brand (ABB, UR, etc.) or the questions outside the scope of the PDF documents, the system replies for each case: “Sorry, I only respond to questions about KUKA and FANUC robots.” OR “Sorry, I do not have this information on Kuka (or Fanuc) in my knowledge base.”
- **Out-of-Documentation Handling**: When a question is not answered in the uploaded PDF, the agent replies: “I don’t have that information in my documentation.”
- **Optional Visual Responses (Bonus)**: If relevant, an agent may embed an image (e.g. a payload curve) encoded as base64. Pure-text answers are acceptable.
- **Conversation History**: The chatbot keeps prior messages to provide context.
- **Confidence Evaluation (Bonus)**: If the model is uncertain, it should ask the user for clarification or state its uncertainty.
- **Bonus Feature**: Confidence Evaluation: Implement a mechanism to estimate answer confidence (second agent, entropy threshold, same agent but this is not ideal). If confidence is low, the system asks for clarification or suggests involving a human engineer.

## Requirements:
- Python 3.9+
- Flask
- Any agent library (LangChain, AutoGen, CrewAI, …) or your own implementation (bonus points).
- OpenAI Python SDK (API given below)
- A vector database for RAG (FAISS, Chroma, Pinecone, Weaviate, pgvector, etc.).
- Unit tests that cover routing logic, unknown-robot handling, out-of-documentation handling, and at least one PDF-based retrieval check. Use pytest.

## API Access:

The chatbot needs access to OpenAI models. Use the token below:

API Key: 

```
AZURE_OPENAI_BASE_URL=[REDACTED]
AZURE_OPENAI_API_KEY=[REDACTED]
AZURE_OPENAI_MODEL_NAME=[REDACTED]
AZURE_OPENAI_API_VERSION=[REDACTED]
```

Embedding model API (if needed):

```
model=[REDACTED]
OPENAI_API_KEY=[REDACTED]
```

If you encounter quota issues, please contact can.gorur@bopti.ai.

## Flask Web Application:
- Endpoint: /chat
- Request Method: POST
- Input Format: JSON

```json
{"question": "What is the repeatability of the KR 10 R1100?"}
```

- Output Format: JSON

```json
{"response": "The KR 10 R1100 has a repeatability of ±0.02 mm.", "agent": "KUKA"}
```


## Example Questions and Expected Responses:
- KUKA Question:
  - **Question**: "What is the repeatability of the KR 10 R1100?"
  - **Expected Response**: The KUKA agent returns the numeric value taken from the manual.

- FANUC Question:
  - **Question**: "Show me the maximum payload curve for the LR-Mate 200iD."
  - **Expected Response**: The FANUC agent explains the curve; including an image is optional bonus.

- Unknown Robot Question:
  - **Question**: "What is the reach of the ABB IRB 120?"
  - **Expected Response**: The orchestrator replies that only KUKA and FANUC are supported.
	
- Out-of-Documentation Question:
  - **Question**: "Which gearbox is used inside the wrist of the KR 10 R1100?" (not in the manual)
  - **Expected Response**: The KUKA agent replies: “I don’t have that information in my documentation.”

- Bonus Difficult Question (Confidence Evaluation):
  - **Question**: "How should I configure the ProfiNet I/O mapping in TIA Portal when integrating the KR 10 R1100 with a Siemens S7-1500 and an external safety PLC?"
  - **Expected Response**: Since this requires user-specific setup knowledge beyond the PDF, the agent should state uncertainty and ask for the user’s input, e.g. “That depends on your exact network topology and safety requirements. Could you share your current ProfiNet configuration or preferences?”


## Project Structure

Below is the structure of the project. You can email the result.

```bash
├── app.py                  # Main Flask app
├── agents.py               # Orchestrator + agents
├── requirements.txt        # Dependencies
├── README.md               # This file
├── docs/                   # PDF manuals
└── tests/                  # Unit tests (pytest)
# They can be in the same file
    ├── test_routing.py
    ├── test_unknown_robot.py
    ├── test_out_of_doc.py
    └── run_tests.py
```
