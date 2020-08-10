from slack_api_functions import slack_api
import configparser

# load config file
bot_config = configparser.RawConfigParser()   
bot_config.read("bot.cfg")
bot_token = bot_config.get('slack-bot-config', 'bot_token')
channel = bot_config.get('slack-bot-config', 'channel')
userID = bot_config.get('slack-bot-config', 'userID')

# ================ run the constructor =============== #
bot = slack_api()

# if you need to get the channel id
#channel_info = bot.readSlackConversations("list", payload = {"token":bot_token})

# fill the bot with data 
bot.setToken(bot_token)
bot.setChannel(channel)
bot.makePayload()

# post to the slack 
import datetime 
today = str(datetime.date.today())

thread_header = "*Here are the astro-ph posts from* " + "*" + today + "!*"
bot.makePayload(text=thread_header)
bot.postSlackChat()

# get ts from the last post
bot.makePayload(limit="1")
last_message = bot.readSlackConversations("history")
thread_ts = last_message['messages'][0]['ts']

# add the thread_ts to the global variables and create the base payload 
bot.setThreadTS(thread_ts)
bot.setUnfurlLinks('false')
bot.makePayload()
base_payload = bot.getPayload()

# post the feed
import feedparser
import time
NewsFeed = feedparser.parse("https://arxiv.org/rss/astro-ph")

# create a list to store responses
resp_tracker = []

for entry in NewsFeed.entries:
    # add the article to the payload 
    base_payload['text'] = "*Title:* " + entry['title'].split(".")[0] + '\n' + "*URL:* " + entry['link']
    # post
    resp = bot.postSlackChat(payload = base_payload, return_response = True)
    
    # update response tracker
    resp_tracker.append(resp)
        
    # sleep for 1s
    time.sleep(1)


# handle response
resp_ok_count = 0
resp_other_count = 0
code_reason = []

for resp in resp_tracker:
    # update flag
    if resp.status_code == 200:
        resp_ok_count = resp_ok_count+1
    else:
        resp_other_count = resp_other_count+1
    # create list of events 
    code_reason.append(str(resp.status_code)+': '+resp.reason)

# check if there's a response otehr than 200 and send to user
if resp_other_count != 0:
    unq_codes = list(set(code_reason))
    
    count_dict = {}
    
    for i in unq_codes:
        count_dict[i] = code_reason.count(i)
    
    bot.setThreadTS('')
    bot.setChannel(userID)
    bot.setText(count_dict)
    bot.makePayload()
    
    bot.postSlackChat(return_response = True)
