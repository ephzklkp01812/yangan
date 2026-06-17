import os
import requests
import random
import time

def load_quotes(file_path="quotes.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        quotes = [line.strip() for line in f if line.strip()]
    return quotes

def get_daily_quote(quotes):
    index = random.randint(0, len(quotes) - 1)
    return quotes[index], index + 1

def push_to_wework(webhook_url, message, msg_type="text"):
    if msg_type == "text":
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
    elif msg_type == "markdown":
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": message
            }
        }
    else:
        raise ValueError(f"Unsupported message type: {msg_type}")
    
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("errcode") != 0:
            print(f"推送失败: {result}")
            return False
        print("推送成功！")
        return True
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return False

def main():
    webhook_url = os.environ.get("WEWORK_WEBHOOK_URL")
    if not webhook_url:
        print("错误: 请设置环境变量 WEWORK_WEBHOOK_URL")
        return
    
    quotes = load_quotes()
    if not quotes:
        print("错误: quotes.txt 文件为空")
        return
    
    quote, day_index = get_daily_quote(quotes)
    today = time.strftime("%Y年%m月%d日")
    
    message = f"""📅 {today}
✨ 每日语录 ({day_index}/{len(quotes)})

{quote}"""
    
    print(f"今日语录:\n{message}")
    
    push_to_wework(webhook_url, message)

if __name__ == "__main__":
    main()
