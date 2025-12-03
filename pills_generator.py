from groq import Groq
import json

def generate_news_pill(title: str, text: str, api_key: str) -> str:
    """
    Generate a short 1-sentence summary (“news pill”) using Groq LLM.
    """

    client = Groq(api_key=api_key)

    prompt = f"""
    You are a news summarization assistant.

    Given the following article title and text, produce ONE single sentence,
    very short (max 25 words), written like a newspaper highlight box.

    TITLE: {title}

    TEXT:
    {text}

    Return only the sentence, nothing else.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    pill = response.choices[0].message.content.strip()
    return pill

def truncate_text(text: str, max_chars: int = 2000) -> str:
    """
    Truncate text to max_chars, avoiding cutting in the middle of a sentence.
    """
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]

    # Try not to cut in the middle of a sentence
    last_period = truncated.rfind(".")
    if last_period > 100:  # avoid extremely short first sentence
        return truncated[:last_period + 1]

    return truncated + "..."


def generate_pills_for_all_articles(articles: dict, api_file="api.txt"):
    """
    Reads API key from api.txt, then adds a 'pill' field to each article.
    """

    # Load API key
    with open(api_file, "r", encoding="utf-8") as f:
        api_key = f.read().strip()

    # Process each article
    for site, art in articles.items():
        print(f"🧠 Generating news pill for: {art['title'][:50]}...")

        pill = generate_news_pill(
            title=art["title"],
            text=truncate_text(art["text"]),
            api_key=api_key
        )

        # Add the pill to the structure
        art["pill"] = pill

        print(f"   ✔ Pill: {pill}\n")

    return articles  # now enriched with "pill"
