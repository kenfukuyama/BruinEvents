import re
from flask_app import app, render_template, redirect, request, session, flash


#! change this to current object
from flask_app.models.magazine import Magazine
from flask_app.models.user import User

import pprint
pp = pprint.PrettyPrinter(indent=4)



# ! read all
@app.route('/dashboard')
def dashboard():
    if not session['logged_in']:
        return redirect('/')

    # pp.pprint(Thought.read_all_join())
    magazines = Magazine.read_all_join()
    # pp.pprint(magazines)
    # recipes = Thought.read_all_join()

    # pp.pprint([i.first_name for i in recipes])
    # print(session['user_id'])


    return render_template('dashboard.html', magazines=magazines)


# # ! read one
@app.route("/show/<string:id>")
def show(id):
    if not session['logged_in']:
        return redirect('/')

    magazine = Magazine.read_one_join_many(data={"id":id})
    # pp.pprint(magazine)
    return render_template('show.html', magazine=magazine)




# ! create - template
@app.route("/magazines/new")
def add_magazine():
    if not session['logged_in']:
        return redirect('/')

    return render_template('create.html')


# ! create post
@app.route("/magazines/create", methods=["POST"])
def create_magazine():
    pp.pprint(request.form)
    if not Magazine.validate(request.form):
        return redirect("/magazines/new")
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "user_id" : session['user_id']
    }
    created_id = Magazine.create(data)
    return redirect("/dashboard")


# ! delete 
@app.route("/magazines/delete/<string:id>")
def delete(id):
    Magazine.delete(data={"id":id})
    return redirect(f'/users/{session["user_id"]}')


@app.route('/subscribe/<string:magazine_id>/<string:user_id>')
def books_users(magazine_id, user_id):
    data = {
        "user_id" : user_id,
        "magazine_id" : magazine_id
    }
    print(data)
    session["connection_id"] = Magazine.create_connect(data)
    return redirect("/dashboard")


# # ! Update - post
# @app.route('/like/<string:id>', methods=['POST'])
# def change_like(id):
#     thought = Thought.read_one(data={"id":id})
#     like = int(request.form['like'])
#     # print(int(thought.like) + like)
#     new_like = int(thought.like) + like

#     # print(request.form)
#     data = {
#         'id': id,
#         'like' : new_like
#     }
#     Thought.update(data)
#     return redirect("/dashboard")






# # ! create post
# @app.route("/recipes/create", methods=["POST"])
# def create_recipe():
#     pp.pprint(request.form)
#     if not Recipe.validate(request.form):
#         return redirect("/recipes/new")
#     data = {
#         "date": request.form['date'],
#         "descript": request.form['descript'],
#         "instruction" : request.form['instruction'],
#         "is_under" : request.form['is_under'],
#         "name" : request.form['name'],
#         "user_id" : session['user_id']
#     }
#     created_id = Recipe.create(data)
#     return redirect("/recipes")


# # ! Update - template
# @app.route('/recipes/edit/<string:recipe_id>')
# def edit_recipe(recipe_id):
#     recipe = Recipe.read_one(data={"recipe_id":recipe_id})
#     return render_template("edit.html", recipe=recipe)


# # ! Update - post
# @app.route('/recipes/update/<string:recipe_id>', methods=['POST'])
# def update_recipe(recipe_id):
#     # pp.pprint(request.form)
#     # print("running", request.form['name'])
#     if not Recipe.validate(request.form):
#         # print("wrong")
#         return redirect(f"/recipes/edit/{recipe_id}")
#     data = {
#         "date": request.form['date'],
#         "descript": request.form['descript'],
#         "instruction" : request.form['instruction'],
#         "is_under" : request.form['is_under'],
#         "name" : request.form['name'],
#         "id" : recipe_id
#     }
#     Recipe.update(data)
#     return redirect("/recipes")

# # ! delete 
# @app.route("/recipes/delete/<string:recipe_id>")
# def delete(recipe_id):
#     Recipe.delete(data={"id":recipe_id})
#     return redirect("/recipes")

