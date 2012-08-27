from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index(color = "green"):
    return render_template('layout.html', color=color)

@app.route('/about')
def about():
    return 'Andy Satchwell, Nathan Addy, Andrew Sturges.'

if __name__ == '__main__':
    app.run(debug=True) #disable this before pushing to production
