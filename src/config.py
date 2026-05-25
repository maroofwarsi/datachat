"""
Centralised configuration for DataChat.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq (free LLM API - no billing required) ──────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# Best free model on Groq: fast, smart, great at data tasks
# Alternatives (all free): "llama-3.1-8b-instant", "mixtral-8x7b-32768"
LLM_MODEL: str = "llama-3.3-70b-versatile"

# ── Agent behaviour ────────────────────────────────────────────────────────────
MAX_ITERATIONS: int = 10        # Max steps the agent takes to answer one question
TEMPERATURE: float = 0.0        # 0 = consistent, factual answers (best for data)
MAX_ROWS_PREVIEW: int = 5       # Rows shown in the data preview table

# ── Chart colours (Plotly) ────────────────────────────────────────────────────
CHART_COLOUR_SEQUENCE = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52",
    "#8172B2", "#937860", "#DA8BC3", "#8C8C8C",
]
