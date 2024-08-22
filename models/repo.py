from sqlalchemy import Column, Integer, String, Table, MetaData, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Repo(Base):
    __tablename__ = 'repo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    repo = Column(String, nullable=False, unique=True)
    owner = Column(String, nullable=False)
    position_cur = Column(Integer)
    position_prev = Column(Integer)
    stars = Column(Integer)
    watchers = Column(Integer)
    forks = Column(Integer)
    open_issues = Column(Integer)
    language = Column(String)

    def __str__(self):
        return (f"{self.repo} - {self.owner} - {self.position_cur}-"
                f"{self.position_prev} - {self.stars}-"
                f"{self.watchers} - {self.forks}- {self.open_issues}-"
                f"{self.language} - {self.id}")


class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    repo_name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    author = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    def __str__(self):
        return f"{self.repo_name} - {self.author} - {self.date}"
