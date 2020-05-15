from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TimelineIndex(Base):
    __tablename__ = "TimelineIndex"

    name = Column(String, primary_key=True)
    since_id = Column(Integer)
    max_id = Column(Integer)

    def __repr__(self):
        return ((self.__class__.__name__
                + "(name={name}, since_id={since_id}, max_id={max_id})")
                .format(name=self.name,
                        since_id=self.since_id,
                        max_id=self.max_id))

    @classmethod
    def find_by_name(cls, name, session):
        "名前に対応するレコードを返す"
        row = session.query(cls).filter(cls.name == name).one_or_none()
        return row

    @classmethod
    def all(cls, session):
        "全てのレコードを返す"
        return session.query(cls).all()
