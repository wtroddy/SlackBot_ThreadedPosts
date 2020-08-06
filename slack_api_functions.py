# libs
import urllib
import json
import requests

class slack_api():
    """Slack API is a class of functions that can be used to prepare and send payloads via HTTP POST or HTTP GET methods.
    
    Full documentation from Slack is available at: https://api.slack.com/methods
    
    See the README.md for details on configuring your slack app and setup to suppor these functions. 
    
    Required Packages: urllib, json, requests
    Python Version: Written and tested in python 3.7.7 (default, May 6 2020)
    Author: Will Roddy (william.t.roddy@gmail.com)
    """
    
    # ================ Constructor =============== #
    def __init__ (self):
        """
        Base init constructor for class. Presets base_url to be the base for all slack api methods.

        Returns
        -------
        None.

        """
        self.base_url = "https://slack.com/api/"
        self.token = ""
        self.channel = ""
        self.thread_ts = ""
        self.text = ""
        self.payload = ""
        self.unfurl_links = ""
    
    # ================ Setter/Getters =============== # 
    # setter functions
    def setToken(self, token):
        """
        Set the User OAuth Access Token. This is a minimally required parameter. 

        Parameters
        ----------
        token : str
            Slack User OAuth Access Token.
            e.g. xoxb-123456789-123456789-abcdefg987654321.

        Returns
        -------
        None.

        """
        self.token = token
        
    def setChannel(self, channel):
        """
        Set the Channel ID

        Parameters
        ----------
        channel : str
            Slack channel where messages should be read/posted from.
            e.g. C0123456789

        Returns
        -------
        None.

        """
        
        self.channel = channel
    
    def setThreadTS(self, thread_ts):
        """
        Set a thread_ts

        Parameters
        ----------
        thread_ts : str
            timestamp of thread.
            e.g. 1234567890.000000

        Returns
        -------
        None.

        """
        self.thread_ts = thread_ts
    
    def setText(self, text):
        """
        Set argument 'text'

        Parameters
        ----------
        text : str
            text valuable, string of message/post/reply/etc.

        Returns
        -------
        None.

        """
        self.text = text
        
    def setUnfurlLinks(self, unfurl_links):
        """
        Set argument for 'unfurl_links'. Can be either true or false.
        Pass true to enable unfurling of primarily text-based content.

        Parameters
        ----------
        unfurl_links : str
            true or false.

        Returns
        -------
        None.

        """
        self.unfurl_links = unfurl_links
    
    # getter functions
    def getToken(self):
        return self.token
    
    def getChannel(self):
        return self.channel
    
    def getThreadTS(self):
        return self.thread_ts
    
    def getText(self):
        return self.text
    
    def getUnfurlLinks(self):
        return self.unfurl_links
    
    # ================ payload management =============== #
    # function to create a payload within the class
    def makePayload(self, **kwargs):
        """
        Function that will create a `dict` from all of the set class variables.
        Class level variables can be overriden with kwargs for that value. 

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # kwargs for non-global variables
        text = kwargs.get('text', self.getText())
        limit = kwargs.get('limit', "")
        
        self.payload = {"token":self.getToken(), 
                        "channel":self.getChannel(),
                        "thread_ts":self.getThreadTS(),
                        "text":text,
                        "limit":limit,
                        "unfurl_links":self.getUnfurlLinks()
                        }
    
    # get the payload
    def getPayload(self):
        return self.payload
    
    # ================ API functions =============== #
    # function to read slack conversations
    def readSlackConversations(self, conversation_method, **kwargs):
        # set variables 
        api_url = self.base_url+'conversations.'+conversation_method
        payload = kwargs.get('payload', self.getPayload())
        
        # encode the json query 
        query = urllib.parse.urlencode(payload)
        
        # generate url 
        request_url = api_url+'?'+query
        
        # read the json data into a dictionary  
        with urllib.request.urlopen(request_url) as url:
            data = json.loads(url.read().decode())
        
        # return the data 
        return(data)
    
    # function to send chats 
    def postSlackChat(self, **kwargs):
        ### variable management 
        # set variables from kwargs
        chat_method = kwargs.get('chat_method', 'postMessage')
        payload = kwargs.get('payload', self.getPayload())
        return_response_flag = kwargs.get('return_response', False)
        
        # set variables from self
        api_url = self.base_url+'chat.'+chat_method
        
        ### Create and Post Request
        # encode the json query 
        request = urllib.parse.urlencode(payload)
        # create the request URL 
        request_url = api_url+'?'+request
        # post the request 
        post_response = requests.post(request_url)
        
        ### Return the response if requested by user
        if (return_response_flag == True):
            return(post_response)

