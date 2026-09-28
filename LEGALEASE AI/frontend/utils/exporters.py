from io import BytesIO

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches

from fpdf import FPDF


def format_txt(text: str) -> bytes:

    return text.encode(
        "utf-8",
        errors="replace"
    )


def format_docx(
    text: str,
    document_type: str
) -> bytes:

    document = Document()

    # Default font
    styles = document.styles

    styles["Normal"].font.name = "Times New Roman"
    styles["Normal"].font.size = Pt(12)

    # Title
    title = document.add_paragraph()

    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = title.add_run(
        document_type.upper()
    )

    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    # Content
    for line in text.splitlines():

        line = line.strip()

        if not line:
            document.add_paragraph()
            continue

        paragraph = document.add_paragraph()

        run = paragraph.add_run(line)

        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

        if (
            len(line) < 100
            and line.upper() == line
        ):
            run.bold = True

    # Footer
    section = document.sections[0]

    footer = section.footer.paragraphs[0]

    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER

    footer_run = footer.add_run(
        "Generated using LegalEase - AI-Assisted Legal Document Generator"
    )

    footer_run.font.size = Pt(8)

    output = BytesIO()

    document.save(output)

    return output.getvalue()


class LegalEasePDF(FPDF):

    def header(self):

        self.set_font(
            "Helvetica",
            "B",
            14
        )

        self.cell(
            0,
            10,
            "LegalEase",
            align="C"
        )

        self.ln(10)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "",
            8
        )

        self.cell(
            0,
            10,
            f"Page {self.page_no()}",
            align="C"
        )


def format_pdf(
    text: str,
    document_type: str
) -> bytes:

    pdf = LegalEasePDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=20
    )

    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        16
    )

    pdf.multi_cell(
        0,
        10,
        document_type.upper(),
        align="C"
    )

    pdf.ln(5)

    pdf.set_font(
        "Helvetica",
        "",
        11
    )

    for line in text.splitlines():

        line = line.strip()

        if not line:
            pdf.ln(5)
            continue

        safe_line = line.encode(
            "latin-1",
            errors="replace"
        ).decode("latin-1")

        pdf.multi_cell(
            0,
            7,
            safe_line
        )

        pdf.ln(1)

    return bytes(pdf.output())
