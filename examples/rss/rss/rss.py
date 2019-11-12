from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    description = Column(String)
    pub_date = Column(DateTime)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', foreign_keys='Post.creator_id')

    def __repr__(self):
        return 'Post("{}" by "{}" publised on {})'.format(
                self.title,
                self.creator.name,
                self.pub_date)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class M2MPostTag(Base):
    __tablename__ = 'm2m_posts_tags'

    id = Column(Integer, primary_key=True)
    post = Column(Integer, ForeignKey('posts.id'))
    tag = Column(Integer, ForeignKey('tags.id'))

