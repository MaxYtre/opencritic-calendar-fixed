# OpenCritic Calendar Filter

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Скрипт для фильтрации и оптимизации календаря релизов видеоигр от [OpenCritic](https://opencritic.com/) под требования Google Calendar.

## 📖 Описание

Официальный календарь OpenCritic (`.ics`) содержит огромное количество событий за все годы, из-за чего его размер значительно превышает ограничение Google Calendar в **1 МБ**. Это делает невозможным его прямой импорт.

Данный скрипт решает эту проблему:
- Загружает актуальный календарь релизов напрямую с серверов OpenCritic.
- Фильтрует события, оставляя только актуальные (по умолчанию: от 2 месяцев назад до 2 лет вперед).
- Генерирует оптимизированный файл `opencritic-calendar-filtered.ics` размером менее 1 МБ, который легко и без ошибок импортируется в Google Calendar или любой другой сервис.

## 🚀 Как подписаться в Google Calendar

Вам **не нужно** ничего скачивать или устанавливать. Просто добавьте этот календарь по ссылке, и он будет обновляться автоматически каждый день!

1. Откройте [Google Calendar](https://calendar.google.com/) на компьютере.
2. Слева найдите раздел **"Другие календари"** (Other calendars) и нажмите на `+`.
3. Выберите **"Добавить по URL"** (From URL).
4. Вставьте следующую ссылку:
   ```text
   https://raw.githubusercontent.com/MaxYtre/opencritic-calendar-fixed/main/opencritic-calendar-filtered.ics
   ```
5. Нажмите **"Добавить календарь"**.

*Примечание: Если у вас включен GitHub Pages для ветки main, вы также можете использовать ссылку `https://maxytre.github.io/opencritic-calendar-fixed/opencritic-calendar-filtered.ics`*

---

## 🛠️ Для разработчиков (Локальный запуск)

Если вы хотите запустить скрипт самостоятельно или изменить параметры фильтрации:

### 1. Требования
- Python 3.8 или выше.
- Пакетный менеджер `pip`.

### 2. Установка зависимостей

Клонируйте репозиторий и установите необходимые зависимости:

```bash
git clone https://github.com/your-username/opencritic-calendar-fixed.git
cd opencritic-calendar-fixed
pip install -r requirements.txt
```

### 3. Запуск

Выполните скрипт из терминала:

```bash
python calendar-processor.py
```

После выполнения в директории появится файл `opencritic-calendar-filtered.ics`, готовый к импорту.

## ⚙️ Настройка

Вы можете изменить временной диапазон фильтрации, отредактировав следующие переменные в начале файла `calendar-processor.py`:

```python
MONTHS_BEFORE = 2  # Количество месяцев назад от текущей даты
YEARS_AFTER = 2    # Количество лет вперед от текущей даты
```

## 🤝 Вклад в проект (Contributing)

Буду рад вашим Pull Request'ам! Если вы нашли ошибку или у вас есть идеи по улучшению (например, автоматизация через GitHub Actions), пожалуйста, создайте [Issue](../../issues).

1. Сделайте Fork проекта
2. Создайте ветку для вашей функции (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте изменения в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).
