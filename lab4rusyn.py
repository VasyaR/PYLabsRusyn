from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/hello-world-12")
def hello():
    return "<h1 style='color:blue'>Hello World 12</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
