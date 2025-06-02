import pytest
from agents import orchestrator

def test_max_payload_r1000_ia_80f():
    response, agent = orchestrator("What is max payload of R-1000iA/80F?")
    assert agent == "FANUC"
    assert "80" in response

def test_max_reach_r2000_ic_210f():
    response, agent = orchestrator("What is max reach of R-2000iC/210F?")
    assert agent == "FANUC"
    assert "2655" in response

def test_mass_m410_ic_185():
    response, agent = orchestrator("Mass of M-410iC/185?")
    assert agent == "FANUC"
    assert "1330" in response or "1600" in response  # depending on interpretation of pedestal note

def test_floor_mounting_m900_ia_200p():
    response, agent = orchestrator("Does M-900iA/200P have floor?")
    assert agent == "FANUC"
    assert "No" in response or "RACK" in response

def test_payload_m900_ib_700e():
    response, agent = orchestrator("What is the max payload of M-900iB/700E?")
    assert agent == "FANUC"
    assert "700" in response

def test_reach_m900_ib_400l():
    response, agent = orchestrator("What is the reach of M-900iB/400L?")
    assert agent == "FANUC"
    assert "3704" in response

def test_mounting_r2000_ic_190s():
    response, agent = orchestrator("Does R-2000iC/190S support inverted mounting?")
    assert agent == "FANUC"
    assert "Yes" in response or "invert" in response.lower()

def test_payload_kr1000_1300():
    response, agent = orchestrator("What is the payload of KR 1000 1300 titan?")
    assert agent == "KUKA"
    assert "1300" in response

def test_reach_kr1000_1300():
    response, agent = orchestrator("What is the maximum reach of KR 1000 1300 titan?")
    assert agent == "KUKA"
    assert "3202" in response or "3,202" in response

def test_weight_kr1000_1300():
    response, agent = orchestrator("What is the weight of KR 1000 1300 titan?")
    assert agent == "KUKA"
    assert "4690" in response or "4,690" in response

def test_mounting_kr1000_1300():
    response, agent = orchestrator("Does KR 1000 1300 titan have floor mounting?")
    assert agent == "KUKA"
    assert "floor" in response.lower() or "yes" in response.lower()

def test_number_of_axes_kr1000_1300():
    response, agent = orchestrator("How many axes does KR 1000 1300 titan have?")
    assert agent == "KUKA"
    assert "5" in response

def test_repeatability_kr1000_1300():
    response, agent = orchestrator("What is the repeatability of KR 1000 1300 titan?")
    assert agent == "KUKA"
    assert "0.20" in response or "±0.20" in response

