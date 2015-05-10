import database.session
import tasks

def clearDb():
    delete = database.session.Delete()

    delete.all_users()
    delete.all_tags()
    delete.all_websties()
    delete.all_tags()
    delete.all_articles()

    delete.close_session()


def addUrlsToDb():
    put = database.session.Put()
    add = Add()

    tag = 'Sport'
    url = 'http://www.premierleague.com/content/premierleague/en-gb/news/newsfeed.rss'
    name ='Barclays Premier League'
    put.website(url, name)

    tag = 'News'
    url = 'https://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=h&num=3&output=rss'
    name ='Google News'
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://www.huffingtonpost.com/feeds/verticals/germany/index.xml'
    name ='HuffingtonPost'
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    name ='New York Times'
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://www.dailymail.co.uk/home/index.rss'
    name ='Daily Mail'
    put.website(url, name)
    add.website_to_tag(tag, url)


    put.close_session()
    add.close_session()



def fetchDataFromAllWebsites():
    get = database.session.Get()
    pages = get.all_websites()

    results = []

    for page in pages:
        url = page.uri
        results.append( tasks.downloadFeeds.delay(url) )

    i = 1
    for result in results:
        while( False == result.ready() ):
            pass

        data = result.get()     #parsed rss feed
        counter = 1

        print('task {0} is ready;'.format(i) )
        print('Number of entries : {0}\n'.format( len(data.entries) ) )

        for entry in data.entries:
            print('Entry {0}'.format(counter) )
            print('Title: ' + entry.title)
            print('Link: ' + entry.link)
            print('Posted: {0}'.format(entry.published) )
            print('\n')
            counter += 1

        i += 1

    get.close_session()




if __name__ == "__main__":
    print('\n** START OF ' + __name__ + 'flask app **\n')

    fetchDataFromAllWebsites()

    # t1 = tasks.task1.delay(4, 4)
    #
    # while( False == t1.ready() ):
    # print('wait for task1')
    #
    # print( 'task1 is ready; result = {0}'.format( t1.get() ) )


    # user = database.session.Get.user(email='Adam@gmail')

    #
    # users = get.all_users()
    # user = get.user(email='Adam@gmail')
    #


    # print(websites)



    # for i in

    # url = 'http://www.premierleague.com/content/premierleague/en-gb/news/newsfeed.rss'
    #
    # downloadTask = tasks.downloadFeeds.delay(url)
    #
    # while( not downloadTask.ready() ):
    #     pass


        # print('wait for tasks.downloadFeeds(url)')

    # data = downloadTask.get()

    # counter = 1

    # print('Number of entries : {0}\n'.format( len(data.entries) ) )
    #
    # for entry in data.entries:
    #     print('Entry {0}'.format(counter) )
    #     print('Title: ' + entry.title)
    #     print('Link: ' + entry.link)
    #     print('Posted: {0}'.format(entry.published) )
    #     print('\n')
    #     counter += 1


    # get



    print('\n** END OF ' + __name__ + ' **')