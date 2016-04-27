import os
import webapp2
import jinja2
import hmac #Used for hashing 
import re #regular expression
import datetime
#Get networkx library from lib folder
from google.appengine.api import mail
import sys 
sys.path.insert(0, 'libs')

SECRET='pjiscool'
DATABASE_FETCH_LIMIT = 500 # max number of users to fetch from the db

from google.appengine.ext import db #Database


#Set up template directory
tempplate_dir = os.path.join(os.path.dirname(__file__),'templates')
#Set Up JinJa Environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(tempplate_dir), autoescape=True)

#Create a global dictionary to store newuser data
userinfo={"Status":"","firstname":"","surname":"","Languages":[],"Gender":"","Gender_Pref":"","DOB":"",
	"About":"","Location":"", "Email":""}

#User Database Model
class UserInfo(db.Model): #used to crete the database. Art is the name of the databse
	Status=db.StringProperty(required=True) #required = true adds the constraint
	firstname=db.StringProperty(required=True)
	surname=db.StringProperty(required=True)
	Language=db.StringListProperty(required=True)
	Gender=db.StringProperty(required=True)
	Gender_Pref=db.StringProperty(required=True)
	DOB=db.StringProperty(required=True)
	About=db.StringProperty(required=False)
	Email=db.StringProperty(required=True)
	Location=db.StringProperty(required=True)
	Latitude = db.FloatProperty(required=True)
	Longitude = db.FloatProperty(required=True)
	#password=db.StringProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True) #Automatically adds the time, check the docs


#Handler for write commands
class Handler(webapp2.RequestHandler):
	def write(self,*a,**kw): #the * takes unamed arguments, and the ** takes the named arguments
		self.response.out.write(*a,**kw)

	def render_str(self, template, **params):
		t= jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

#Home Page. Also has the possiblilty to generate a fixed database for trialing
class MainPage(Handler):

	def render_front(self, team="",names="",loc="",time_dep="",time_arr="",hitch=0,bike=0,
			walk=0,item_weight=0, alcohol=0,monuments=0, complete=False, error="",
			dist="",timeS="", hours="", bonus="", Total_Score=""):

		self.render("home.html", team=team,names=names,loc=loc,time_dep=time_dep,time_arr=time_arr,hitch=hitch,bike=bike,
			walk=walk,item_weight=item_weight, alcohol=alcohol,monuments=monuments, complete=complete,error=error,
			dist=dist,timeS=timeS, hours=hours, bonus=bonus, Total_Score=Total_Score)

	def get(self):
		self.render_front()

	def post(self):
		team=self.request.get("team")
		names=self.request.get("names")
		loc=self.request.get("loc")
		time_dep=self.request.get("time_dep")
		time_arr=self.request.get("time_arr")
		hitch=self.request.get("hitch")
		bike=self.request.get("bike")
		walk=self.request.get("walk")

		item_weight=self.request.get("item_weight")
		alcohol=self.request.get("alcohol")
		monuments=self.request.get("monuments")

		if not team or not names or not loc or not time_dep or not time_arr:
			error="Please complete the Form and click submit"
			complete=False
			Dist_score=0
			Time_Score=0
			Bonus_Score=0
			Total_Score=0
			hours_taken=0
		else:
			error=""
			complete=True
			print time_dep


			time_taken=datetime.datetime.strptime(time_arr, "%m/%d/%Y %H:%M %p")-datetime.datetime.strptime(time_dep, "%m/%d/%Y %H:%M %p")
			hours_taken= time_taken.total_seconds()/3600

			Dist_score=float(hitch)*2 + float(bike)*10 + float(walk)*20
			Time_Score=hours_taken*10
			Bonus_Score = float(item_weight)*20 + float(monuments)*50 + float(alcohol)*15

			Total_Score=Dist_score+Time_Score+Bonus_Score


		self.render_front(team=team,names=names,loc=loc,time_dep=time_dep,time_arr=time_arr,hitch=hitch,bike=bike,
			walk=walk,item_weight=item_weight, alcohol=alcohol,monuments=monuments, complete=complete,error=error, 
			dist=Dist_score,timeS=Time_Score, hours=hours_taken, bonus=Bonus_Score, Total_Score=Total_Score)





app = webapp2.WSGIApplication([
	('/', MainPage),


], debug=True)
