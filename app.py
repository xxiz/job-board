from modules import app, sqlalchemy, SQLAlchemy
from models import Job, db
import traceback # ! DEBUG
from flask import render_template, request, abort
import datetime, json

with open('site.json', 'r') as f:
    site_data = json.load(f)

# add jobe model to db
def new_job(model):
    try:
        db.session.add(model)
        db.session.commit()
    except Exception as e:
        print(f"Error adding job: {e}")
        with open('db_creation.log', 'w') as f:
            f.write(traceback.format_exc())

def modify_job(id, new_model):
    try:
        job = Job.query.filter_by(id=id).first()
        job.posted_on = new_model.posted_on
        job.expires_on = new_model.expires_on
        job.title = new_model.title
        job.summary = new_model.summary
        job.description = new_model.description
        job.company = new_model.company
        job.location = new_model.location
        job.url = new_model.url
        job.position = new_model.position
        db.session.commit()
    except Exception as e:
        print(f"Error modifying job: {e}")
        with open('db_creation.log', 'w') as f:
            f.write(traceback.format_exc())

def delete_job(id):
    try:
        job = Job.query.filter_by(id=id).first()
        db.session.delete(job)
        db.session.commit()
    except Exception as e:
        print(f"Error deleting job: {e}")
        with open('db_creation.log', 'w') as f:
            f.write(traceback.format_exc())

@app.route('/', methods=['GET'])
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs, config=site_data)

@app.route('/new/', methods=['POST', 'GET'])
def new():
    if request.method =="POST":
        new_posting = Job(
            posted_on = datetime.datetime.now(),
            expires_on = datetime.datetime.strptime(request.form['expires_on'], '%Y/%m/%d'),
            title = request.form['title'],
            summary = request.form['summary'],
            description = request.form['description'],
            company = request.form['company'],
            location = request.form['location'],
            url = request.form['url'],
            position = request.form['position']
        )
        try:
            new_job(new_posting)
        except Exception as e:
            print(f"Error adding job: {e}")
            with open('db_creation.log', 'w') as f:
                f.write(traceback.format_exc())
            abort(500)

        return "Success"
    else:
        return '''
        <form method="POST">
            Location: <input name="location" type="text">
            <br>
            Title: <input name="title" type="text">
            <br>
            Summary: <input name="summary" type="text">
            <br>
            Description: <input name="description" type="text">
            <br>
            Company: <input name="company" type="text">
            <br>
            Position: <input name="position" type="text">
            <br>
            URL: <input name="url" type="text">
            <br>
            Expires on: <input name="expires_on" type="text">
            <br>
            <input type="submit">
        </form>

        '''

@app.route('/edit/<int:id>/', methods=['POST'])
def edit(id):
    posted_on = datetime.datetime.strptime(request.form['posted_on'], '%Y/%m/%d')
    expires_on = datetime.datetime.strptime(request.form['expires_on'], '%Y/%m/%d')
    title = request.form['title']
    summary = request.form['summary']
    description = request.form['description']
    company = request.form['company']
    location = request.form['location']
    url = request.form['url']
    position = request.form['position']
    new_posting = Job(posted_on, expires_on, title, summary, description, company, location, url)
    modify_job(id, new_posting)
    return ""

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    delete_job(id)
    return ""

@app.route('/job/<int:id>/', methods=['GET'])
def job(id):
    job = Job.query.filter_by(id=id).first()
    if job is None:
        abort(404)
    return render_template('job.html', job=job, config=site_data)

@app.route('/jobmaster', methods=['GET'])
def login():
    return render_template('jobmaster.html')