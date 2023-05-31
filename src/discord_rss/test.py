from modules.db_operate import urlDatabase
import modules.parse_rss as parse_rss

if __name__ == "__main__":
    db = urlDatabase()
    db.addUrl('aaa')
    print(db.getData('url'))
    for url in db.getData('url'):
        parsed = parse_rss.parse_rss(url[0])
        for item in parsed:
            print(item['title'])

