import database.session
import tasks
from dateutil import parser
from database.session import DatabaseSessionError

##python-dateutil


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
        parsedPages.append( tasks.downloadFeeds.delay(page.uri) )        #celery task

    for parsedPage in parsedPages:
        while( False == parsedPage.ready() ):
            pass

        pageUrl, data = parsedPage.get()     #parsed rss feed

        for entry in data.entries:
            time = parser.parse(entry.published)
            put.article(head = entry.title, uri = entry.link, time = time)
            add.article_to_website(website_uri = pageUrl, article_uri = entry.link)


    get.close_session()
    put.close_session()
    add.close_session()


if __name__ == "__main__":
    print('\n** START OF ' + __name__ + 'flask app **\n')

    get = database.session.Get()

    # clearDb()
    database.session.addUrlsAndTagsToDb()

    fetchDataByTag('News')
    # fetchDataByTag('all')

    articles = get.all_articles()

    print(len(articles))
    print(articles)

    get.close_session()

    print('\n** END OF ' + __name__ + ' **')

