# imports
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

# ! Improt any other models
from flask_app.models import event

# ! Change the name
DATABASE = "bruinevents"

class User:
    #! user contructor
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # external table
        self.myevents = []
        self.likedevents = []


    #! create a new user
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (`name`, `email`, `password`) VALUES (%(name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    #! read all users
    @classmethod
    def read_all(cls):
        query = "SELECT * from users"
        res = connectToMySQL(DATABASE).query_db(query)
        res_arr = []
        for row_dict in res:
            res_arr.append(cls(row_dict))
        return res_arr

    #! read one user
    @classmethod
    def read_one(cls, data):
        query = "SELECT * from users WHERE id = %(user_id)s"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            res_arr.append(cls(row_dict))
        return res_arr[0]

    #! read user by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * from users WHERE email = %(email)s"
        res = connectToMySQL(DATABASE).query_db(query, data)
        if len(res) < 1:
            return False
        # only the first one
        return cls(res[0])


    #! update user
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET `name` = %(name)s, `email` = %(email)s WHERE (`id` = %(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #! validate user register
    @staticmethod
    def validate_user_register(user:dict) -> bool:
        is_valid = True
        if (len(user['name']) < 3):
            flash("Name must be at least 3 characters", "name")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter valid email address", "email")
            is_valid = False

        if (len(user['password']) < 8):
            flash("Password must be at least 8 characters", "password")
            is_valid = False

        if (user['password'] != user['password_confirmed']):
            flash("Password did not match", "password_confirmed")
            is_valid = False

        data = {
            "email" : user['email']
        }
        #! email validation
        if User.get_by_email(data):
            flash("Email alreay taken", "email")
            is_valid = False

        return is_valid

    #! valid user login
    def validate_user_login(user:dict) -> bool:
        is_valid = True
        return is_valid

    #! read one - join - 
    @classmethod
    def read_one_join(cls, data):
        query = "SELECT * from users LEFT JOIN events ON events.user_id = users.id WHERE users.id = %(id)s;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        user = cls(res[0])
        # when there is no events
        if not res[0]['events.id']:
            return user

        # where there is event
        for row_dict in res:
            data = {
                "id" : row_dict['events.id'],
                "name" : row_dict['events.name'],
                "description" : row_dict['description'],
                "event_date" : row_dict['event_date'],   
                "start_time" : row_dict['start_time'],
                "end_time" : row_dict['end_time'],
                "place" : row_dict['place'],
                "event_image" : row_dict['event_image'],
                "user_id" : row_dict['user_id'],
                "created_at" : row_dict['events.created_at'],
                "updated_at" : row_dict['events.updated_at']
            }
            obj = event.Event(data)
            user.myevents.append(obj)
        return user


    #! read one - join - liked events
    @classmethod
    def read_one_join_likes(cls, data):
        query = "SELECT * FROM users LEFT JOIN likes on likes.user_id = users.id LEFT JOIN events ON events.id = likes.event_id WHERE users.id = %(id)s;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        user = cls(res[0])
        # when there is no events
        # if not res[0]['events.id']:
        #     return user

        # where there is event
        for row_dict in res:
            # to prevent the deleting the events users liked, but delted by others
            if not row_dict['events.id']:
                continue

            data = {
                "id" : row_dict['events.id'],
                "name" : row_dict['events.name'],
                "description" : row_dict['description'],
                "event_date" : row_dict['event_date'],   
                "start_time" : row_dict['start_time'],
                "end_time" : row_dict['end_time'],
                "place" : row_dict['place'],
                "event_image" : row_dict['event_image'],
                "user_id" : row_dict['user_id'],
                "created_at" : row_dict['events.created_at'],
                "updated_at" : row_dict['events.updated_at']
            }
            obj = event.Event(data)
            user.myevents.append(obj)
        return user
    
    # TODO implement validatio for update and create for events
    # #! valid update
    # @staticmethod
    # def validate_user_update(user:dict) -> bool:
    #     is_valid = True
    #     if (len(user['first_name']) < 3):
    #         flash("You must have at least 3 letters for first name", 'first_name')
    #         is_valid = False

    #     if (len(user['last_name']) < 3):
    #         flash("You must have at least 3 letters for last name", "last_name")
    #         is_valid = False

    #     if not EMAIL_REGEX.match(user['email']):
    #         flash("Please enter valid email address", "email")
    #         is_valid = False

    #     return is_valid














