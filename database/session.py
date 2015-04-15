from database.model import db
from sqlalchemy.orm import sessionmaker
from database.model.models import User, Tag, Article
import types

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
        tag_exist = session.query(Tag).filter_by(name=name).all()
        if not tag_exist:
            session.add(Tag(name=name))
            session.commit()
            print "Tag added with success"
        else:
            session.rollback()
            session.close()
            raise AlreadyExists("Tag")

    @staticmethod
    def articles():
        pass


class Delete():
    def users(self):
        pass

    def tags(self):
        pass

    def websites(self):
        pass

    def artticles(self):
        pass

    @staticmethod
    def all_tags():
        pass

    @staticmethod
    def all_websties():
        pass

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
