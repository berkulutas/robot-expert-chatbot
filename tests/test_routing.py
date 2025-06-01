import pytest
from agents import orchestrator


def test_kuka_routing():
    # Simulate routing decision
    response, agent = orchestrator("What is the repeatability of the KR 1000 1300?")
    assert agent == "KUKA"


def test_fanuc_routing():
    # Simulate routing decision
    response, agent = orchestrator("Show me the maximum payload curve for the LR-Mate 200iD.")
    assert agent == "FANUC"