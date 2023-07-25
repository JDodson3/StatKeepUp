from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Player:
    db = "ship2you"
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.height = db_data['height']
        self.weight = db_data['weight']
        self.grade = db_data['grade']
        self.points_game = db_data['points_game']
        self.rebounds_game = db_data['rebounds_game']
        self.assists_game = db_data['assists_game']
        self.blocks_game = db_data['blocks_game']
        self.steals_game = db_data['steals_game']
        self.bio = db_data['bio']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def save(cls,form_data):
        query = 'INSERT INTO players (first_name, last_name, height, weight, grade, points_game, rebounds_game, assists_game, blocks_game, steals_game, bio, user_id) VALUES (%(first_name)s,%(last_name)s,%(height)s,%(weight)s,%(grade)s,%(points_game)s,%(rebounds_game)s,%(assists_game)s,%(blocks_game)s,%(steals_game)s,%(bio)s,%(user_id)s);'
        return connectToMySQL(cls.db).query_db(query,form_data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM players JOIN users on players.user_id = users.id;'
        results = connectToMySQL(cls.db).query_db(query)
        players = []
        for row in results:
            this_player = cls(row)
            user_data = {
                "id": row['users.id'],
                "team_name": row['team_name'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            coach = user.User(user_data)
            this_player.creator = coach
            players.append(this_player)
        return players
        
    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM players WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def update(cls,form_data):
        query = 'UPDATE players SET first_name=%(first_name)s, last_name=%(last_name)s, height=%(height)s, weight=%(weight)s, grade=%(grade)s, points_game=%(points_game)s, rebounds_game=%(rebounds_game)s, assists_game=%(assists_game)s, blocks_game=%(blocks_game)s, steals_game=%(steals_game)s, bio=%(bio)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,form_data)

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM players WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_player(form_data):
        isValid = True
        if len(form_data['first_name']) < 2:
            flash("First Name must be at least 2 characters long.")
            isValid = False
        if len(form_data['last_name']) < 2:
            flash("Last Name must be at least 2 characters long.")
            isValid = False
        if float(form_data['height']) < 1:
            flash("Height must be at least 1 numbers long.")
            isValid = False
        if float(form_data['weight']) < 2:
            flash("Weight must be at least 2 numbers long.")
            isValid = False
        if len(form_data['grade']) < 2:
            flash("Class must be at least 2 characters long.")
            isValid = False
        if len(form_data['bio']) < 2:
            flash("Position must be at least 2 characters long.")
            isValid = False
        if float(form_data['points_game']) < 1:
            flash("Points per game must be at least 1 number long.")
            isValid = False
        if float(form_data['rebounds_game']) < 1:
            flash("Points per game must be at least 1 number long.")
            isValid = False
        if float(form_data['assists_game']) < 1:
            flash("Points per game must be at least 1 number long.")
            isValid = False
        if float(form_data['blocks_game']) < 1:
            flash("Points per game must be at least 1 number long.")
            isValid = False
        if float(form_data['steals_game']) < 1:
            flash("Points per game must be at least 1 number long.")
            isValid = False
        return isValid

    @classmethod
    def get_all_players_with_creator(cls, data ):
        query = "SELECT * FROM players JOIN users ON players.user.id = users.id;"
        results = connectToMySQL('rosters').query_db(query,data)
        all_players = []
        for row in results:
            one_player = cls(row)
            one_players_coach_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'team_name': row['team_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
                }
            coach = user.User(one_players_coach_info)
            one_player.creator = coach
            all_players.append(one_player)
        return all_players