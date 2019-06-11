from flask import Flask
from flask_ask import Ask, statement, question, session
from piazza_api import Piazza
import json
import requests
import time
import unidecode
import re

app = Flask(__name__)
ask = Ask(app, "/piazza_reader")

def get_headlines():
    """
    Description: This function will start the process of retrieving 
    piazza posts and concatenating them.

    Parameters:
        None

    Return:
        The string for alexa to read out

    """
    #retrieves login information
    with open('config.json') as login_info:
        user_pass_dict = json.load(login_info)

    #creates a session to allow use of amazon
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am making a project: shbanki'})

    #creates piazza object and logs into account
    p = Piazza()
    p.user_login(user_pass_dict["user"], user_pass_dict["passwd"])

    #goes to specific class information
    class_board = p.network("jsux9glwaxm4m")


    post_index = 1
    number_of_posts = 3

    data = class_board.iter_all_posts(number_of_posts)

    current_post = next(data)
    output = concatenate_post(current_post)

    while(number_of_posts > post_index):
        output += 'The next post reads... '
        current_post = next(data)
        output += concatenate_post(current_post)
        post_index += 1

    

    return output

def concatenate_post(data):
    """
    Description: This function will start the process of retrieving 
    piazza posts and concatenating them.

    Parameters:
        The current post as a dictionary.

    Return:
        The formatted output

    """
    #initializes the output string
    output = ''
    #initializes counts for loops
    child_index = 0
    grand_child_index = 0;
    #initialize how many elements in children array and grandchildren
    children = len(data['children'])
    grand_children = 0

    #first adds the subject and content of post which always exist
    output += data['history'][0]['subject']
    output += '... '
    output += data['history'][0]['content']
    output += '... '

    if(children > 0):    
        #concetenates the answer to the question
        if('history' in data['children'][0]):
            output += data['children'][0]['history'][0]['content']
            output += '... '

        child_index += 1

        #deals with followup discussions
        while(children > child_index):
            output += data['children'][child_index]['subject']
            output += '... '

            #initialize variables for grandchild loop
            grand_child_index = 0
            grand_children = len(data['children'][child_index]['children'])
            
            #concatenates replies to followups
            while(grandChildren > grandChildIndex):
                output += data['children'][1]['children'][grand_child_index]['subject']
                output += '... '
                grand_child_index += 1

            child_index += 1

    formatted_output = format_fix(output)

    return formatted_output

def format_fix(output):

    #removes all formatting specifiers from piazza api
    output = re.sub('<[^>]+>', '', output)

    #fixes alexa's speech in certain cases
    output = output.replace('w/', 'with')
    output = output.replace('~', 'about ')
    output = output.replace('/', '/ ')
    output = output.replace('pt', 'point')
    output = output.replace('IA', 'I A')

    return output


@app.route('/')
def homepage():
    return "Port Forwarding Successful"

@ask.launch
def start_skill():
    welcome_message = 'Hello would you like me to read some piazza posts?'
    return question(welcome_message)

@ask.intent("AMAZON.YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The piazza posts read... {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    bye_text = 'Okay then, bye.'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)