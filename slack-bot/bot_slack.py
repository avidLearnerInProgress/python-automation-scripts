import os, time, re
from parseconfig import read_config
from slackclient import SlackClient

CONFIG_FILE = 'slack.ini'
slack_token = read_config(CONFIG_FILE)
print(type(slack_token))

sc = SlackClient(slack_token)
print(sc)

def send_slack_msg(channel = "general", msg = "empty message", attachments = []):
    return sc.api_call(
                    "chat.postMessage",
                    channel = channel,
                    text = msg,
                    attachments = [attachments]
                    )
	'''
	"chat.postMessage",
	  channel = "general",
	  text = "Hello from Python! :tada:",
	  attachments = [{
	    "fallback": "Required plain-text summary of the attachment.",
	    "color": "#2eb886",
	    "pretext": "Optional text that appears above the attachment block",
	    "author_name": "Bobby Tables",
	    "author_link": "http://flickr.com/bobby/",
	    "author_icon": "http://flickr.com/icons/bobby.jpg",
	    "title": "Slack API Documentation",
	    "title_link": "https://api.slack.com/",
	    "text": "Optional text that appears within the attachment",
	    "fields": [{
	      "title": "Priority",
	      "value": "High",
	      "short": False
	    }],
	    "footer": "Slack API",
	    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
	    "ts": 123456789
	'''

def main():
    channel = "random"
    msg = "Hello world"
    attachments = { "text" : "My attachments" }
    response = send_slack_msg(channel, msg, attachments)
    if response["ok"]:
        print("Posted successfully.!")
    else:
        print(response)

if __name__ == '__main__':
    main()