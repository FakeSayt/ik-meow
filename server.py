from flask import Flask
import config
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=config.PORT)

Thread(target=run_web).start()
