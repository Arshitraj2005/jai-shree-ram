from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask app is running 24x7 using UptimeRobot!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# Optional for local testing
if __name__ == "__main__":
    keep_alive()
