#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания PDF файла с кодом motorsport8_index.md
с красивым форматированием и поддержкой кириллицы
"""

import os
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# === НАСТРОЙКА ШРИФТОВ С КИРИЛЛИЦЕЙ ===

BASE_DIR = Path(__file__).resolve().parent

# Положи эти файлы рядом со скриптом или поправь путь
FONT_MONO = BASE_DIR / "DejaVuSansMono.ttf"
FONT_MONO_BOLD = BASE_DIR / "DejaVuSansMono-Bold.ttf"

if not FONT_MONO.exists() or not FONT_MONO_BOLD.exists():
    raise FileNotFoundError(
        f"Не найдены шрифты DejaVuSansMono*.ttf рядом со скриптом: "
        f"{FONT_MONO} / {FONT_MONO_BOLD}"
    )

pdfmetrics.registerFont(TTFont("DejaVuSansMono", str(FONT_MONO)))
pdfmetrics.registerFont(TTFont("DejaVuSansMono-Bold", str(FONT_MONO_BOLD)))


def read_md_file(file_path: str) -> str:
    """Прочитать Markdown файл"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def create_pdf_with_md_code(md_code: str, output_path: str) -> None:
    """Создать PDF с кодом Markdown"""

    pagesize = A4

    doc = SimpleDocTemplate(
        output_path,
        pagesize=pagesize,
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="motorsport8_index.md",
        author="СайтСотика",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#007acc"),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="DejaVuSansMono-Bold",
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#666666"),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName="DejaVuSansMono",
    )

    code_style = ParagraphStyle(
        "Code",
        parent=styles["Normal"],
        fontSize=8.5,
        fontName="DejaVuSansMono",
        textColor=colors.HexColor("#222222"),
        leftIndent=4,
        spaceAfter=0,
        leading=10,
        backColor=colors.HexColor("#f5f5f5"),
    )

    elements = []

    # Заголовок
    elements.append(Spacer(1, 10 * mm))
    elements.append(Paragraph("📄 motorsport8_index.md", title_style))
    elements.append(Spacer(1, 3 * mm))

    file_info = (
        f"Создано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | "
        f"Строк: {len(md_code.splitlines())}"
    )
    elements.append(Paragraph(file_info, subtitle_style))
    elements.append(Spacer(1, 8 * mm))

    code_lines = md_code.splitlines()

    def build_table(lines, start_index: int) -> Table:
        table_data = []
        table_data.append(
            [
                Paragraph("<b>№</b>", code_style),
                Paragraph("<b>Код</b>", code_style),
            ]
        )

        for i, line in enumerate(lines, start_index):
            # Экранируем спецсимволы
            esc = (
                line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            # Номер строки
            line_num_para = Paragraph(
                f"<font color='#999999'>{i:04d}</font>", code_style
            )

            # Без обрезки — пусть переносит по словам/символам
            code_para = Paragraph(esc, code_style)

            table_data.append([line_num_para, code_para])

        table = Table(table_data, colWidths=[0.8 * inch, 6.5 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f4f8")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#007acc")),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("ALIGN", (1, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "DejaVuSansMono-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f9f9f9")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#f9f9f9")],
                    ),
                    ("FONTNAME", (0, 1), (-1, -1), "DejaVuSansMono"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]
            )
        )
        return table

    lines_per_page = 60
    total_lines = len(code_lines)

    # Первая страница
    first_chunk = code_lines[:lines_per_page]
    elements.append(build_table(first_chunk, 1))

    # Остальные страницы
    if total_lines > lines_per_page:
        remaining = code_lines[lines_per_page:]
        start = lines_per_page + 1

        while remaining:
            elements.append(PageBreak())
            chunk = remaining[:lines_per_page]
            elements.append(build_table(chunk, start))
            remaining = remaining[lines_per_page:]
            start += len(chunk)

    doc.build(elements)
    print(f"✅ PDF успешно создан: {output_path}")
    print(f"📊 Статистика: {total_lines} строк кода")


def main():
    md_file = r"C:\Users\sotik\IdeaProjects\sotikdima1975-star.github.io\motorsport8_index.md"
    output_pdf = r"C:\Users\sotik\IdeaProjects\sotikdima1975-star.github.io\pdf_output\motorsport8_index_code.pdf"

    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    if not os.path.exists(md_file):
        print(f"❌ Ошибка: файл не найден: {md_file}")
        return

    print("🔄 Чтение Markdown файла...")
    md_code = read_md_file(md_file)

    print("📝 Создание PDF с кодом Markdown...")
    create_pdf_with_md_code(md_code, output_pdf)

    if os.path.exists(output_pdf):
        file_size = os.path.getsize(output_pdf) / 1024
        print(f"📦 Размер PDF: {file_size:.2f} KB")
        print(f"✨ Готово! Файл: {output_pdf}")
    else:
        print("❌ Ошибка при создании PDF")


if __name__ == "__main__":
    main()
