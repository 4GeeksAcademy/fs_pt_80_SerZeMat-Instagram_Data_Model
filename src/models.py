import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Users Table 
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50),unique= True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    #Relationships. When there is more than one foreign key, we implement foreign_keys to control how the relationship is resolved
    followers = relationship('Followers', foreign_keys='Followers.user_to_id', back_populates='followed')
    following = relationship('Followers', foreign_keys='Followers.user_from_id', back_populates='follower')
    posts = relationship('Posts', back_populates='users')
    comments = relationship('Comments', back_populates='users')
    likes = relationship('Likes', back_populates='users')

# Followers Table
class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    #Relationships
    follower = relationship('Users', foreign_keys=[user_from_id], back_populates='following')
    followed = relationship('Users', foreign_keys=[user_to_id], back_populates='followers')

# Comments Table
class Comments (Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)  
    comment_text =Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    #relationship
    user = relationship('Users', back_populates='comments')
    post = relationship('Posts', back_populates='comments')
    


# Posts Table
class Posts (Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    #Relationship
    user = relationship('Users', back_populates='posts')
    media = relationship('Media', back_populates='posts')
    comments = relationship('Comments', back_populates='posts')
    likes = relationship('Likes', back_populates='posts')


# Medias Table
class Media (Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    #Relationship
    post = relationship('Posts', back_populates='media')


# Likes Table
class Likes (Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    #Relationahip
    user = relationship('Users', back_populates='likes')
    post = relationship('Posts', back_populates='likes')


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
