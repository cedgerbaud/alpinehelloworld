import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world ! This is Cedric\'s Alpine container speaking'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
