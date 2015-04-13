from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
article = Table('article', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('head', TEXT),
    Column('content', TEXT),
    Column('picture', TEXT),
    Column('time', DATETIME),
    Column('website_id', INTEGER),
)

articles = Table('articles', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('head', Text),
    Column('content', Text),
    Column('picture', Text),
    Column('time', DateTime),
    Column('website_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['article'].drop()
    post_meta.tables['articles'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['article'].create()
    post_meta.tables['articles'].drop()
