from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
Base = declarative_base()
