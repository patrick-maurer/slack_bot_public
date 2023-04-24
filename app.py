# Libraries
import slack
import os
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from psycopg2.errors import UniqueViolation

# Local Modules
import init_db as db
from webscraper import status

# Initialization
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/", app)
client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
conn, cur = db.init()


# add article to database
@app.route("/add", methods=["POST"])
def add():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    try:
        text = data.get("text").split(" ")[:2]  # get first and second string of the user's message
        code, author = text
        status(code, author)
        db.add_article(conn, cur, user_id, code, author)  # add article to database
        client.chat_postMessage(
            channel=channel_id,
            text=f"Article {code} added to database.",  # inform user about success
        )
    except UnboundLocalError:  # error if article not found
        client.chat_postMessage(
            channel=channel_id,
            text="Article not found.",
        )
    except UniqueViolation:  # error if article already in database
        client.chat_postMessage(
            channel=channel_id,
            text=f"Article {code} already added.",
        )
    except:  # catch other unkown errors
        client.chat_postMessage(
            channel=channel_id,
            text="Error",
        )
    return Response(), 200


# delete article rom database
@app.route("/del", methods=["POST"])
def delete():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    try:
        code = data.get("text").split(" ")[0]  # get first string of user's message
        db.delete_article(conn, cur, user_id, code)  # delete article from database
        client.chat_postMessage(
            channel=channel_id,
            text=f"Article {code} deleted.",  # inform user about success
        )
    except:  # error if article not in database
        client.chat_postMessage(
            channel=channel_id,
            text="Article not in database.",
        )
    return Response(), 200


# get status of all articles
@app.route("/get_status", methods=["POST"])
def get_status():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    try:
        article_list = db.get_articles(cur, user_id)  # retrieve all articles
        for entry in article_list:
            code, author = entry
            client.chat_postMessage(
                channel=channel_id,
                text=f"The status of article {code} is: {status(code, author)}",
            )
        if len(article_list) == 0:
            client.chat_postMessage(
                channel=channel_id,
                text="No article in database. Try to /add an article.",
            )
    except:  # catch other unkown errors
        client.chat_postMessage(channel=channel_id, text="Something went wrong. Try to /reset.")
    return Response(), 200


# reset database
@app.route("/reset", methods=["POST"])
def reset():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    try:
        db.reset_database(conn, cur, user_id)
    except:
        pass
    client.chat_postMessage(channel=channel_id, text="Reset successful.")
    return Response(), 200
