# -*- coding: utf-8 -*-

# Copyright (C) 2017 github.com/shyal
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Make sure to import the latest database version in here
"""

from textwrap import dedent
from vulcan.vulcan_db.versions.store_002 import *
import itertools

# used to cache our sessions
# this is a very crude form of session management
session = None

def get_session(db_path=None):
    """
    This currently does a bit too much
    """
    global session
    assert db_path or session

    if session:
        return session

    path = os.path.expanduser(db_path)

    if not path == ':memory:':
        db_exists = os.path.exists(path)
        dirname = os.path.dirname(path)
        if dirname and not os.path.isdir(dirname):
          os.makedirs(dirname)
    else:
        db_exists = False

    # create our Engine object
    engine = sqlalchemy.create_engine(f'sqlite:///{path}', encoding='utf-8', echo=False)

    # this becomes a session maker
    Session = sessionmaker(bind=engine)

    # safe to call even if tables already exist
    Base.metadata.create_all(bind=engine, tables=None, checkfirst=True)

    # we now have our session
    session = Session()

    # query database for version information
    query = session.query(MigrateVersion)

    # if we don't have any version info, then let's make sure to add it
    if not query.count() == 1:
        v = MigrateVersion(repository_id='vulcan', repository_path='vulcan_db', version=version)
        session.add(v)
        session.commit()

    db_version = query.first().version
    if db_version != version:
        print(dedent(f"""
            Your database version is:           {db_version}
            Latest database schema version is:  {version}
            Please run:

            $ vulcan migrate

            to upgrade your database to the latest schema
            """))
        exit(-1)

    return session


class Cards(object):
    
    @staticmethod
    def tags():
        session = get_session()
        return list(sorted(itertools.chain(*[[y.strip() for y in x[0].split(',')] for x in session.query(Card.context).distinct()])))

    @staticmethod
    def drop():
        session = get_session()
        for card in session.query(Card):
            session.delete(card)
        session.commit()


