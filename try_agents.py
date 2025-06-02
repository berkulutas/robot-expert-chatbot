from agents import orchestrator

# Conversation history as a list of turns
history = []

while True:
    question = input("\nAsk a robot question (or type 'exit'): ")
    if question.lower() == 'exit':
        break

    # Pass question and history to orchestrator
    response, agent = orchestrator(question, history=history)

    # Display response
    print(f"\n🤖 {agent}:\n{response}")

    # Update history
    history.append({
        "user": question,
        "assistant": response
    })
    print(history)
