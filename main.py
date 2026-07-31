from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
import vk_api

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Parser API is online"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/parse/web")
def parse_web(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0"
        }
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)
        soup = BeautifulSoup(response.text, "html.parser")
        
        posts = []
        # Находим все блоки сообщений на веб-зеркале Telegram (t.me/s/...)
        message_elements = soup.find_all("div", class_="js-widget_message")
        
        for msg in message_elements:
            # Текст поста
            text_element = msg.find("div", class_="js-message_text")
            text = text_element.get_text(separator="\n").strip() if text_element else ""
            
            # Ссылка на конкретный пост
            link_element = msg.find("a", class_="tgme_widget_message_date")
            post_url = link_element["href"] if link_element and link_element.has_attr("href") else ""
            
            # Дата публикации
            time_element = msg.find("time")
            post_date = time_element["datetime"] if time_element and time_element.has_attr("datetime") else ""
            
            if text:
                posts.append({
                    "text": text,
                    "url": post_url,
                    "date": post_date
                })
                
        # Если нашли посты — берем самый свежий (последний)
        latest_post = posts[-1] if posts else {"text": "Постов не найдено", "url": "", "date": ""}
        
        return {
            "success": True,
            "text": latest_post["text"],
            "url": latest_post["url"],
            "date": latest_post["date"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
