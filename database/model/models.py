from database.model import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship


users_tags = Table('users_tags', db.metadata,
                   Column('user_id', Integer, ForeignKey('users.id')),
                   Column('tag_id', Integer, ForeignKey('tags.id')))

users_articles = Table('users_articles', db.metadata,
                       Column('user_id', Integer, ForeignKey('users.id')),
                       Column('article_id', Integer, ForeignKey('articles.id'))
                       )


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), nullable=False)
    nickname = Column(String(64))
    password = Column(String(50), nullable=False)

    # Many to many Users <-> Tags
    tags = relationship('Tag', secondary=users_tags,
                        backref='users',
                        lazy='dynamic')

    # Many to many Users <-> unviewed articles
    articles = relationship('Article', secondary=users_articles,
                            backref='users',
                            lazy='dynamic')

    def __repr__(self):
        return "<User (email = '%s', nickname = '%s', password = '%s')>" % \
            (self.email, self.nickname, self.password)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    # One to Many Tag -> Websites
    websites = relationship('Website', backref='tag',
                            cascade="save-update, merge, delete")

    def __repr__(self):
        return "<Tag (name = '%s')>" % self.name


class Website(db.Model):
    __tablename__ = 'websites'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    name = Column(String(120))

    # Many to One: websites -> tag
    tag_id = Column(Integer, ForeignKey('tags.id'))

    # One to Many: website -> articles
    articles = relationship('Article', backref='website',
                            cascade="save-update, merge, delete")

    def __repr__(self):
        return "<Website (name = '%s', url = '%s')>" % \
            (self.name, self.url)


class Article(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    head = Column(Text())
    url = Column(Text())
    picture = Column(Text())
    time = Column(DateTime)

    # Many to One: articles -> website
    website_id = Column(Integer, ForeignKey('websites.id'))

    def __repr__(self):
        return "<Article (head = '%s', url = '%s', date = '%s')>" % \
            (self.head, self.url, self.time)
