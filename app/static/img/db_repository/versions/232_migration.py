from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_resources = Table('std_resources', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('resource_id', Integer, primary_key=True, nullable=False),
    Column('dst_id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('body', String(length=500)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_resources'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_resources'].drop()
