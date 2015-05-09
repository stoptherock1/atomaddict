from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
articles = Table('articles', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('head', Text),
    Column('content', Text),
    Column('picture', Text),
    Column('time', DateTime),
    Column('website_id', Integer),
)

tags = Table('tags', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=30)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120), nullable=False),
    Column('nickname', String(length=64)),
    Column('password', String(length=50), nullable=False),
)

users_articles = Table('users_articles', post_meta,
    Column('user_id', Integer),
    Column('article_id', Integer),
)

users_tags = Table('users_tags', post_meta,
    Column('user_id', Integer),
    Column('tag_id', Integer),
)

websites = Table('websites', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('uri', Text, nullable=False),
    Column('name', String(length=120)),
    Column('tag_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['articles'].create()
    post_meta.tables['tags'].create()
    post_meta.tables['users'].create()
    post_meta.tables['users_articles'].create()
    post_meta.tables['users_tags'].create()
    post_meta.tables['websites'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['articles'].drop()
    post_meta.tables['tags'].drop()
    post_meta.tables['users'].drop()
    post_meta.tables['users_articles'].drop()
    post_meta.tables['users_tags'].drop()
    post_meta.tables['websites'].drop()
