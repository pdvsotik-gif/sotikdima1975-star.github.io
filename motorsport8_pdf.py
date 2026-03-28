#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


BASE_DIR = Path(__file__).resolve().parent

FONT_MONO = BASE_DIR / "DejaVuSans.ttf"
FONT_MONO_BOLD = BASE_DIR / "DejaVuSans-Bold.ttf"

FONT_URLS = {
    FONT_MONO: "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/main/ttf/DejaVuSans.ttf",
    FONT_MONO_BOLD: "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/main/ttf/DejaVuSans-Bold.ttf",
}

# === СКАЧИВАЕМ ШРИФТЫ, ЕСЛИ ИХ НЕТ ===
for path, url in FONT_URLS.items():
    if not path.exists():
        print(f"Скачиваю шрифт: {path.name}")
        urllib.request.urlretrieve(url, path)

# === РЕГИСТРАЦИЯ ===
pdfmetrics.registerFont(TTFont("DejaVuSansMono", str(FONT_MONO)))
pdfmetrics.registerFont(TTFont("DejaVuSansMono-Bold", str(FONT_MONO_BOLD)))


def read_md_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def create_pdf_with_md_code(md_code: str, output_path: str) -> None:

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="motorsport8_index.md",
        author="СайтСотика",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#007acc"),
        alignment=TA_CENTER,
        fontName="DejaVuSansMono-Bold",
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#666666"),
        alignment=TA_CENTER,
        fontName="DejaVuSansMono",
        spaceAfter=15,
    )

    code_style = ParagraphStyle(
        "Code",
        parent=styles["Normal"],
        fontSize=8.5,
        fontName="DejaVuSansMono",
        textColor=colors.HexColor("#222222"),
        leading=10,
        backColor=colors.HexColor("#f5f5f5"),
        leftIndent=4,
        spaceAfter=0,
    )

    elements = []

    elements.append(Spacer(1, 10 * mm))
    elements.append(Paragraph("📄 motorsport8_index.md", title_style))
    elements.append(Paragraph(
        f"Создано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | "
        f"Строк: {len(md_code.splitlines())}",
        subtitle_style
    ))

    code_lines = md_code.splitlines()

    def build_table(lines, start_index):
        table_data = [
            [
                Paragraph("<b>№</b>", code_style),
                Paragraph("<b>Код</b>", code_style)
            ]
        ]

        for i, line in enumerate(lines, start_index):
            esc = (
                line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )

            num = Paragraph(f"<font color='#999999'>{i:04d}</font>", code_style)
            code = Paragraph(esc, code_style)

            table_data.append([num, code])

        table = Table(table_data, colWidths=[0.8 * inch, 6.5 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f4f8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#007acc")),
            ("FONTNAME", (0, 0), (-1, 0), "DejaVuSansMono-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#f9f9f9")]),
            ("FONTNAME", (0, 1), (-1, -1), "DejaVuSansMono"),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))

        return table

    lines_per_page = 60
    total = len(code_lines)

    chunk = code_lines[:lines_per_page]
    elements.append(build_table(chunk, 1))

    remaining = code_lines[lines_per_page:]
    index = lines_per_page + 1

    while remaining:
        elements.append(PageBreak())
        chunk = remaining[:lines_per_page]
        elements.append(build_table(chunk, index))
        remaining = remaining[lines_per_page:]
        index += len(chunk)

    doc.build(elements)
    print(f"PDF создан: {output_path}")


def main():
    md_file = r"C:\Users\sotik\IdeaProjects\sotikdima1975-star.github.io\motorsport8_index.md"
    output_pdf = r"C:\Users\sotik\IdeaProjects\sotikdima1975-star.github.io\pdf_output\motorsport8_index_code.pdf"

    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    if not os.path.exists(md_file):
        print(f"Файл не найден: {md_file}")
        return

    md_code = read_md_file(md_file)
    create_pdf_with_md_code(md_code, output_pdf)


if __name__ == "__main__":
    main()
