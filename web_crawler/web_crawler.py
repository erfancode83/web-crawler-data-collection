# web_crawler.py

import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
import os

# پیکربندی لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# URL اصلی سایت
BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books_data.csv"

def get_page(url):
    """دریافت صفحه HTML از یک URL"""
    try:
        logger.info(f"در حال درخواست صفحه: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # اگر کد وضعیت 200 نبود، خطا بده
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"خطا در دریافت صفحه {url}: {e}")
        return None

def parse_books(html_content):
    """استخراج اطلاعات کتاب‌ها از صفحه HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    books = []
    book_elements = soup.select('article.product_pod')  # هر کتاب یک <article> با کلاس product_pod است

    for book in book_elements:
        try:
            # استخراج عنوان
            title = book.h3.a['title'].strip()

            # استخراج قیمت
            price = book.select_one('p.price_color').text.strip()

            # استخراج وضعیت موجودی (مثلاً "In stock (22 available)")
            availability = book.select_one('p.instock.availability').text.strip()

            # استخراج لینک صفحه کتاب (نسبی)
            relative_link = book.h3.a['href']
            full_link = BASE_URL + relative_link if not relative_link.startswith('http') else relative_link

            books.append({
                'title': title,
                'price': price,
                'availability': availability,
                'link': full_link
            })
        except Exception as e:
            logger.warning(f"خطا در پردازش یک کتاب: {e}")
            continue  # اگر یک کتاب مشکل داشت، بقیه رو ادامه بده

    return books

def save_to_csv(books, filename):
    """ذخیره داده‌ها در فایل CSV"""
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'price', 'availability', 'link'])
        if not file_exists:
            writer.writeheader()  # فقط اولین بار هدر بنویس
        writer.writerows(books)
    logger.info(f"{len(books)} کتاب به فایل {filename} اضافه شد.")

def crawl_books_catalog():
    """اسکن تمام صفحات دسته‌بندی کتاب‌ها"""
    page_num = 1
    while True:
        if page_num == 1:
            url = BASE_URL + "catalogue/page-1.html"
        else:
            url = BASE_URL + f"catalogue/page-{page_num}.html"

        html = get_page(url)
        if html is None:
            break  # اگر صفحه‌ای دیگه نیست (مثلاً 404)، متوقف شو

        # چک کنیم آیا صفحه‌ای واقعاً وجود داره (با دیدن اگر عنصری از کتاب وجود داره)
        if "No books available!" in html:
            logger.info("تمام صفحات پردازش شد.")
            break

        books = parse_books(html)
        if not books:
            logger.info("هیچ کتابی برای پردازش یافت نشد. متوقف می‌شود.")
            break

        save_to_csv(books, OUTPUT_FILE)
        logger.info(f"صفحه {page_num} پردازش شد.")
        page_num += 1

        # تأخیر بین درخواست‌ها برای احترام به سرور
        time.sleep(1)

if __name__ == "__main__":
    logger.info("شروع فرآیند اسکریپینگ...")
    crawl_books_catalog()
    logger.info("فرآیند اسکریپینگ کامل شد.")