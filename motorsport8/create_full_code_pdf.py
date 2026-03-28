#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Профессиональный скрипт для создания PDF с кодами всех файлов проекта Motorsport 8
Включает: index.1.html, style.css, script.js, все файлы из js/ и css/
"""

import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

def read_file_content(file_path):
    """Прочитать содержимое файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

def escape_html(text):
    """Экранировать HTML специальные символы для отображения в PDF"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;')
    )

def create_code_table(code_lines, start_line_num=1):
    """Создать таблицу с кодом и нумерацией строк"""
    data = []
    for i, line in enumerate(code_lines, start=start_line_num):
        # Экранируем HTML символы для безопасного отображения
        escaped_line = escape_html(line.rstrip())
        data.append([str(i), escaped_line])

    # Стили таблицы
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ])

    # Ширина колонок: номера строк - 30pt, код - остальное
    col_widths = [30, 450]

    table = Table(data, colWidths=col_widths, style=table_style)
    return table

def get_file_language(filename):
    """Определить язык файла по расширению"""
    ext = Path(filename).suffix.lower()
    languages = {
        '.html': 'HTML',
        '.css': 'CSS',
        '.js': 'JavaScript',
        '.json': 'JSON',
        '.md': 'Markdown',
        '.py': 'Python',
        '.sql': 'SQL'
    }
    return languages.get(ext, 'Text')

def create_professional_pdf(output_pdf_path, base_path):
    """Создать профессиональный PDF со всеми кодами файлов"""

    # Регистрация шрифтов
    arial_path = r'C:\Windows\Fonts\arial.ttf'
    arial_bold_path = r'C:\Windows\Fonts\arialbd.ttf'
    courier_path = r'C:\Windows\Fonts\cour.ttf'

    if os.path.exists(arial_path):
        pdfmetrics.registerFont(TTFont('Arial', arial_path))
    if os.path.exists(arial_bold_path):
        pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bold_path))
    if os.path.exists(courier_path):
        pdfmetrics.registerFont(TTFont('Courier', courier_path))

    # Создание документа
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    # Стили
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2c3e50'),
        fontName='Arial-Bold' if 'Arial-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
    )

    file_title_style = ParagraphStyle(
        'FileTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=15,
        spaceBefore=20,
        textColor=HexColor('#3498db'),
        fontName='Arial-Bold' if 'Arial-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
        borderWidth=1,
        borderColor=HexColor('#bdc3c7'),
        borderPadding=5,
        borderRadius=3,
    )

    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        fontName='Arial' if 'Arial' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
    )

    # Содержимое документа
    story = []

    # Заголовок
    story.append(Paragraph("Исходный код проекта Motorsport 8", title_style))
    story.append(Paragraph("Профессиональная документация с полными листингами кода", info_style))
    story.append(Paragraph(f"Сгенерировано: {Path(output_pdf_path).parent.name}", info_style))
    story.append(PageBreak())

    # Список файлов для включения
    files_to_include = [
        # Основные файлы motorsport8
        ("motorsport8/index.1.html", "Главная страница (PDF-friendly версия)"),
        ("motorsport8/style.css", "Объединённые стили CSS"),
        ("motorsport8/script.js", "Объединённый JavaScript"),

        # Все файлы из js/
        ("js/game-tabs.js", "Скрипт переключения вкладок игры"),
        ("js/header.js", "Скрипт навигации и мобильного меню"),
        ("js/welcome.js", "Скрипт страницы приветствия"),

        # Все файлы из css/
        ("css/about.css", "Стили страницы 'Обо мне'"),
        ("css/game.css", "Основные стили игровых страниц"),
        ("css/game-tabs.css", "Стили вкладок игры"),
        ("css/header.css", "Стили главного заголовка и навигации"),
        ("css/landing.css", "Стили главной страницы"),
        ("css/racing.css", "Стили гоночной тематики"),
        ("css/responsive.css", "Адаптивные стили для всех устройств"),
        ("css/welcome.css", "Стили страницы приветствия"),
    ]

    total_files = 0
    total_lines = 0

    for file_path, description in files_to_include:
        full_path = base_path / file_path

        if not full_path.exists():
            print(f"⚠️  Файл не найден: {full_path}")
            continue

        # Читаем содержимое файла
        content = read_file_content(str(full_path))
        lines = content.split('\n')
        line_count = len(lines)

        total_files += 1
        total_lines += line_count

        # Заголовок файла
        story.append(Paragraph(f"{file_path}", file_title_style))
        story.append(Paragraph(f"{description} • {get_file_language(file_path)} • {line_count} строк", info_style))
        story.append(Spacer(1, 10))

        # Таблица с кодом
        code_table = create_code_table(lines)
        story.append(code_table)
        story.append(Spacer(1, 20))

        print(f"✅ Добавлен файл: {file_path} ({line_count} строк)")

    # Финальная страница со статистикой
    story.append(PageBreak())
    story.append(Paragraph("Статистика проекта", file_title_style))
    story.append(Paragraph(f"Всего файлов: {total_files}", info_style))
    story.append(Paragraph(f"Всего строк кода: {total_lines}", info_style))
    story.append(Paragraph("Документация сгенерирована автоматически", info_style))

    # Генерируем PDF
    doc.build(story)
    print(f"🎉 Профессиональный PDF создан: {output_pdf_path}")
    print(f"📊 Статистика: {total_files} файлов, {total_lines} строк кода")

def main():
    # Пути
    script_dir = Path(__file__).parent
    base_path = script_dir.parent  # Корень проекта
    output_pdf = script_dir / "motorsport8_full_code.pdf"

    print("🚀 Создание профессионального PDF со всеми кодами проекта...")

    try:
        create_professional_pdf(str(output_pdf), base_path)
        print("✅ Задача выполнена успешно!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()