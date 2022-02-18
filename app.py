from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    #return "<h1>Hello~ flask</h1>"



app.run(debug=True)