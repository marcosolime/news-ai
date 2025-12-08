import os
from weasyprint import HTML, CSS

def generate_newspaper_pdf(articles: dict, output_path: str):
    """
    Generate a newspaper-style PDF with 3 columns per page,
    Ubuntu fonts, minimal margins, pill news, and dense layout.
    """

    # --- Load content ---
    pills_html = "<ul>"
    for url, art in articles.items():
        pills_html += f"<li>{art['pill']}</li>"
    pills_html += "</ul>"

    # --- Articles section ---
    articles_html = ""
    for url, art in articles.items():
        articles_html += f"""
        <article>
            <h2>{art['title']}</h2>
            <div class="meta">
                <span><strong>{art['author']}</strong></span> – 
                <span>{art['date']}</span> –
                <a href="{art['url']}">{art['url']}</a>
            </div>
            <p>{art['text']}</p>
        </article>
        """

    # --- Final HTML template ---
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">

<style>

    @font-face {{
        font-family: 'Ubuntu';
        src: url('fonts/Ubuntu-Regular.ttf');
    }}
    @font-face {{
        font-family: 'Ubuntu Bold';
        src: url('fonts/Ubuntu-Bold.ttf');
    }}
    @page {{
        margin: 0.3cm;
    }}

    
    body {{
        font-family: 'Ubuntu';
        margin: 0;
        padding: 0;
        font-size: 11px;
        line-height: 1.25;
        color: #111;
    }}

    /* 3 columns newspaper layout */
    .content {{
        column-count: 3;
        column-gap: 18px;
        widows: 2;
        orphans: 2;
    }}

    /* Title only on first page */
    #front-title {{
        text-align: center;
        font-family: 'Ubuntu Bold';
        font-size: 40px;
        margin-bottom: 10px;
        margin-top: 0;
    }}

    /* Pill news block */
    #pill-news {{
        background: #ededed;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
    }}

    #pill-news h3 {{
        font-family: 'Ubuntu Bold';
        margin-top: 0;
    }}

    article {{
        break-inside: auto;
        margin-bottom: 15px;
        text-align: justify;
    }}

    h2 {{
        font-family: 'Ubuntu Bold';
        font-size: 17px;
        margin-bottom: 4px;
        line-height: 1.1;
    }}

    .meta {{
        font-size: 10px;
        color: #555;
        margin-bottom: 5px;
    }}

</style>
</head>

<body>

    <div class="content">
    
        <h1 id="front-title">News AI</h1>

        <section id="pill-news">
            <h3>News Pills</h3>
            {pills_html}
        </section>

        {articles_html}

    </div>

</body>
</html>
"""
    
    # --- Save PDF ---
    HTML(string=html_content, base_url=".").write_pdf(output_path)

    print(f"PDF generated: {output_path}")