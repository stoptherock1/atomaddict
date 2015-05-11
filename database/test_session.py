from database.session import Delete, Get, Put, Add


if __name__ == "__main__":
    delete = Delete()
#   delete all
    delete.all_users()
    delete.all_tags()
    delete.all_websties()
    delete.all_tags()
    delete.all_articles()
    delete.close_session()
    # You can delete also by delete.user(email='...')
    # put some things
    put = Put()
    user = put.user(email='piotrek@gmail', password='piotrek',
                    nickname='Piotrek')

#    W zasadzie to mozna by tak:
#
#     put = Put()
#     try:
#         put.user(...)
#         put.website(uri='...', name='...') etc. etc.
#     exception DatabaseSessionError as error:
#         Handle error ->
#         Poprzez print error dostaniesz odpowiedz typu 'already exist', albo
#                         'not all parameters are passed' itp
#
    cnn = put.website(uri='http://rss.cnn.com/rss/cnn_topstories.rss',
                      name='cnn.com')
    nyt = put.website(uri='http://rss.nytimes.com/services/xml/rss/nyt/HomePage \
                          .xml',
                      name='New York Times')
    gadget_of_the_week = put.website(uri='http://feeds.feedburner.com/time/ \
                                         gadgetoftheweek',
                                         name='Gadget of the Week')
    world_news = put.tag(name='Worlds News')

    science = put.tag(name='Science')

    a1 = put.article(head='33 million in U.S. under severe weather threat',
                     uri='adsf')
    a2 = put.article(head='Tropical Storm Ana notches down as it hits \
                           South Carolina',
                     uri='adsfdfsdf')
    a3 = put.article(head='3DConnexion SpaceNavigator',
                     uri='http://content.time.com/time/business/article/0,8599,\
                     1573203,00.html?utm_source=feedburner&utm_medium=feed&utm_\
                     campaign=Feed%3A+time%2Fgadgetoftheweek+%28TIME%3A+Gadget+\
                     of+the+Week%29&utm_content=FeedBurner',
                     picture='http://img.timeinc.net/time/daily/2007/facelift/\
                     360_space_0102.jpg')

    a4 = put.article(head='Panasonic Plasma and More',
                     uri='http://content.time.com/time/business/article/0,8599\
                     ,1571909,00.html?utm_source=feedburner&utm_medium=feed&utm\
                     _campaign=Feed%3A+time%2Fgadgetoftheweek+%28TIME%3A+Gadget\
                     +of+the+Week%29&utm_content=FeedBurner',
                     picture='http://img.timeinc.net/time/daily/2006/facelift/\
                     360_panasonic42inchplasma.jpg')
    a5 = put.article(head='Nikon D40 Digital SLR Camera',
                     uri='http://content.time.com/time/business/article/0,8599,\
                     1566933,00.html?utm_source=feedburner&utm_medium=feed&utm_\
                     campaign=Feed%3A+time%2Fgadgetoftheweek+%28TIME%3A+Gadget+\
                     of+the+Week%29&utm_content=FeedBurner')
    put.close_session()

    # add some things

    add = Add()
    add.website_to_tag(tagname=world_news, website_uri=cnn)
    add.website_to_tag(tagname=world_news, website_uri=nyt)
    add.website_to_tag(tagname=science, website_uri=gadget_of_the_week)

    add.article_to_website(website_uri=cnn, article_uri=a1)
    add.article_to_website(website_uri=cnn, article_uri=a2)
    add.article_to_website(website_uri=gadget_of_the_week, article_uri=a3)
    add.article_to_website(website_uri=gadget_of_the_week, article_uri=a4)
    add.article_to_website(website_uri=gadget_of_the_week, article_uri=a5)
    add.close_session()

    # get some things

    get = Get()
    users = get.all_users()
    print users
    websites = get.all_websites()
    print websites
    for w1 in websites:
        print w1.tag

    tags = get.tag(world_news)
    print tags
    print tags.websites
    for web in tags.websites:
        print web.articles

    get.close_session()

    add = Add()
    add.tag_to_user(user, world_news)
    add.tag_to_user(user, science)

    add.close_session()

    get = Get()
    user = get.user(email=user)
    print user
    print user.tags
    if user.tags:
        for tag in user.tags:
            print tag
            if tag.websites:
                for web in tag.websites:
                    print web

    print "user"
    user = get.all_users()[0]

    print user.email
    print user.tags
    for tag in user.tags:
        print tag

    get.close_session()
