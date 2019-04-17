from flask import Flask

import requests;
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/request")
def request():
    with open("data.json") as json_file:
        json_data = json.load(json_file)
    data = json.dumps(json_data)
    print(data)
    response = requests.post("http://127.0.0.1:4050/response", json=data)
    if response.ok:
        print(response.content)
    return '''
            <html><body>
            Hello. <a href="http://127.0.0.1:4050/get_csv">Click Here to Download the CSV.</a>
            </body></html>
            '''

if __name__== '__main__':
    app.run(port=4049)