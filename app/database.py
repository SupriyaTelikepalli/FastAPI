from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:supriya@localhost/fastapidb'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
while True:
    try:
        conn = psycopg2.connect(host='localhost',dbname='fastapidb', user='postgres',password='supriya',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection is successful')
        break
    except Exception as error:
        print('connecting to database failed')
        print("Error: ",error)
        time.sleep(2)
'''