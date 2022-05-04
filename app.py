from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():    

    return render_template('index.html')

@app.route('/departures/<departure>/')
def departure():    

    return render_template('departure.html')

@app.route('/tours/<id>/')
def tour():    

    return render_template('tour.html')