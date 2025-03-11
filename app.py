from flask import Flask, render_template, request, redirect, url_for

parking = Flask(__name__)


@parking.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('warning'))
    return render_template('index.html')

@parking.route('/warning')
def warning():
    return render_template('warning.html')