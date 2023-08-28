from bs4 import BeautifulSoup
from web_spider import *
from rss_handler import *
# 导入 html 标签处理库
import html
import time

HANDLE_RULE = {
    "xianzhi":{
        "title": "先知社区",
        "link": "https://paper.seebug.org/",
        "description": "先知社区",
        "capture": {
            "title": {"tag": "h1", "class": "post-title"},
            "description": {"tag": "section", "class": "post-content"},
            "pubDate": {"tag": "time", "class": "fulldate"}
        }
    }
}

def genrate_rss_by_html(urls,rule_id):
    if HANDLE_RULE.get(rule_id) is None:
        return None
    title = HANDLE_RULE[rule_id].get("title")
    if title is None:
        title = "RSS-Full-Text-Generator"
    link = HANDLE_RULE[rule_id].get("link")
    if link is None:
        link = "https://www.soft98.top/"
    description = HANDLE_RULE[rule_id].get("description")
    if description is None:
        description = "RSS-Full-Text-Generator"
    items = []
    for url in urls:
        item = handle_html(url,rule_id)
        items.append(item)
    return getRSSContent(title, link, description, items)

def handle_html(url,rule_id):
    web_html = getHTMLText(url)
    # print(web_html)
    soup = BeautifulSoup(web_html, "html.parser")
    capture = HANDLE_RULE[rule_id]["capture"]
    if capture is None:
        return None
    title = capture_html(capture, "title", soup)
    if title is None:
        title = ""
    # 需要完整 html
    description = capture_html(capture, "description", soup, "html")
    if description is None:
        description = ""
    else:
        # 并对description 的html 标签编码
        description = html.escape(description)
    pubDate = capture_html(capture, "pubDate", soup)
    if pubDate is None:
        pubDate = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
    else:
        # 2023年08月25日转换为Fri, 25 Aug 2023 05:40:00 +0000 格式，先转换为时间戳，再转换为时间格式
        pubDate = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.strptime(pubDate, "%Y年%m月%d日"))
    # print(pubDate)
    item = {
        "title": title,
        "link": url,
        "description": description,
        "author": None,
        "pubDate": pubDate
    }
    return item

def capture_html(capture, flag, soup, type="str"):
    if capture.get(flag) is None:
        return None
    # 解析 capture，根据设置的内容抓取规则
    if capture[flag].get("tag") is None:
        return None
    tag = capture[flag]["tag"]
    attrs = {}
    for key in capture[flag].keys():
        if key == "tag":
            continue
        attrs[key] = capture[flag][key]
    content = soup.find(tag, attrs=attrs)
    if content is not None:
        if type == "str":
            return content.string
        elif type == "html":
            return content.prettify()
        else:
            return content
    else:
        return None

def genrate_rss_by_json(urls,rule_id):
    if HANDLE_RULE.get(rule_id) is None:
        return None
    title = HANDLE_RULE[rule_id].get("title")
    if title is None:
        title = "RSS-Full-Text-Generator"
    link = HANDLE_RULE[rule_id].get("link")
    if link is None:
        link = "https://www.soft98.top/"
    description = HANDLE_RULE[rule_id].get("description")
    if description is None:
        description = "RSS-Full-Text-Generator"
    items = []
    for url in urls:
        item = handle_json(url,rule_id)
        items.append(item)
    return getRSSContent(title, link, description, items)

def handle_json(url,rule_id):
    pass