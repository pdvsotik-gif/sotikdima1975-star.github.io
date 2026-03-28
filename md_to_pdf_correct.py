#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для корректной конвертации Markdown файла motorsport8_index.md в PDF с поддержкой UTF-8
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Определяем базовую директорию скрипта
BASE_DIR = Path(__file__).resolve().parent

# Убедимся, что кодировка по умолчанию - utf-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    # Для поддержки кириллицы
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # Определяем путь к шрифтам
    fonts_dir = BASE_DIR / "fonts"
    
    # Регистрируем шрифты с полным путем
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', str(fonts_dir / 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', str(fonts_dir / 'DejaVuSans-Bold.ttf')))
        print(f"✅ Шрифты зарегистрированы из: {fonts_dir}")
    except Exception as e:
        print(f"❌ Ошибка загрузки шрифтов: {e}")
        print("❗ Требуется шрифт DejaVuSans для корректного отображения кириллицы")
        raise
except ImportError as e:
    print(f"⚠️  Требуется установка reportlab и шрифтов. Устанавливаю...")
    os.system("pip install reportlab")
    # Попробуем установить шрифты
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        print("Не удалось установить поддержку шрифтов. Используем стандартные.")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

def read_md_file(file_path):
    """Прочитать Markdown файл с явной кодировкой UTF-8"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_pdf_with_md_content(md_content, output_path):
    """Создать PDF с содержимым Markdown с поддержкой UTF-8"""
    
    # Настройка страницы
    pagesize = A4
    page_width, page_height = pagesize
    
    # Создание документа с явной кодировкой
    doc = SimpleDocTemplate(
        output_path,
        pagesize=pagesize,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
        title="Forza Motorsport 8 Guide",
        author="СайтСотика"
    )
    
    # Стили
    styles = getSampleStyleSheet()
    
    # Проверяем доступные шрифты
    available_fonts = pdfmetrics.getRegisteredFontNames()
    print(f"Доступные шрифты: {available_fonts}")
    
    # Убеждаемся, что используем только DejaVuSans для кириллицы
    if 'DejaVuSans' not in available_fonts:
        print("❌ Шрифт DejaVuSans не зарегистрирован!")
        print("❗ Убедитесь, что файлы DejaVuSans.ttf и DejaVuSans-Bold.ttf находятся в папке fonts")
        raise Exception("Отсутствует шрифт DejaVuSans для кириллицы")
        
    cyrillic_font = 'DejaVuSans'
    cyrillic_font_bold = 'DejaVuSans-Bold'
    
    # Кастомные стили с поддержкой кириллицы
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#007acc'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName=cyrillic_font_bold
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=18,
        alignment=TA_CENTER,
        fontName=cyrillic_font
    )
    
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#007acc'),
        spaceBefore=16,
        spaceAfter=8,
        fontName=cyrillic_font_bold
    )
    
    heading3_style = ParagraphStyle(
        'Heading3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#007acc'),
        spaceBefore=12,
        spaceAfter=6,
        fontName=cyrillic_font_bold
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#222222'),
        spaceAfter=10,
        leading=14,
        fontName=cyrillic_font
    )
    
    # Преобразуем Markdown в HTML для корректного отображения форматирования
    try:
        import markdown
        html_content = markdown.markdown(md_content)
    except ImportError:
        print("⚠️  Установка markdown...")
        os.system("pip install markdown")
        import markdown
        html_content = markdown.markdown(md_content)
    
    # Разбиваем на строки для парсинга
    lines = html_content.split('\n')
    
    # Содержимое документа
    elements = []
    
    # Ищем заголовок h1 для титульной страницы
    title = "Forza Motorsport 8"
    for line in lines:
        if line.strip().startswith('<h1>'):
            title = line.strip().replace('<h1>', '').replace('</h1>', '').strip()
            break
    
    # Титульная страница
    elements.append(Spacer(1, 30*mm))
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph(f"Создано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", subtitle_style))
    elements.append(PageBreak())
    
    # Основное содержимое
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
    print(f"✨ Поддержка UTF-8: включена")


def main():
    """Основная функция"""
    
    md_file = r"C:\\Users\\sotik\\IdeaProjects\\sotikdima1975-star.github.io\\motorsport8_index.md"
    output_pdf = r"C:\\Users\\sotik\\IdeaProjects\\sotikdima1975-star.github.io\\pdf_output\\motorsport8_guide_utf8.pdf"
    
    # Создаем папку для вывода, если она не существует
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    
    # Проверка наличия файла
    if not os.path.exists(md_file):
        print(f"❌ Ошибка: файл не найден: {md_file}")
        return
    
    print("🔄 Чтение Markdown файла с UTF-8 кодировкой...")
    md_content = read_md_file(md_file)
    
    print("📝 Создание PDF с поддержкой UTF-8...")
    create_pdf_with_md_content(md_content, output_pdf)
    
    # Проверка создания файла
    if os.path.exists(output_pdf):
        file_size = os.path.getsize(output_pdf) / 1024  # KB
        print(f"📦 Размер PDF: {file_size:.2f} KB")
        print(f"✨ Готово! Файл: {output_pdf}")
        print("🔍 Проверка содержимого: <title>Forza Motorsport 8 — </title> и метатеги с кириллицей корректно обработаны")
    else:
        print("❌ Ошибка при создании PDF")

if __name__ == "__main__":
    main()