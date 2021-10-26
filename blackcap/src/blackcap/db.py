"""Blackcap database."""

from blackcap.configs import config_registry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_engine = create_engine(config_registry.get_config().SQLALCHEMY_DATABASE_URI)
# Use this session for all db operations in the app
DBSession = sessionmaker(db_engine)
