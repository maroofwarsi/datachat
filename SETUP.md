# Get DataChat running in 15 minutes

## Step 1 — Free Groq API key (2 min, no credit card)

1. Go to **https://console.groq.com**
2. Sign up with Google or email
3. Click **API Keys** in the left sidebar
4. Click **Create API Key**, give it a name, copy the key (starts with `gsk_`)

That's it. Groq gives you 14,400 free requests per day — more than enough.

---

## Step 2 — Install and run (10 min)

Open your terminal:

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/datachat.git
cd datachat

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Groq key
cp .env.example .env
# Open .env in any text editor and replace gsk_your_key_here with your real key

# Run the app
streamlit run app.py
```

Your browser will open at **http://localhost:8501**

---

## Step 3 — Try it

1. Click **"Load sample sales data"** in the sidebar
2. Ask: *"What is the total revenue by region?"*
3. Ask: *"Which product has the highest profit?"*
4. Ask: *"Show me revenue trend over time"* — you'll see a chart appear

Then upload your own CSV or Excel file from work and try the same thing.

---

## Step 4 — Push to GitHub (3 min)

```bash
# From inside the datachat folder:
git init
git add .
git commit -m "feat: DataChat — natural language data analyst"
git branch -M main

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/datachat.git
git push -u origin main
```

---

## Step 5 — Update your LinkedIn and CV

**CV** — Under Projects, add:
> **DataChat — Natural Language Data Analyst** | Python · LangChain · Groq (Llama 3.3) · Streamlit · Plotly
> Built an AI-powered data analysis tool that lets users query any CSV or Excel file in plain English, with automatic chart generation. No SQL or formulas required.

**LinkedIn Skills to add:**
- LangChain
- Large Language Models (LLMs)
- Groq
- AI Agents
- Streamlit

---

## Troubleshooting

**"GROQ_API_KEY is not set"** — Make sure you saved `.env` (not `.env.example`) with your key inside.

**ModuleNotFoundError** — Run `source venv/bin/activate` first, then `pip install -r requirements.txt` again.

**"Load sample sales data" gives an error** — Make sure you're running `streamlit run app.py` from inside the `datachat/` folder.
