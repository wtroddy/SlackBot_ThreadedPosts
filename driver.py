from slack_api_functions import slack_api
import configparser

# load config file
bot_config = configparser.RawConfigParser()   
bot_config.read("bot.cfg")
bot_token = bot_config.get('slack-bot-config', 'bot_token')
channel = bot_config.get('slack-bot-config', 'channel')

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

thread_header = "*Here the astro-ph posts from* " + "*" + today + "!*"
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

for entry in NewsFeed.entries:
    # add the article to the payload 
    base_payload['text'] = "*Title:* " + entry['title'].split(".")[0] + '\n' + "*URL:* " + entry['link']
    # post
    bot.postSlackChat(payload = base_payload)
    # sleep for 1s
    time.sleep(1)