import openai
import os, sys


def load_key():
    openai.api_key = os.getenv("api_key")

def contains(line, token):
    return token in line

  
def build_primer(content):
    primer = "You: "
    primer += f"N is {content}"
    primer += "You are N. "
    primer += "I am M.\n"
    return primer


def chat(cinput):
    context = ""
    ccinput = cinput.split('`')[0]
    context += build_primer(ccinput)

    contentBegin = len(context)
    # Update the conversation context with the user's input
    context += f"You: {cinput}\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        #engine="text-curie-001",
        prompt=(context + "OpenAI: "),
        max_tokens = 256,
        #max_tokens = 512,
        #stop=[".", "\n"],
        temperature=0.5
    )

    reply = response['choices'][0]['text']

    # Update the conversation context with the AI's response
    context += f"\nOpenAI: {reply}\n"
    #context += '\n'

    """
    rlines = reply.split('\n')
    p = "OpenAI: "
    for line in rlines:
        print(f"{p}", line)
        p = " - "
    """
    print(context)
    return context[contentBegin:]


from flask import Flask
from flask import render_template
from dotenv import load_dotenv

# extracts response from content
def split_reply(data):
    for i in range(len(data)):
        ii = i+len("OpenAI:")
        if "OpenAI:" == data[i:ii]:
            return data[ii:]
    return data

project_folder = os.path.expanduser('~/mysite')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)

# closed user api
@app.route(f"/auth/{os.getenv('api_owner', 'none')}/<string:data>", methods=("GET", "POST"))
def rt_auth_echo(data):
    load_key()
    bot = data.split('`')[0]
    data = split_reply(chat(data))
    return render_template("index.html", bot=f"{bot} : {os.getenv('api_owner')}", data=data)


""" # open public api interface

@app.route("/echo/<string:data>", methods=("GET", "POST"))
def rt_index(data):
    load_key()
    bot = data.split('`')[0]
    data = split_reply(chat(data))
    return render_template("index.html", bot=bot, data=data)
"""


""" # open public api

@app.route("/api/<string:data>", methods=("GET", "POST"))
def rt_echo(data):
    load_key()
    r = split_reply(chat(data))
    return f"<p>{r}</p>"
"""
