from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(config.DATABASE_CONNECT_URL,
                       convert_unicode=True, echo=config.DATABASE_SQL_ECHO)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import app.db.user
    import app.db.message
    import app.db.room

    Base.metadata.create_all(bind=engine)
