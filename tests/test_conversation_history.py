import pytest
from agents import orchestrator

def test_fanuc_payload_and_followup():
    history = []

    # Turn 1: Payload
    q1 = "what is max payload of m900ia"
    expected_keywords1 = ["200 kg"]
    response1, agent1 = orchestrator(q1, history=history)
    assert agent1 == "FANUC"
    assert any(keyword in response1.lower() for keyword in expected_keywords1)
    history.append({"user": q1, "assistant": response1})

    # Turn 2: Reach (follow-up)
    q2 = "what is reach of it"
    expected_keywords2 = ["3507 mm", "3,507 mm"]
    response2, agent2 = orchestrator(q2, history=history)
    assert agent2 == "FANUC"
    assert any(keyword in response2.lower() for keyword in expected_keywords2)


def test_kuka_multi_turn_context():
    history = []

    # Turn 1: Reach
    q1 = "what is max reach of kr 1000 1300"
    expected_keywords1 = ["3202 mm", "3,202 mm"]
    response1, agent1 = orchestrator(q1, history=history)
    assert agent1 == "KUKA"
    assert any(keyword in response1.lower() for keyword in expected_keywords1)
    history.append({"user": q1, "assistant": response1})

    # Turn 2: Payload
    q2 = "what is rated payload of it"
    expected_keywords2 = ["1300 kg", "1,300 kg"]
    response2, agent2 = orchestrator(q2, history=history)
    assert agent2 == "KUKA"
    assert any(keyword in response2.lower() for keyword in expected_keywords2)
    history.append({"user": q2, "assistant": response2})

    # Turn 3: Protection
    q3 = "it has any procection classification"
    expected_keywords3 = ["ip 65", "ip 67"]
    response3, agent3 = orchestrator(q3, history=history)
    assert agent3 == "KUKA"
    assert any(keyword in response3.lower() for keyword in expected_keywords3)
