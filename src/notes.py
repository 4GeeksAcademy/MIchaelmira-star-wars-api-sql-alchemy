# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
# from sqlalchemy.orm import declarative_base
# from eralchemy2 import render_er
# import datetime

# Base = declarative_base()


# class Planet(Base): 
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(500), nullable=True)
#     character_pic = db.Column(db.String(512), nullable=True)

# class Character(Base):
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(500), nullable=True)
#     character_pic = db.Column(db.String(512), nullable=True)

# class FavoriteLike(Base): 
    
#     id = db.Column(db.Integer, primary_key=True)
#     character_id = db.db.Column(db.Integer, db.ForeignKey('character.id'))
#     planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# class User(Base):
#     id = db.Column(db.Integer, primary_key=True)
#     register_id = db.Column(db.Integer, db.ForeignKey('register.id'))

#     def to_dict(self):
#         return {}

# ## Draw from SQLAlchemy base
# render_er(Base, 'diagram.png')
#     # def __repr__(self):
#     #     return '<User %r>' % self.username

#     # def serialize(self):
#     #     return {
#     #         "id": self.id,
#     #         "email": self.email,
#     #         # do not serialize the password, its a security breach
#     #     }