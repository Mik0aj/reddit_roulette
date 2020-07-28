#!/home/mikoaj/anaconda3/envs/redditbot/bin/python

import praw
import yaml
from random import randrange
import os


class Reddit_Roulette:
    # init method or constructor
    def __init__(self, subreddits=['LifeProTips'], limit=1, defaultsub=1, random=False, topoftheday=True, offline=False):
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
        self.offline = offline

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

    def __choose_options(self):
        """Uses __option() to decide what function to use"""
        switcher = {
            0: self.__zero(),
            1: self.__one(),
            2: self.__two(),
            3: self.__three(),
            # 4: self.four(),
            # 5: five,
            # 6: six,
            # 7: seven,
        }
        return switcher.get(self.__options(), lambda: "Invalid option")

    def __options(self):
        """Returns int based on config.yml if none exists it defaults to 0, value is calculated binary 
        where the first boolean variable is considered the least important value
        e.g. random = false topoftheday = true offline = false will 
        returns 2"""
        a = 1 if self.random else 0
        b = 2 if self.topoftheday else 0
        c = 4 if self.offline else 0
        return a+b+c

    def __zero(self):
        self.set_subreddit(randrange(self.defaultsub))
        return self.hot_post().title

    def __one(self):
        self.set_subreddit(randrange(len(self.subreddits)))
        return self.hot_post().title

    def __two(self):
        self.set_subreddit(randrange(self.defaultsub))
        return self.post_of_the_day().title

    def __three(self):
        self.set_subreddit(randrange(len(self.subreddits)))
        return self.post_of_the_day().title
    # def four():

    # def five():

    # def six():

    # def seven():

    def main(self):
        print(self.__choose_options())


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
