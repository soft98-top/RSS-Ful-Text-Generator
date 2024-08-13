import requests

HTTP_CONFIG = {
    "timeout": 30,
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }
}

def getHTMLText(url):
    try:
        r = requests.get(url, headers=HTTP_CONFIG["headers"], timeout=HTTP_CONFIG["timeout"])
        r.raise_for_status() # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print(e)
        return None

def getJsonText(url):
    try:
        r = requests.get(url, headers=HTTP_CONFIG["headers"], timeout=HTTP_CONFIG["timeout"])
        r.raise_for_status() # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.json()
    except:
        return None