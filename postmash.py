from flask import Flask
app = Flask(__name__)

@app.route('/')
def butt():
    return 'Butt'

if __name__ == '__main__':
    app.run()
