# libs
import urllib
import json
import requests

# function to read slack conversations
def readSlackConversations(conversation_method, payload):
    # set variables 
    base_url = 'https://slack.com/api/conversations.'
    query = urllib.parse.urlencode(payload)
    
    # generate url 
    request_url = base_url+conversation_method+'?'+query
    
    # read the json data into a dictionary  
    with urllib.request.urlopen(request_url) as url:
        data = json.loads(url.read().decode())
    
    return(data)

def chatSlackBot(chat_method, payload):
    base_url = 'https://slack.com/api/chat.'
    msg_encoded = urllib.parse.urlencode(payload)
    request_url = base_url+chat_method+'?'+msg_encoded
    requests.post(request_url)


# inputs 
bot_token = 'xoxb-1267335254901-1292568446048-f9jkpFk7KV7bAlD3prukGGho'

# payload settings
payload_list = {'token':bot_token}
payload_history = {'token':bot_token, 'channel':'C0182S96WKW', 'limit':'1'}

# run function to get the list of all channels 
slack_channels = readSlackConversations('list', payload_list)


### post a new message
import time
chatSlackBot('postMessage', {'token':bot_token, 'channel':'C0182S96WKW', 'text':"i'm a bot, I'm starting this thread. \n I'm testing the links. \n it is currently: "+time.ctime()})

### get the last message from the history 
slack_conversations_history = readSlackConversations('history', payload_history)
# get the timestamp of the last message 
msg_ts = slack_conversations_history['messages'][0]['ts']

#### post the feed
import feedparser
NewsFeed = feedparser.parse("https://arxiv.org/rss/astro-ph")

for entry in NewsFeed.entries:
    ### reply to the last msg
    chatSlackBot('postMessage', {'token':bot_token, 'channel':'C0182S96WKW', 
                                 'text':entry['link'], 'thread_ts':msg_ts})
    time.sleep(1)


for entry in NewsFeed.entries:

