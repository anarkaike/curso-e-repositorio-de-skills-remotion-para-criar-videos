
import requests
from duckduckgo_search import DDGS
import urllib.parse

def test_pollinations():
    prompt = "professional photo of Volta as Aulas"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
    print(f"Testing Pollinations URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Pollinations OK")
        else:
            print("Pollinations Failed")
    except Exception as e:
        print(f"Pollinations Error: {e}")

def test_ddg():
    print("Testing DDG Search...")
    try:
        with DDGS() as ddgs:
            images = list(ddgs.images("Volta as Aulas", max_results=1))
            if images:
                img_url = images[0]['image']
                print(f"Found DDG Image: {img_url}")
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(img_url, headers=headers, timeout=5)
                    print(f"Image Fetch Status: {response.status_code}")
                except Exception as e:
                    print(f"Image Fetch Error: {e}")
            else:
                print("No DDG images found")
    except Exception as e:
        print(f"DDG Search Error: {e}")

if __name__ == "__main__":
    test_pollinations()
    test_ddg()
