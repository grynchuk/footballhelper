import os
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Kohana cemku"


app.run(host='0.0.0.0', port=os.environ['PORT'], debug=True)