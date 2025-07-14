import csv
import requests
from bs4 import BeautifulSoup
import json
import re # Добавлен для регулярных выражений в filter_text_log

# --- Функции для чтения данных ---

def read_csv_data(file_path):
    """
    Считывает данные из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        list: Список словарей, где каждый словарь представляет строку данных.
              Возвращает пустой список, если файл не найден или произошла ошибка.
    """
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                data.append(row)
        print(f"Успешно прочитаны данные из CSV-файла: {file_path}")
    except FileNotFoundError:
        print(f"Ошибка: CSV-файл не найден по пути: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка при чтении CSV-файла: {e}")
    return data

def read_text_log(file_path):
    """
    Считывает данные из простого текстового файла (лога).

    Args:
        file_path (str): Путь к текстовому файлу.

    Returns:
        list: Список строк из файла. Возвращает пустой список, если файл не найден или произошла ошибка.
    """
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"Успешно прочитаны данные из текстового файла: {file_path}")
    except FileNotFoundError:
        print(f"Ошибка: Текстовый файл не найден по пути: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка при чтении текстового файла: {e}")
    return [line.strip() for line in lines] # Удаляем символы новой строки

def fetch_web_page_content(url):
    """
    Скачивает полное HTML-содержимое веб-страницы.

    Args:
        url (str): URL веб-страницы.

    Returns:
        str: HTML-содержимое страницы в виде строки. Возвращает None, если произошла ошибка.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Вызывает исключение для ошибок HTTP (4xx или 5xx)
        print(f"Успешно скачан контент с URL: {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании веб-страницы с {url}: {e}")
    return None

def parse_web_page_text(html_content):
    """
    Парсит HTML-контент и извлекает весь видимый текст.

    Args:
        html_content (str): HTML-содержимое веб-страницы.

    Returns:
        str: Весь видимый текст с веб-страницы. Возвращает пустую строку, если контент пуст или произошла ошибка.
    """
    if not html_content:
        return ""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Удаляем скрипты и стили, чтобы они не попадали в текст
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()
        text = soup.get_text(separator=' ', strip=True)
        print("Успешно извлечен текст из HTML-контента.")
        return text
    except Exception as e:
        print(f"Ошибка при парсинге HTML-контента: {e}")
        return ""

def parse_web_page_elements(html_content, tag_name):
    """
    Парсит HTML-контент и извлекает текст из указанных HTML-элементов.

    Args:
        html_content (str): HTML-содержимое веб-страницы.
        tag_name (str): Имя HTML-тега, элементы которого нужно извлечь (например, 'h1', 'p', 'a').

    Returns:
        list: Список строк, где каждая строка - это текст из найденного элемента.
              Возвращает пустой список, если контент пуст, тег не найден или произошла ошибка.
    """
    if not html_content:
        print(f"Предупреждение: HTML-контент пуст для парсинга '{tag_name}'.")
        return []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(tag_name)
        extracted_texts = [element.get_text(strip=True) for element in elements]
        print(f"Успешно извлечены элементы <{tag_name}> из HTML-контента.")
        return extracted_texts
    except Exception as e:
        print(f"Ошибка при парсинге HTML-контента для тега '{tag_name}': {e}")
        return []

# --- Функции для генерации отчетов ---

def generate_csv_summary(data):
    """
    Генерирует простую сводку для CSV-данных.
    Показывает количество записей и заголовки столбцов.

    Args:
        data (list): Список словарей, полученный из CSV.

    Returns:
        str: Строка с отчетом.
    """
    if not data:
        return "Отчет по CSV: Данные не найдены."

    num_records = len(data)
    headers = list(data[0].keys()) if data else []

    report = f"--- Отчет по CSV данным ---\n"
    report += f"Всего записей: {num_records}\n"
    report += f"Заголовки столбцов: {', '.join(headers)}\n"
    report += "Пример первых 3-х записей:\n"
    for i, row in enumerate(data[:3]):
        report += f"  Запись {i+1}: {row}\n"
    report += "---------------------------\n"
    print("Сводка по CSV данным успешно сгенерирована.")
    return report

def generate_text_log_summary(lines):
    """
    Генерирует простую сводку для текстовых логов.
    Показывает количество строк и первые/последние несколько строк.

    Args:
        lines (list): Список строк из текстового файла.

    Returns:
        str: Строка с отчетом.
    """
    if not lines:
        return "Отчет по текстовому логу: Данные не найдены."

    num_lines = len(lines)
    report = f"--- Отчет по текстовому логу ---\n"
    report += f"Всего строк: {num_lines}\n"
    report += "Пример первых 5-ти строк:\n"
    for i, line in enumerate(lines[:5]):
        report += f"  {line}\n"
    if num_lines > 5:
        report += "...\n"
        report += "Пример последних 5-ти строк:\n"
        for i, line in enumerate(lines[-5:]):
            report += f"  {line}\n"
    report += "---------------------------------\n"
    print("Сводка по текстовому логу успешно сгенерирована.")
    return report

def generate_web_page_summary(text_content, url, extracted_elements=None):
    """
    Генерирует простую сводку для текстового содержимого веб-страницы,
    включая извлеченные элементы.

    Args:
        text_content (str): Извлеченный весь видимый текст с веб-страницы.
        url (str): URL страницы.
        extracted_elements (dict, optional): Словарь с извлеченными элементами.
                                            Ключ - имя тега, значение - список текстов.
    Returns:
        str: Строка с отчетом.
    """
    report = f"--- Отчет по веб-странице ---\n"
    report += f"URL: {url}\n"

    if text_content:
        summary_length = 500
        summary_text = text_content[:summary_length] + ("..." if len(text_content) > summary_length else "")
        report += f"Длина всего текста (символов): {len(text_content)}\n"
        report += f"Первые {summary_length} символов текста:\n"
        report += f"--------------------------------------------------\n"
        report += f"{summary_text}\n"
        report += f"--------------------------------------------------\n"
    else:
        report += f"Текстовое содержимое не найдено.\n"

    if extracted_elements:
        report += "\nИзвлеченные элементы:\n"
        for tag, texts in extracted_elements.items():
            if texts:
                report += f"  <{tag}> (количество: {len(texts)}):\n"
                for i, text in enumerate(texts[:3]): # Показываем первые 3 примера
                    report += f"    - {text[:100]}...\n" # Обрезаем для краткости
                if len(texts) > 3:
                    report += "    (и еще...)\n"
            else:
                report += f"  <{tag}>: Не найдено.\n"
    report += "--------------------------------------------------\n"
    print("Сводка по веб-странице успешно сгенерирована.")
    return report

# --- Функции для фильтрации данных ---

def filter_csv_data(data, column_name, operator, value):
    """
    Фильтрует CSV-данные по заданному критерию.

    Args:
        data (list): Список словарей (CSV-данные).
        column_name (str): Имя столбца для фильтрации.
        operator (str): Оператор сравнения ('==', '!=', '>', '<', '>=', '<=', 'contains', 'not contains').
        value (str or int or float): Значение для сравнения.

    Returns:
        list: Отфильтрованный список словарей.
    """
    filtered_data = []
    print(f"Применяем фильтр к CSV: {column_name} {operator} {value}")
    for row in data:
        if column_name not in row:
            continue # Пропускаем строку, если столбца нет

        row_value = row[column_name]

        # Пытаемся преобразовать значения для числовых сравнений
        try:
            row_value_num = float(row_value)
            value_num = float(value)
        except (ValueError, TypeError):
            row_value_num = None
            value_num = None

        match = False
        if operator == '==':
            match = (row_value == str(value))
        elif operator == '!=':
            match = (row_value != str(value))
        elif operator == '>':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num > value_num)
        elif operator == '<':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num < value_num)
        elif operator == '>=':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num >= value_num)
        elif operator == '<=':
            if row_value_num is not None and value_num is not None:
                match = (row_value_num <= value_num)
        elif operator == 'contains':
            match = (str(value).lower() in row_value.lower())
        elif operator == 'not contains':
            match = (str(value).lower() not in row_value.lower())
        else:
            print(f"Предупреждение: Неизвестный оператор фильтрации для CSV: {operator}")
            continue

        if match:
            filtered_data.append(row)
    print(f"Отфильтровано CSV записей: {len(filtered_data)}")
    return filtered_data

def filter_text_log(lines, keyword=None, regex_pattern=None):
    """
    Фильтрует текстовые строки лога по ключевому слову или регулярному выражению.

    Args:
        lines (list): Список строк из текстового файла.
        keyword (str, optional): Ключевое слово для поиска (регистронезависимый).
        regex_pattern (str, optional): Регулярное выражение для поиска.

    Returns:
        list: Отфильтрованный список строк.
    """
    # import re # Импортируем re только здесь, так как он нужен только для этой функции - этот импорт перемещен в начало файла
    filtered_lines = []
    if keyword:
        print(f"Применяем фильтр к логу по ключевому слову: '{keyword}'")
        search_keyword = keyword.lower()
        for line in lines:
            if search_keyword in line.lower():
                filtered_lines.append(line)
    elif regex_pattern:
        print(f"Применяем фильтр к логу по регулярному выражению: '{regex_pattern}'")
        try:
            compiled_regex = re.compile(regex_pattern)
            for line in lines:
                if compiled_regex.search(line):
                    filtered_lines.append(line)
        except re.error as e:
            print(f"Ошибка в регулярном выражении '{regex_pattern}': {e}")
    else:
        print("Предупреждение: Не задан ни ключевое слово, ни регулярное выражение для фильтрации лога.")
        return lines # Возвращаем все строки, если фильтр не задан

    print(f"Отфильтровано строк лога: {len(filtered_lines)}")
    return filtered_lines


if __name__ == "__main__":
    print("--- Запуск программы для тестирования ---")

    # --- Пример использования CSV-данных и их фильтрации ---
    csv_file = 'example.csv'
    # Убедись, что 'example.csv' содержит данные, например:
    # Name,Age,City
    # Alice,30,New York
    # Bob,24,London
    # Charlie,35,Paris
    # David,29,Berlin
    # Eve,42,Rome
    raw_csv_data = read_csv_data(csv_file)

    if raw_csv_data:
        # Пример 1: Сводка по всем CSV данным
        print("\n--- Отчет по всем CSV данным ---")
        print(generate_csv_summary(raw_csv_data))

        # Пример 2: Фильтрация CSV - Age > 30
        print("\n--- Отчет по CSV данным (Age > 30) ---")
        filtered_csv_age_data = filter_csv_data(raw_csv_data, 'Age', '>', 30)
        print(generate_csv_summary(filtered_csv_age_data))

        # Пример 3: Фильтрация CSV - City contains 'New'
        print("\n--- Отчет по CSV данным (City contains 'New') ---")
        filtered_csv_city_data = filter_csv_data(raw_csv_data, 'City', 'contains', 'New')
        print(generate_csv_summary(filtered_csv_city_data))
    else:
        print("\nНе удалось прочитать CSV данные для тестирования.")


    # --- Пример использования текстового лога и его фильтрации ---
    log_file = 'example.txt'
    # Убедись, что 'example.txt' содержит данные, например:
    # [2023-10-26 10:00:01] INFO: Application started successfully.
    # [2023-10-26 10:00:05] DEBUG: Processing user request for report generation.
    # [2023-10-26 10:00:10] WARN: Low disk space detected on drive C.
    # [2023-10-26 10:00:15] INFO: Report for CSV data generated.
    # [2023-10-26 10:00:20] ERROR: Failed to connect to external service.
    # This is just a simple line of text to test the reader.
    # Another line of text.
    # End of the log file.
    raw_text_data = read_text_log(log_file)

    if raw_text_data:
        # Пример 1: Сводка по всем строкам лога
        print("\n--- Отчет по всем строкам лога ---")
        print(generate_text_log_summary(raw_text_data))

        # Пример 2: Фильтрация лога по ключевому слову "ERROR"
        print("\n--- Отчет по логу (только ERROR сообщения) ---")
        filtered_error_logs = filter_text_log(raw_text_data, keyword='ERROR')
        print(generate_text_log_summary(filtered_error_logs))

        # Пример 3: Фильтрация лога по регулярному выражению для INFO сообщений
        # (Например, ищем строки, содержащие "INFO" и цифры после даты)
        print("\n--- Отчет по логу (только INFO сообщения через regex) ---")
        filtered_info_logs_regex = filter_text_log(raw_text_data, regex_pattern=r'INFO:.*')
        print(generate_text_log_summary(filtered_info_logs_regex))
    else:
        print("\nНе удалось прочитать текстовый лог для тестирования.")

    # --- Пример использования веб-страницы и извлечения конкретных элементов ---
    web_url = "https://en.wikipedia.org/wiki/Comrat" # Используем реальный URL для демонстрации
    # web_url = "https://example.com" # Или этот, если хочешь попроще
    html_content = fetch_web_page_content(web_url)

    if html_content:
        # Извлекаем весь текст для общей сводки
        parsed_full_text = parse_web_page_text(html_content)

        # Извлекаем конкретные элементы: заголовки (h1, h2, h3) и ссылки (a)
        # Сохраняем в словарь для удобства передачи в generate_web_page_summary
        extracted_elements_dict = {
            'h1': parse_web_page_elements(html_content, 'h1'),
            'h2': parse_web_page_elements(html_content, 'h2'),
            'p': parse_web_page_elements(html_content, 'p'),
            'a': parse_web_page_elements(html_content, 'a')
        }

        print("\n--- Отчет по веб-странице с извлеченными элементами ---")
        web_report_with_elements = generate_web_page_summary(
            parsed_full_text,
            web_url,
            extracted_elements=extracted_elements_dict
        )
        print(web_report_with_elements)
    else:
        print("\nНе удалось скачать или обработать веб-страницу для тестирования.")

    input("\nНажмите Enter для выхода...") # Оставляем для удобства