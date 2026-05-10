"""
LangChain Pandas DataFrame Agent powered by Groq (free).

The agent can:
- Answer questions about the data in plain English
- Write and run Python/pandas code to compute answers
- Handle multi-step questions (e.g. "filter by region, then show the top 5")
- Return structured results for chart generation
"""

import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

from src.config import GROQ_API_KEY, LLM_MODEL, TEMPERATURE, MAX_ITERATIONS


AGENT_PREFIX = """You are DataChat, a friendly and precise data analyst assistant.

You have access to a pandas DataFrame called `df`. Use it to answer the user's questions.

Rules:
- Always show the actual numbers, not just code.
- For "show me", "list", or "what are" questions, print the results clearly.
- For aggregation questions (totals, averages, counts), give a direct number answer.
- Keep answers concise — one or two sentences plus the data.
- If you're unsure, say so rather than guessing.
- Format large numbers with commas (e.g. 1,234,567).
- When the user asks for a chart or graph, describe what you would plot (the code will handle the chart separately).
"""


def build_agent(df: pd.DataFrame):
    """
    Create a LangChain pandas agent backed by Groq's free LLM.

    The agent has access to the full pandas API and will write Python code
    internally to answer questions — you never need to write pandas yourself.

    Args:
        df: The loaded and cleaned DataFrame to query.

    Returns:
        A configured LangChain AgentExecutor.

    Raises:
        EnvironmentError: If GROQ_API_KEY is not set.
    """
    if not GROQ_API_KEY:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. See SETUP.md for how to get a free key."
        )

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=TEMPERATURE,
    )

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        prefix=AGENT_PREFIX,
        verbose=False,
        max_iterations=MAX_ITERATIONS,
        handle_parsing_errors=True,
        allow_dangerous_code=True,  # Required for pandas agent (runs Python locally)
    )

    return agent


def ask(agent, question: str) -> str:
    """
    Ask the agent a question and return its plain-English answer.

    Args:
        agent: Built AgentExecutor from build_agent().
        question: Natural language question about the data.

    Returns:
        The agent's answer as a string.
    """
    try:
        result = agent.invoke({"input": question})
        return result.get("output", "No answer returned.")
    except Exception as e:
        return f"I ran into an issue answering that: {str(e)}"
