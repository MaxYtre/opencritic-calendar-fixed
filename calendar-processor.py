#!/usr/bin/env python3
"""
OpenCritic Calendar Processor
Загружает календарь OpenCritic, фильтрует события на 2 года вперед
и создает оптимизированный ICS файл для Google Calendar
"""

import requests
import re
from datetime import datetime, timedelta
from typing import List, Tuple
import os

def download_opencritic_calendar() -> str:
    """Загружает оригинальный календарь OpenCritic"""
    url = "https://img.opencritic.com/calendar/OpenCritic.ics"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка загрузки календаря: {e}")
        return ""

def parse_ics_events(ics_content: str) -> List[str]:
    """Парсит ICS файл и возвращает список событий"""
    events = []
    lines = ics_content.split('\n')
    
    current_event = []
    in_event = False
    
    for line in lines:
        if line.strip() == 'BEGIN:VEVENT':
            in_event = True
            current_event = [line]
        elif line.strip() == 'END:VEVENT':
            current_event.append(line)
            events.append('\n'.join(current_event))
            current_event = []
            in_event = False
        elif in_event:
            current_event.append(line)
    
    return events

def extract_event_date(event: str) -> datetime:
    """Извлекает дату из события"""
    # Ищем DTSTART
    dtstart_match = re.search(r'DTSTART(?:;[^:]*)?:(\d{8}T?\d*)', event)
    if dtstart_match:
        date_str = dtstart_match.group(1)
        # Парсим дату
        if 'T' in date_str:
            return datetime.strptime(date_str[:8], '%Y%m%d')
        else:
            return datetime.strptime(date_str[:8], '%Y%m%d')
    return datetime.min

def filter_events_by_date(events: List[str], start_date: datetime, end_date: datetime) -> List[str]:
    """Фильтрует события по диапазону дат"""
    filtered_events = []
    
    for event in events:
        event_date = extract_event_date(event)
        if start_date <= event_date <= end_date:
            filtered_events.append(event)
    
    return filtered_events

def create_ics_file(events: List[str], original_header: str, original_footer: str) -> str:
    """Создает новый ICS файл с отфильтрованными событиями"""
    ics_content = []
    
    # Добавляем заголовок календаря
    ics_content.append(original_header.strip())
    
    # Добавляем события
    for event in events:
        ics_content.append(event)
    
    # Добавляем футер
    ics_content.append(original_footer.strip())
    
    return '\n'.join(ics_content)

def extract_calendar_wrapper(ics_content: str) -> Tuple[str, str]:
    """Извлекает заголовок и футер календаря"""
    lines = ics_content.split('\n')
    
    header_lines = []
    footer_lines = []
    
    # Собираем заголовок до первого события
    i = 0
    while i < len(lines) and lines[i].strip() != 'BEGIN:VEVENT':
        header_lines.append(lines[i])
        i += 1
    
    # Собираем футер после последнего события
    in_event = False
    for line in reversed(lines):
        if line.strip() == 'END:VEVENT':
            in_event = True
            continue
        if not in_event:
            footer_lines.insert(0, line)
        else:
            break
    
    return '\n'.join(header_lines), '\n'.join(footer_lines)

def main():
    """Основная функция обработки календаря"""
    print("Загружаем календарь OpenCritic...")
    ics_content = download_opencritic_calendar()
    
    if not ics_content:
        print("Не удалось загрузить календарь")
        return
    
    print(f"Загружен календарь размером: {len(ics_content):,} символов")
    
    # Определяем диапазон дат (2 года вперед от сегодня)
    today = datetime.now()
    end_date = today + timedelta(days=730)  # 2 года
    
    print(f"Фильтруем события с {today.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}")
    
    # Парсим события
    events = parse_ics_events(ics_content)
    print(f"Найдено событий в исходном календаре: {len(events):,}")
    
    # Фильтруем события по дате
    filtered_events = filter_events_by_date(events, today, end_date)
    print(f"Событий после фильтрации: {len(filtered_events):,}")
    
    # Извлекаем заголовок и футер календаря
    header, footer = extract_calendar_wrapper(ics_content)
    
    # Создаем новый ICS файл
    new_ics = create_ics_file(filtered_events, header, footer)
    
    # Проверяем размер
    file_size_mb = len(new_ics.encode('utf-8')) / (1024 * 1024)
    print(f"Размер нового календаря: {file_size_mb:.2f} МБ")
    
    # Сохраняем файл
    output_filename = "opencritic-calendar-filtered.ics"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(new_ics)
    
    print(f"Календарь сохранен в файл: {output_filename}")
    print(f"Готов для импорта в Google Calendar!")
    
    # Проверяем, что размер подходит для Google Calendar
    if file_size_mb > 1.0:
        print("⚠️  ВНИМАНИЕ: Файл все еще превышает 1 МБ для Google Calendar")
        print("   Возможно, нужно сократить период или дополнительно оптимизировать")
    else:
        print("✅ Размер файла подходит для Google Calendar (< 1 МБ)")

if __name__ == "__main__":
    main()