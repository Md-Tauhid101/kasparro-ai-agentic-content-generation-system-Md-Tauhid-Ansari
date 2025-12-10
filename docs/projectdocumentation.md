# Kasparro – Agentic Content Generation System Documentation

## Problem Statement
D2C brands require scalable, structured, high‑quality product content (FAQ pages, product pages, comparison pages). Manual creation does not scale, and traditional template-based systems fail due to product variability and inconsistent input formats. The challenge is to design an agentic system that can ingest raw product data and generate consistent structured content with minimal hallucinations and strong deterministic logic.

## Solution Overview
The system is designed as a modular multi‑agent pipeline where:
- A ParserAgent normalizes raw input into a canonical ProductModel.
- A QuestionAgent generates structured FAQs using a controlled LLM wrapper.
- An FAQPageAgent assembles FAQ pages using deterministic templates.
- A ProductPageAgent constructs structured product pages using reusable logic blocks.
- A ComparisonAgent generates a synthetic competitor and produces comparison pages.

Outputs follow strict JSON templates ensuring consistency across products. The pipeline is orchestrated using LangGraph, enabling clean branching and deterministic execution.

## Scopes & Assumptions
- Input JSON contains required product fields (name, ingredients, benefits, usage, price).
- LLM output may contain malformed JSON, so robust recovery and parsing logic is required.
- Comparison product is synthetic (no reliance on external datasets).
- No UI rendering is included—only structured JSON generation.
- Output JSON files are consumed downstream by SEO tooling, CMS systems, or formatting engines.

## System Design

### High-Level DAG
```
            Raw Input JSON
                    │
                    ▼
               ParserAgent
                    │
     ┌──────────────┼───────────────┐
     ▼              ▼               ▼
QuestionAgent   ProductPageAgent   ComparisonAgent
     │              │               │
     ▼              ▼               ▼
 FAQPageAgent   ProductPage      ComparisonPage
     │
     ▼
   FAQPage
```

### Core Architectural Principles
- **Separation of Concerns:** Agents handle orchestration logic; blocks handle deterministic
  content building; templates define final JSON structure.
- **LLM Safety:** LLM is isolated inside QuestionAgent and wrapped with JSON-recovery safeguards.
- **Deterministic Blocks:** Benefits, usage, safety, ingredients, and pricing blocks are pure functions.
- **Pydantic Models:** All major structures enforce validation and output consistency.
- **MVP Orchestrator:** A simple, linear pipeline that runs ParserAgent first, then fans out to
  FAQ, product page, and comparison generators without agent-to-agent dependency.


### Optional Diagram (Flowchart)
```
[Raw Input] → [ParserAgent]
      ├────────→ [QuestionAgent] → [FAQPageAgent] → FAQPage
      ├────────→ [ProductPageAgent] → ProductPage
      └────────→ [ComparisonAgent] → ComparisonPage
```

This design enables scalable, reliable content generation for large product catalogs with minimal human intervention.
