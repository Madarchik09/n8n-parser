from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup

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
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=15.0)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Находим все блоки с текстами сообщений в Telegram
        message_divs = soup.find_all("div", class_=["tgme_widget_message_text", "js-message_text"])
        
        posts = []
        for div in message_divs:
            text = div.get_text(separator="\n").strip()
            if text:
                posts.append(text)
                
        if posts:
            # Забираем самый свежий пост
            latest_vacancy = posts[-1]
            return {
                "success": True,
                "text": latest_vacancy,
                "total_found": len(posts)
            }
        else:
            return {
                "success": False,
                "text": "Посты не найдены"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
