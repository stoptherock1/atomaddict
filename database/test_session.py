from database.session import Delete, Get, Put, Add


if __name__ == "__main__":
#     delete = Delete()
# # delete all
#     delete.all_users()
#     delete.all_tags()
#     delete.all_websties()
#     delete.all_tags()
#     delete.all_articles()
#     delete.close_session()
    # You can delete also by delete.user(email='...')
    # put some things
    put = Put()
    user = put.user(email='piotrek@gmail', password='piotrek',
                    nickname='Piotrek')
    user = 'piotrek@gmail'
    cnn = put.website(url='http://rss.cnn.com/rss/cnn_topstories.rss',
                      name='cnn.com')
    nyt = put.website(url='http://rss.nytimes.com/services/xml/rss/nyt/HomePage\
.xml',
                      name='New York Times')
    gadget_of_the_week = put.website(url='http://feeds.feedburner.com/time/\
gadgetoftheweek',
                                         name='Gadget of the Week')
    world_news = put.tag(name='Worlds News')

    science = put.tag(name='Science')

    a3 = put.article(head='3DConnexion SpaceNavigator',
                     url='http://content.time.com/time/business/article/0,8599,\
1573203,00.html?utm_source=feedburner&utm_medium=feed&utm_\
campaign=Feed%3A+time%2Fgadgetoftheweek+%28TIME%3A+Gadget+\
of+the+Week%29&utm_content=FeedBurner',
                     picture='http://img.timeinc.net/time/daily/2007/facelift/\
360_space_0102.jpg')

    a4 = put.article(head='Panasonic Plasma and More',
                     url='http://content.time.com/time/business/article/0,8599\
,1571909,00.html?utm_source=feedburner&utm_medium=feed&utm\
_campaign=Feed%3A+time%2Fgadgetoftheweek+%28TIME%3A+Gadget\
+of+the+Week%29&utm_content=FeedBurner',
                     picture='http://img.timeinc.net/time/daily/2006/facelift/\
                     360_panasonic42inchplasma.jpg')
    a5 = put.article(head='Nikon D40 Digital SLR Camera',
                     url='http://content.time.com/time/business/article/0,8599,\
1566933,00.html?utm_source=feedburner&utm_medium=feed&utm_\
campaign=Feed%3A+time%2Fgadgetoftheweek+%28TIME%3A+Gadget+\
of+the+Week%29&utm_content=FeedBurner')

    put.close_session()

    # add some things

    add = Add()
    add.website_to_tag(tagname=world_news, website_url=cnn)
    add.website_to_tag(tagname=world_news, website_url=nyt)
    add.website_to_tag(tagname=science, website_url=gadget_of_the_week)

    add.article_to_website(website_url=gadget_of_the_week, article_url=a3)
    add.article_to_website(website_url=gadget_of_the_week, article_url=a4)
    add.article_to_website(website_url=gadget_of_the_week, article_url=a5)

    add.close_session()

    # get some things

    get = Get()
    users = get.all_users()
    print users
    websites = get.all_websites()
    print websites
    for w1 in websites:
        print w1.tag

#     tags = get.tag(world_news)
#     print tags
#     print tags.websites
#     for web in tags.websites:
#         print web.articles

    get.close_session()

    add = Add()

    print "---------------------"
    add.tag_to_user(user, world_news)
    add.tag_to_user(user, 'Sport')
    add.tag_to_user(user, 'News')
    add.tag_to_user(user, science)

    add.close_session()
    print "-----------------------"
    get = Get()
    print user
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
