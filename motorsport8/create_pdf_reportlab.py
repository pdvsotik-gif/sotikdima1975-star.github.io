#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания PDF файла из motorsport8/index.1.html с использованием reportlab
С поддержкой русского языка
"""

import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def clean_html_text(html_content):
    """Очистить HTML от тегов и получить текст"""
    # Удаляем все HTML теги
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    # Удаляем лишние пробелы и переносы
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def extract_sections(html_content):
    """Извлечь секции из HTML"""
    sections = []

    # Разделяем по основным секциям
    section_patterns = [
        (r'<div id="guides"[^>]*>.*?</div>', 'Гайды'),
        (r'<div id="videos"[^>]*>.*?</div>', 'Видео'),
        (r'<div id="news"[^>]*>.*?</div>', 'Новости'),
        (r'<div id="tracks"[^>]*>.*?</div>', 'Трассы'),
    ]

    for pattern, title in section_patterns:
        match = re.search(pattern, html_content, re.DOTALL)
        if match:
            section_html = match.group(0)
            section_text = clean_html_text(section_html)
            sections.append((title, section_text))

    return sections

def create_pdf_from_html(html_path, output_pdf_path):
    """Создать PDF из HTML файла"""

    if not os.path.exists(html_path):
        print(f"Ошибка: HTML файл не найден - {html_path}")
        return False

    try:
        # Регистрация шрифта для поддержки русского языка
        arial_path = r'C:\Windows\Fonts\arial.ttf'
        arial_bold_path = r'C:\Windows\Fonts\arialbd.ttf'
        if os.path.exists(arial_path):
            pdfmetrics.registerFont(TTFont('Arial', arial_path))
            print("✅ Шрифт Arial зарегистрирован")
        if os.path.exists(arial_bold_path):
            pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bold_path))
            print("✅ Шрифт Arial-Bold зарегистрирован")

        # Читаем HTML файл
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Извлекаем секции
        sections = extract_sections(html_content)

        # Настройка страницы
        pagesize = A4
        page_width, page_height = pagesize

        # Создание документа
        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=pagesize,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=20*mm,
            bottomMargin=20*mm,
        )

        # Стили
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.blue,
            fontName='Arial-Bold' if 'Arial-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
        )
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            textColor=colors.darkblue,
            fontName='Arial-Bold' if 'Arial-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
        )
        normal_style = styles['Normal']
        normal_style.fontSize = 12
        normal_style.leading = 14
        normal_style.fontName = 'Arial' if 'Arial' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'

        # Создание содержимого
        story = []

        # Заголовок
        story.append(Paragraph("Forza Motorsport 8 — Гайды и разборы", title_style))
        story.append(Spacer(1, 20))

        # Секции
        for section_title, section_text in sections:
            story.append(Paragraph(section_title, section_title_style))
            story.append(Spacer(1, 10))

            # Разбиваем текст на параграфы
            paragraphs = section_text.split('\n')
            for para in paragraphs:
                para = para.strip()
                if para:
                    story.append(Paragraph(para, normal_style))
                    story.append(Spacer(1, 6))

            story.append(Spacer(1, 20))

        # Генерируем PDF
        doc.build(story)

        print(f"✅ PDF успешно создан: {output_pdf_path}")
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании PDF: {e}")
        return False

def main():
    # Пути к файлам
    script_dir = Path(__file__).parent
    html_file = script_dir / "index.1.html"
    pdf_file = script_dir / "motorsport8_pdf.pdf"

    print("🚀 Начинаем создание PDF из HTML...")

    if create_pdf_from_html(str(html_file), str(pdf_file)):
        print("🎉 PDF файл успешно создан!")
        print(f"📁 Расположение: {pdf_file}")
    else:
        print("💥 Не удалось создать PDF файл")

if __name__ == "__main__":
    main()