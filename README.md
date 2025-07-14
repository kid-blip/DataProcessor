# DataProcessor
This project is a versatile command-line tool developed in **Python** (or **C++**, if that was your primary language for this project) designed for efficient reading, processing, filtering, and generating reports from various data sources. The program aims to automate data analysis and reporting tasks from structured files, logs, and web pages.

## About The Project

Developed as an ambitious personal project, this tool demonstrates capabilities in handling diverse data formats. It provides users with powerful functions for extracting necessary information and presenting it in an organized manner. Special attention has been given to functionality and flexible data processing.

## Key Features

### 1. CSV File Processing

* **Reading:** Successfully reads data from CSV files, with support for various delimiters (defaulting to comma, but extendable for others).
* **Filtering:** Robust filtering capabilities for records based on specified conditions across any column. Supports filters based on:
    * Value comparisons (e.g., `Age > 30`, `Price < 100`).
    * Substring search (`City contains 'New'`).
* **Reporting:** Generates detailed summary reports for all or filtered CSV data, including total record count, column headers, and examples of the first/last records.

### 2. Text Log Analysis

* **Reading:** Reads content from plain text files commonly used as logs.
* **Keyword Filtering:** Extracts lines containing a specific keyword or phrase.
* **Regular Expression (Regex) Filtering:** Advanced line filtering based on complex patterns, allowing for the identification of specific events (e.g., `ERROR` messages, specific timestamps).
* **Reporting:** Provides log summaries, including total line count and examples of filtered entries.

### 3. Web Page Parsing (HTML Web Scraping)

* **Content Downloading:** Successfully fetches the complete HTML content from a given URL.
* **Text Extraction:** Extracts all visible text from the page, cleaned of HTML tags.
* **Specific HTML Element Extraction:** Automatically identifies and extracts content from common and important HTML tags, such as:
    * `<h1>` (Level 1 Headings)
    * `<h2>` (Level 2 Headings)
    * `<p>` (Paragraphs)
    * `<a>` (Links)
* **Reporting:** Generates reports on web pages, including the URL, total text length, and a list of extracted elements with their counts and content examples.

## How To Run

### Prerequisites

* Python 3.x (if the project is in Python)
* C++ Compiler (if the project is in C++)

### Installation of Dependencies (for Python version)

If your project is in Python, you will need the `requests` and `BeautifulSoup4` libraries for web fetching and HTML parsing. Install them using `pip`:

```bash
pip install requests beautifulsoup4
