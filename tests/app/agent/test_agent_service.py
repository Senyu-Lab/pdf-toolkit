
from types import SimpleNamespace
from unittest.mock import Mock

from app.agent.agent_service import AgentService


def test_ask_returns_agent_answer():
    agent = Mock()
    agent.run.return_value = SimpleNamespace(
        answer="This PDF contains four pages."
    )

    agent_factory = Mock(return_value=agent)
    service = AgentService(agent_factory=agent_factory)

    answer = service.ask(
        pdf_path="test_data/sample.pdf",
        question="How many pages are in this PDF?",
    )

    assert answer == "This PDF contains four pages."
    agent_factory.assert_called_once_with("test_data/sample.pdf")
    agent.run.assert_called_once_with(
        "How many pages are in this PDF?"
    )


def test_create_default_agent_uses_pdf_agent(monkeypatch):
    from types import SimpleNamespace

    import pdf_agent.agent

    from app.agent.agent_service import AgentService

    created = {}

    class FakePDFAgent:
        def __init__(self, file_path, llm=None):
            created["file_path"] = file_path
            created["llm"] = llm

        def run(self, question):
            return SimpleNamespace(answer="Mock answer")

    monkeypatch.setattr(pdf_agent.agent, "PDFAgent", FakePDFAgent)

    service = AgentService()
    answer = service.ask("test_data/sample.pdf", "Summarize this PDF")

    assert answer == "Mock answer"
    assert created["file_path"] == "test_data/sample.pdf"



def test_ask_passes_llm_to_default_agent(monkeypatch):
    from types import SimpleNamespace

    import pdf_agent.agent

    from app.agent.agent_service import AgentService

    created = {}

    class FakePDFAgent:
        def __init__(self, file_path, llm=None):
            created["file_path"] = file_path
            created["llm"] = llm

        def run(self, question):
            return SimpleNamespace(answer="Mock answer")

    monkeypatch.setattr(pdf_agent.agent, "PDFAgent", FakePDFAgent)

    fake_llm = object()
    service = AgentService(llm=fake_llm)

    answer = service.ask("test_data/sample.pdf", "Summarize this PDF")

    assert answer == "Mock answer"
    assert created["file_path"] == "test_data/sample.pdf"
    assert created["llm"] is fake_llm
