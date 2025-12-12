# Kasparro – Agentic Content Generation System

This project implements a **multi-agent, LangChain + LangGraph powered content generation system** for D2C skincare brands.  
The pipeline transforms raw product JSON into structured, SEO-ready JSON outputs:

- `product_page.json`
- `faq.json`
- `comparison_page.json`

using:

- LangChain LLM chains (parser, Q-generation, FAQ, product page, comparison)  
- LangGraph workflow orchestration  
- Pydantic models for strict schema enforcement  
- Automatic fictional Product B generation for comparison  

All required documentation is available in:

---

## 🚀 Features

- True multi-agent architecture using LangChain + LangGraph
- Structured JSON enforced with Pydantic models
- Automatic creation of fictional **Product B** for competitive comparison
- Deterministic + LLM-driven hybrid system
- Clean modular folder structure
- Fully compatible with the **uv** package manager

---

## 📁 Clone the Repository

```bash
git clone https://github.com/Md-Tauhid101/kasparro-ai-agentic-content-generation-system-Md-Tauhid-Ansari.git
```

---

## ▶️ Environment Setup Using **uv** (Recommended)

This project is structured to work cleanly with **uv**, a fast Python package manager and environment runner.

### 1. Install uv (if not installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

---

### 2. Create and activate a virtual environment

```bash
uv venv
```

Activate:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

---

### 3. Install project dependencies

```bash
uv sync
```

If you’re using **Groq LLM**, ensure:

```bash
uv pip install groq
```

---

### 4. Set your environment variables

If using `GroqGROQ_API_KEY` in .env file
If you are using a local LLM model, set variables required by your `llm.py`.

---

## 📥 Input Format

Save the following example as `sample_input.json`:

```json
{
  "product_name": "GlowBoost Vitamin C Serum",
  "concentration": "10% Vitamin C",
  "skin_type": ["Oily", "Combination"],
  "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
  "benefits": ["Brightening", "Fades dark spots"],
  "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
  "side_effects": "Mild tingling for sensitive skin",
  "price": "₹699"
}
```

---

## ▶️ Run the Pipeline

With uv, you can run the script directly:

```bash
uv run python src/main.py src/sample_input.json
```

Or without uv’s wrapper (if environment is activated):

```bash
python src/main.py -i src/sample_input.json
```

Outputs will appear in:

```
  faq.json
  product_page.json
  comparison_page.json
```

---

## ▶️ Programmatic Usage

You may run the pipeline from Python as well:

```python
from src.orchestrator import Orchestrator

orc = Orchestrator()
result = orc.run_pipeline({
  "product_name": "GlowBoost Vitamin C Serum",
  "concentration": "10% Vitamin C",
  "skin_type": ["Oily", "Combination"],
  "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
  "benefits": ["Brightening", "Fades dark spots"],
  "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
  "side_effects": "Mild tingling for sensitive skin",
  "price": "₹699"
})

print(result["product_page"])
```

---

## 📄 Documentation

All assignment-required documentation is located here:

```
docs/projectdocumentation.md
```

It contains:

- Problem Statement  
- Solution Overview  
- Scopes & Assumptions  
- System Design (MANDATORY)

---


