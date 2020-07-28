#!/home/mikoaj/anaconda3/envs/redditbot/bin/python

import praw
import yaml
import pickle
from random import randrange
import os


class Reddit_Roulette:
	# init method or constructor
	def __init__(self, subreddits=['LifeProTips'], limit=1, defaultsub=1, random=False, topoftheday=True, offline=False, allow_storage=True):
		self.reddit = praw.Reddit(client_id="fFcdnMjfvMZDkQ",
								  client_secret="irpkw_HGxr3ScjyXntpSPuE-HmI",
								  user_agent="tip bot",
								  username="mikoajo",
								  password="19216801")
		self.subreddits = subreddits
		self.limit = limit
		self.defaultsub = defaultsub
		self.random = random
		self.topoftheday = topoftheday
		self.offline = offline
		self.allow_storage = allow_storage
		if offline:
			try:
				with open("data.pkl", "rb") as f:
					self.submissions = self.__restore(f)
			except Exception as e:
				print(e)
				self.submissions = []
		else:
			self.submissions = []

	def set_subreddit(self, sub):
		self.subreddit = self.reddit.subreddit(self.subreddits[sub])

	def post_of_the_day(self):
		# only way to get submissions is through loop
		for submission in self.subreddit.top():
			if not submission.stickied:
				return submission

	def offline_post(self):
		rand = randrange(len(self.submissions))
		return self.submissions[rand]

	def hot_post(self):
		# only way to get submissions is through loop
		rand = randrange(self.limit)
		n = 1
		for submission in self.subreddit.hot(limit=self.limit):
			print(n, submission, rand)
			if not submission.stickied and n == rand:
				return submission
			elif submission.stickied and n == rand:
				rand += 1
			n += 1

	def __choose_options(self):
		"""Uses __option() to decide what function to use"""
		switcher = {
			0: self.__zero,
			1: self.__one,
			2: self.__two,
			3: self.__three,
			4: self.four,
			5: self.four,
			6: self.four,
			7: self.four,
		}
		func = switcher.get(self.__options(), lambda: "Invalid option")
		return func

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

	def four(self):
		return self.offline_post().title

	def __restore(self, f):
		data = pickle.load(f)
		return data

	def __store(self):
		try:
			with open("data.pkl", "wb") as f:
				self.set_subreddit(randrange(len(self.subreddits)))
				for submission in self.subreddit.hot(limit=self.limit):
					if not submission.stickied:
						self.submissions.append(submission)
				lista = set(self.submissions)
				pickle.dump(self.submissions, f)
		except Exception as e:
			print(e)

	def main(self):
		function = self.__choose_options()
		print(function())
		if self.allow_storage:
			self.__store()


try:
	if os.path.isfile('config.yml'):
		with open('config.yml') as f:
			config = yaml.load(f, Loader=yaml.FullLoader)
			red = Reddit_Roulette(subreddits=config['subreddits'], limit=config['limit'],
								  random=config['random'], topoftheday=config['topoftheday'], offline=config["offline"], defaultsub=config['defaultsub'],
								   allow_storage=config['allow_storage'])
	else:
		red = Reddit_Roulette()
except Exception as e:
	red = Reddit_Roulette()
	print(e)
finally:
	red.main()
