import threading
import time
import webbrowser

from Downloader import Downloader
from Interface import Interface
from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == "POST":
        title = request.form['title'].strip()
        auth = request.form['by'].strip()
        print("->", title)
        d = threading.Thread(target=thread_function, args=(title, auth))
        d.start()

        return render_template('loading.html', title=title, auth=auth)

    return render_template('index.html')

@app.route('/send/<string:title>/<string:auth>', methods=['POST','GET'])
def download_file(title, auth):
    if auth == "1":
        auth = ""
    else:
        auth = " " + auth[1:]

    title = "/" + title + auth + ".mp4"
    d = Downloader()
    path = d.downloadPath + title
    return send_file(path, as_attachment=True)\

def thread_function(title, auth):
    interface = Interface()
    interface.download(title, auth)
    socketio.emit('ready', {'title': title, 'auth': auth})

def open_page_thread():
    webbrowser.open('http://127.0.0.1:5000')  # Go to example.com

def open_page():
    d = threading.Thread(target=open_page_thread, args=())
    d.start()

if __name__ == "__main__":
    open_page()
    app.run(debug=True)
    socketio.run(app)
