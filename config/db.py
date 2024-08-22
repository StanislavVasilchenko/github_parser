from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import declared_attr, DeclarativeBase
import databases
from config.settings import get_db_url

DATABASE_URL = get_db_url()

database = databases.Database(DATABASE_URL)

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
