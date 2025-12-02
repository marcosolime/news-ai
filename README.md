
📰 News-ai
This is an AI tool that automatically fetches articles from a list of URLs of newspapers and creates summaries/AI-generated contents using Open LLMs.

🔖 Intructions
- Clone/download the repository
- In the local repository, locate `sites.json` and add the list of your favourite newspaper websites 
- Genereate API key at [https://console.groq.com/keys](https://console.groq.com/keys) *(this is for accessing the LLM)*
- In the local repository, create a file named `api.txt` and paste your API key
- Install Docker Desktop [https://www.docker.com/](https://www.docker.com/) and launch it
- Build the image with `docker build -t news-ai .`
- Run the image with `docker run -it --rm -v "[\path\to\folder]\output:/app/output" news-ai` *(modify [\path\to\folder] with the absolute path of the project directory. E.g.: "C:\Users\marco\news-ai")*
- Done! 🚀 You will find your newly-created newspaper in the `output` directory

🤖 Data structure
- Data structure containing the contents of the articles

```python
    articles = {
        "https://www.website_a.com/": {
            "title": "...",
            "author": "...",
            "date": "...",
            "text": "...",
            "url": "https://..."
        },
        "https://www.website_b.org/": {
            ...
        },
        ...
    }
```
