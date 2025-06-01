import pytest
from agents import orchestrator


def test_unknown_robot_brand():
    response, agent = orchestrator("What is the reach of the ABB IRB 120?")
    
    assert agent == "Orchestrator"
    assert "only support KUKA and FANUC" in response