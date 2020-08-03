# =========== py script to delete slack messages in a thread ========== #
# this script will find the ts for all threaded messages in a channel
# and delete all replies to that thread
#
# to run: 
#   put in the same folder as slack_api_functions.py and bot_token.txt
#   update hard coded values:
#    1. channel ID on line 18 
#    2. change the search pattern on line 35

# ================ setup =============== #
# libs and functions 
import pandas as pd
import time
from slack_api_functions import slack_api
# inputs 
bot_token = open("bot_token.txt", "r").read()
channel = "C0181PVV6EN"

# ================ run the constructor =============== #
bot = slack_api()

# ================ set and make payload =============== #
bot.setToken(bot_token)
bot.setChannel(channel)
bot.makePayload()

# ================ select posts to delete =============== #
# get all of the channels history 
channel_history = bot.readSlackConversations("history")
# convert to a pd df, select just the threads with replies
message_history_df = pd.DataFrame.from_dict(channel_history['messages'])
threads = message_history_df[message_history_df["reply_count"].notnull()]
# get the messages that match a pattern 
threads = threads[threads["text"].str.contains("This message was deleted.")]

# ================ delete selected posts =============== #
# setup payloads 
bot.makePayload(limit="100")            # set high enough for longest thread
base_payload = bot.getPayload()         # get the current payload
replies_payload = base_payload.copy()   # payload for reading replies
delete_payload = base_payload.copy()    # payload for deleteing replies

# loop and delete
for thread_ts in threads['thread_ts']:
    # set the current thread ts 
    replies_payload['ts'] = thread_ts
    # get the replies within this thread
    replies = bot.readSlackConversations("replies", payload = replies_payload)
    # loop through and delete
    for r in replies['messages']:
        delete_payload['ts'] = r['ts']
        bot.postSlackChat(chat_method = "delete", payload = delete_payload)
        time.sleep(0.5)