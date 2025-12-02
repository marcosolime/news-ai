from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Frame, PageTemplate, BaseDocTemplate, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


# ============================================================
#  SHARED STYLES FOR BOTH LAYOUTS
# ============================================================

def get_styles():
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_LEFT,
        spaceAfter=12,
        textColor="#222222"
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor="#555555",
        spaceAfter=10,
    )

    url_style = ParagraphStyle(
        'URLStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor="#888888",
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10.5,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )

    return title_style, meta_style, url_style, body_style


# ============================================================
#  ONE-COLUMN PDF LAYOUT
# ============================================================

def create_pdf_one_column(articles: dict, filename="output/newspaper_one_column.pdf"):
    """
    Creates a beautiful single-column newspaper layout.
    """
    title_style, meta_style, url_style, body_style = get_styles()

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    story = []

    for site, art in articles.items():
        # Title
        story.append(Paragraph(art["title"], title_style))

        # Author + Date
        meta = ""
        if art["author"]:
            meta += f"<b>{art['author']}</b>"
        if art["date"]:
            meta += f" • {art['date']}"
        story.append(Paragraph(meta, meta_style))

        # URL
        story.append(Paragraph(f"<i>{art['url']}</i>", url_style))

        # Body text
        paragraphs = art["text"].split("\n\n")
        for p in paragraphs:
            if p.strip():
                story.append(Paragraph(p.strip(), body_style))

        # Separator line
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=0.7, color="#BBBBBB"))
        story.append(Spacer(1, 18))

    doc.build(story)
    print(f"📄 One-column PDF generated: {filename}")


# ============================================================
#  TWO-COLUMN NEWSPAPER LAYOUT (Corriere-style)
# ============================================================

def create_pdf_two_columns(articles: dict, filename="output/newspaper_two_columns.pdf"):
    """
    Two-column layout where:
    - The article header (title + metadata + url) is kept together
    - The body can flow naturally across columns/pages
    - New article starts in the same column unless the header wouldn't fit
    """

    title_style, meta_style, url_style, body_style = get_styles()

    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Column sizes
    column_gap = 1*cm
    frame_width = (A4[0] - doc.leftMargin - doc.rightMargin - column_gap) / 2
    frame_height = A4[1] - doc.topMargin - doc.bottomMargin

    # Create two frames
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, frame_width, frame_height, id='col1')
    frame2 = Frame(doc.leftMargin + frame_width + column_gap, doc.bottomMargin,
                   frame_width, frame_height, id='col2')

    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    doc.addPageTemplates([template])

    story = []

    for site, art in articles.items():

        # -------- HEADER BLOCK (keep together) --------
        header = []

        header.append(Paragraph(art["title"], title_style))

        meta = ""
        if art["author"]:
            meta += f"<b>{art['author']}</b>"
        if art["date"]:
            meta += f" • {art['date']}"

        if meta:
            header.append(Paragraph(meta, meta_style))

        header.append(Paragraph(f"<i>{art['url']}</i>", url_style))

        # Keep only the header together
        story.append(KeepTogether(header))

        # -------- BODY (allowed to flow across columns/pages) --------
        paragraphs = art["text"].split("\n\n")
        for p in paragraphs:
            if p.strip():
                story.append(Paragraph(p.strip(), body_style))

        # Separator between articles
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=0.7, color="#BBBBBB"))
        story.append(Spacer(1, 20))

    doc.build(story)
    print(f"📰 Two-column PDF generated: {filename}")
