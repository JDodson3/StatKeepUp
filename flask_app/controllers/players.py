from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.player import Player
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    # catch for invalid user_id somehow being in session, clear it via logout so user can login
    if not user:
        return redirect('/user/logout')
    data ={
        'id': session['user_id']
    }  
    return render_template('dashboard.html', user=user, players=Player.get_all())

@app.route('/players/new')
def add_player():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('new_player.html', user=user)

@app.route('/players/new/create', methods=['POST'])
def create_player():
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'grade': request.form['grade'],
            'points_game': request.form['points_game'],
            'rebounds_game': request.form['rebounds_game'],
            'assists_game': request.form['assists_game'],
            'blocks_game': request.form['blocks_game'],
            'steals_game': request.form['steals_game'],
            'bio': request.form['bio'],
            'user_id': session['user_id']
	}    
    Player.save(data)
    return redirect('/dashboard')

@app.route('/players/<int:id>/view')
def view_player(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({'id':session['user_id']})
    return render_template('view_player.html', user=user, player=Player.get_by_id({'id': id}))

@app.route('/players/<int:id>/edit')
def edit_player(id):
	if 'user_id' not in session:
		return redirect('/')
	user = User.get_by_id({"id":session['user_id']})
	return render_template('edit_player.html', user=user, player=Player.get_by_id({'id':id}))

@app.route('/players/<int:id>/update', methods=['POST'])
def update_player(id):
	if 'user_id' not in session:
		return redirect('/')
	if not Player.validate_player(request.form):
		return redirect(f'/players/{id}/edit')
	data = {
		'id': id,
		'first_name': request.form['first_name'],
		'last_name': request.form['last_name'],
		'height': request.form['height'],
		'weight': request.form['weight'],
		'grade': request.form['grade'],
		'points_game': request.form['points_game'],
		'rebounds_game': request.form['rebounds_game'],
		'assists_game': request.form['assists_game'],
		'blocks_game': request.form['blocks_game'],
		'steals_game': request.form['steals_game'],
		'bio': request.form['bio']
	}
	Player.update(data)
	return redirect('/dashboard')

@app.route('/players/<int:id>/delete')
def delete_player(id):
	if 'user_id' not in session:
		return redirect('/')
	Player.delete({'id':id})
	return redirect('/dashboard')
