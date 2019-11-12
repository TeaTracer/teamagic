import sys
from sqlalchemy import create_engine
import datetime
import requests
from sqlalchemy.orm import sessionmaker
from teamagic import *
from .rss import Base, Post, User, Tag, M2MPostTag


class MiracleTag(Miracle):
    name = Itself()


class MiracleUser(Miracle):
    name = Itself()


def convert_pub_date(date):
    # "Mon, 04 Nov 2019 13:25:58 GMT"
    return datetime.datetime.strptime(date[:-4], "%a, %d %b %Y %H:%M:%S")


class MiraclePost(Miracle):
    title = At("title")
    link = At("link")
    description = At("description")
    pub_date = At("pubDate", convertion=convert_pub_date)
    creator = At("{http://purl.org/dc/elements/1.1/}creator", MiracleUser)
    tags = Each("category", MiracleTag)


class MiracleData(Miracle):
    posts = At("channel", Each("item", MiraclePost))


def get_or_create(session, model, **kwargs):
    """SqlAlchemy implementation of Django's get_or_create.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True

if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    r = requests.get(sys.argv[1])
    text = r.text
    Session = sessionmaker(bind=engine)
    session = Session()
    posts = MiracleData(XML(text)).posts
    for mpost in posts:
        muser = mpost.creator
        user, _ = get_or_create(session, User, name=muser.name)
        session.add(user)

        post, _ = get_or_create(session, Post,
            title=mpost.title,
            link=mpost.link,
            description=mpost.description,
            pub_date=mpost.pub_date,
            creator_id=user.id
        )
        session.add(post)

        for mtag in mpost.tags:
            tag, _ = get_or_create(session, Tag, name=mtag.name)
            session.add(tag)
            m2m, _ = get_or_create(session, M2MPostTag, post=post.id, tag=tag.id)
            session.add(m2m)

    session.commit()
    for x in session.query(Post).all():
        print(x)
