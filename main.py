from datetime import datetime
from flask import Flask, request, render_template
import json

app = Flask(__name__)

def load_messages():
    with open('db.json', 'r') as json_file:
        return json.load(json_file)["messages"]

all_messages = load_messages()

def save_messages():
    with open('db.json', 'w') as json_file:
        json.dump({
        "messages" : all_messages
    }, json_file)

@app.route("/")
def index_page():
    return "Hello"

@app.route("/get_messages")
def get_messages():
    return {"messages" : all_messages}

@app.route("/chat")
def display_chat():
    return render_template("form.html")

def add_message(sender, text):
    all_messages.append({
        "text" : text,
        "sender" : sender,
        "time" : datetime.now().strftime("%H:%M:%S")
    })

@app.route("/send_message")
def send_message():
    sender = request.args["name"]
    text = request.args["text"]
    add_message(sender, text)
    save_messages()

    return "OK"

@app.route("/count")
def count_of_messages():
    return f"Всего сообщений - <b>{len(all_messages)}</b>"

def print_message(message):
    for msg in message:
        print(f'[{msg["sender"]}]: {msg["text"]} // {msg["time"]}')


print_message(all_messages)

app.run()