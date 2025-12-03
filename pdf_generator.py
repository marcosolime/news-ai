from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm


# ------------------------------------------------------
#  SHARED STYLES
# ------------------------------------------------------

def get_styles():
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=styles["Title"],
        fontSize=32,
        alignment=TA_CENTER,
        spaceAfter=24,
        textColor="#222222",
    )

    pill_title_style = ParagraphStyle(
        "PillTitle",
        parent=styles["Heading2"],
        fontSize=18,
        textColor="#aa0000",
        spaceAfter=12,
    )

    pill_item_style = ParagraphStyle(
        "PillItem",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        leftIndent=12,
        spaceAfter=6,
    )

    title_style = ParagraphStyle(
        "ArticleTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        spaceAfter=12,
        alignment=TA_LEFT,
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontSize=9,
        textColor="#666666",
        spaceAfter=8,
    )

    url_style = ParagraphStyle(
        "URLStyle",
        parent=styles["Normal"],
        fontSize=8,
        textColor="#888888",
        spaceAfter=12,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=14.5,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )

    return (
        header_style,
        pill_title_style,
        pill_item_style,
        title_style,
        meta_style,
        url_style,
        body_style,
    )


# ------------------------------------------------------
#  PDF GENERATOR
# ------------------------------------------------------

def create_news_pdf(articles: dict, filename="news_ai.pdf"):
    """
    Produces a newspaper-style PDF:
    - Title header: 'News-AI'
    - News pills (bullet list)
    - Two-column layout for articles
    """

    (
        header_style,
        pill_title_style,
        pill_item_style,
        title_style,
        meta_style,
        url_style,
        body_style,
    ) = get_styles()

    # Base document
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # Columns
    column_gap = 1 * cm
    frame_width = (A4[0] - doc.leftMargin - doc.rightMargin - column_gap) / 2
    frame_height = A4[1] - doc.topMargin - doc.bottomMargin

    frame1 = Frame(doc.leftMargin, doc.bottomMargin, frame_width, frame_height, id="col1")
    frame2 = Frame(
        doc.leftMargin + frame_width + column_gap,
        doc.bottomMargin,
        frame_width,
        frame_height,
        id="col2",
    )

    template = PageTemplate(id="TwoCol", frames=[frame1, frame2])
    doc.addPageTemplates([template])

    story = []

    # ------------------------------------------------------
    #  HEADER
    # ------------------------------------------------------
    story.append(Paragraph("News-AI", header_style))
    story.append(Spacer(1, 12))

    # ------------------------------------------------------
    #  NEWS PILLS — bullet list
    # ------------------------------------------------------
    story.append(Paragraph("News Pills", pill_title_style))
    story.append(Spacer(1, 6))

    for site, art in articles.items():
        pill_text = art.get("pill", "").strip()
        if pill_text:
            bullet = f"• {pill_text}"
            story.append(Paragraph(bullet, pill_item_style))
            story.append(Spacer(1, 4))

    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="100%", color="#cccccc", thickness=1))
    story.append(Spacer(1, 18))

    # ------------------------------------------------------
    #  ARTICLES (two-column flowing content)
    # ------------------------------------------------------

    for site, art in articles.items():

        # HEADER BLOCK (kept together)
        header_block = [
            Paragraph(art["title"], title_style)
        ]

        meta = ""
        if art["author"]:
            meta += f"<b>{art['author']}</b>"
        if art["date"]:
            if meta:
                meta += " • "
            meta += art["date"]

        if meta:
            header_block.append(Paragraph(meta, meta_style))

        header_block.append(Paragraph(f"<i>{art['url']}</i>", url_style))

        story.append(KeepTogether(header_block))

        # BODY paragraphs
        for p in art["text"].split("\n\n"):
            if p.strip():
                story.append(Paragraph(p.strip(), body_style))

        # Separator between articles
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", color="#bbbbbb", thickness=0.8))
        story.append(Spacer(1, 20))

    # Build PDF
    doc.build(story)
    print(f"📄 PDF generated: {filename}")
