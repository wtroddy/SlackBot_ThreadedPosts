# ThreadedRSS: SlackBot for Threaded Posts

This is a collection of python scripts that supports interfacing with the slack app API to post to channels as a bot. The primary use case (and inspiration) for this was to post an RSS feed as threaded replies to a single post, rather than posting many messages each day. Although, it has some flexibility and can act as an interface to any of the Slack API methods.

## Future Sections:
- setting up your slack app 
- configuring python and .cfg files
- about these scripts
- integrating RSS feeds (or other feeds)
- configuring crontab
- example uses

## Setup Slack App [DRAFT]
This section will describe how to setup a slack app in your workspace so that it works with these python scripts. 

Steps:
1. Create App 
2. Add Bot Token Scopes
	- channels:history
	- channels:read 
	- chat:write
	- incoming-webhook
3. Install app in workspace and add to channel
4. Save the bot User OAuth Access Token 
5. in the channel run @botname to add the bot to the channel
