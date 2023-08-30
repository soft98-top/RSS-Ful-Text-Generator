from web_spider import *
from web2rss import *

def handle_page(url):
    capture = {
        "title": {"tag": "h5", "class": "post-title"},
        "pubDate": {"tag": "time", "class": "fulldate"},
        "description": {"tag": "section", "class": "post-content"}
    }
    web_html = getHTMLText(url)
    soup = BeautifulSoup(web_html, "html.parser")
    items = []
    articles = soup.find_all("article", {"class": "post"})
    for i in range(len(articles)):
        title = capture_html(capture, "title", soup=soup, index=i)
        if title is None:
            title = ""
        pubDate = capture_html(capture, "pubDate", soup=soup, index=i)
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
        description = capture_html(capture, "description", soup=soup, index=i)
        if description is None:
            description = ""
        link = capture_html(capture, "title", soup=soup, index=i, type="other")
        # 此时 link 是一个soup 对象，需要提取出href，查找当前 soup 下的 a 标签
        link = link.find("a")["href"]
        if link is None:
            link = ""
        # 此时 link 是相对路径，需要拼接成绝对路径
        link = "https://paper.seebug.org" + link
        item = {
            "title": html.escape(title),
            "link": link,
            "description": html.escape(description),
            "author": None,
            "pubDate": pubDate
        }
        items.append(item)
    return items

def spider_xianzhi():
    url = "https://paper.seebug.org/?page={}"
    items = []
    index = 1
    while True:
        page_url = url.format(index)
        print(page_url)
        page_items = handle_page(page_url)
        if len(page_items) == 0:
            break
        items.extend(page_items)
        index += 1
        time.sleep(1)
    return items