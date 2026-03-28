#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания PDF файла с кодом motorsport8_index.md
с использованием только разрешённых шрифтов
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Определяем базовую директорию скрипта
BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / "fonts"

# Убедимся, что кодировка по умолчанию - utf-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Список разрешённых шрифтов
ALLOWED_FONTS = {
    'DejaVuSans': 'DejaVuSans.ttf',
    'DejaVuSans-Bold': 'DejaVuSans-Bold.ttf'
}

# Шрифты, которые следует заменить
FONTS_TO_REPLACE = {
    'Arial': 'DejaVuSans',
    'Helvetica': 'DejaVuSans',
    'Times': 'DejaVuSans',
    'Courier': 'DejaVuSans'
}

def check_and_register_fonts():
    """Проверить наличие и зарегистрировать шрифты"""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # Проверяем наличие всех необходимых шрифтов
    missing_fonts = []
    for font_name, font_file in ALLOWED_FONTS.items():
        font_path = FONTS_DIR / font_file
        if not font_path.exists():
            missing_fonts.append(f"{font_name} ({font_file})")
    
    if missing_fonts:
        raise FileNotFoundError(f"Отсутствуют необходимые шрифты: {', '.join(missing_fonts)}\nПоместите их в папку {FONTS_DIR}")
    
    # Регистрируем шрифты
    for font_name, font_file in ALLOWED_FONTS.items():
        font_path = FONTS_DIR / font_file
        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
        print(f"✅ Зарегистрирован шрифт: {font_name}")
    
    return pdfmetrics

def read_md_file(file_path):
    """Прочитать Markdown файл с явной кодировкой UTF-8"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_pdf_with_md_code(md_code, output_path, pdfmetrics):
    """Создать PDF с кодом Markdown, используя только разрешённые шрифты"""
    
    # Настройка страницы
    from reportlab.lib.pagesizes import A4
    pagesize = A4
    page_width, page_height = pagesize
    
    # Создание документа
    from reportlab.platypus import SimpleDocTemplate
    doc = SimpleDocTemplate(
        output_path,
        pagesize=pagesize,
        rightMargin=10*mm,
        leftMargin=10*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
        title="motorsport8_index.md",
        author="СайтСотика",
    )
    
    # Проверяем зарегистрированные шрифты
    available_fonts = pdfmetrics.getRegisteredFontNames()
    print(f"Доступные шрифты: {available_fonts}")
    
    # Проверяем, что все разрешённые шрифты зарегистрированы
    for font_name in ALLOWED_FONTS.keys():
        if font_name not in available_fonts:
            raise RuntimeError(f"Шрифт {font_name} не зарегистрирован!")
    
    # Стили
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    styles = getSampleStyleSheet()
    
    # Используем только разрешённые шрифты
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#007acc'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='DejaVuSans-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='DejaVuSans'
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=9,
        fontName='DejaVuSans',
        textColor=colors.HexColor('#222222'),
        leftIndent=6,
        spaceAfter=0,
        leading=10,
        backColor=colors.HexColor('#f5f5f5')
    )
    
    # Содержимое документа
    from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle
    elements = []
    
    # Заголовок
    elements.append(Spacer(1, 10*mm))
    elements.append(Paragraph("📄 motorsport8_index.md", title_style))
    elements.append(Spacer(1, 3*mm))
    
    # Информация о файле
    file_info = f"Создано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | Строк: {len(md_code.split(chr(10)))}"
    elements.append(Paragraph(file_info, subtitle_style))
    elements.append(Spacer(1, 8*mm))
    
    # Добавление кода со скруллинговой таблицей
    code_lines = md_code.split('\n')
    
    # Создание таблицы с номерами строк и кодом
    table_data = []
    
    # Заголовок таблицы
    table_data.append([
        Paragraph("<b>№</b>", code_style),
        Paragraph("<b>Код</b>", code_style)
    ])
    
    # Добавляем строки кода (максимум 50 строк на страницу)
    lines_per_page = 50
    
    for i, line in enumerate(code_lines[:lines_per_page], 1):
        # Экранируем специальные символы для XML/HTML
        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        line_num_para = Paragraph(f"<font color='#999999'>{i:04d}</font>", code_style)
        
        # Обрезаем длинные строки
        if len(line) > 100:
            line = line[:97] + "..."
        
        code_para = Paragraph(f"<font face='DejaVuSans' size='8'>{line}</font>", code_style)
        table_data.append([line_num_para, code_para])
    
    # Создание таблицы
    table = Table(table_data, colWidths=[0.8*inch, 6.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#007acc')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 10*mm))
    
    # Добавление оставшегося кода на следующие страницы
    if len(code_lines) > lines_per_page:
        elements.append(PageBreak())
        
        # Вторая и последующие страницы
        remaining_lines = code_lines[lines_per_page:]
        table_data = []
        table_data.append([
            Paragraph("<b>№</b>", code_style),
            Paragraph("<b>Код</b>", code_style)
        ])
        
        for i, line in enumerate(remaining_lines, lines_per_page + 1):
            line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            line_num_para = Paragraph(f"<font color='#999999'>{i:04d}</font>", code_style)
            
            if len(line) > 100:
                line = line[:97] + "..."
            
            code_para = Paragraph(f"<font face='DejaVuSans' size='8'>{line}</font>", code_style)
            table_data.append([line_num_para, code_para])
        
        table = Table(table_data, colWidths=[0.8*inch, 6.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#007acc')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(table)
    
    # Построение PDF
    doc.build(elements)
    print(f"✅ PDF успешно создан: {output_path}")
    print(f"📊 Статистика: {len(code_lines)} строк кода")
    print(f"🔍 Использованы только разрешённые шрифты: {list(ALLOWED_FONTS.keys())}")
    print(f"🔍 Заменены запрещённые шрифты: {list(FONTS_TO_REPLACE.keys())}")
    
def main():
    """Основная функция"""
    
    # Установка reportlab если необходимо
    try:
        import reportlab
    except ImportError:
        print("⚠️  Установка reportlab...")
        os.system("pip install reportlab")
    
    md_file = r"C:\\Users\\sotik\\IdeaProjects\\sotikdima1975-star.github.io\\motorsport8_index.md"
    output_pdf = r"C:\\Users\\sotik\\IdeaProjects\\sotikdima1975-star.github.io\\pdf_output\\motorsport8_index_code_final.pdf"
    
    # Создаем папку для вывода, если она не существует
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    
    # Проверка наличия файла
    if not os.path.exists(md_file):
        print(f"❌ Ошибка: файл не найден: {md_file}")
        return
    
    try:
        # Проверяем и регистрируем шрифты
        from reportlab.pdfbase import pdfmetrics
        pdfmetrics = check_and_register_fonts()
        
        print("🔄 Чтение Markdown файла с UTF-8 кодировкой...")
        md_code = read_md_file(md_file)
        
        print("📝 Создание PDF с кодом Markdown...")
        create_pdf_with_md_code(md_code, output_pdf, pdfmetrics)
        
        # Проверка создания файла
        if os.path.exists(output_pdf):
            file_size = os.path.getsize(output_pdf) / 1024  # KB
            print(f"📦 Размер PDF: {file_size:.2f} KB")
            print(f"✨ Готово! Файл: {output_pdf}")
            print("🔍 Проверка содержимого: код MD-файла полностью встроен в PDF")
        else:
            print("❌ Ошибка при создании PDF")
            
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("👉 Решение: скачайте шрифты DejaVuSans из https://github.com/dejavu-fonts/dejavu-fonts и поместите в папку fonts")
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()