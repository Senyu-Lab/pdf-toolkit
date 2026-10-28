
from pathlib import Path

import pdf_agent.agent


class AgentService:
    def __init__(self, agent_factory=None, llm=None):
        self.agent_factory = agent_factory or pdf_agent.agent.PDFAgent
        self.llm = llm


    def ask(self, pdf_path: str | Path, question: str) -> str:
        if self.llm is None:
            agent = self.agent_factory(str(pdf_path))
        else:
            agent = self.agent_factory(str(pdf_path), llm=self.llm)

        result = agent.run(question)
        return result.answer

