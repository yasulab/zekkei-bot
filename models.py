from google.appengine.ext import db

class Message(db.Model):
	zid = db.IntegerProperty()
	msg = db.StringProperty()
	loc = db.StringProperty()
	pict_url = db.StringProperty()

class Reply(db.Model):
	text = db.StringProperty()
	uname = db.StringProperty()
	datetime = db.DateTimeProperty()
	#datetime = db.DateTimeProperty(auto_now_add=True)

class Odai(db.Model):
	text = db.StringProperty()
	uname = db.StringProperty()
	datetime = db.DateTimeProperty()
