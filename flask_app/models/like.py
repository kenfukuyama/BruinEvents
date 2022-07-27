# imports
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

# import models
from flask_app.models import event
# database
DATABASE = "bruinevents"


class Like:
    #! like contructor
    def __init__(self, data) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.event_id = data['event_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    #! create many to many
    @staticmethod
    def create_connect(data):
        query = "INSERT INTO likes (`user_id`, `event_id`) VALUES (%(user_id)s, %(event_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #! Delete many to many
    @staticmethod
    def delete_connect(data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND event_id = %(event_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #! read user by email
    @classmethod
    def check_like(cls, data):
        query = "SELECT * from likes WHERE user_id = %(user_id)s AND event_id = %(event_id)s;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        if len(res) < 1:
            return False
        # only the first one
        return cls(res[0])


    #! Get all the likes of specific users
    @staticmethod
    def get_user_likes(data):
        query = "SELECT * from likes WHERE user_id = %(user_id)s;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        events_liked = []
        for row_dict in res:
            events_liked.append(row_dict['event_id'])

        return events_liked


