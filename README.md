# Kasparro – Agentic Content Generation System

This repository contains a modular, agent-driven pipeline that generates structured product content for D2C brands. The system transforms raw product JSON into:

- **Product Page JSON**
- **FAQ Page JSON**
- **Comparison Page JSON**

using deterministic content blocks, Pydantic models, and a controlled LLM wrapper.

All in-depth documentation lives in:

```
docs/projectdocumentation.md
```

---

## 🚀 Features

- Modular multi-agent architecture (Parser, FAQ, Product Page, Comparison)
- Deterministic logic blocks for reliable structure
- Robust LLM JSON recovery
- Simple MVP orchestrator (no LangGraph)
- Clean JSON output for downstream SEO/CMS systems
- Fully compatible with **uv** package manager

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
python src/main.py src/sample_input.json
```

Outputs will appear in:

```
output/
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


