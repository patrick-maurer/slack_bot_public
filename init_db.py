# Libraries
import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


# initialize database
def init():
    conn = psycopg2.connect(
        host=os.environ["HOST_NAME"],
        database=os.environ["DATABASE_NAME"],
        user=os.environ["USER_NAME"],
        password=os.environ["PASSWORD"],
    )
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS articles (user_id TEXT, code TEXT, author TEXT, UNIQUE (user_id, code, author));"""
    )
    conn.commit()
    return conn, cur


# add article
def add_article(conn, cur, user_id, code, author):
    """
    add article to database

    :param conn: connection to database
    :param cur: database cursor
    :user_id: unique user identifier
    :code: article code
    :author: author last name
    """
    with conn:
        cur.execute(
            "INSERT INTO articles (user_id, code, author) VALUES (%s, %s, %s) ",
            (user_id, code, author),
        )


def get_articles(cur, user_id):
    """
    get articles from database

    :param cur: database cursor
    :user_id: unique user identifier
    :return: list of all code, author pairs
    """
    cur.execute(
        "SELECT code, author FROM articles WHERE user_id = %s",
        [user_id],
    )
    return cur.fetchall()


def delete_article(conn, cur, user_id, code):
    """
    delete articles from database

    :param conn: connection to database
    :param cur: database cursor
    :user_id: unique user identifier
    """
    with conn:
        cur.execute(
            "SELECT code, author FROM articles WHERE user_id = %s AND code = %s",
            [user_id, code],
        )
        if cur.fetchall() == []:
            raise Exception
        cur.execute(
            "DELETE FROM articles WHERE user_id = %s AND code = %s",
            [user_id, code],
        )


def reset_database(conn, cur, user_id):
    """
    reset database

    :param conn: connection to database
    :param cur: database cursor
    :user_id: unique user identifier
    """
    with conn:
        cur.execute(
            "DELETE FROM articles WHERE user_id = %s",
            [user_id],
        )
