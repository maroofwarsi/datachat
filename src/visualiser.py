"""
Automatic chart generation for DataChat.

Detects the type of question asked and generates an appropriate
Plotly chart from the DataFrame - no manual configuration needed.
"""

import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional

from src.config import CHART_COLOUR_SEQUENCE


def detect_chart_intent(question: str) -> Optional[str]:
    """
    Detect if the user's question implies a chart, and what kind.

    Returns one of: 'bar', 'line', 'pie', 'scatter', or None.
    """
    q = question.lower()

    chart_keywords = {
        "line": ["trend", "over time", "by month", "by week", "by day", "growth", "timeline"],
        "bar": ["compare", "comparison", "by region", "by product", "by category",
                "top", "bottom", "highest", "lowest", "ranking", "breakdown"],
        "pie": ["share", "proportion", "percentage", "distribution", "split"],
        "scatter": ["correlation", "relationship between", "vs", "versus"],
    }

    for chart_type, keywords in chart_keywords.items():
        if any(kw in q for kw in keywords):
            return chart_type

    # Generic chart request
    if any(w in q for w in ["chart", "graph", "plot", "visualise", "visualize", "show me"]):
        return "bar"

    return None


def auto_chart(df: pd.DataFrame, question: str) -> Optional[go.Figure]:
    """
    Generate a Plotly chart based on the question and DataFrame columns.

    Tries to intelligently pick axes based on column types and the question.

    Args:
        df: The loaded DataFrame.
        question: The user's question (used to pick chart type and columns).

    Returns:
        A Plotly Figure object, or None if no chart is appropriate.
    """
    chart_type = detect_chart_intent(question)
    if chart_type is None:
        return None

    q = question.lower()

    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    if not numeric_cols:
        return None

    # Pick the most relevant numeric column based on the question
    y_col = _pick_column(q, numeric_cols, fallback=numeric_cols[0])

    # Pick the most relevant categorical column
    x_col = _pick_column(q, cat_cols, fallback=cat_cols[0] if cat_cols else None)

    if x_col is None:
        return None

    try:
        if chart_type == "line":
            # Aggregate by x_col
            agg_df = df.groupby(x_col)[y_col].sum().reset_index()
            fig = px.line(
                agg_df, x=x_col, y=y_col,
                title=f"{y_col} over {x_col}",
                color_discrete_sequence=CHART_COLOUR_SEQUENCE,
                markers=True,
            )

        elif chart_type == "bar":
            # Check if there's a secondary grouping (e.g. by product and region)
            color_col = None
            for col in cat_cols:
                if col != x_col and col.lower() in q:
                    color_col = col
                    break

            agg_df = df.groupby(
                [x_col] + ([color_col] if color_col else [])
            )[y_col].sum().reset_index()

            fig = px.bar(
                agg_df, x=x_col, y=y_col,
                color=color_col,
                title=f"{y_col} by {x_col}",
                color_discrete_sequence=CHART_COLOUR_SEQUENCE,
                barmode="group" if color_col else "relative",
            )

        elif chart_type == "pie":
            agg_df = df.groupby(x_col)[y_col].sum().reset_index()
            fig = px.pie(
                agg_df, names=x_col, values=y_col,
                title=f"{y_col} share by {x_col}",
                color_discrete_sequence=CHART_COLOUR_SEQUENCE,
            )

        elif chart_type == "scatter":
            y2_col = _pick_column(q, [c for c in numeric_cols if c != y_col], fallback=None)
            if y2_col is None:
                return None
            fig = px.scatter(
                df, x=y_col, y=y2_col,
                color=x_col if x_col in cat_cols else None,
                title=f"{y_col} vs {y2_col}",
                color_discrete_sequence=CHART_COLOUR_SEQUENCE,
            )
        else:
            return None

        # Clean up chart styling
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="sans-serif", size=13),
            margin=dict(t=50, b=40, l=40, r=20),
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#f0f0f0")

        return fig

    except Exception:
        return None


def _pick_column(question: str, columns: list, fallback) -> Optional[str]:
    """
    Pick the most relevant column from a list based on keywords in the question.

    Tries to match column names (case-insensitive) against words in the question.
    Falls back to the provided default if no match found.
    """
    q_words = set(re.sub(r"[^a-z0-9_ ]", "", question.lower()).split())
    for col in columns:
        col_words = set(col.lower().replace("_", " ").split())
        if col_words & q_words:
            return col
    return fallback
