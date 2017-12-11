#!/usr/bin/env python3
""" main webapp for project """
import os
from flask import Flask, request
from flask import render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

import pdb


app = Flask(__name__)
if os.path.isfile('config.py'):
    app.config.from_object('config')
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

users = ['anon', 'kevin', 'newsch']
materials = ['skin', 'organic', 'synthetic', 'blend']

class Slide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime())
    user = db.Column(db.String(64))
    speed = db.Column(db.Integer())
    material = db.Column(db.String(64))
    water = db.Column(db.Boolean())
    comments = db.Column(db.String(256))


    def __init__(self, user, speed, material, water, comments=None):
        self.time = datetime.utcnow()
        self.user = user
        self.speed = speed
        self.material = material
        self.water = water
        self.comments = comments

    # def __repr__(self):
    #     return "slide by {} \ton {}:\n\tspeed:\t{}\n\tmaterial:\t{}\n\twater:\t{}\n\tcomments:\t{}".format(self.user, self.time, self.speed, self.material, self.water, self.comments)


@app.route('/', methods=['POST', 'GET'])
def index():
    print(request.method)
    if request.method == 'POST':  # handle new datapoints
        print(request)
        print(request.form)
        filtered_request = {
            **request.values.to_dict(flat=True),
            'user': 'anon' if request.form['user'] == '' else request.form['user'],
            'speed': int(request.form['speed']),
            'water': bool(request.form.get('water')),
            'comments': None if request.form['comments'] == '' else request.form['comments'],
        }
        print(filtered_request)
        new_slide = Slide(**filtered_request)
        print('***New slide***\n{}'.format(new_slide))
        db.session.add(new_slide)
        db.session.commit()
        return redirect('/', code=303)
    else:  # return index page
        print('users: {}\nmaterials: {}'.format(users, materials))
        return render_template('add_slide.html', users=users, materials=materials)


if __name__ == '__main__':
    app.debug = True  # updates the page as the code is saved
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 9001))
    app.run(host='0.0.0.0', port=PORT)
