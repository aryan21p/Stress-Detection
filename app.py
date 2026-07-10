from flask import Flask, render_template
from routes.detection import detection

app = Flask(__name__)

app.register_blueprint(detection)

app.config["SECRET_KEY"] = "sensation-tech-secret-key"


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)