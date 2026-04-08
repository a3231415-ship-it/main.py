# main.py
import requests
from bs4 import BeautifulSoup
import os
import random
import datetime

# 1. 讀取 GitHub Secrets 裡的金鑰 (安全起見，不直接寫在程式碼裡)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# 2. 定義你要隨機抽查的股票清單 (台股代號，可自行增減)
STOCK_LIST = ['2330', '2317', '2454', '2881', '2603', '0050']

def get_stock_price(stock_id):
    """爬取 Yahoo 股市即時股價"""
    url = f"https://tw.stock.yahoo.com/quote/{stock_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 解析 Yahoo 股市的股價 (Fz(32px) 是目前常見的 class)
        price_element = soup.find('span', class_=lambda c: c and 'Fz(32px)' in c)
        return price_element.text if price_element else "無法解析"
    except Exception as e:
        return f"錯誤: {e}"

def send_telegram_msg(message):
    """透過 API 傳送訊息到 Telegram"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("未設定 Telegram Token 或 Chat ID")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    # 隨機選出一檔股票
    target_stock = random.choice(STOCK_LIST)
    price = get_stock_price(target_stock)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 組合訊息格式
    msg = f"📊 【定時隨機股價回報】\n股票代號: {target_stock}\n即時價格: {price}\n更新時間: {now}"
    
    print(msg) # 印在 GitHub Actions 的日誌中方便除錯
    send_telegram_msg(msg)
