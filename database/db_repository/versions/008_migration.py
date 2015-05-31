from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users_articles = Table('users_articles', pre_meta,
    Column('user_id', INTEGER),
    Column('article_id', INTEGER),
)

users_readed_articles = Table('users_readed_articles', post_meta,
    Column('user_id', Integer),
    Column('article_id', Integer),
)

users_unreaded_articles = Table('users_unreaded_articles', post_meta,
    Column('user_id', Integer),
    Column('article_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users_articles'].drop()
    post_meta.tables['users_readed_articles'].create()
    post_meta.tables['users_unreaded_articles'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users_articles'].create()
    post_meta.tables['users_readed_articles'].drop()
    post_meta.tables['users_unreaded_articles'].drop()
