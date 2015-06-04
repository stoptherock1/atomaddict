from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users_unreaded_articles = Table('users_unreaded_articles', pre_meta,
    Column('user_id', INTEGER),
    Column('article_id', INTEGER),
)

settings = Table('settings', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('language', String(length=15)),
    Column('tile_size', String(length=10)),
    Column('user_id', Integer),
)

users_unread_articles = Table('users_unread_articles', post_meta,
    Column('user_id', Integer),
    Column('article_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users_unreaded_articles'].drop()
    post_meta.tables['settings'].create()
    post_meta.tables['users_unread_articles'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users_unreaded_articles'].create()
    post_meta.tables['settings'].drop()
    post_meta.tables['users_unread_articles'].drop()
