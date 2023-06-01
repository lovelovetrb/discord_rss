import feedparser

# RSS Feed URL


def parse_rss(url):
    d = feedparser.parse(url)
    feed = []
    for index, entry in enumerate(d.entries):
        temp = {}
        temp['title'] = entry.title
        temp['link'] = entry.link
        feed.append(temp)
        if(index == 3):
            break
    return feed

