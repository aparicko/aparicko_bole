import json
import logging
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, get_flashed_messages
import requests
import os

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

app = Flask(__name__)
app.secret_key = "my secret key"


data = {}

@app.route('/')
def home_page():
    return render_template('home.html', data=data)

@app.route('/create_job')
def create_job():
    print(request.args)
    messages = []
    if 'jobs' not in data:
        data.add('jobs', [])
    id = len(data['jobs']) + 1
    
    job = {"id": id, "status": "in-progress", "image_url": "https://via.placeholder.com/151", "jenkins_url": "https://via.placeholder.com/151"}
    if 'job name' in request.args and len(request.args['job name']) > 0:
        job['name'] = request.args['job name'] + '-' 
    if 'gbn' in request.args and len(request.args['gbn']) > 0:
        job['name'] += request.args['gbn']
    
    if 'name' not in job:
        job['name'] = 'Job default'
    
    data['jobs'].append(job)
    job_json_string = json.dumps(job)
    messages.append(f'Job {job["name"]} created successfully')

    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return render_template('home.html', data=data, messages=messages)


def init_db():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as json_file:
            global data 
            data = json.load(json_file)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
