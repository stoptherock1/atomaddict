from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
settings = Table('settings', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('language', VARCHAR(length=15)),
    Column('tile_size', VARCHAR(length=10)),
    Column('user_id', INTEGER),
)

settings = Table('settings', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('language', String(length=15)),
    Column('tiles_size', String(length=10)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['settings'].columns['tile_size'].drop()
    post_meta.tables['settings'].columns['tiles_size'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['settings'].columns['tile_size'].create()
    post_meta.tables['settings'].columns['tiles_size'].drop()
