# 🕷️ Web Crawler for Data Collection (Python)

A simple yet robust web scraper that collects structured data from [Books to Scrape](https://books.toscrape.com/), a website designed for learning web scraping.

## 🎯 Goal
- Fetch product data (title, price, availability, link) from multiple pages.
- Save data in a clean CSV format.
- Handle errors gracefully and respect server limits.

## 🛠️ Technologies Used
- **Python 3.x**
- `requests` – for HTTP requests
- `BeautifulSoup4` – for HTML parsing
- `csv` – for structured data export
- `logging` – for error tracking and monitoring

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/web-crawler-data-collection.git
   cd web-crawler-data-collection
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Usage

Run the crawler:
```bash
python web_crawler.py
```

Output files:
- `books_data.csv` – collected book data (created after run)
- `crawler.log` – execution logs

> ⏱️ The script waits 1 second between requests to be respectful to the server.

## 📝 Notes
- This project uses [books.toscrape.com](https://books.toscrape.com/), a legal and public sandbox for scraping practice.
- Do not use this crawler on websites without checking their `robots.txt` and terms of service.

## 📄 License
MIT License – feel free to use and learn from this code!