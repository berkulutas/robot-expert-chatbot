import pytest
from agents import orchestrator

def test_out_of_documentation_kuka():
    response, agent = orchestrator("Which gearbox is used inside the wrist of the KR 1000 1300?")
    
    assert agent == "KUKA"
    assert "don’t have that information" in response

def test_out_of_documentation_fanuc():
    response, agent = orchestrator("Which gearbox is used inside the wrist of the M-900iB/360E?")
    
    assert agent == "FANUC"
    assert "don’t have that information" in response