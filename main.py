#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import wsgiref.handlers
import os
import csv
import string
import random
from StringIO import StringIO
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template

# For Import Models on GAE DB
from models import *
import datetime
from email.utils import parsedate

# For Twitter Import
from appengine_twitter import AppEngineTwitter
from basehandler import BaseHandler, h
import twitter

class CsvUploader(webapp.RequestHandler):
	def get(self):
		template_values = {
			'messages': Message.all(),
		}
		path = os.path.join(os.path.dirname(__file__), "upload.html")
		self.response.out.write(template.render(path, template_values))
	def post(self):
		rawfile = self.request.get('file')
		csvfile = csv.reader(StringIO(rawfile))
		for row in csvfile:
			m = Message(
				zid = int(row[0]),
				msg = unicode(row[1], "utf-8"),
				loc = unicode(row[2], "utf-8"),
				pict_url = unicode(row[3], "utf-8"),
				)
			m.put()
		self.redirect(self.request.uri)

class DeleteMessage(webapp.RequestHandler):	
	def get(self):
		query = Message.all()
		for q in query:
			print "deleted: ",
			print q.zid,
			print q.msg.encode('utf-8'),
			print q.loc.encode('utf-8'),
			print q.pict_url.encode('utf-8'),
			q.delete()

class ShowMessage(webapp.RequestHandler):
	def get(self):
		template_values = {
			'messages': Message.all(),
		}
		path = os.path.join(os.path.dirname(__file__), "show.html")
		self.response.out.write(template.render(path, template_values))
		
class Random(webapp.RequestHandler):
	def get(self):
		show_num = 3
		i = 0
		MAX_DB = 91864
		qlist = []
		while i < show_num:
			i += 1
			if debug_flag:
				rand = random.randint(0,DEBUG_DB)
			else:
				rand = random.randint(0,MAX_DB)
			cmdline = "SELECT * FROM Message WHERE zid = " + str(rand)
			query = db.GqlQuery(cmdline)
			#print "cmdline = " + cmdline
			qlist.append(query[0])
			print getRandomlySelectedWord()
		print "[Zekkei ID]\t[Message]\t[Location]\t[Picture URL]"
		for q in qlist:
			print str(q.zid) + '\t\t',
			print q.msg.encode('utf-8') + '\t',
			print q.loc.encode('utf-8') + '\t',
			print q.pict_url.encode('utf-8')
		print
		
		
class TwitterTweet(webapp.RequestHandler):
	def get(self):
		# User Setting and Run Twitter Bot
		tweet = ""
		tmp_tweet = ""
			
		while len(tweet) < MAX_LEN:
			tmp_tweet = tweet
			word = getRandomlySelectedWord()
			tweet += SPACE + word

		tweet = tmp_tweet
		print "Length of 'tweet': " + str(len(tweet))
		print "I am tweeting: " + tweet #.encode('utf-8')
		print "Status of Tweet Result: " + str(gae_twitter.update(tweet))
		
class Test1(webapp.RequestHandler):
	def get(self):
		print BR
		print "Auto-generated Sample Tweet:" + BR
		print "'"+getRandomlySelectedWord()+"'"
		print BR + BR
	
def getRandomlySelectedWord():
	if debug_flag:
		rand = random.randint(0,DEBUG_DB)
	else:
		rand = random.randint(0,MAX_DB)
	query = db.GqlQuery("SELECT * FROM Message WHERE zid = " + str(rand))
	q = query[0]
	word = q.msg.encode('utf-8') +SPACE+ q.loc.encode('utf-8')+SPACE \
	       +"<a href='"+q.pict_url.encode('utf-8')+"'>"+q.pict_url.encode('utf-8')+"</a>"
	return word
		
def rfc2datetime(rfc):
	pd = parsedate(rfc)[0:6]
	return datetime.datetime(*pd)

def twitter_api_init_gae(self,
			 username=None,
			 password=None,
			 input_encoding=None,
			 request_headers=None):
	import urllib2
	from twitter import Api
	self._cache = None
	
	self._urllib = urllib2
	self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
	self._InitializeRequestHeaders(request_headers)
	self._InitializeUserAgent()
	self._InitializeDefaultParameters()
	self._input_encoding = input_encoding
	self.SetCredentials(username, password)

def UTC2JST(dt):
	"""Convert UTC into JST"""
	dt = dt + datetime.timedelta(hours=9)
	return dt

def getOdai(reply):
	"""Replace Zenkaku with spaces, and then get Odai from the given reply."""
	return string.replace(reply, "　", " ").lstrip("@tango_bot").lstrip()

def main():
	# overriding API __init__
	twitter.Api.__init__ = twitter_api_init_gae

	# Global Variables
	global BOT_USERNAME,BOT_PASSWORD,BR,MAX_LEN,MAX_DB,DEBUG_DB,SPACE,DT_FORMAT
	BOT_USERNAME = 'zekkei_bot'
	BOT_PASSWORD = '???'
        BR = "<br>"
	MAX_LEN = 140
	DEBUG_DB = 4
	MAX_DB = 91864
	SPACE = " "
	DT_FORMAT = '%a, %d %b %Y %H:%M:%S'

	# Global Setting
	global gae_twitter,api,debug_flag
	gae_twitter = AppEngineTwitter(BOT_USERNAME, BOT_PASSWORD)
	api = twitter.Api(username=BOT_USERNAME, password=BOT_PASSWORD)
	#debug_flag = False
	debug_flag = True
	
	
	application = webapp.WSGIApplication(
		[#('/', CsvUploader),
		 ('/upload', CsvUploader),
		 ('/delete', DeleteMessage),
		 ('/show', ShowMessage),
		 ('/random', Random),
		 ('/cron/tweet', TwitterTweet),
		 ('/test', Test1)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
