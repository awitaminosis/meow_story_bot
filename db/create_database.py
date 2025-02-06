from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy_utils import database_exists, create_database
from decouple import config

from models.journey import Journey


db_user = config('DB_USER')
db_user_password = config('DB_USER_PASSWORD')
db_database = config('DB_DATABASE')
DATABASE_URL = f"postgresql://{db_user}:{db_user_password}@localhost:5432/{db_database}"

# Create a base class for declarative models
Base = declarative_base()

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    if not database_exists(engine.url):
        create_database(engine.url)

    Journey.__table__.create(bind=engine, checkfirst=True)
    Base.metadata.create_all(engine)
    print("Tables created.")


def create_db():
    db_user = config('DB_USER')
    db_user_password = config('DB_USER_PASSWORD')
    db_database = config('DB_DATABASE')

    connection = psycopg2.connect(user=db_user, password=db_user_password)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()
    # Создаем базу данных
    cursor.execute("select * from information_schema.tables where table_name=%s", (db_database,))
    try:
        cursor.execute(f'create database {db_database}')
    except psycopg2.errors.DuplicateDatabase:
        pass
        # Закрываем соединение
    cursor.close()
    connection.close()
    print('Database created')


if __name__ == "__main__":
    create_db()
    create_tables()
    print('done')
