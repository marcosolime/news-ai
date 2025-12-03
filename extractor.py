import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import trafilatura

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0 Safari/537.36"
)

def extract_top_article_url(homepage_url: str, verbose=False):
    """
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
