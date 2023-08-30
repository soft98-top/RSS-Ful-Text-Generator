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
            rss_items += RSS_ITEM_TEMPLATE_NO_AUTHOR_NO_PUBDATE.format(**item)
        elif item["author"] is None:
            rss_items += RSS_ITEM_TEMPLATE_NO_AUTHOR.format(**item)
        elif item["pubDate"] is None:
            rss_items += RSS_ITEM_TEMPLATE_NO_PUBDATE.format(**item)
        else:
            rss_items += RSS_ITEM_TEMPLATE.format(**item)
    if rss_items == "":
        return None
    return RSS_TEMPLATE.format(title=title, link=link, description=description, items=rss_items)