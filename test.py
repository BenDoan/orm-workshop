from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

def main():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base = declarative_base()
    session = sessionmaker(bind=engine)()

    class Test(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        foo = Column(String)

    Base.metadata.create_all(engine)

    me = Test(foo="Good")
    session.add(me)
    session.commit()

    print(session.query(Test).scalar().foo)
main()
