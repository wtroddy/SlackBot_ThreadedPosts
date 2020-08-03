# libs
import urllib
import json
import requests

class slack_api():
    """doc string 
    """
    
    # ================ Constructor =============== #
    def __init__ (self):
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
        self.token = token
        
    def setChannel(self, channel):
        self.channel = channel
    
    def setThreadTS(self, thread_ts):
        self.thread_ts = thread_ts
    
    def setText(self, text):
        self.text = text
        
    def setUnfurlLinks(self, unfurl_links):
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
        """ need to add documentation and error handlings
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
        """ doc string 
        """
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
        """doc string 
        """
        # set variables 
        chat_method = kwargs.get('chat_method', 'postMessage')
        payload = kwargs.get('payload', self.getPayload())
        return_response_flag = kwargs.get('return_response', False)
        api_url = self.base_url+'chat.'+chat_method

        # encode the json query 
        request = urllib.parse.urlencode(payload)
        
        # create the request URL 
        request_url = api_url+'?'+request
        
        # post the request 
        post_response = requests.post(request_url)
        if (return_response_flag == True):
            return(post_response)
