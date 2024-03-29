#!/usr/bin/env python3
from flask import Flask, abort, request, g

from passlib.hash import pbkdf2_sha256

from sqlalchemy.exc import IntegrityError
import json

from db import Db

app = Flask(__name__)

app.config['DATABASE'] = "devel.db"

@app.before_request
def before_request():
    g.db = Db(app.config['DATABASE'])

@app.route('/')
def hello():
    return "Lunchelp API"

@app.route('/user/add', methods=['POST'])
def user_add():
    if (request.form.get("email", "") == "" or
       request.form.get("name", "") == "" or
       request.form.get("password", "") == ""):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    hashed_pw = pbkdf2_sha256.encrypt(request.form['password'],
                                        rounds=20000, salt_size=16)

    user = g.db.User(email=request.form['email'],
            name=request.form['name'],
            password=hashed_pw)# TODO: hash password
    try:
        g.db.session.add(user)
        g.db.session.commit()#TODO: necessary?
    except IntegrityError:
        g.db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate user'})

    if user is None:
        return json.dumps({'status': 500, 'message': "Could not insert resturant"})

    return user.get_json()

@app.route('/user/get', methods=['POST'])
def user_get():
    if request.form.get("email", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    user = g.db.session.query(g.db.User).filter_by(email=request.form['email']).first()

    if user is None:
        return json.dumps({'status': 500, 'message': "Could not find user"})

    return user.get_json()

@app.route('/user/delete', methods=['POST'])
def user_delete():
    if request.form.get("email", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    user = g.db.session.query(g.db.User).filter_by(email=request.form['email']).first()

    if user is None:
        return json.dumps({'status': 500, 'message': "Could not find user"})

    g.db.session.delete(user)
    g.db.session.commit()

    return user.get_json()

@app.route('/group/add', methods=['POST'])
def group_add():
    if (request.form.get("name", "") == ""):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    group = g.db.Group(name=request.form['name'])

    try:
        g.db.session.add(group)
        g.db.session.commit()#TODO: necessary?
    except IntegrityError:
        g.db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate group'})#TODO: accurate?

    if group is None:
        return json.dumps({'status': 500, 'message': "Could not insert group"})

    return group.get_json()

@app.route('/group/get', methods=['POST'])
def group_get():
    if request.form.get("name", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    group = g.db.session.query(g.db.Group).filter_by(name=request.form['name']).first()

    if group is None:
        return json.dumps({'status': 500, 'message': "Could not find group"})

    return group.get_json()

@app.route('/group/delete', methods=['POST'])
def group_delete():
    if request.form.get("name", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    group = g.db.session.query(g.db.Group).filter_by(name=request.form['name']).first()

    if group is None:
        return json.dumps({'status': 500, 'message': "Could not find group"})

    g.db.session.delete(group)
    g.db.session.commit()

    return group.get_json()
@app.route('/resturant/add', methods=['POST'])
def resturant_add():
    if (request.form.get("name", "") == "" or
        request.form.get("address", "") == ""):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    resturant = g.db.Resturant(name=request.form['name'], address=request.form['address'])

    try:
        g.db.session.add(resturant)
        g.db.session.commit()#TODO: necessary?
    except IntegrityError:
        g.db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate resturant'})#TODO: accurate?

    if resturant is None:
        return json.dumps({'status': 500, 'message': "Could not insert resturant"})

    return resturant.get_json()

@app.route('/resturant/get', methods=['POST'])
def resturant_get():
    if request.form.get("name", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    resturant = g.db.session.query(g.db.Resturant).filter_by(name=request.form['name']).first()

    if resturant is None:
        return json.dumps({'status': 500, 'message': "Could not find resturant"})

    return resturant.get_json()

@app.route('/resturant/delete', methods=['POST'])
def resturant_delete():
    if request.form.get("name", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    resturant = g.db.session.query(g.db.Resturant).filter_by(name=request.form['name']).first()

    if resturant is None:
        return json.dumps({'status': 500, 'message': "Could not find resturant"})

    g.db.session.delete(resturant)
    g.db.session.commit()

    return resturant.get_json()

@app.route('/event/add', methods=['POST'])
def event_post():
    if (request.form.get("name", "") == "" or
        request.form.get("desc", "") == "" or
        request.form.get("resturant_id", "") == "" or
        request.form.get("group_id", "") == "" or
        request.form.get("time", "") == ""):#TODO: int validation?
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    event = g.db.Event(name=request.form['name'],
                    desc=request.form['desc'],
                    resturant_id=int(request.form['resturant_id']),
                    group_id=int(request.form['group_id']),
                    time=int(request.form['time']))

    try:
        g.db.session.add(event)
        g.db.session.commit()#TODO: necessary?
    except IntegrityError:
        g.db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate event'})#TODO: accurate?

    if event is None:
        return json.dumps({'status': 500, 'message': "Could not insert event"})

    return event.get_json()

@app.route('/event/get', methods=['POST'])
def event_get():
    if request.form.get("id", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    event = g.db.session.query(g.db.Event).filter_by(id=request.form['id']).first()

    if event is None:
        return json.dumps({'status': 500, 'message': "Could not find event"})

    return event.get_json()

@app.route('/event/delete', methods=['POST'])
def event_delete():
    if request.form.get("id", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    event = g.db.session.query(g.db.Event).filter_by(id=request.form['id']).first()

    if event is None:
        return json.dumps({'status': 500, 'message': "Could not find event"})

    g.db.session.delete(event)
    g.db.session.commit()

    return event.get_json()

@app.route('/userevent/add', methods=['POST'])
def event_post():
    if (request.form.get("user_id", "") == "" or
        request.form.get("group_id", "") == "" or
        request.form.get("is_admin", "") == ""):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    user_group = g.db.UserGroup(user_id=request.form['user_id'],
                            group_id=request.form['group_id'],
                            is_admin=request.form['is_admin'])

    try:
        g.db.session.add(user_group)
        g.db.session.commit()#TODO: necessary?
    except IntegrityError:
        g.db.session.rollback()
        return json.dumps({'status': 400, 'message': 'Duplicate usergroup'})#TODO: accurate?

    if user_group is None:
        return json.dumps({'status': 500, 'message': "Could not insert event"})

    return user_group.get_json()

@app.route('/usergroup/get', methods=['POST'])
def event_get():
    if request.form.get("id", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    user_group = g.db.session.query(g.db.UserGroup).filter_by(id=request.form['id']).first()

    if user_group is None:
        return json.dumps({'status': 500, 'message': "Could not find event"})

    return user_group.get_json()

@app.route('/event/delete', methods=['POST'])
def event_delete():
    if request.form.get("id", "") == "":
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    event = g.db.session.query(g.db.Event).filter_by(id=request.form['id']).first()

    if event is None:
        return json.dumps({'status': 500, 'message': "Could not find event"})

    g.db.session.delete(event)
    g.db.session.commit()

    return event.get_json()

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove after dev
