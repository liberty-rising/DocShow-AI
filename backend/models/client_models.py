from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TableMetadata(Base):
    __tablename__ = 'table_metadata'
    table_name = Column(String, primary_key=True, index=True)
    create_statement = Column(String)
    description = Column(String)