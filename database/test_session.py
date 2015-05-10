from database.session import Delete, Get, Put, Add


if __name__ == "__main__":

    
    
    
    
    
    # delete all

    delete = Delete()
    delete.all_users()
    delete.all_tags()
    delete.all_websties()
    delete.all_tags()
    delete.all_articles()
    delete.close_session()
    
    # You can delete also by delete.user(email='...')

    # put some things
    

    put = Put()
    put.user(email='Alice@gmail', password='Alicepass', nickname='Alice')
    put.user(email='George@gmail', password='George', nickname='George')
    put.user(email='Adam@gmail', password='Adam', nickname='Adam')
    put.user(email='Bob@gmail', password='Bob', nickname='')
    put.user(email='Margaret@gmail', password='Margaret', nickname='Margaret')
    
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



    

    put.website(uri='google.com', name='google')
    put.website(uri='wp.pl', name='wp')
    put.website(uri='premierleague.com', name='liga angielska')
    put.website(uri='pudelek.pl', name=None)

    put.tag(name='informacje')
    put.tag(name='sport')
    put.tag(name='smieci')

    a1 = put.article(head='super wygrana', content='super wygrana druzyny')
    a2 = put.article(head='paris hilton', content='paris hilton na pokazie')
    a3 = put.article(head='paris asdfhilton', content='asdfparis hilton na ' +
                     'pokazie')
    a4 = put.article(head='pozar', content='wielkipozar!')
    put.close_session()

    # add some things

    add = Add()
    add.website_to_tag(tagname='informacje', website_uri='google.com')
    add.website_to_tag(tagname='sport', website_uri='premierleague.com')
    add.website_to_tag(tagname='informacje', website_uri='wp.pl')
    add.website_to_tag(tagname='smieci', website_uri='pudelek.pl')

    add.tag_to_user(email='Adam@gmail', tagname='informacje')
    add.tag_to_user(email='Bob@gmail', tagname='informacje')
    add.article_to_website(website_uri='wp.pl', article_id=a4)
    add.article_to_website(website_uri='google.com', article_id=a4)
    add.article_to_website(website_uri='premierleague.com', article_id=a1)
    add.article_to_website(website_uri='pudelek.pl', article_id=a2)
    add.article_to_website(website_uri='pudelek.pl', article_id=a3)
    add.close_session()

    # get some things

    get = Get()
    users = get.all_users()
    print users
    websites = get.all_websites()
    print websites
    for w1 in websites:
        print w1.tag

    tags = get.tag('informacje')
    print tags.websites

    articles = get.all_articles()
    print articles
    for a in articles:
        print a.website
        print a.users

    user = get.user(email='Adam@gmail')
    print "\n", user
    for t in user.tags:
        print t
        for w in t.websites:
            print w
            for a in w.articles:
                print a

    get.close_session()
 
 
 # wypis z konsoli   
#===============================================================================
#         import sys; print('%s %s' % (sys.executable or sys.platform, sys.version))
# PyDev console: starting.
# C:\Program Files\Python27\python.exe 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)]
#  
# from database.session import Get
# get = Get()
# wesites = get.all_websites()
# websites = wesites
# websites
# [<Website (name = 'WPPL', uri = 'wp.pl')>, <Website (name = 'jakies gowno', uri = 'costam.com')>]
# get.website(uri="google")
# web = get.website(uri="google")
# web
# web = get.website(uri="wp.pl")
# web
# <Website (name = 'WPPL', uri = 'wp.pl')>
# web.name
# u'WPPL'
# web.uri
# u'wp.pl'
# web.tag
# get.close_session()
# from database.session import Add
# Add
# <class database.session.Add at 0x00000000038E6E28>
# add = Add()
# add.website_to_tag(tagname='informacje', website_uri='wp.pl')
# website added to tag
# add.close_session()
# get = Get()
# web = get.website(uri='wp.pl')
# web
# <Website (name = 'WPPL', uri = 'wp.pl')>
# web.tag
# <Tag (name = 'informacje')>
# get.close_session()
# web
# <Website (name = 'WPPL', uri = 'wp.pl')>
# web.name
# u'WPPL'
# web.tag
# <Tag (name = 'informacje')>
# web.tag.users
#        
#        
#        
#        
#        
#        
#        
#        
#        
#     # delete all
#        
# #     session = Session()
# #     session.query(Website).add(uri="google", name="asdasdas")
# #     session.commit()
# #     session.close()
# #     session = Session()
# #     websites = session.query(Website).all()
# #     website = session.query(Website).filter_by(uri="google").first()
# #     
# #     # Put(), Get(), Add(), Delete()
# #     
# #     put = Put()
# #     put.website(uri, name)
# #     put.user(email, password, nickname)
# #     put.close()
# #     
# #     get = Get()
# #     website = get.website(uri="asdasd)
# #     website.
# #     get.close()
# #     
# #     
# #     
# #     #------------------------------------------
# #     
#        
#===============================================================================