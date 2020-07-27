#!/home/mikoaj/anaconda3/envs/redditbot/bin/python

import praw
import yaml
from random import randrange
import os


class Reddit_Roulette:
    # init method or constructor
    def __init__(self, subreddits=['LifeProTips'], limit=1, random=False, topoftheday=True, defaultsub=1):
        self.reddit = praw.Reddit(client_id="fFcdnMjfvMZDkQ",
                                  client_secret="irpkw_HGxr3ScjyXntpSPuE-HmI",
                                  user_agent="tip bot",
                                  username="mikoajo",
                                  password="19216801")
        self.subreddits = subreddits
        self.limit = limit
        self.random = random
        self.topoftheday = topoftheday
        self.defaultsub = defaultsub

    def set_subreddit(self, sub):
        self.subreddit = self.reddit.subreddit(self.subreddits[sub])

    def post_of_the_day(self):
        for submission in self.subreddit.top():
            if not submission.stickied:
                return submission

    def hot_post(self):
        submissions = []
        for submission in self.subreddit.hot(limit=self.limit):
            if not submission.stickied:
                submissions.append(submission)
        rand = randrange(self.limit-1)
        return submissions[rand]

    def main(self):
        if self.random and self.topoftheday:
            self.set_subreddit(randrange(len(self.subreddits)))
            print(self.post_of_the_day().title)
        elif not self.random and self.topoftheday:
            self.set_subreddit(randrange(self.defaultsub))
            print(self.post_of_the_day().title)
        elif self.random and not self.topoftheday:
            self.set_subreddit(randrange(len(self.subreddits)))
            print(self.hot_post().title)
        else:
            self.set_subreddit(randrange(self.defaultsub))
            print(self.hot_post().title)


try:
    if os.path.isfile('config.yml'):
        with open('config.yml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            red = Reddit_Roulette(subreddits=config['subreddits'], limit=config['limit'],
                                  random=config['random'], topoftheday=config['topoftheday'], defaultsub=config['defaultsub'])
    else:
        red = Reddit_Roulette()
except Exception as e:
    red = Reddit_Roulette()
    print(e)
finally:
    red.main()