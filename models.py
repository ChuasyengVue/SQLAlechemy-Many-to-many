"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg"



class User (db.Model):

    __tablename__ = 'users'


    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
        
    first_name = db.Column(db.Text,
                            nullable = False)
        
    last_name = db.Column(db.Text,
                            nullable = False)
        
        
    image_url = db.Column(db.Text,
                          nullable = False,
                          default = DEFAULT_IMAGE_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
         return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):

    __tablename__ = 'posts'


    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    title = db.Column(db.Text,
                      nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)
    
    created_at = db.Column(db.DateTime,
                           nullable = False,
                           default = datetime.datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    @property
    def friendly_date(self):
        """return time format date"""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    
    


class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)




class Tag(db.Model):

    __tablename__ = 'tags'


    id = db.Column(db.Integer,
                   primary_key =True,
                   autoincrement = True)
    
    name = db. Column(db.Text,
                      nullable = False,
                      unique = True)
    
    posts = db.relationship(
        'Post',
        secondary='posts_tags',
        # cascade='all, delete',
        backref='tags')


    
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)