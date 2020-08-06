# ThreadedRSS: SlackBot for Threaded Posts

This is a collection of python scripts that supports interfacing with the slack app API to post to channels as a bot. The primary use case (and inspiration) for this was to post an RSS feed as threaded replies to a single post, rather than posting many messages each day. Although, it has some flexibility and can act as an interface to any of the Slack API methods.

    """Slack API is a class of functions that can be used to prepare and send payloads via HTTP POST or HTTP GET methods.
    
    Full documentation from Slack is available at: https://api.slack.com/methods
    
    See the README.md for details on configuring your slack app and setup to suppor these functions. 
    
    Required Packages: 
        urllib
        json
        requests
    
    Written and tested in python 3.7.7 (default, May 6 2020)
    
    Author: Will Roddy (william.t.roddy@gmail.com)
    """