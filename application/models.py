from datetime import datetime
from application import db
from werkzeug.security import generate_password_hash,check_password_hash
from application import login
from flask_login import UserMixin
 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
          
class User(UserMixin,db.Model):
      def set_password(self,password):
          self.password_hash = generate_password_hash(password)
        
      def check_password(self,password):
          return check_password_hash(self.password_hash,password)
      
      id = db.Column(db.Integer,primary_key = True,unique = True)
      username = db.Column(db.String(64),index = True,unique = True)
      email =  db.Column(db.String(120),index = True,unique = True)
      password_hash = db.Column(db.String(128))
      posts = db.relationship('Posts',backref = 'author',lazy = 'dynamic')
      devices = db.relationship('Devices', backref='Owner', lazy='dynamic')

      @login.user_loader
      def load_user(id):
          return User.query.get(int(id))
      
      def __repr__(self):
          return "<User {}>".format(self.username)
       
class Posts(db.Model):
      id = db.Column(db.Integer,primary_key = True,unique = True)
      body = db.Column(db.String(140))
      timestamp = db.Column(db.DateTime,index = True,default = datetime.utcnow)
      user_id = db.Column(db.Integer,db.ForeignKey('user.id')) 

      def __repr__(self):
          return "<Post {}>".format(self.body)

"""class Loads(db.Model):
      id = db.Column(db.Integer,primary_key = True,unique = True)
      name = db.Column(db.String(140))
      power = db.Column(db.Integer)
      user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
      
      def __repr__(self):
          return "<Load {} with Power {}>".format(self.name,self.Power)"""

class Devices(db.Model):
      id = db.Column(db.Integer,primary_key = True,unique = True)
      name = db.Column(db.String(140))
      power = db.Column(db.Integer)
      user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
      
      def __repr__(self):
          return "<Device {} with Power {}>".format(self.name,self.power)
