
# run function to get the list of all channels 
slack_channels = slack_api.readSlackConversations('list', {'token':bot_token})


# 
payload_history = {'token':bot_token, 'channel':'C0182S96WKW', 'limit':'1'}



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
    pass
