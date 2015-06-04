import database.session
import tasks
from dateutil import parser


def fetchDataByTag(tagName):

    get = database.session.Get()
    put = database.session.Put()
    add = database.session.Add()

    pages = []

    if tagName == 'all':
        pages = get.all_websites()
    else:
        tag = get.tag(tagName)
        tags = get.all_tags()

        if tag.websites:
            for website in tag.websites:
                pages.append(website)

    parsedPages = []

    for page in pages:
        # celery task
        parsedPages.append(tasks.downloadFeeds.delay(page.url))

    for parsedPage in parsedPages:
        while(False == parsedPage.ready()):
            pass

        # parsed rss feed
        pageUrl, data = parsedPage.get()

        for entry in data.entries:
            if 'published' in entry:
                time = parser.parse(entry.published)
            else:
                time = None
            title = entry.get('title', 'No Title')
            link = None
            picture = None
            if 'links' in entry:
                links = entry.links
                if links.__len__() >= 1:
                    link = links[0].href
                if links.__len__() >= 2:
                    picture = links[1].href

            put.article(head=title, url=link, time=time, picture=picture)
            add.article_to_website(website_url=pageUrl, article_url=entry.link)

    get.close_session()
    put.close_session()
    add.close_session()


if __name__ == "__main__":
    print('\n** START OF ' + __name__ + 'flask app **\n')

    get = database.session.Get()

    # clearDb()
#     database.session.addUrlsAndTagsToDb()

#     fetchDataByTag('News')
    fetchDataByTag('all')

#     articles = get.all_articles()
#
#     print(len(articles))
#     print(articles)

    get.close_session()

    print('\n** END OF ' + __name__ + ' **')

