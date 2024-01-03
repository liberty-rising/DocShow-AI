from typing import List

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
from settings import DATABASE_URL


class GPTLangSQL:
    def __init__(self, tables: List[str]):
        if not tables:
            raise ValueError("No tables provided")
        self.db = SQLDatabase.from_uri(DATABASE_URL, include_tables=tables)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=OpenAI(temperature=0))
        self.agent_executor = create_sql_agent(
            llm=OpenAI(temperature=0),
            toolkit=self.toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )

    def generate(self, prompt):
        return self.agent_executor.run(prompt)
