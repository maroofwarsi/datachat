# DataChat — Talk to Your Data in Plain English

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green)](https://python.langchain.com)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%28Free%29-orange)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Upload any CSV or Excel file and ask questions about it in plain English. No formulas. No SQL. No code.

---

## What it does

Instead of writing `=SUMIF(B:B,"North",C:C)` in Excel, you just ask:

> *"What are the total sales by region?"*

And DataChat answers instantly, with a chart.

---

## Demo

![DataChat Demo](assets/demo.gif)

**Example questions you can ask:**
- *"Which product made the most profit?"*
- *"Show me revenue trend over time"*
- *"Who is the top performing sales rep?"*
- *"What percentage of revenue came from laptops?"*
- *"Compare units sold by region and product"*
- *"Which month had the lowest sales?"*

---

## How it works

```
Your question (plain English)
        │
        ▼
  LangChain Pandas Agent
  (writes Python/pandas internally)
        │
        ▼
  Groq LLM — Llama 3.3 70B (free)
        │
        ▼
  Plain English answer + auto chart
```

The agent uses Llama 3.3 (running on Groq's free API) to understand your question, write the correct pandas code, run it against your data, and return a human-readable answer.

---

## Tech stack

| Layer | Technology | Cost |
|---|---|---|
| LLM | Llama 3.3 70B via Groq | Free |
| Agent | LangChain Pandas Agent | Free |
| Data | Pandas | Free |
| Charts | Plotly Express | Free |
| UI | Streamlit | Free |

**Total cost: £0 / €0 / $0**

---

## Quickstart

### 1. Get a free Groq API key (2 minutes)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up — no credit card required
3. Click **API Keys → Create API Key**
4. Copy the key (starts with `gsk_`)

### 2. Set up the project
```bash
git clone https://github.com/YOUR_USERNAME/datachat.git
cd datachat

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Open .env and paste your Groq key
```

### 3. Run
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) — upload any CSV or try the included sample.

---

## Project structure

```
datachat/
├── app.py                  # Streamlit UI — chat interface
├── src/
│   ├── config.py           # Model settings, constants
│   ├── loader.py           # CSV/Excel loading and cleaning
│   ├── agent.py            # LangChain pandas agent (the brain)
│   └── visualiser.py       # Auto chart generation (Plotly)
├── data/
│   └── sample_sales.csv    # Sample dataset to try immediately
├── tests/
│   ├── test_loader.py
│   └── test_visualiser.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Running tests

```bash
pytest tests/ -v
```

---

## Real-world use cases

This tool is useful anywhere you have tabular data and want quick answers:

- **Sales reporting** — compare performance across regions, products, reps
- **Project tracking** — query task lists, deadlines, status breakdowns
- **HR data** — headcount by department, leave trends, attrition
- **Finance** — budget vs actuals, cost breakdowns, monthly trends
- **Operations** — SLA performance, ticket volumes, cycle times

---

## Roadmap

- [ ] Multi-file support (join two datasets)
- [ ] Export chat history and charts as PDF report
- [ ] Natural language SQL mode for database connections
- [ ] Deploy to Streamlit Cloud (one-click sharing)

---

## License

MIT
