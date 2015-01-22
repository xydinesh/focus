from sqlalchemy import (
    Column,
    Index,
    Integer,
    DateTime,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension
import datetime
import pytz

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

class FocusModel(Base):
    __tablename__ = 'productivity_focus'
    id = Column(Integer, primary_key=True)
    focus = Column(Integer, default=0)
    productivity = Column(Integer, default=0)
    energy = Column(Integer, default=0)
    motivation = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.datetime.now(tz=pytz.timezone('EST')))

    def __repr__(self):
        return 'focus:{0} productivity:{1} energy:{2} motivation:{3} created: {4}'.format(self.focus,
        self.productivity, self.energy, self.motivation, self.create_time)


Index('my_index', MyModel.name, unique=True, mysql_length=255)
Index('focus_ctime', FocusModel.create_time)
