from typing import List

from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent

# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.agents.agent_types import AgentType
from langchain_community.llms import OpenAI

# from langchain_openai import ChatOpenAI as OpenAI
from langchain_community.utilities import SQLDatabase
from settings import (
    APP_ENV,
    DATABASE_LANGCHAIN_POOL_MAX_OVERFLOW,
    DATABASE_LANGCHAIN_POOL_SIZE,
    DATABASE_POOL_URL,
    DATABASE_URL,
)


class GPTLangSQL:
    def __init__(self, tables: List[str]):
        if not tables:
            raise ValueError("No tables provided")
        if APP_ENV == "prod":
            self.db = SQLDatabase.from_uri(
                DATABASE_POOL_URL,
                include_tables=tables,
                pool_size=DATABASE_LANGCHAIN_POOL_SIZE,
                max_overflow=DATABASE_LANGCHAIN_POOL_MAX_OVERFLOW,
            )
        else:
            self.db = SQLDatabase.from_uri(DATABASE_URL, include_tables=tables)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=OpenAI(temperature=0))
        self.agent_executor = create_sql_agent(
            llm=OpenAI(temperature=0),
            toolkit=self.toolkit,
            verbose=True,
            # agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )

    def generate(self, prompt):
        return self.agent_executor.run(prompt)
