from google import genai
from google.genai import types
import os

def synthesize_articles(
    tech_articles: list[dict],
    politics_articles: list[dict],
    local_articles: list[dict]
) -> str:
    """
    Groups and synthesizes the provided tech, politics, and local articles using Google Gemini 3.1 Flash-Lite.
    Returns a strategic Markdown newsletter digest.
    """
    if not tech_articles and not politics_articles and not local_articles:
        return (
            "# Weekly Digest\n\n"
            "No new articles or updates were detected over the past week in "
            "Technology, Geopolitics, or Local News (Illinois/Chicago/Naperville)."
        )
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    # Initialize the google-genai Client
    client = genai.Client(api_key=api_key)
    
    # Format articles for the LLM context by category
    context_parts = []
    
    if tech_articles:
        context_parts.append("=== CATEGORY: TECH ANNOUNCEMENTS & COMPANY UPDATES ===")
        for idx, article in enumerate(tech_articles):
            context_parts.append(
                f"--- Tech Article #{idx+1} ---\n"
                f"Company: {article.get('company', 'Unknown')}\n"
                f"Title: {article.get('title', 'No Title')}\n"
                f"URL: {article.get('url', '')}\n"
                f"Published Date: {article.get('published_date', '')}\n"
                f"Content:\n{article.get('markdown', '')}\n"
            )
            
    if politics_articles:
        context_parts.append("=== CATEGORY: GLOBAL POLITICS & GEOPOLITICS ===")
        for idx, article in enumerate(politics_articles):
            context_parts.append(
                f"--- Politics Article #{idx+1} ---\n"
                f"Title: {article.get('title', 'No Title')}\n"
                f"URL: {article.get('url', '')}\n"
                f"Published Date: {article.get('published_date', '')}\n"
                f"Content:\n{article.get('markdown', '')}\n"
            )
            
    if local_articles:
        context_parts.append("=== CATEGORY: LOCAL ILLINOIS, CHICAGO, & NAPERVILLE NEWS ===")
        for idx, article in enumerate(local_articles):
            context_parts.append(
                f"--- Local Article #{idx+1} ---\n"
                f"Location: {article.get('location', 'Illinois')}\n"
                f"Title: {article.get('title', 'No Title')}\n"
                f"URL: {article.get('url', '')}\n"
                f"Published Date: {article.get('published_date', '')}\n"
                f"Content:\n{article.get('markdown', '')}\n"
            )
            
    combined_articles_context = "\n\n".join(context_parts)
    
    system_instruction = (
        "You are an expert technology analyst, geopolitical strategist, and local community reporter.\n"
        "Your task is to synthesize a batch of recent articles into a premium, professional weekly newsletter digest in Markdown.\n\n"
        "You MUST adhere to the following structure:\n\n"
        "1. **Weekly Executive Summary**: An elegant, high-level prose analysis identifying the most critical "
        "overarching themes, strategic shifts, or trends across tech, politics, and local news.\n"
        "2. **Company Highlights**: Separate headings or bullet points for companies mentioned in the tech articles (OpenAI, Google, "
        "Anthropic, xAI, Cursor, Cognition, NVIDIA). Each highlight MUST begin with the article title formatted as a clickable markdown hyperlink "
        "linking directly to its original URL. Example: `* [GPT-4o Voice Mode](https://openai.com/...): Detailed synthesis...`\n"
        "3. **Global Politics & Geopolitics**: Concise, highly analytical synthesis of major international events and policy shifts. "
        "Each summary bullet MUST begin with the article title formatted as a clickable markdown hyperlink linking directly to its original URL.\n"
        "4. **Local Briefing (Illinois, Chicago, Naperville)**: Structured local news briefings grouped under clear subheadings "
        "for **Illinois**, **Chicago**, and **Naperville** based on the location. "
        "Each summary bullet MUST begin with the article title formatted as a clickable markdown hyperlink linking directly to its original URL.\n\n"
        "If a section has no articles in the context, do not generate it at all (omit the section and heading entirely).\n"
        "Maintain a highly professional, objective, analytical, and insightful tone. Avoid buzzwords and fluffy marketing speech."
    )
    
    prompt = (
        f"Here are the raw articles collected from various sources over the past week:\n\n"
        f"{combined_articles_context}\n\n"
        f"Please synthesize these into the Weekly Digest newsletter."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
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

