#!/home/mikoaj/anaconda3/envs/redditbot/bin/python 

import praw
import yaml
from random import randrange

class Reddit_Roulette:
    # init method or constructor
    def __init__(self,subreddits,limit):
        self.reddit = praw.Reddit(client_id="fFcdnMjfvMZDkQ",
                                  client_secret="irpkw_HGxr3ScjyXntpSPuE-HmI",
                                  user_agent="tip bot",
                                  username="mikoajo",
                                  password="19216801")
        self.subreddits = subreddits
        self.limit=limit

    def set_subreddit(self,sub):
        self.subreddit = self.reddit.subreddit(self.subreddits[sub])

    def post_of_the_day(self):
        for submission in self.subreddit.top():
        	if not submission.stickied:
        		return submission

    def hot_post(self):
        submissions=[]
        for submission in self.subreddit.hot(limit=self.limit):
        	if not submission.stickied:
        		submissions.append(submission)
        rand=randrange(self.limit-1)
        return submissions[rand]

with open('config.yml') as f:    
    config = yaml.load(f, Loader=yaml.FullLoader)
    tip=Reddit_Roulette(config["subreddits"],config["limit"])
    if config["random"] and config["topoftheday"]:
    	tip.set_subreddit(randrange(len(tip.subreddits)))
    	print(tip.post_of_the_day().title)
    elif not config["random"] and config["topoftheday"]:
    	tip.set_subreddit(randrange(config["defaultsub"]))
    	print(tip.post_of_the_day().title)
    elif config["random"] and not config["topoftheday"]:
    	tip.set_subreddit(randrange(len(tip.subreddits)))
    	print(tip.hot_post().title)
    else:
    	tip.set_subreddit(randrange(config["defaultsub"]))
    	print(tip.hot_post().title)