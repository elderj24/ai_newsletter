# Developer Handbook: AI Newsletter Pipeline

This document tracks project state, conventions, architectural decisions, and tasks for the AI Newsletter project.

## Project Metadata
* **Owner**: JD Elder (Tilia LLC)
* **Goal**: Automatic ingestion, LLM synthesis, and email delivery of weekly AI news from specific providers.
* **Status**: Completed. All codebase modules written, unit-tested (8/8 passing tests), and GitHub Actions workflow configured.

---

## Architectural Decisions
1. **Language & Tooling**: Python was selected for its robust data parsing libraries, excellent integration with the new Google `google-genai` SDK, and easy testability via `pytest`.
2. **Ingestion via Exa.ai**: Exa was selected over building custom web scrapers. Scrapers are notoriously brittle and prone to breaking whenever Google, Anthropic, or OpenAI change their website layouts. Exa offers a clean domain-scoped API search that fetches recent URLs along with pre-cleaned, scrape-ready markdown.
3. **Synthesis via Gemini API**: We will utilize the Gemini API, specifically leveraging Gemini 1.5 Pro to synthesize large text batches with its extensive context window.
4. **State Storage (SQLite)**: A small, single-table SQLite database will track previously sent URLs (`url`, `title`, `published_date`, `sent_at`) to ensure we do not email duplicate articles week-over-week.
5. **Delivery via Resend**: Resend provides a clean developer API and modern Python client. It renders HTML emails beautifully and provides a robust free tier.
6. **Orchestration**: A weekly GitHub Actions cron job will run the pipeline, keeping the architecture entirely serverless and free to host.

---

## Conventions & Rules
* **Virtual Environment**: Always run within a Python virtual environment (`.venv`). Do not install packages globally.
* **Testing**: Write unit tests using `pytest` for all ingestion, synthesis, database state management, and email formatting functions.
* **Coding Style**: Asynchronous code (`async/await`) where appropriate, prioritizing clean, self-documenting code over clever hacks.
* **Error Handling**: Build defensive, resilient code. Do not write happy-path-only logic. Scraping or API failures must be gracefully caught, logged, and skipped/retried without crashing the entire pipeline.
* **Structure**: Maintain a clean, flat directory layout:
  ```text
  ai_newsletter/
  ├── .github/
  │   └── workflows/
  │       └── weekly_newsletter.yml
  ├── src/
  │   ├── __init__.py
  │   ├── ingestion.py      # Article retrieval
  │   ├── database.py       # SQLite state tracking
  │   ├── synthesis.py      # LLM prompt and aggregation
  │   ├── delivery.py       # Resend email builder
  │   └── main.py           # Pipeline entry point
  ├── tests/
  │   ├── test_ingestion.py
  │   ├── test_database.py
  │   ├── test_synthesis.py
  │   └── test_delivery.py
  ├── .env.template
  ├── .gitignore
  ├── GEMINI.md
  └── README.md
  ```
* **Guardrails**:
  * Never commit or push to Git without explicit user approval.
  * Never install packages or overwrite files without asking.
  * Present a structured plan before making changes.

---

## To-Do List & Next Steps

1. `[x]` **Repository Setup**
   - Create `.gitignore` to ignore `.venv`, `.env`, SQLite databases (`*.db`), and cache files.
   - Initial commit of project configuration and documentation files (pending approval).
2. `[x]` **Virtual Environment & Dependencies**
   - Create `.venv` locally.
   - Create `requirements.txt` with `google-genai`, `exa-py`, `resend`, `python-dotenv`, `pytest`, `pytest-asyncio`, and `httpx`.
3. `[x]` **Database & State Implementation**
   - Build `src/database.py` to initialize SQLite and manage deduplication.
   - Implement unit tests in `tests/test_database.py`.
4. `[x]` **Ingestion Module**
   - Build `src/ingestion.py` using Exa API to query target domains.
   - Implement unit tests in `tests/test_ingestion.py`.
5. `[x]` **Synthesis Module**
   - Build `src/synthesis.py` integrating the Gemini API.
   - Write targeted prompts for summarizing and synthesizing company updates.
   - Implement unit tests in `tests/test_synthesis.py`.
6. `[x]` **Delivery Module**
   - Build `src/delivery.py` integrating the Resend API to send HTML digests.
   - Implement unit tests in `tests/test_delivery.py`.
7. `[x]` **Pipeline Main Entry & GitHub Actions**
   - Assemble modules in `src/main.py`.
   - Setup `.github/workflows/weekly_newsletter.yml` to trigger the pipeline weekly.
