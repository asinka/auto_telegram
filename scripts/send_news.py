import os
import time

from telebot import TeleBot, formatting
import requests

from news_sources.n1_news_source import N1NewsSource

bot = TeleBot(
    token=os.environ.get('BOT_TOKEN'),
    parse_mode='html',
    disable_web_page_preview=True
)
chat_id = os.environ.get('CHANNEL_ID')
source = N1NewsSource()

if __name__ == '__main__':
    news_to_post = source.get_news()
    for news in news_to_post:
        # photo = requests.get(news.img_url).content
        photo = source.create_mem_from_photo(news=news)

        bot.send_photo(
            chat_id=chat_id,
            photo=open(photo, 'rb'),
            caption=news.summary
        )
        print(f"News {news.title} was sent")
        photo.unlink()
        time.sleep(3)
