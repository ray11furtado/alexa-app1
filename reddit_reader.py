from flask import Flask
from flask_ask import Ask, statement, question, session
from account_info import USERNAME, PASSWORD
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")
subreddit = "hockey"
reddit_url = "https://www.reddit.com"
reddit_api_url = "{}/api/login".format(reddit_url)



def get_reddit_data():
    user_pass_dict = {'user': USERNAME,
                      'passwd': PASSWORD,
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'Testing Alexa: Ray'})
    print(reddit_api_url)
    sess.post(reddit_api_url, data=user_pass_dict)
    # REDDIT API is picky when making rapid API calls
    time.sleep(1)
    url = "{}/r/{}/.json?limit=5".format(reddit_url, subreddit)
    html = sess.get(url)
    data = json.loads(html.content.decode("utf-8"))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']] # flake8: noqa
    titles = '...'.join([i for i in titles])
    return titles



# Welcome start skill for Alexa


@ask.launch
def start_skill():
    s = "Would you like me to read some reddit headlines?"
    return question(s)



# Handles user choosing subreddit

# @ask.launch
# def start_skill():

# Handles if user says yes



@ask.intent("YesIntent")
def share_headlines():
    s = "What subreddit would you like me to read?"
    return question(s)
    # headlines = get_reddit_data()
    # headline_msg = "Current headlines are {}".format(headlines)
    # return statement(headline_msg)


@ask.intent("NoIntent")
def no_intent():
    bye = "Okay then, bye"
    return statement(bye)




@ask.intent("AnswerIntent", mapping={'subreddit': subreddit})
def subredditCheck():
    s = "is {} the correct subreddit?".format(subreddit)
    return question(s)






if __name__ == "__main__":
    app.run(debug=True)
