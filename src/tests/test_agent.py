from src.agent.graph import agent_app


# TEST 1
def test_agent_rag_flow():
    """Test autonomous RAG retrieval and generation node execution."""
    res = agent_app.invoke(
        {"question": "What is progressive overloading?", "retry_count": 0}
    )
    assert "generation" in res
    assert len(res["generation"]) > 0


# TEST 2
def test_agent_math_calculator_tool():
    """Test function-calling calculator tool routing."""
    res_math = agent_app.invoke({"question": "Calculate 1.6 * 72", "retry_count": 0})
    assert "generation" in res_math
    assert "115.2" in res_math["generation"]
