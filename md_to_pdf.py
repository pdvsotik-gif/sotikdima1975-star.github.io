#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для конвертации Markdown файла motorsport8_index.md в PDF
"""

import os
import markdown
from pathlib import Path
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.pdfgen import canvas
except ImportError:
    print("⚠️  Требуется установка reportlab. Устанавливаю...")
    os.system("pip install reportlab")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER


def read_md_file(file_path):
    """Прочитать Markdown файл"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def convert_md_to_pdf(md_content, output_path):
    """Конвертировать Markdown в PDF"""
    
    # Настройка страницы
    pagesize = A4
    page_width, page_height = pagesize
    
    # Создание документа
    doc = SimpleDocTemplate(
        output_path,
        pagesize=pagesize,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
        title="Forza Motorsport 8 Guide",
        author="СайтСотика",
    )
    
    # Стили
    styles = getSampleStyleSheet()
    
    # Кастомные стили
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#007acc'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=18,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#007acc'),
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'Heading3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#007acc'),
        spaceBefore=12,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#222222'),
        spaceAfter=10,
        leading=14,
        fontName='Helvetica'
    )
    
    # Преобразуем Markdown в HTML
    html_content = markdown.markdown(md_content)
    
    # Разбиваем на строки для парсинга
    lines = html_content.split('\n')
    
    # Содержимое документа
    elements = []
    
    # Ищем заголовок h1 для титульной страницы
    title = "Forza Motorsport 8"
    for line in lines:
        if line.startswith('<h1>'):
            title = line.replace('<h1>', '').replace('</h1>', '').strip()
            break
    
    # Титульная страница
    elements.append(Spacer(1, 30*mm))
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph(f"Создано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", subtitle_style))
    elements.append(PageBreak())
    
    # Основное содержимое
    current_style = normal_style
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('<h1>'):
            line = line.replace('<h1>', '').replace('</h1>', '')
            p = Paragraph(line, title_style)
            elements.append(p)
        elif line.startswith('<h2>'):
            line = line.replace('<h2>', '').replace('</h2>', '')
            p = Paragraph(line, heading2_style)
            elements.append(p)
        elif line.startswith('<h3>'):
            line = line.replace('<h3>', '').replace('</h3>', '')
            p = Paragraph(line, heading3_style)
            elements.append(p)
        elif line.startswith('<p>'):
            line = line.replace('<p>', '').replace('</p>', '')
            # Преобразуем простые теги
            line = line.replace('<strong>', '<b>').replace('</strong>', '</b>')
            line = line.replace('<em>', '<i>').replace('</em>', '</i>')
            p = Paragraph(line, normal_style)
            elements.append(p)
        elif line.startswith('<li>'):
            line = line.replace('<li>', '').replace('</li>', '')
            p = Paragraph(f"• {line}", normal_style)
            elements.append(p)
    
    # Построение PDF
    doc.build(elements)
    print(f"✅ PDF успешно создан: {output_path}")


def main():
    """Основная функция"""
    
    md_file = r"C:\\Users\\sotik\\IdeaProjects\\sotikdima1975-star.github.io\\motorsport8_index.md"
    output_pdf = r"C:\\Users\\sotik\\IdeaProjects\\sotikdima1975-star.github.io\\pdf_output\\motorsport8_guide.pdf"
    
    # Создаем папку для вывода, если она не существует
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    
    # Проверка наличия файла
    if not os.path.exists(md_file):
        print(f"❌ Ошибка: файл не найден: {md_file}")
        return
    
    print("🔄 Чтение Markdown файла...")
    md_content = read_md_file(md_file)
    
    print("📝 Создание PDF из Markdown...")
    convert_md_to_pdf(md_content, output_pdf)
    
    # Проверка создания файла
    if os.path.exists(output_pdf):
        file_size = os.path.getsize(output_pdf) / 1024  # KB
        print(f"📦 Размер PDF: {file_size:.2f} KB")
        print(f"✨ Готово! Файл: {output_pdf}")
    else:
        print("❌ Ошибка при создании PDF")

if __name__ == "__main__":
    main()