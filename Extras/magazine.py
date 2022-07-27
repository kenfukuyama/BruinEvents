from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


from flask_app.models import user



# ! Change the name if necessary
DATABASE = "users"


class Magazine:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = str(data['user_id'])
        self.first_name = ""
        self.last_name = ""
        self.users = []
        self.sub_count = 0




    # ! read all but with users joined
    @classmethod
    def read_all_join(cls):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id = magazines.user_id;"
        res = connectToMySQL(DATABASE).query_db(query)
        res_arr = []
        if not res:
            return res_arr

        for row_dict in res:
            obj = cls(row_dict)
            obj.first_name = row_dict['first_name']
            obj.last_name = row_dict['last_name']
            res_arr.append(obj)
        return res_arr


    #! read one - join
    @classmethod
    def read_one(cls, data):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id = magazines.user_id WHERE magazines.id = %(id)s;"
        res = connectToMySQL(DATABASE).query_db(query, data)
        res_arr = []
        if not res:
            return res_arr

        for row_dict in res:
            obj = cls(row_dict)
            obj.first_name = row_dict['first_name']
            obj.last_name = row_dict['last_name']
            res_arr.append(obj)
        return res_arr[0]

    # ! validation
    @staticmethod
    def validate(form:dict) -> bool:
        is_valid = True
        if (len(form['title']) < 2):
            flash("title must be at least 2 characters")
            is_valid = False
        if (len(form['description']) < 10):
            flash("description must be at least 10 characters")
            is_valid = False

        return is_valid

    # ! create new
    @classmethod
    def create(cls, data):
        query = "INSERT INTO magazines (`title`, `description`, `user_id`) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    # ! delete one
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM magazines WHERE (`id` = %(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    

    #! read_one - join many to many
    @classmethod
    def read_one_join_many(cls, data):
        query = "SELECT * from magazines LEFT JOIN subscriptions ON subscriptions.magazine_id = magazines.id LEFT JOIN users ON users.id = subscriptions.user_id WHERE magazines.id = %(id)s"
        res = connectToMySQL(DATABASE).query_db(query, data)

        magazine = cls(res[0])


        magazine.first_name = res[0]['first_name']
        magazine.last_name = res[0]['last_name']

        for row_dict in res:
            data = {
                "id" : row_dict["users.id"],
                "first_name" : row_dict["first_name"],
                "last_name" : row_dict["last_name"],
                "email" : row_dict["email"],
                "password" : row_dict["password"],
                "created_at" : row_dict["users.created_at"],
                "updated_at" : row_dict["users.updated_at"]
            }
            magazine.users.append(user.User(data))
        return magazine


    #! create many to many
    @classmethod
    def create_connect(cls, data):
        query = "INSERT INTO subscriptions (`user_id`, `magazine_id`) VALUES (%(user_id)s, %(magazine_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! update one
    @classmethod
    def update(cls, data):
        query = "UPDATE thoughts SET `like` = %(like)s WHERE (`id` = %(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)






    # ! delete one
    @staticmethod
    def delete(data):
        query = "DELETE FROM thoughts WHERE (`id` = %(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    #! create many to many
    @classmethod
    def create_connect(cls, data):
        query = "INSERT INTO likes (`user_id`, `thought_id`) VALUES ('3', '1');"
        return connectToMySQL(DATABASE).query_db(query, data)


    # ! read all
    @classmethod
    def read_all(cls):
        #! change the thought
        query = "SELECT * from thoughts"
        res = connectToMySQL(DATABASE).query_db(query)
        res_arr = []
        for row_dict in res:
            res_arr.append(cls(row_dict))
        return res_arr