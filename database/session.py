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


class AlreadyExists(DatabaseSessionError):
    def __init__(self, value):
        super(AlreadyExists, self).__init__(value + 'already exist')


class FunctionParameterError(DatabaseSessionError):
    def __init__(self, message):
        super(FunctionParameterError, self).__init__('Not all parameters'
                                                     'are passed',
                                                     message)


class Put():
    def __init__(self):
        self.session = Session()

    def website(self, uri, name=None):
        '''Create website.

        Name and uri are necessary.
        Uri must be unique.
        '''
        if not uri or uri is "":
            raise FunctionParameterError("Uri is necessary")
        if not name or name is "":
            name = uri
        website_exists = self.session.query(Website).filter_by(uri=uri).all()
        if not website_exists:
            website = Website(uri=uri, name=name)
            self.session.add(website)
            self.session.commit()
            print "Website added with success"
            return website.uri
        else:
            self.session.rollback()
            raise AlreadyExists("Websie")
            return None

    def article(self, head, uri, time=None, picture=None):
        '''Create article.

        Head and uri are necessary.
        '''
        if not head or head is "":
            raise FunctionParameterError("Head is necessary")
        if not uri or uri is "":
            raise FunctionParameterError("Content is necessary")
        uri_exist = self.session.query(Article).filter_by(uri=uri).all()
        if not uri_exist:
            if not time:
                time = datetime.utcnow()
            article = Article(head=head, uri=uri, time=time,
                              picture=picture)
            self.session.add(article)
            self.session.commit()
            print "Article added with succes"
            return article.uri
        else:
            self.session.rollback()
            raise AlreadyExists("Article")
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
            raise AlreadyExists("Tag")
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
            if nickname is (None or ""):
                nickname = email
            user = User(email=email, nickname=nickname,
                        password=password)
            self.session.add(user)
            self.session.commit()
            print "User added with success"
            return user.email
        else:
            self.session.rollback()
            raise AlreadyExists("User")
            return None

    def close_session(self):
        self.session.close()


class Get():
    def __init__(self):
        self.session = Session()

    def close_session(self):
        self.session.close()

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

    def website(self, uri):
        '''Get website with given uri'''
        website = self.session.query(Website).filter_by(uri=uri).first()
        return website

    def all_tags(self):
        '''Get all tags as a list.'''
        tags = self.session.query(Tag).all()
        return tags

    def tag(self, name):
        '''Get tag with given name'''
        tag = self.session.query(Tag).filter_by(name=name).first()
        return tag

    def all_articles(self):
        '''Get all articles as a list.'''
        articles = self.session.query(Article).all()
        return articles

    def article(self, uri):
        '''Get user with given email'''
        article = self.session.query(Article).filter_by(uri=uri).first()
        return article


class Delete():
    def __init__(self):
        self.session = Session()

    def close_session(self):
        self.session.close()

    def website(self, uri):
        website = self.session.query(Website).filter_by(uri=uri).first()
        self.session.delete(website)
        self.session.commit()

    def tag(self, name):
        tag = self.session.query(Tag).filter_by(name=name).first()
        self.session.delete(tag)
        self.session.commit()

    def artticle(self, uri):
        article = self.session.query(Article).filter_by(uri=uri).first()
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

    def website_to_tag(self, tagname, website_uri):
        '''Add website to tag'''
        tag_exists = self.session.query(Tag).filter_by(name=tagname).first()
        website_exists = self.session.query(Website).\
            filter_by(uri=website_uri).first()
        if tag_exists and website_exists:
            tag_exists.websites.append(website_exists)
            print 'website added to tag'
        self.session.commit()

    def tag_to_user(self, email, tagname):
        '''Add tag to user'''
        user_exists = self.session.query(User).filter_by(email=email).first()
        tag_exists = self.session.query(Tag).filter_by(name=tagname).first()
        if tag_exists and user_exists:
            user_exists.tags.append(tag_exists)
            print 'tag added to user'
        self.session.commit()

    def article_to_website(self, website_uri, article_uri):
        '''Add article to website'''
        website_exists = self.session.query(Website).filter_by(uri=website_uri).\
            first()
        article_exists = self.session.query(Article).filter_by(uri=article_uri).\
            first()
        if website_exists and article_exists:
            website_exists.articles.append(article_exists)
            print 'article added to website'
        self.session.commit()
