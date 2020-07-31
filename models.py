#!/usr/bin/env python
#-*- coding: utf-8 -*-

from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        result = check_password_hash(self.password, password)
        return result

class Contributors(db.Model):
    __tablename__ = "contributors"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    def __repr__(self):
        return "<contributor: {}="">".format(self.user_name)

class Receipes(db.Model):
    __tablename__ = "receipes"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    release_date = db.Column(db.String)
    ingredients = db.Column(db.String)
    content = db.Column(db.String)
    contributor_id = db.Column(db.String)
    contributor_name = db.Column(db.String)
    images = db.Column(db.String)

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    def __init__(self, title, type, release_date,ingredients,content,contributor_id,contributor_name,images):
        self.title = title
        self.type = type
        self.release_date = release_date
        self.ingredients = ingredients
        self.content = content
        self.contributor_id = contributor_id
        self.contributor_name = contributor_name
        self.images = images