from src.services.qa_service import answer_question


def test_answer_question_structure():
    qestion = "What is progressive overload?"
    result = answer_question(qestion, top_k=2)

    assert isinstance(result, dict)

    assert "question" in result
    assert "answer" in result
    assert "sources" in result

    assert result["question"] == qestion
    assert len(result["answer"]) > 0
    assert len(result["sources"]) <= 2


def test_answer_question_sources_for_mat():
    result = answer_question("tmux keybindings", top_k=2)
    if result["sources"]:
        source_item = result["sources"][0]

        assert "source" in source_item
        assert "similarity" in source_item
        assert isinstance(source_item["similarity"], float)
