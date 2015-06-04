from database.model import db
from sqlalchemy.orm import sessionmaker
from database.model.models import User, Tag, Website, Article
from datetime import datetime

Session = sessionmaker(bind=db.engine)


class DatabaseSessionError(Exception):
    '''Base class of exceptions for database session.

    To handle it you can write like this:

    try:
        put.user(...)
    exception DatabaseSessionError as error:
        print error
    '''
    def __init__(self, value, message=""):
        self.value = value
        self.message = message

    def __str__(self):
        return repr(self.value)

    def get_message(self):
        return self.message


class FunctionParameterError(DatabaseSessionError):
    def __init__(self, message):
        super(FunctionParameterError, self).__init__('Not all parameters'
                                                     'are passed',
                                                     message)


class Put():
    def __init__(self):
        self.session = Session()

    def website(self, url, name=None):
        '''Create website.

        Name and url are necessary.
        url must be unique.
        '''
        if not url or url is "":
            raise FunctionParameterError("url is necessary")
        if not name or name is "":
            name = url
        website_exists = self.session.query(Website).filter_by(url=url).all()
        if not website_exists:
            website = Website(url=url, name=name)
            self.session.add(website)
            self.session.commit()
            print "Website added with success"
            return website.url
        else:
            self.session.rollback()
            return None

    def article(self, head, url, time=None, picture=None):
        '''Create article.

        Head and url are necessary.
        '''
        if not head or head is "":
            raise FunctionParameterError("Head is necessary")
        if not url or url is "":
            raise FunctionParameterError("Content is necessary")
        url_exist = self.session.query(Article).filter_by(url=url).all()
        if not url_exist:
            if not time:
                time = datetime.utcnow()
            article = Article(head=head, url=url, time=time,
                              picture=picture)
            self.session.add(article)
            self.session.commit()
            print "Article added with succes"
            return article.url
        else:
            self.session.rollback()
            return None

    def tag(self, name):
        '''Create tag.

        Name is necessary and it must be unique
        '''
        if not name or name is "":
            raise FunctionParameterError("Name is necessary")
        tag_exists = self.session.query(Tag).filter_by(name=name).all()
        if not tag_exists:
            tag = Tag(name=name)
            self.session.add(tag)
            self.session.commit()
            print "Tag added with success"
            return tag.name
        else:
            self.session.rollback()
            return None

    def user(self, email, password, nickname=None):
        '''Create user.

        Email and password are necessary.
        Email must be unique.
        '''
        if not email or email is "":
            raise FunctionParameterError("Email is required")
        if not password or password is "":
            raise FunctionParameterError("Password is required")
        user_exist = self.session.query(User).filter_by(email=email).all()
        if not user_exist:
            if not nickname or nickname is "":
                nickname = email
            user = User(email=email, nickname=nickname,
                        password=password)
            self.session.add(user)
            self.session.commit()
            print "User added with success"
            return user.email
        else:
            self.session.rollback()
            return None

    def close_session(self):
        self.session.close()


class Get():
    def __init__(self):
        self.session = Session()

    def close_session(self):
        self.session.close()

    def user_tags_as_dictionary(self, email):
        '''Return user tags as a dictionary

            Dictionary of all tasks and boolean
            value which describes whether
            the user has that tag.
        '''
        user = self.user(email=email)
        if not user:
            return None
        user_tags = []
        for tag in user.tags:
            user_tags.append(tag)

        available_tags = self.all_tags()

        all_tags = dict((tag.name, tag in user_tags)
                        for tag in available_tags)

        return all_tags

    # articles based on tags
    def user_tags_and_articles(self, email):
        user = self.user(email=email)
        if not user:
            return None
        tags = []
        for tag in user.tags:
            tags.append(tag)
        articles = []
        if tags:
            for tag in tags:
                if tag.websites:
                    for web in tag.websites:
                        if web.articles:
                            for article in web.articles:
                                articles.append((article, tag))
        user_and_tags_and_articles = (user, articles)
        return user_and_tags_and_articles

    def all_users(self):
        '''Get all users as a list.'''
        users = self.session.query(User).all()
        return users

    def user(self, email):
        '''Get user with given email'''
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def all_websites(self):
        '''Get all websites as a list.'''
        websites = self.session.query(Website).all()
        return websites

    def website(self, url):
        '''Get website with given url'''
        website = self.session.query(Website).filter_by(url=url).first()
        return website

    def all_tags(self):
        '''Get all tags as a list.'''
        tags = self.session.query(Tag).order_by(Tag.name).all()
        return tags

    def tag(self, name):
        '''Get tag with given name'''
        tag = self.session.query(Tag).filter_by(name=name).first()
        return tag

    def all_articles(self):
        '''Get all articles as a list.'''
        articles = self.session.query(Article).all()
        return articles

    def article(self, url):
        '''Get user with given email'''
        article = self.session.query(Article).filter_by(url=url).first()
        return article


class Delete():
    def __init__(self):
        self.session = Session()

    def close_session(self):
        self.session.close()

    def website(self, url):
        website = self.session.query(Website).filter_by(url=url).first()
        self.session.delete(website)
        self.session.commit()

    def tag(self, name):
        tag = self.session.query(Tag).filter_by(name=name).first()
        self.session.delete(tag)
        self.session.commit()

    def artticle(self, url):
        article = self.session.query(Article).filter_by(url=url).first()
        self.session.delete(article)
        self.session.commit()

    def user(self, email):
        user = self.session.query(User).filter_by(email=email).first()
        self.session.delete(user)
        self.session.commit()

    def all_tags(self):
        '''delete all tags'''
        tags = self.session.query(Tag).all()
        for t in tags:
            self.session.delete(t)
        self.session.commit()

    def all_websties(self):
        '''delete all websites'''
        websites = self.session.query(Website).all()
        for w in websites:
            self.session.delete(w)
        self.session.commit()

    def all_articles(self):
        '''Delete all articles'''
        articles = self.session.query(Article).all()
        for a in articles:
            self.session.delete(a)
        self.session.commit()

    def all_users(self):
        '''Delete all users.'''
        users = self.session.query(User).all()
        if users:
            for u in users:
                self.session.delete(u)
                self.session.commit()


class Add():
    def __init__(self):
        self.session = Session()

    def close_session(self):
        self.session.close()

    def website_to_tag(self, tagname, website_url):
        '''Add website to tag'''
        tag_exists = self.session.query(Tag).filter_by(name=tagname).first()
        website_exists = self.session.query(Website).\
            filter_by(url=website_url).first()
        if not tag_exists or not website_exists:
            return
        for website in tag_exists.websites:
            if website is website_exists:
                return
        tag_exists.websites.append(website_exists)
        print 'website added to tag'
        self.session.commit()

    def tag_to_user(self, email, tagname):
        '''Add tag to user'''
        user_exists = self.session.query(User).filter_by(email=email).first()
        tag_exists = self.session.query(Tag).filter_by(name=tagname).first()
        if not user_exists or not tag_exists:
            return
        for tag in user_exists.tags:
            if tag is tag_exists:
                return
        user_exists.tags.append(tag_exists)
        print 'tag added to user'
        self.session.commit()

    def article_to_website(self, website_url, article_url):
        '''Add article to website'''
        website_exists = self.session.query(Website).filter_by(url=website_url).\
            first()
        article_exists = self.session.query(Article).filter_by(url=article_url).\
            first()
        if not website_exists or not article_exists:
            return
        for article in website_exists.articles:
            if article is article_exists:
                return
        website_exists.articles.append(article_exists)
        print 'article added to website'
        #dodanie nowych artykulow uzytkwnikom
        if website_exists.tag:
            tag = website_exists.tag
            for user in tag.users:
                user.articles.append(article_exists)
        self.session.commit()


def clearDb():
    delete = Delete()

    delete.all_users()
    delete.all_tags()
    delete.all_websties()
    delete.all_tags()
    delete.all_articles()

    delete.close_session()


def addUrlsAndTagsToDb():
    put = Put()
    add = Add()

    tag = 'Sport'
    url = 'http://www.premierleague.com/content/premierleague/en-gb/news/newsfeed.rss'
    name = 'Barclays Premier League'
    put.tag(tag)
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://www.nytimes.com/services/xml/rss/nyt/Sports.xml'
    name = 'New York Times - Sport'
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://www.sportingnews.com/rss'
    name = 'Sporting News'
    put.website(url, name)
    add.website_to_tag(tag, url)

    tag = 'News'
    url = 'https://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=h&num=3&output=rss'
    name = 'Google News'
    put.tag(tag)
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://www.huffingtonpost.com/feeds/verticals/germany/index.xml'
    name = 'HuffingtonPost'
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://rss.cnn.com/rss/si_topstories.rss'
    name = 'Sport Illustrated'
    put.website(url, name)
    add.website_to_tag(tag, url)

    url = 'http://www.dailymail.co.uk/home/index.rss'
    name = 'Daily Mail'
    put.website(url, name)
    add.website_to_tag(tag, url)

    add.close_session()
    put.close_session()


# when user choose tag from list
def set_user_tags(email, tags):
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    if not user:
        session.close()
        return None
    # remove tag from user
    for tag in user.tags:
        if tag.name not in tags:
            user.tags.remove(tag)
            # remove articles
            remove_articles_from_user_after_unchecking_tag(user=user, tag=tag)
    # add last ten articles
    for name in tags:
        tag = session.query(Tag).filter_by(name=name).first()
        if not tag:
            return None
        if tag not in user.tags:
            user.tags.append(tag)
            # add first 10 articles
            add_articles_to_user_after_checking_tag(user, tag)
    session.commit()
    session.close()


def mark_articles_as_readed(user_email, article_id):
    '''If article exsist remove it from user'''
    session = Session()
    user = session.query(User).filter_by(email=user_email).first()
    art = session.query(Article).filter_by(id=article_id).first()
    if user:
        if art in user.articles:
            user.articles.remove(art)
    session.commit()
    session.close()


# remove articles from user
def remove_articles_from_user_after_unchecking_tag(user, tag):
    '''After deleting tag it removes articles from user
    '''
    for article in user.articles:
        if article.website.tag == tag:
            user.articles.remove(article)


def add_articles_to_user_after_checking_tag(user, tag):
    '''Adds articles to user after selecting tag checkbox

        It adds 10 articles per each site to user
    '''
    if tag.websites:
        for web in tag.websites:
            if web.articles:
                articles = web.articles
                nr_of_added_articles = 0
                for article in articles:
                    user.articles.append(article)
                    nr_of_added_articles += 1
                    if nr_of_added_articles > 10:
                        break


def get_user_unreaded_articles_as_dict(email, tagname=None):
    '''Returns dictionary of tags and lists of articles

        {'tag.name' : [article1, article2, article3], ...}
        It returns articles for tagname, if tagname is None
        it returns dictionary of lists of articles for all tags that
        user has.
    '''
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    if not user:
        session.close()
        return None

    tags_and_articles = []
    if not tagname:
        tags = user.tags
        if not tags:
            session.close()
            return None
        articles = user.articles
        for tag in tags:
            article_for_tag = []
            for art in articles:
                if art.website.tag is tag:
                    article_for_tag.append(art)
            tags_and_articles.append([tag.name, article_for_tag])
    else:
        tag = session.query(Tag).filter_by(name=tagname).first()
        if not tag:
            session.close()
            return None
        articles = user.articles
        article_for_tag = []
        for art in articles:
            if art.website.tag is tag:
                article_for_tag.append(art)
        tags_and_articles.append([tag.name, article_for_tag])

    session.close()
    return dict(tags_and_articles)
