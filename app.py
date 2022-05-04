from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/data')
def index():    

    return render_template('index.html')

@app.route('/data/departures/<departure>/')
def departure():    

    return render_template('departure.html')

@app.route('/data/tours/<id>/')
def tour():    

    return render_template('tour.html')