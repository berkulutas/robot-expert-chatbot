from agents import orchestrator

while True:
    question = input("\nAsk a robot question (or type 'exit'): ")
    if question.lower() == 'exit':
        break
    response, agent = orchestrator(question)
    print(f"\n🤖 {agent} Agent:\n{response}")
