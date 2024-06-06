import os
from dotenv import load_dotenv
import feedparser
from telegram import Bot
from telegram.constants import ParseMode
import logging
import asyncio

# Load environment variables from .env file
load_dotenv()

# Tentukan path untuk file log di dalam direktori proyek
log_file = os.path.join(os.path.dirname(__file__), 'output.log')

# Setting up logging
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Daftar URL RSS feed
rss_urls = [
    "https://feeds.feedburner.com/TheHackersNews",  # The Hacker News
    "https://www.middleeastmonitor.com/feed/",  # Middle East Monitor (MEMO)
    "https://feeds.bbci.co.uk/news/rss.xml",  # BBC News
    "http://rss.cnn.com/rss/edition.rss",  # CNN
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",  # NY Times
    "http://feeds.feedburner.com/TechCrunch/",  # TechCrunch
    "https://www.globalissues.org/news/feed",  # Global Issues
    "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml",  # Defense News
    "https://www.militarytimes.com/arc/outboundfeeds/rss/?outputType=xml",  # Military Times
    "https://www.aljazeera.com/xml/rss/all.xml"  # Al Jazeera - Middle East
]

# Token API dari BotFather

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') # Mengambil token dari environment variable
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') # Mengambil chat ID dari environment variable

def format_message(news):
    message = f"*{news['title']}*\n\n" \
              f"{news['description']}\n\n" \
              f"[Read more]({news['link']})\n\n" \
              f"{news['published'].split(',')[1].strip() if ',' in news['published'] else news['published']}"
    
    return message

def get_latest_news():
    latest_news = []
    for url in rss_urls:
        logging.info(f"Fetching news from: {url}")
        feed = feedparser.parse(url)
        for entry in feed.entries:  # Ambil semua berita dari setiap feed
            news = {
                'title': entry.title,
                'link': entry.link,
                'description': entry.get('summary', entry.get('description', 'No description available'))
            }
            
            # Gunakan 'published' jika tersedia, jika tidak gunakan 'updated'
            news['published'] = entry.get('published', entry.get('updated', 'Date not available'))
            
            # Cek apakah terdapat enclosure dengan URL gambar
            if 'media_content' in entry and len(entry.media_content) > 0:
                news['image_url'] = entry.media_content[0]['url']
            elif 'enclosures' in entry and len(entry.enclosures) > 0:
                news['image_url'] = entry.enclosures[0].get('href')
            
            latest_news.append(news)
    return latest_news

async def send_news():
    bot = Bot(token=TOKEN)
    news_list = get_latest_news()
    for news in news_list:
        # Formatting pesan dengan menggunakan fungsi format_message
        message = format_message(news)
        
        try:
            if "image_url" in news:
                logging.info(f"Sending news with image: {news['title']}")
                await bot.send_photo(chat_id=CHAT_ID, photo=news['image_url'], caption=message, parse_mode=ParseMode.MARKDOWN)
            else:
                logging.info(f"Sending news without image: {news['title']}")
                await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logging.error(f"Failed to send news: {news['title']}. Error: {e}")
        else:
            logging.info(f"Sent news: {news['title']}")
        await asyncio.sleep(1)  # Beri jeda antar pesan

if __name__ == "__main__":
    try:
        asyncio.run(send_news())
        logging.info("Script executed successfully.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
