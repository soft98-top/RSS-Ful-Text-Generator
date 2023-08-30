from bs4 import BeautifulSoup
from web_spider import *
from rss_handler import *
# 导入 html 标签处理库
import html
import time
from dateutil import parser


def genrate_rss_by_html(urls,handle_config):
    if handle_config is None:
        return None
    title = handle_config.get("title")
    if title is None:
        title = "RSS-Full-Text-Generator"
    link = handle_config.get("link")
    if link is None:
        link = "https://www.soft98.top/"
    description = handle_config.get("description")
    if description is None:
        description = "RSS-Full-Text-Generator"
    items = []
    for url in urls:
        item = handle_html(url,handle_config.get('capture'))
        items.append(item)
    return getRSSContent(title, link, description, items)

def handle_html(url,capture):
    web_html = getHTMLText(url)
    # print(web_html)
    soup = BeautifulSoup(web_html, "html.parser")
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
        try:
            pubDate_obj = parser.parse(pubDate)
            pubDate_obj = pubDate_obj.timetuple()
        except:
            try:
                pubDate_obj = time.strptime(pubDate, "%Y年%m月%d日")
            except:
                pubDate_obj = time.localtime()
        pubDate = time.strftime("%a, %d %b %Y %H:%M:%S +0000", pubDate_obj)
    # print(pubDate)
    item = {
        "title": title,
        "link": url,
        "description": description,
        "author": None,
        "pubDate": pubDate
    }
    return item

def capture_html(capture, flag, soup, type="str", index=0):
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
    if capture[flag].get("_index") is not None:
        index = int(capture[flag]["_index"])
    content = soup.find_all(tag, attrs)
    if len(content) > 0:
        if index >= len(content):
            index = 0
        content = content[index]
    if content is not None:
        if type == "str":
            return content.string
        elif type == "html":
            return content.prettify()
        else:
            return content
    else:
        return None

def genrate_rss_by_json(handle_config,items):
    if handle_config is None:
        return None
    title = handle_config.get("title")
    if title is None:
        title = "RSS-Full-Text-Generator"
    link = handle_config.get("link")
    if link is None:
        link = "https://www.soft98.top/"
    description = handle_config.get("description")
    if description is None:
        description = "RSS-Full-Text-Generator"
    return getRSSContent(title, link, description, items)

def handle_json(url,rule_id):
    pass