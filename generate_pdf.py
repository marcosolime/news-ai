import os
from weasyprint import HTML, CSS

def generate_newspaper_pdf(articles: dict, output_path: str, font="Ubuntu"):
    """
    Generate a newspaper-style PDF with 3 columns per page,
    switchable fonts (Ubuntu, Volkhov, etc.).
    """

    # --- Build font paths ---
    font_regular = f"fonts/{font}-Regular.ttf"
    font_bold = f"fonts/{font}-Bold.ttf"

    if not os.path.exists(font_regular):
        raise FileNotFoundError(f"Missing font: {font_regular}")

    if not os.path.exists(font_bold):
        raise FileNotFoundError(f"Missing font: {font_bold}")

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

    /* DYNAMIC FONT LOADING */
    @font-face {{
        font-family: '{font}';
        src: url('{font_regular}');
    }}

    @font-face {{
        font-family: '{font} Bold';
        src: url('{font_bold}');
    }}

    /* Page margins */
    @page {{
        margin: 0.3cm;
    }}

    body {{
        font-family: '{font}';
        margin: 0;
        padding: 0;
        font-size: 11px;
        line-height: 1.25;
        color: #111;
    }}

    /* 3-column layout */
    .content {{
        column-count: 3;
        column-gap: 18px;
        widows: 2;
        orphans: 2;
    }}

    #front-title {{
        text-align: center;
        font-family: '{font} Bold';
        font-size: 40px;
        margin-bottom: 10px;
        margin-top: 0;
    }}

    #pill-news {{
        background: #ededed;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
    }}

    #pill-news h3 {{
        font-family: '{font} Bold';
        margin-top: 0;
    }}

    article {{
        break-inside: auto;
        margin-bottom: 15px;
        text-align: justify;
    }}

    h2 {{
        font-family: '{font} Bold';
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
    
    # Save PDF
    HTML(string=html_content, base_url=".").write_pdf(output_path)
    print(f"PDF generated with font {font}: {output_path}")
