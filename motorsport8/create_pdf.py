#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания PDF файла из motorsport8/index.1.html с использованием WeasyPrint
"""

import os
import sys
from pathlib import Path

# Попытка импорта weasyprint
try:
    from weasyprint import HTML, CSS
    print("✅ weasyprint найден")
except ImportError:
    print("⚠️  Требуется установка weasyprint...")
    os.system("pip install weasyprint")
    from weasyprint import HTML, CSS

def create_pdf_from_html(html_path, output_pdf_path):
    """Создать PDF из HTML файла с использованием WeasyPrint"""

    if not os.path.exists(html_path):
        print(f"Ошибка: HTML файл не найден - {html_path}")
        return False

    try:
        # Читаем HTML файл
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Создаем HTML объект
        html_doc = HTML(string=html_content, base_url=os.path.dirname(html_path))

        # Создаем PDF
        html_doc.write_pdf(output_pdf_path)

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
        sys.exit(1)

if __name__ == "__main__":
    main()