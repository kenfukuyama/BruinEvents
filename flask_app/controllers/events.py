# imports
from flask_app import app, render_template, redirect, request, session, flash
import pprint
pp = pprint.PrettyPrinter(indent=4)

from flask_app.models.event import Event

#! Main Show Page
@app.route('/events/dashboard')
def dashboard():
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    events = Event.read_all()
    return render_template('event_dashboard.html', events=events)


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
    Event.delete(request.form)
    return redirect('/users/dashboard/myevents')


#! Updating Events - Page
@app.route('/users/dashboard/events/edit/<string:id>')
def edit_events_page(id):
    # check if they are logged in
    if not "user_id" in session:
        return redirect('/')

    event = Event.read_one(data={"id": id})
    pp.pprint(vars(event))
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
