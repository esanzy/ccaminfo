#-*-coding:utf8-*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import collections

class SQLDriver():
    def __init__(self, uri):
        self.engine = create_engine(uri)
        self.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()

    def select_all(self, query, ordered=False, params=None):
        s = self.db_session()
        if params is None:
            result = s.execute(query)
        else:
            result = s.execute(query, params)
        row = result.fetchone()
        rows = []
        while row is not None:
            if ordered:
                rows.append(collections.OrderedDict((col, getattr(row, col)) for col in result._metadata.keys))
            else:
                rows.append(dict((col, getattr(row, col)) for col in result._metadata.keys))
            row = result.fetchone()

        return rows

    def select_one(self, query, ordered=False, params=None):
        s = self.db_session()
        if params is None:
            result = s.execute(query)
        else:
            result = s.execute(query, params)
        row = result.fetchone()
        if ordered:
            result = collections.OrderedDict((col, getattr(row, col)) for col in result._metadata.keys)
        else:
            result = dict((col, getattr(row, col)) for col in result._metadata.keys)
        return result

    def raw_query(self, query, params=None):
        s = self.db_session()
        if params is None:
            s.execute(query)
        else:
            s.execute(query, params)

    def commit(self):
        s = self.db_session()
        s.commit()

db = SQLDriver("mysql+mysqldb://root:nimd@123!@localhost/cmcweb?charset=utf8")
