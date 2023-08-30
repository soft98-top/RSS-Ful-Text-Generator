from web2rss import *
from spider_xianzhi import *
import json

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


# 从配置中获取处理规则
def get_handle_config(rule_id):
    return HANDLE_RULE.get(rule_id)
# 转义数据
def data_escape(items):
    escape_items = []
    for item in items:
        item["title"] = html.escape(item["title"])
        item["description"] = html.escape(item["description"])
        escape_items.append(item)
    return escape_items

def test1():
    '''测试生成rss全文本'''
    urls = [
        "https://paper.seebug.org/3012/"
    ]
    print(genrate_rss_by_html(urls,get_handle_config('xianzhi')))

def test2():
    '''测试先知社区单页面解析'''
    url = "https://paper.seebug.org/?page=1"
    items = handle_page(url)
    print(items)
    print(json.dumps(items,indent=4,ensure_ascii=False))

def test3():
    '''测试先知社区爬虫'''
    items = spider_xianzhi()
    # 保存到文件
    with open("xianzhi.json","w",encoding="utf-8") as f:
        json.dump(items,f,indent=4,ensure_ascii=False)

def test4():
    '''测试先知社区json生成rss'''
    # 从文件读取
    with open("xianzhi.json","r",encoding="utf-8") as f:
        items = json.load(f)
    rss_data = genrate_rss_by_json(get_handle_config('xianzhi'),items)
    # 写入文件
    with open("xianzhi.xml","w",encoding="utf-8") as f:
        f.write(rss_data)