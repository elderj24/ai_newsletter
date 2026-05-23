# AI Newsletter Ingestion & Synthesis Pipeline

A Python-based weekly data pipeline that automatically aggregates, filters, synthesizes, and emails a structured digest of recent AI announcements from the industry's leading companies and tools.

## Objective
The pipeline runs weekly to curate, summarize, and synthesize news from official press releases and product blogs of:
* **Google / Gemini**
* **Anthropic**
* **OpenAI**
* **xAI**
* **Cursor**
* **Cognition**

It provides a high-value, signal-rich email summary tailored for strategic, investment, and private equity analysis.

## Mental Model & Data Pipeline
1. **Ingestion**: Weekly search and extraction of official blogs/announcements using Exa.ai's neural search engine.
2. **State & Deduplication**: Storage of parsed article URLs in a lightweight local SQLite database to prevent redundant processing.
3. **LLM Synthesis**: Synthesis of news via the Google Gemini API (using Gemini 1.5 Pro) to extract key themes, breakthroughs, and strategic implications.
4. **Delivery**: Responsive, professionally formatted HTML email delivery using Resend.
5. **Orchestration**: Automated weekly schedule powered by GitHub Actions.

## Tech Stack
* **Language**: Python 3.11+
* **Database**: SQLite (local state tracking)
* **LLM**: Google Gemini API (`google-genai` SDK)
* **Search / Ingestion API**: Exa.ai API (neural tech-focused search)
* **Email Provider**: Resend API
* **Testing Framework**: `pytest`
* **Scheduling**: GitHub Actions

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/elderj24/ai_newsletter.git
   cd ai_newsletter
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
Create a `.env` file at the root:
```env
GEMINI_API_KEY=your_gemini_api_key
EXA_API_KEY=your_exa_api_key
RESEND_API_KEY=your_resend_api_key
RECIPIENT_EMAIL=your_email@example.com
```

## Running the Pipeline
```bash
python src/main.py
```

## Running Tests
```bash
pytest
```
