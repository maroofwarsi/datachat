# DataChat - Talk to Your Data

Upload a CSV or Excel file and ask questions about it in plain English. It answers with text and charts - no SQL, no Excel formulas needed.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## Why I built this

I kept getting asked "can you pull this data for me?" at work - people had the spreadsheet but didn't know how to query it. This lets anyone just ask the question directly.

---

## What it looks like

Instead of writing `=SUMIF(B:B,"North",C:C)` you just ask:

> "What are the total sales by region?"

And it answers, with a chart.

Some questions I tested it with:

- "Which product made the most profit?"
- "Show me revenue trend over time"
- "Who is the top performing sales rep?"
- "Which month had the lowest sales?"
- "Compare units sold by region and product"

---

## How it works

Your question goes to a LangChain Pandas Agent. The agent uses Groq (Llama 3.3 70B) to figure out what pandas code to run, executes it against your data, and returns a plain English answer. If your question sounds like it wants a chart, it generates one automatically with Plotly.

Tech used:

- LangChain - for the pandas agent
- Groq (Llama 3.3 70B) - the LLM, free API
- Pandas - data handling
- Plotly - charts
- Streamlit - the UI

Total cost: $0

---

## Setup

**Step 1 - Get a free Groq API key**

Go to [console.groq.com](https://console.groq.com), sign up (no card needed), and create an API key. It starts with `gsk_`.

**Step 2 - Clone and install**

```bash
git clone https://github.com/maroofwarsi/datachat.git
cd datachat

py -3.11 -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

**Step 3 - Add your key**

Copy `.env.example` to `.env` and paste your Groq key in:

```
GROQ_API_KEY=gsk_your_key_here
```

**Step 4 - Run**

```bash
streamlit run app.py
```

Opens at [http://localhost:8501](http://localhost:8501). Click "Load sample sales data" to try it immediately.

---

## Project structure

```
datachat/
├── app.py              - Streamlit UI
├── src/
│   ├── agent.py        - LangChain pandas agent
│   ├── loader.py       - CSV/Excel loading
│   ├── visualiser.py   - chart generation
│   └── config.py       - settings
├── data/
│   └── sample_sales.csv
├── tests/
└── requirements.txt
```

---

## Tests

```bash
pytest tests/ -v
```

---

## Where it's useful

Anywhere you have a spreadsheet and just want a quick answer - sales data, project trackers, HR exports, budget files. Basically anything tabular.

---

## What's next

- [ ] Support for multiple files at once
- [ ] Export the conversation and charts as a PDF
- [ ] Connect directly to a database instead of uploading files
- [ ] One-click deploy to Streamlit Cloud

---

## License

MIT
