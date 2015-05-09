from database.model import db
from sqlalchemy.orm import sessionmaker
from database.model.models import User, Tag, Website, Article
from datetime import datetime

Session = sessionmaker(bind=db.engine)


class DatabaseSessionError(Exception):
    '''Base class of exceptions for database session.

    To handle it you can write like this:

    try:
        Create.create_user(...)
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

    def website(self, uri, name):
        '''Create website.

        Name and uri are necessary.
        Uri must be unique.
        '''
        if uri is None or "":
            raise FunctionParameterError("Uri is necessary")
        if name is None or "":
            raise FunctionParameterError("Name is necessary")
        website_exists = self.session.query(Website).filter_by(uri=uri).all()
        if not website_exists:
            self.session.add(Website(uri=uri, name=name))
            self.session.commit()
            print "Website added with success"
        else:
            self.session.rollback()
            raise AlreadyExists("Websie")

    def article(self, head, content, time=None, picture=None):
        '''Create article.

        Head and content are necessary.
        '''
        if head is None or "":
            raise FunctionParameterError("Head is necessary")
        if content is None or "":
            raise FunctionParameterError("Content is necessary")
        if time is None:
            time = datetime.utcnow()
        self.session.add(Article(head=head, content=content, time=time,
                                 picture=picture))
        self.session.commit()

    def tag(self, name):
        '''Create tag.

        Name is necessary and it must be unique
        '''
        if name is None or "":
            raise FunctionParameterError("Name is necessary")
        tag_exists = self.session.query(Tag).filter_by(name=name).all()
        if not tag_exists:
            self.session.add(Tag(name=name))
            self.session.commit()
            print "Tag added with success"
        else:
            self.session.rollback()
            raise AlreadyExists("Tag")

    def user(self, email, password, nickname=None):
        '''Create user.

        Email and password are necessary.
        Email must be unique.
        '''
        if email is None or "":
            raise FunctionParameterError("Email is required")
        if password is None or "":
            raise FunctionParameterError("Password is required")
        user_exist = self.session.query(User).filter_by(email=email).all()
        if not user_exist:
            if nickname is '' or "" or None:
                nickname = email
            user = User(email=email, nickname=nickname,
                        password=password)
            self.session.add(user)
            self.session.commit()
            print "User added with success"
        else:
            self.session.rollback()
            raise AlreadyExists("User")

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

    def article(self, id_):
        '''Get user with given email'''
        article = self.session.query(Article).filter_by(id=id_).first()
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

    def artticle(self, id_):
        article = self.session.query(Article).filter_by(id=id_).first()
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
            print('website added to tag')
        self.session.commit()
