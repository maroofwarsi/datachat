"""Tests for automatic chart detection and generation."""

import pytest
import pandas as pd

from src.visualiser import detect_chart_intent, auto_chart


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Region": ["North", "South", "North", "South"],
        "Revenue": [10000, 12000, 11000, 13000],
        "Units": [50, 60, 55, 65],
    })


def test_detect_line_chart():
    assert detect_chart_intent("Show revenue trend over time") == "line"
    assert detect_chart_intent("How has revenue grown by month?") == "line"


def test_detect_bar_chart():
    assert detect_chart_intent("Compare revenue by region") == "bar"
    assert detect_chart_intent("Top 5 products by revenue") == "bar"


def test_detect_pie_chart():
    assert detect_chart_intent("What is the revenue share by region?") == "pie"
    assert detect_chart_intent("Show me the proportion of units by product") == "pie"


def test_detect_no_chart():
    assert detect_chart_intent("What is the total revenue?") is None
    assert detect_chart_intent("How many rows are there?") is None


def test_auto_chart_returns_figure(sample_df):
    fig = auto_chart(sample_df, "Compare revenue by region")
    assert fig is not None


def test_auto_chart_returns_none_for_plain_question(sample_df):
    fig = auto_chart(sample_df, "What is the total revenue?")
    assert fig is None


def test_auto_chart_line(sample_df):
    fig = auto_chart(sample_df, "Show revenue trend over time by month")
    assert fig is not None
    assert fig.layout.title.text is not None
