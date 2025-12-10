import json
from groq import Groq
from extractor import extract_best_article_url, extract_article
from pills_generator import generate_pills_for_all_articles
#from pdf_generator import create_news_pdf
from generate_pdf import generate_newspaper_pdf

def load_sites(path="sites.json"):
    """Load the list of sites from json."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("sites", [])

def debug_print_articles(articles: dict, limit=400):
    print("\n===== DEBUG: EXTRACTED ARTICLES =====\n")

    for i, (site, art) in enumerate(articles.items(), start=1):
        print(f"--- 📰 ARTICLE {i} ({site}) ---")
        print(f"🔖 Title    : {art['title']}")
        print(f"🧑 Author   : {art['author']}")
        print(f"📅 Date     : {art['date']}")
        print(f"🔗 URL      : {art['url']}")
        print(f"💊 Pill (AI): {art['pill']}")
        print("")
        print(f"Text (limit {limit} chars):")
        print(art['text'][:limit] + "...")
        print("\n------------------------------------\n")

def main():
    # load the api key and create client
    api_key = open("api.txt").read().strip()
    client = Groq(api_key=api_key)
    print("Groq client initialized.")

    sites = load_sites()
    print(f"Found {len(sites)} sites to be processed.")
    
    articles = {}
    
    for site in sites:
        print(f"\n==============================================")
        print(f"Processing site: {site}")
        print("==============================================\n")

        # step 1: find top article
        #url_article = extract_top_article_url(site, verbose=False)
        url_article = extract_best_article_url(site, k=20, client=client, verbose=True)
        if not url_article:
            print(f"Unable to find top article from {site}")
            continue

        print(f"✅ URL top article found: {url_article}")
        
        # step 2: extract contents
        data = extract_article(url_article)
        if not data:
            print(f"Impossible to extract contents from: {url_article}")
            continue

        print(f"✅ Content successfully extracted.")

        # store in dictionary
        articles[site] = data
    
    # enrich with new-pills
    articles = generate_pills_for_all_articles(articles, client)

    print("Generating PDF...")
    #create_news_pdf(articles, "output/newspaper.pdf")
    generate_newspaper_pdf(articles, "output/newspaper.pdf", font="Volkhov")
    print("DONE!")
    
    debug_print_articles(articles)
    
if __name__ == "__main__":
    main()