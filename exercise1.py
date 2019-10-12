from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

def main():
    engine = create_engine('sqlite:///exercise1.db', echo=False)
    Base = declarative_base()
    session = sessionmaker(bind=engine)()

    # Code here

main()
