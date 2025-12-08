import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import trafilatura
from groq import Groq

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0 Safari/537.36"
)

def extract_top_article_url(homepage_url: str, verbose=False):
    """
    **DEPRECATED**

    From the website url, it extracts the url of the top article
    """
    try:
        html = requests.get(homepage_url, headers={"User-Agent": UA}, timeout=10).text

    except Exception as e:
        print("Download error:", e)
        return None

    soup = BeautifulSoup(html, "html.parser")
    candidates = []

    # look for article tag
    for art in soup.find_all("article"):
        a = art.find("a", href=True)
        if a and len(a.text.strip()) > 30:
            candidates.append((80, a["href"], a.text.strip()))

    # look for h1 h2 h3 tags
    for tag in ["h1", "h2", "h3"]:
        for h in soup.find_all(tag):
            a = h.find("a", href=True)
            if a and len(a.text.strip()) > 30:
                score = 70 if tag == "h1" else 60
                candidates.append((score, a["href"], a.text.strip()))

    # look for a tag with long length
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if len(text) > 40:
            candidates.append((50, a["href"], text))

    if not candidates:
        print(f"No article links found in {homepage_url}.")
        return None

    # order by score (high-low) and get first
    candidates.sort(key=lambda x: x[0], reverse=True)
    best = candidates[0]
    score, href, title = best

    # make absolute url
    absolute_url = urljoin(homepage_url, href)

    if verbose:
        print(f"Found {len(candidates)} candidates")
        print(f"Best candidate: {title[:60]}...")
        print(f"Url: {absolute_url}")

    return absolute_url

def extract_top_k_article_urls(homepage_url: str, k: int = 5, verbose=False):
    """
    Extracts the top-k candidate article URLs
    Each item is a dict: {"score": int, "url": str, "title": str}.
    """

    try:
        html = requests.get(homepage_url, headers={"User-Agent": UA}, timeout=10).text
    except Exception as e:
        print("Download error:", e)
        return []

    soup = BeautifulSoup(html, "html.parser")
    candidates = []

    # ARTICLE TAG
    for art in soup.find_all("article"):
        a = art.find("a", href=True)
        if a and len(a.text.strip()) > 30:
            candidates.append({
                "score": 80,
                "url": urljoin(homepage_url, a["href"]),
                "title": a.text.strip(),
            })

    # H1, H2, H3
    for tag in ["h1", "h2", "h3"]:
        for h in soup.find_all(tag):
            a = h.find("a", href=True)
            if a and len(a.text.strip()) > 30:
                score = 70 if tag == "h1" else 60
                candidates.append({
                    "score": score,
                    "url": urljoin(homepage_url, a["href"]),
                    "title": a.text.strip(),
                })

    # LONG A TAGS
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if len(text) > 40:
            candidates.append({
                "score": 50,
                "url": urljoin(homepage_url, a["href"]),
                "title": text,
            })

    if not candidates:
        if verbose:
            print(f"No article links found in {homepage_url}")
        return []

    # Sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)

    if verbose:
        print(f"Found {len(candidates)} candidates in {homepage_url}")
        for i, c in enumerate(candidates[:k]):
            print(f"{i})", c["title"][:70], "...", f"(score={c['score']})")

    return candidates[:k]

def choose_best_article(titles, client, verbose=False):
    """
    Given a list of titles, returns an integer selecting which one is most newsworthy.
    """

    # Build list of titles in the prompt
    titles_text = "\n".join(f"{i}. {t}" for i, t in enumerate(titles))

    prompt = f"""
    You are a professional news editor.

    Given a list of article headlines, select which one 
    is the MOST important and newsworthy. 
    Respond ONLY with a single number (0,1,2,...).
    No explanation. Just the number.

    TITLES:
    {titles_text}
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=3
        )

        answer = response.choices[0].message.content.strip()

        if verbose:
            print(f"LLM selected article {answer}.")

        # try to parse integer
        idx = int(answer)
        if 0 <= idx < len(titles):
            return idx

    except Exception as e:
        print("LLM error:", e)

    # fallback
    return 0

def extract_best_article_url(homepage_url, k, client, verbose=False):
    """
    1. Extract top-k candidate article URLs from homepage.
    2. Ask LLM to choose which is most important.
    3. Return the chosen URL.
    """
    candidates = extract_top_k_article_urls(homepage_url, k, verbose=verbose)
    if not candidates:
        return None

    titles = [c["title"] for c in candidates]

    best_idx = choose_best_article(titles, client, verbose=verbose)
    best = candidates[best_idx]

    if verbose:
        print(f"LLM selected index {best_idx}: {best['title'][:80]}...")

    return best["url"]

def extract_article(url: str):
    """
    Extracts title, author, date, text and url from a news article page.
    Uses trafilatura for robust extraction.
    """

    # download the page
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print(f"Could not download article: {url}")
        return None

    # extract structured info
    data = trafilatura.extract(downloaded, 
                               include_comments=False,
                               include_formatting=False,
                               include_tables=False,
                               with_metadata=False)  # metadata (header)
    if not data:
        print(f"Could not parse article: {url}")
        return None

    #breakpoint()

    # convert to dict
    result = trafilatura.metadata.extract_metadata(downloaded)
    
    # Prepare return dictionary
    article = {
        "title": result.title if result and result.title else "",
        "author": result.author if result and result.author else "",
        "date": result.date if result and result.date else "",
        "text": data,
        "url": url
    }

    # Ensure non-null values
    for k, v in article.items():
        if v is None:
            article[k] = ""

    return article
