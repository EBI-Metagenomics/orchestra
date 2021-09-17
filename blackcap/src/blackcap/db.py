"""Blackcap database."""

from blackcap.configs import config_registry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_engine = create_engine(config_registry.get_config().get_sql_db_uri())
# Use this session for all db operations in the app
DBSession = sessionmaker(db_engine)
