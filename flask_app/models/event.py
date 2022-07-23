# imports
from dataclasses import dataclass
from doctest import debug_script
from re import X
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

# database
DATABASE = "bruinevents"

class Event:
    # ! contructor
    def __init__(self, data) -> None:
        # not null attributs
        # TODO: change this whenver you add new attributes
        self.id = data['id']
        self.name = data.get('name')
        self.description = data.get('description')
        self.event_date = data.get('event_date')
        self.start_time = data.get('start_time')
        self.end_time = data.get('end_time')
        self.place = data.get('place')
        self.event_image =data.get('event_image')
        self.user_id = data.get('user_id')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

        # additional join attributes
        # TODO: change this whenver you add new attributes


    # ! read all
    @classmethod
    def read_all(cls):
        query = "SELECT * from events"
        res = connectToMySQL(DATABASE).query_db(query)
        res_arr = []
        for row_dict in res:
            res_arr.append(cls(row_dict))
        return res_arr


    # ! read one
    @classmethod
    def read_one(cls, data):
        query = "SELECT * from events WHERE id = %(id)s"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            res_arr.append(cls(row_dict))
        return res_arr[0]

    
    #! create a new event
    @classmethod
    def create(cls, data):
        query = "INSERT INTO events (`name`, `description`, `place`, `event_date`, start_time, end_time, user_id) VALUES (%(name)s, %(description)s, %(place)s, %(event_date)s, %(start_time)s, %(end_time)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! delete one
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM events WHERE (`id` = %(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! update one event
    @classmethod
    def update(cls, data):
        query = "UPDATE events SET `name` = %(name)s, `description` = %(description)s, `event_date` = %(event_date)s, `start_time` = %(start_time)s, `end_time` = %(end_time)s, `place` = %(place)s WHERE (`id` = %(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)