
# 📰 **News-AI**

An AI-powered tool that automatically fetches news articles from your favorite newspaper websites, extracts their contents, and generates summaries or AI-enhanced insights using **Open LLMs**.

The tool runs completely inside Docker and outputs a beautifully formatted PDF newspaper.

---

## 🔖 **Instructions**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/marcosolime/news-ai.git
cd news-ai
```

### 2️⃣ Edit your list of newspaper websites

Open the file:

```
sites.json
```

Add or remove websites as needed:

```json
{
    "sites": [
        "https://www.ilpost.it/",
        "https://www.ansa.it/",
        "https://www.agi.it/"
    ]
}
```

### 3️⃣ Generate your API Key (for LLM access)

Go to:
👉 [https://console.groq.com/keys](https://console.groq.com/keys)

Copy your API key.

### 4️⃣ Store your API Key

Inside the project directory, create a file named:

```
api.txt
```

Paste your API key into it (one line only).

### 5️⃣ Install Docker Desktop

Download and install from:
👉 [https://www.docker.com/](https://www.docker.com/)

Make sure Docker Desktop is **running** before continuing.

### 6️⃣ Build the Docker image

From inside the project folder:

```bash
docker build -t news-ai .
```

### 7️⃣ Run the application

You must mount a local folder to store the generated PDFs.

**Windows (PowerShell):**

```powershell
docker run -it --rm `
  -v "C:\Users\marco\news-ai\output:/app/output" `
  news-ai
```

**Linux / macOS:**

```bash
docker run -it --rm \
  -v "$(pwd)/output:/app/output" \
  news-ai
```

### 8️⃣ Done! 🚀

Your freshly generated newspaper PDF will appear in:

```
output/
```


## 🤝 **Contributing**

PRs, ideas, and suggestions are welcome.
This project is modular and designed for easy extension (AI modules, new layouts, NLP features).

---

## 📜 **License**

MIT License — free for personal and commercial use.

---
