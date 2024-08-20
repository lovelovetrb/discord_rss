import feedparser


# RSS Feed URL
def parse_rss(url):
    d = feedparser.parse(url)
    feed = []
    for index, entry in enumerate(d.entries):
        if index == 3:
            break
        else:
            temp = {}
            temp["title"] = entry.title
            temp["link"] = entry.link
            feed.append(temp)
    return feed
