from flask import Flask
from flask_ask import Ask, statement, question, session
from account_info import USERNAME, PASSWORD
import json
import requests
import time
import unidecode

app = Flask(__name__)
app = Ask(app, "/reddit_reader")

def get_headlines():
    pass
