from flask import render_template
import flask
import requests
from bs4 import BeautifulSoup
import html
import time
from dateutil import parser

app = flask.Flask(__name__, template_folder='web')

class RSS_HANDLE:
    RSS_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{title}</title>
<link>{link}</link>
<description>{description}</description>
<language>zh-cn</language>
{items}
</channel>
</rss>
'''
    RSS_ITEM_TEMPLATE = '''
<item>
<title>{title}</title>
<link>{link}</link>
<description>{description}</description>
<author>{author}</author>
<pubDate>{pubDate}</pubDate>
</item>
'''
    RSS_ITEM_TEMPLATE_NO_AUTHOR = '''
<item>
<title>{title}</title>
<link>{link}</link>
<description>{description}</description>
<pubDate>{pubDate}</pubDate>
</item>
'''
    RSS_ITEM_TEMPLATE_NO_PUBDATE = '''
<item>
<title>{title}</title>
<link>{link}</link>
<description>{description}</description>
<author>{author}</author>
</item>
'''
    RSS_ITEM_TEMPLATE_NO_AUTHOR_NO_PUBDATE = '''
<item>
<title>{title}</title>
<link>{link}</link>
<description>{description}</description>
</item>
'''

    def getRSSContent(title, link, description, items):
        rss_items = ""
        for item in items:
            if item is None:
                continue
            if item["author"] is None and item["pubDate"] is None:
                rss_items += RSS_HANDLE.RSS_ITEM_TEMPLATE_NO_AUTHOR_NO_PUBDATE.format(**item)
            elif item["author"] is None:
                rss_items += RSS_HANDLE.RSS_ITEM_TEMPLATE_NO_AUTHOR.format(**item)
            elif item["pubDate"] is None:
                rss_items += RSS_HANDLE.RSS_ITEM_TEMPLATE_NO_PUBDATE.format(**item)
            else:
                rss_items += RSS_HANDLE.RSS_ITEM_TEMPLATE.format(**item)
        if rss_items == "":
            return None
        return RSS_HANDLE.RSS_TEMPLATE.format(title=title, link=link, description=description, items=rss_items)

class WEB_SPIDER:
    HTTP_CONFIG = {
        "timeout": 30,
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        }
    }

    def getHTMLText(url):
        try:
            r = requests.get(url, headers=WEB_SPIDER.HTTP_CONFIG["headers"], timeout=WEB_SPIDER.HTTP_CONFIG["timeout"])
            r.raise_for_status() # 如果状态不是200，引发HTTPError异常
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            print(e)
            return None

    def getJsonText(url):
        try:
            r = requests.get(url, headers=WEB_SPIDER.HTTP_CONFIG["headers"], timeout=WEB_SPIDER.HTTP_CONFIG["timeout"])
            r.raise_for_status() # 如果状态不是200，引发HTTPError异常
            r.encoding = r.apparent_encoding
            return r.json()
        except:
            return None

class WEB_HANDLE:
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
            item = WEB_HANDLE.handle_html(url,handle_config.get('capture'))
            items.append(item)
        return RSS_HANDLE.getRSSContent(title, link, description, items)

    def handle_html(url,capture):
        web_html = WEB_SPIDER.getHTMLText(url)
        # print(web_html)
        soup = BeautifulSoup(web_html, "html.parser")
        if capture is None:
            return None
        title = WEB_HANDLE.capture_html(capture, "title", soup)
        if title is None:
            title = ""
        # 需要完整 html
        description = WEB_HANDLE.capture_html(capture, "description", soup, "html")
        if description is None:
            description = ""
        else:
            # 并对description 的html 标签编码
            description = html.escape(description)
        pubDate = WEB_HANDLE.capture_html(capture, "pubDate", soup)
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
        return RSS_HANDLE.getRSSContent(title, link, description, items)

    def handle_json(url,rule_id):
        pass

class RSS_GEN:
    def spider_xianzhi():
        items = []
        for i in range(1, 3):
            url = "https://paper.seebug.org/?page=" + str(i)
            items += RSS_GEN.handle_page(url)
        return items

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rss', methods=['GET'])
def rss():
    # 从请求中获取参数
    target = flask.request.args.get('t')

# 单文件集成，类功能提取，数据存储到sqlite数据库，定时运行
# 接口功能有主页简介概述、RSS需求网址提交、RSS订阅获取、管理端
# handle_html 改造为可以支持多级标签，并支持自动识别返回值是单个还是多个
# 配置方面还要增加字段，作为判断是否需要更新的依据
# 需要增加测试接口，用于验证配置是否正确
    
if __name__ == '__main__':
    app.run(debug=True)