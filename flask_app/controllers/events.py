# imports
from flask_app import app, render_template, redirect, request, session, flash

import pprint
pp = pprint.PrettyPrinter(indent=4)
import os
import requests

from flask_app.models.event import Event
from flask_app.models.like import Like





#! Main Show Page
@app.route('/events/dashboard')
def dashboard():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    
    # create filted events if there is a filter
    # events = Event.read_all_filter_day_of_week(data={'user_id': session['user_id']}, filters=session['filters']) if ("filters" in session) else Event.read_all(data={"user_id": session["user_id"]})

    if "search" in session:
        events = Event.search(data={"search": session["search"], 'user_id': session['user_id']})
        # clears all the search and filters 
        session.pop("search")
        if "filters" in session:
            session.pop("filters") 
    elif "filters" in session:
        events = Event.read_all_filter_day_of_week(data={'user_id': session['user_id']}, filters=session['filters'])
        # clears all the search and filters 
        if "search" in session:
            session.pop("search")
    else:
        events = Event.read_all(data={"user_id": session["user_id"]})

    filters = session['filters'] if ("filters" in session) else []

    return render_template('event_dashboard.html', 
                            events=events, 
                            filters=filters)


#! Create Event Page
@app.route('/events/create')
def create_events_page():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    return render_template('event_create.html')


#! Creat Event POST
@app.route('/events/create', methods=['POST'])
def create_events_post():
    id_created = Event.create(request.form)
    # pp.pprint(request.form)
    return redirect('/users/dashboard/myevents')



#! Deleteing events POST
@app.route('/events/delete', methods=['POST'])
def delete():
    Like.delete_all_likes_for_events(data={'event_id': request.form['id']})
    Event.delete(request.form)
    return redirect('/users/dashboard/myevents')


#! Updating Events - Page
@app.route('/users/dashboard/events/edit/<string:id>')
def edit_events_page(id):
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')

    event = Event.read_one(data={'user_id': session['user_id'], 'id': id})
    # pp.pprint(vars(event))
    # pp.pprint(event.start_time)

    if str(event.user_id) != session['user_id']:
        return redirect('/')


    # change the time object to correct html format
    s = event.start_time.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    event.start_time = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    # change the time object to correct html format
    s = event.end_time.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    event.end_time = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    return render_template('user_dashboard_my_events_edit.html', event=event)


#! Updating events POST
@app.route('/events/update', methods=['POST'])
def update():
    Event.update(request.form)
    return redirect(f'/users/dashboard/events/edit/{request.form["id"]}')


# *================================================================
# * Events Date Query Routes
# *================================================================

#! Get Events Today
@app.route('/events/dashboard/today')
def events_today():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    events = Event.read_all_today(data={'user_id': session['user_id']})
    return render_template('event_dashboard.html', events=events)

#! Get events Tommorrow
@app.route('/events/dashboard/tommorrow')
def events_tommorrow():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    events = Event.read_all_tommorrow(data={'user_id': session['user_id']})
    return render_template('event_dashboard.html', events=events)


#! Get events thursdays
@app.route('/events/dashboard/thursdays')
def events_thursdays():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    events = Event.read_all_thursdays(data={'user_id': session['user_id']})
    return render_template('event_dashboard.html', events=events)


#! Get events fridays
@app.route('/events/dashboard/fridays')
def events_fridays():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    events = Event.read_all_fridays(data={'user_id': session['user_id']})
    return render_template('event_dashboard.html', events=events)

#! Get events weekend
@app.route('/events/dashboard/weekend')
def events_weekend():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    events = Event.read_all_this_weekend(data={'user_id': session['user_id']})
    return render_template('event_dashboard.html', events=events)

#! Get events this month
@app.route('/events/dashboard/month')
def events_month():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    events = Event.read_all_this_month(data={'user_id': session['user_id']})
    return render_template('event_dashboard.html', events=events)



# *================================================================
# * Events Filter routes
# *================================================================
#! Filter Events POST
@app.route('/events/filter', methods=['POST'])
def events_filter():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    
    session['filters'] = request.form.getlist('dayfilter')
    # pp.pprint(dayfilters)
    # session['filterd_events'] = Event.read_all_filter_day_of_week(dayfilters)
    # session['filters'] = dayfilters
    # pp.pprint(session['filters'])
    return redirect('/events/dashboard')


#! Filter clear
@app.route('/events/filters/clear')
def events_filters_clear():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    
    # clear the filters
    if "filters" in session:
        session.pop("filters")

    return redirect('/events/dashboard')



#! Like Request 
# @app.route('/events/like/<string:id>')
# def like_event(id):
#     # check if they are logged in
#     if not "user_id" in session:
#         return redirect('/')

#     data = {
#         "user_id" : session['user_id'],
#         "event_id" : id
#     }
#     if not Like.check_like(data):
#         connection_id = Like.create_connect(data)
#     # pp.pprint(data)
#     return redirect(request.referrer)


#! Like POST
@app.route('/events/like' , methods=['POST'])
def like_event():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')

    # pp.pprint(request.form)
    data = {
        "event_id" : request.form["event_id"],
        "user_id" : session["user_id"]
    }
    if request.form['liked'] == '1':
        Like.delete_connect(data)
    else:
        if not Like.check_like(data):
            Like.create_connect(data)
        
    return redirect(request.referrer)

#! Remvoe Like  
@app.route('/events/likes/remove', methods=['POST'])
def unlike_event():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')

    data = {
        "user_id" : session['user_id'],
        "event_id" : request.form['event_id']
    }
    Like.delete_connect(data)
    # pp.pprint(data)
    return redirect(request.referrer)


# *================================================================
# * Search
# *================================================================

@app.route('/events/search', methods=['POST'])
def search():
    # pp.pprint(request.form)
    # data = {
    #     "search" : f'%%{request.form["search"]}%%',
    #     "user_id" : session['user_id']
    # }
    session['search'] = f'%%{request.form["search"]}%%'
    # events = Event.search(data)
    # pp.pprint([vars(i) for i in events])
    
    return redirect('/events/dashboard')


# *================================================================
# * Show individual event
# *================================================================
@app.route('/events/show/<string:id>') 
def show_event(id):
    event = Event.read_one(data={'user_id': session['user_id'], 'id': id})
    # pp.pprint(vars(event))
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    res = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={event.place}&key={api_key}').json()

    # pp.pprint(res)
    # TODO: default is royce hall
    location = res['results'][0]['geometry']['location'] if res['status'] == 'OK' else {'lat': 34.0728552, 'lng': -118.4421766}


    # pp.pprint(location)


    return render_template('event_show_v1.html', event=event, location=location, api_key=api_key)