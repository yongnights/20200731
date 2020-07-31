#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm

from wtforms import Form, StringField, SelectField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField("Email ", validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken!')


class ReceipesSearch(Form):
    # choices = [('Receipe', 'Receipe'), ('Type', 'Type'), ('Ingredient', 'Ingredient')]
    # select = SelectField('Search for receipes: ', choices=choices)
    select = StringField('Search for receipes: ')
    # search = StringField('')


class ReceipesForm(Form):
    title = StringField('Title: ', validators=[DataRequired()])
    type = StringField('Type: ', validators=[DataRequired()])
    release_date = StringField('Release_date: ', validators=[DataRequired()])
    ingredients = StringField('Ingredients: ', validators=[DataRequired()])
    content = StringField('Content: ', validators=[DataRequired()])
    contributor_id = StringField('contributor_id: ', validators=[DataRequired()])
    contributor_name = StringField('contributor_name: ', validators=[DataRequired()])
    images = StringField('images: ', validators=[DataRequired()])
