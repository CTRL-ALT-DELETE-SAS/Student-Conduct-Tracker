from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from App.models import staff, User
from datetime import datetime, timedelta
from App.models.staff import Staff

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    jwt_authenticate_admin,
    login 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    staffuser = login(data['email'], data['password'])
    user = login(data['email'], data['password'])
    if user:
        session['logged_in'] = True
        token = jwt_authenticate(data['ID'], data['password'])
        return redirect('/staffHome')
    else:
        return redirect('/')
    #existing_staffuser = staff.query.filter((staff.email == data['email']) & (staff.password == data['password'] )).first()
    #if existing_staffuser:
    '''email = data.get('email')
    password = data.get('password')
    staffuser = login(data['email'], data['password'])
    existingstaffuser = staff.query.filter(email=email).first()
    if existingstaffuser and staffuser.check_password(password):
        return redirect('/staffHome')
    else:
        return redirect('/')'''
    #email = data.get('email')
    #return 'bad username or password given', 401


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return redirect('/'), jsonify('logged out!')
   

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
	data = request.json
	token = jwt_authenticate(data['ID'], data['password'])
	if not token:
		return jsonify(message='bad username or password given'), 401
	return jsonify(access_token=token)

@auth_views.route('/api/admin/login', methods=['POST'])
def admin_login_api():
  data = request.json
  token = jwt_authenticate_admin(data['ID'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)


@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"firstname: {jwt_current_user.firstname}, lastname: {jwt_current_user.lastname}, id : {jwt_current_user.ID}"})
