from google import genai
from google.genai import types
import os

def synthesize_articles(articles: list[dict]) -> str:
    """
    Groups and synthesizes the provided articles using Google Gemini 1.5 Pro.
    Returns a strategic Markdown newsletter digest.
    """
    if not articles:
        return (
            "# Tilia AI Digest\n\n"
            "No new corporate announcements or product updates were detected from "
            "Google, OpenAI, Anthropic, xAI, Cursor, or Cognition over the past week."
        )
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    # Initialize the new google-genai Client
    client = genai.Client(api_key=api_key)
    
    # Format articles for the LLM context
    context_parts = []
    for idx, article in enumerate(articles):
        context_parts.append(
            f"--- Article #{idx+1} ---\n"
            f"Company: {article.get('company', 'Unknown')}\n"
            f"Title: {article.get('title', 'No Title')}\n"
            f"URL: {article.get('url', '')}\n"
            f"Published Date: {article.get('published_date', '')}\n"
            f"Content:\n{article.get('markdown', '')}\n"
        )
    combined_articles_context = "\n\n".join(context_parts)
    
    system_instruction = (
        "You are an expert Principal AI Researcher and private equity investment analyst at Tilia LLC.\n"
        "Your task is to synthesize a batch of recent corporate announcements and product updates from the "
        "following key companies: Google Gemini, OpenAI, Anthropic, xAI, Cursor, and Cognition.\n\n"
        "Draft a premium, professional weekly newsletter digest in Markdown tailored for private equity "
        "partners. You MUST adhere to the following structure:\n\n"
        "1. **Executive Summary**: An elegant, high-level prose analysis identifying the 2-3 most critical "
        "overarching industry trends and themes from the week's announcements. Highlight the strategic shift in the market.\n"
        "2. **Company Highlights**: Separate headings for each company mentioned in the articles (OpenAI, Google, "
        "Anthropic, xAI, Cursor, Cognition). For each company, provide highly-informative bulleted highlights. "
        "Crucially: Each highlight MUST begin with the article title formatted as a clickable markdown hyperlink "
        "linking directly to its original URL. For example: `* [GPT-4o Voice Mode Released](https://openai.com/...): Detailed synthesis of what this means...`\n"
        "3. **Strategic & Investment Takeaways**: Deep strategic commentary focusing on:\n"
        "   - **API Economics & Costs**: Impact of new models on developer pricing and API efficiency.\n"
        "   - **Developer Experience (DX) & Velocity**: How these updates change coding workflows or developer tooling.\n"
        "   - **Tilia PE Perspective**: Strategic implications for private equity deal sourcing, software portfolio "
        "company operations, and potential cost reduction/automation opportunities in mid-market businesses.\n\n"
        "Maintain a highly professional, objective, analytical, and investment-oriented tone. Avoid buzzwords and fluffy marketing speech."
    )
    
    prompt = (
        f"Here are the raw articles collected from official blogs and announcements over the past week:\n\n"
        f"{combined_articles_context}\n\n"
        f"Please synthesize these into the strategic Tilia AI Digest weekly newsletter."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3  # Focus on highly analytical and structured response
            )
        )
        return response.text or "Error: Generation returned empty text."
    except Exception as e:
        print(f"Error during Gemini synthesis: {e}")
        raise e
