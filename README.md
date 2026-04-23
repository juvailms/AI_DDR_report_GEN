# AI DDR Report Generator

## Overview
This project builds an AI-powered pipeline to generate a **Detailed Diagnostic Report (DDR)** from:
- Property Inspection Reports
- Thermal Image Reports

The system extracts structured insights from unstructured documents and produces a **client-friendly report with image mapping**.

---

## Key Features
- Extracts text and images from PDF documents
- Generates image captions using BLIP model
- Combines inspection + thermal data intelligently
- Avoids duplicate observations
- Handles missing and conflicting information
- Maps relevant images to observations
- Produces structured JSON + readable Markdown report

---

## System Workflow

1. **PDF Processing**
   - Extract text and images using PyMuPDF

2. **Image Understanding**
   - Generate captions using BLIP model

3. **Data Fusion**
   - Combine inspection text + thermal data + image captions

4. **LLM Processing**
   - Structured DDR generation using LLM (LLaMA 3 via Groq)

5. **Output Generation**
   - JSON structured report
   - Markdown client-ready DDR report

---

## Tech Stack
- Python
- PyMuPDF (fitz)
- Transformers (BLIP)
- Groq API (LLaMA 3.1)
- Pydantic (data validation)

---
