from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Running the tool!'

@app.route('/hello')
def hello():
    return 'In a hello function now.'

if __name__ == '__main__':
    app.run()
