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
    return {"status": "ok"}

@app.post("/parse/vk")
def parse_vk(domain: str, token: str):
    try:
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        wall = vk.wall.get(domain=domain, count=10)
        return {"success": True, "data": wall['items']}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/parse/web")
def parse_web(url: str):
    try:
        response = httpx.get(url, timeout=10.0)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else ""
        return {"success": True, "title": title, "content_length": len(response.text)}
    except Exception as e:
        return {"success": False, "error": str(e)}
