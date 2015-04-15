from database.model import db
from sqlalchemy.orm import sessionmaker
from database.model.models import User, Tag, Article, Website
import types
from datetime import datetime

Session = sessionmaker(bind=db.engine)


class DatabaseSessionError(Exception):
    '''Base class of exceptions for database session.

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


class Create():
    @staticmethod
    def users(list_of_users):
        '''Create users.

        users([(...),(...)]
        They must be passed as a list of tuples, which should
        look like this one:
        (email, password, nickname)
        '''
        if isinstance(list_of_users, types.ListType):
            for user in list_of_users:
                if isinstance(user, types.TupleType):
                    if len(user) == 2:
                        Create.user(email=user[0], password=user[1])
                    elif len(user) == 3:
                        Create.user(email=user[0], password=user[1],
                                    nickname=user[2])

    @staticmethod
    def user(email, password, nickname=None):
        '''Create user.

        Email and password are necessary.
        '''
        if email is None or "":
            raise FunctionParameterError("Email is required")
        if password is None or "":
            raise FunctionParameterError("Password is required")
        session = Session()
        user_exist = session.query(User).filter_by(email=email).all()
        if not user_exist:
            if nickname is None or "":
                nickname = email
            user = User(email=email, nickname=nickname, password=password)
            session.add(user)
            session.commit()
            print "User added with success"
        else:
            session.rollback()
            session.close()
            raise AlreadyExists("User")
        session.close()

    @staticmethod
    def websites():
        pass

    @staticmethod
    def website(uri, name):
        '''Create website.

        Name and uri are necessary.
        '''
        if uri is None or "":
            raise FunctionParameterError("Uri is necessary")
        if name is None or "":
            raise FunctionParameterError("Name is necessary")
        session = Session()
        website_exists = session.query(Website).filter_by(uri=uri).all()
        if not website_exists:
            session.add(Website(uri=uri, name=name))
            session.commit()
            print "Website added with success"
        else:
            session.rollback()
            session.close()
            raise AlreadyExists("Websie")
        session.close()

    @staticmethod
    def tags(list_of_tags):
        '''Create tags.

        They must be passed as a list, which should
        contains their names.
        '''
        if isinstance(list_of_tags, types.ListType):
            for tag in list_of_tags:
                Create.tag(name=str(tag))

    @staticmethod
    def tag(name):
        '''Create tag.

        Name is necessary and it must be unique
        '''
        if name is None or "":
            raise FunctionParameterError("Name is necessary")
        session = Session()
        tag_exists = session.query(Tag).filter_by(name=name).all()
        if not tag_exists:
            session.add(Tag(name=name))
            session.commit()
            print "Tag added with success"
        else:
            session.rollback()
            session.close()
            raise AlreadyExists("Tag")
        session.close()

    @staticmethod
    def articles():
        pass

    @staticmethod
    def article(head, content, time=None, picture=None):
        '''Create article.

        Head and content are necessary.
        '''
        if head is None or "":
            raise FunctionParameterError("Head is necessary")
        if content is None or "":
            raise FunctionParameterError("Content is necessary")
        session = Session()
        if time is None:
            time = datetime.utcnow()
        session.add(Article(head=head, content=content, time=time,
                            picture=picture))
        session.commit()
        session.close()


class Delete():
    @staticmethod
    def user(email):
        session = Session()
        user = session.query(User).filter_by(email=email).first()
        session.delete(user)
        session.commit()
        session.close()

    @staticmethod
    def tag(name):
        session = Session()
        tag = session.query(Tag).filter_by(name=name).first()
        session.delete(tag)
        session.commit()
        session.close()

    @staticmethod
    def website(uri):
        session = Session()
        website = session.query(Website).filter_by(uri=uri).first()
        session.delete(website)
        session.commit()
        session.close()

    @staticmethod
    def artticle(id_):
        session = Session()
        article = session.query(Article).filter_by(id=id_).first()
        session.delete(article)
        session.commit()
        session.close()

    @staticmethod
    def all_tags():
        '''delete all tags'''
        session = Session()
        tags = session.query(Tag).all()
        for t in tags:
            session.delete(t)
        session.commit()
        session.close()

    @staticmethod
    def all_websties():
        '''delete all websites'''
        session = Session()
        websites = session.query(Website).all()
        for w in websites:
            session.delete(w)
        session.commit()
        session.close()

    @staticmethod
    def all_articles():
        '''Delete all articles'''
        session = Session()
        articles = session.query(Article).all()
        for a in articles:
            session.delete(a)
        session.commit()
        session.close()

    @staticmethod
    def all_users():
        '''Delete all users.'''
        session = Session()
        users = session.query(User).all()
        if users:
            for u in users:
                session.delete(u)
                session.commit()
        session.close()


class Get():
    @staticmethod
    def all_users():
        '''Get all users as a list.'''
        session = Session()
        users = session.query(User).all()
        session.close()
        return users

    @staticmethod
    def user(email):
        '''Get user with given email'''
        session = Session()
        user = session.query(User).filter_by(email=email).first()
        session.close()
        return user

    @staticmethod
    def all_websites():
        '''Get all websites as a list.'''
        session = Session()
        websites = session.query(Website).all()
        session.close()
        return websites

    @staticmethod
    def website(uri):
        '''Get website with given uri'''
        session = Session()
        website = session.query(Website).filter_by(uri=uri).first()
        session.close()
        return website

    @staticmethod
    def all_tags():
        '''Get all tags as a list.'''
        session = Session()
        tags = session.query(Tag).all()
        session.close()
        return tags

    @staticmethod
    def tag(name):
        '''Get tag with given name'''
        session = Session()
        tag = session.query(Tag).filter_by(name=name).first()
        session.close()
        return tag

    @staticmethod
    def all_articles():
        '''Get all articles as a list.'''
        session = Session()
        articles = session.query(Article).all()
        session.close()
        return articles

    @staticmethod
    def article(id_):
        '''Get user with given email'''
        session = Session()
        article = session.query(Article).filter_by(id=id_).first()
        session.close()
        return article

    @staticmethod
    def users_tags(email):
        '''Get user's tags as a list.'''
        session = Session()
        user = session.query(User).filter_by(email=email).first()
        tags = user.tags.all()
        session.close()
        return tags

    @staticmethod
    def users_websites(email):
        '''Get user's websites as a list'''
        session = Session()
        user = session.query(User).filter_by(email=email).first()
        websites = []
        tags = user.tags.all()
        for tag in tags:
            websites.append(tag.websites.all())
        session.close()
        return websites

    @staticmethod
    def tags_websites(name):
        '''Get tag's websites as a list'''
        session = Session()
        tag = session.query(Tag).filter_by(name=name).first()
        websites = tag.websites.all()
        session.close()
        return websites


class Add():
    @staticmethod
    def tag_to_user(email, tagname):
        '''Add tag to user'''
        session = Session()
        user_exists = session.query(User).filter_by(email=email).first()
        tag_exists = session.query(Tag).filter_by(name=tagname).first()
        if tag_exists and user_exists:
            user_exists.tags.append(tag_exists)
        session.commit()
        session.close()

    @staticmethod
    def website_to_tag(tagname, website_uri):
        '''Add website to tag'''
        session = Session()
        tag_exists = session.query(Tag).filter_by(name=tagname).first()
        website_exists = session.query(Website).\
            filter_by(uri=website_uri).first()
        if tag_exists and website_exists:
            tag_exists.websites.append(website_exists)
        session.commit()
        session.close()

    @staticmethod
    def article_to_website(website_uri, article_id):
        '''Add article to website'''
        session = Session()
        website_exists = session.query(Website).filter_by(uri=website_uri).\
            first()
        article_exists = session.query(Article).filter_by(id=article_id).\
            first()
        if website_exists and article_exists:
            website_exists.articles.append(article_exists)
