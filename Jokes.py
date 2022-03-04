import json
import random

def joke():
    joke = json.load(open('jokes.json'))
    dict = random.choice(joke)
    item = (dict['body'])
    return item