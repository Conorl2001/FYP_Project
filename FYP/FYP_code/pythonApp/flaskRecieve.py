from threading import Thread
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from flask_cors import CORS
import main


def runFlaskReceiver(button, progress, progressLabel):
    app = Flask(__name__)
    CORS(app)

    @app.route('/', methods=['POST'])
    def receive_url():
        url = request.json['url']
        parsedURL = urlparse(url)
        domain = parsedURL.netloc
        progress["length"] = 400
        progressLabel.config(text=domain + " is currently being scanned")
        result = main.runCore(url, progress)
        progress["value"] = 0
        response = {'result': result}
        progressLabel.config(text=url + " has been scanned")
        return jsonify(response)

    def runFlask():
        try:
            app.run(port=5000)
        except Exception as e:
            button.config(text="Error")

    # Start Flask app in a separate thread to prevent GUI freezing
    flaskThread = Thread(target=runFlask)
    flaskThread.daemon = True
    flaskThread.start()
    
    # Change the button text to "Running"
    button.config(text="Running")