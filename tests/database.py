from tests.settings import settings
from sqlmodel import create_engine, Session
database_url=("postgresql+psycopg://"
f"{settings.database_user}:"
f"{settings.database_password}@"
f"{settings.database_host}/"
f"{settings.database_db}")
engine=create_engine(database_url,echo=True)
def create_test_session():
    with Session(engine) as session:
        yield session