import os
import telebot
import csv
import prettytable as pt
from models.fifa_crawler import FIFADataCrawler
from datetime import datetime

bot = telebot.TeleBot('7521810466:AAFzjXgkTg0AgA7JgWxNYD-vwL5GWFtxSIs')
bot_chatID = "" 

def render_table(file_path):
    table = pt.PrettyTable()
    with open(file_path, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        table.field_names = headers
        rows = list(reader)
        table.add_rows(rows)
        
        today = datetime.now().strftime('%d/%m/%Y')
        table.title = f"Bảng xếp hạng FIFA - {today}"

    return table

@bot.message_handler(commands=['bxh_fifa'])
def send_csv_table(message):

    driver_path = r'C:\Users\Admin\Desktop\DE\crawl\chromedriver-win64\chromedriver.exe'
    crawler = FIFADataCrawler(driver_path)
    crawler.crawl_data()

    filename = crawler.get_filename()
    path_data = r'C:\Users\Admin\Desktop\DE\crawl\fifa_botTele\data'
    file_path = os.path.join(path_data, filename)

    if os.path.exists(file_path):
        table = render_table(file_path)
        table_str = str(table) 
        max_message_length = 4096 
        while len(table_str) > max_message_length:
            part = table_str[:max_message_length]
            table_str = table_str[max_message_length:]
            bot.reply_to(message, part)
        if table_str:
            bot.reply_to(message, table_str)
    else:
        bot.reply_to(message, "Khong tim thay file data")

if __name__ == "__main__":
    bot.polling()
