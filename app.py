# Libraries
import slack
import os
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from psycopg2.errors import UniqueViolation

# Local Modules
import init_db as db
from webscraper import url

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/", app)
client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

conn, cur = db.init()


@app.route("/add", methods=["POST"])
def add():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    try:
        text = data.get("text").split(" ")[:2]
        code, author = text
        url(code, author)
        db.add_article(conn, cur, user_id, code, author)
        client.chat_postMessage(
            channel=channel_id,
            text=f"Article {code} added to database.",
        )
    except UnboundLocalError:
        client.chat_postMessage(
            channel=channel_id,
            text="Article not found.",
        )
    except UniqueViolation:
        client.chat_postMessage(
            channel=channel_id,
            text=f"Article {code} already added.",
        )
    except:
        client.chat_postMessage(
            channel=channel_id,
            text="Error",
        )
    return Response(), 200


@app.route("/del", methods=["POST"])
def delete():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    try:
        code = data.get("text").split(" ")[0]
        db.delete_article(conn, cur, user_id, code)
        client.chat_postMessage(
            channel=channel_id,
            text=f"Article {code} deleted.",
        )
    except:
        client.chat_postMessage(
            channel=channel_id,
            text="Article not in database.",
        )
    return Response(), 200


@app.route("/get_status", methods=["POST"])
def get_status():
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    try:
        l = db.get_articles(conn, cur, user_id)
        for entry in l:
            code, author = entry
            client.chat_postMessage(
                channel=channel_id,
                text=f"The status of article {code} is: {url(code, author)}",
            )
        if len(l) == 0:
            client.chat_postMessage(
                channel=channel_id,
                text="No article in database. Try to /add an article.",
            )
    except:
        client.chat_postMessage(
            channel=channel_id, text="Something went wrong. Try to /reset."
        )
    return Response(), 200


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
