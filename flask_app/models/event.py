# imports
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL

import pprint
pp = pprint.PrettyPrinter(indent=4)

# database
DATABASE = "bruinevents"

class Event:
    sql_query_select_with_login_liked = "SELECT * FROM events LEFT JOIN Likes ON likes.event_id = events.id AND likes.user_id = %(user_id)s"
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
        self.login_user_liked = False



    # *================================================================
    # * Basic CRUD
    # *================================================================


    # ! read one
    @classmethod
    def read_one(cls, data):
        query = Event.sql_query_select_with_login_liked + " WHERE events.id = %(id)s"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
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



    # *================================================================
    # * Events Date Queries
    # *================================================================

    # ! read all
    @classmethod
    def read_all(cls, data):
        query = Event.sql_query_select_with_login_liked + ";"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr

    #! select today's event
    @classmethod
    def read_all_today(cls, data):
        query = Event.sql_query_select_with_login_liked + " WHERE event_date >= CURDATE() AND event_date < CURDATE() + INTERVAL 1 DAY;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr


    #! select tommorrow's event
    @classmethod
    def read_all_tommorrow(cls, data):
        query = Event.sql_query_select_with_login_liked + " WHERE event_date > CURDATE() AND event_date <= CURDATE() + INTERVAL 1 DAY;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr
    

    #! select thursdays' event
    @classmethod
    def read_all_thursdays(cls, data):
        query = Event.sql_query_select_with_login_liked + " WHERE DAYOFWEEK(event_date) = 5;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr

    #! select fridays' event
    @classmethod
    def read_all_fridays(cls, data):
        query = Event.sql_query_select_with_login_liked + " WHERE DAYOFWEEK(event_date) = 6;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr
    
    #! select this weekend query
    @classmethod
    def read_all_this_weekend(cls, data):
        query = Event.sql_query_select_with_login_liked + " WHERE DAYOFWEEK(event_date) in (1, 7) AND event_date >= CURDATE() AND (event_date <= CURDATE() + INTERVAL 8 DAY);"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr

    #! select this month query
    @classmethod
    def read_all_this_month(cls, data):
        query = Event.sql_query_select_with_login_liked + " WHERE event_date >= CURDATE() AND (event_date <= CURDATE() + INTERVAL 31 DAY);"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr


    #! select filters with day of the week
    @classmethod
    def read_all_filter_day_of_week(cls, data, filters):
        # basic structure
        query = Event.sql_query_select_with_login_liked
        
        # append all the filters days
        if len(filters) > 0:
            query += " WHERE DAYOFWEEK(event_date) in ("
            for i in range(0, len(filters)):
                query += (filters[i] + ",") if (i != len(filters)-1) else (filters[i])
            query += ")"

        # ending semi colon
        query += ";"
        
        # run the query 
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr

    # *================================================================
    # * SEARCH QUERES
    # *================================================================

    @classmethod
    def search(cls, data):
        # basic structure
        query = Event.sql_query_select_with_login_liked + " WHERE name LIKE %(search)s OR place LIKE %(search)s OR description LIKE %(search)s;"

        
        # run the query 
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        for row_dict in res:
            # pp.pprint(row_dict)
            event = cls(row_dict)
            if str(row_dict.get('Likes.user_id')) == session['user_id']:
                event.login_user_liked = True
            res_arr.append(event)
        return res_arr