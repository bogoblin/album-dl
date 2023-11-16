import time

import simple_websocket.ws
from flask import Flask, request, send_file, render_template
from flask_sock import Sock
from ytmusicapi import YTMusic
from threading import Thread
from tkinter import Tk
from tkinter.filedialog import askdirectory

import downloader
import webbrowser

app = Flask(__name__,
            static_url_path='',
            static_folder="static",
            template_folder="templates"
            )
app.config["TEMPLATES_AUTO_RELOAD"] = True

sock = Sock(app)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query', '')
    search = YTMusic().search(query, 'albums')
    return render_template(
        'search.html',
        search=search,
        number_of_results=len(search),
        query=query
    )


@app.route("/album", methods=['GET'])
def get_album():
    browse_id = request.args.get('browseId', '')
    album = YTMusic().get_album(browse_id)
    if request.accept_mimetypes.accept_html:
        return render_template('album.html', album=album)

    return album


@app.route("/download", methods=['POST'])
def download():
    album = downloader.Album(
        audioPlaylistId=request.form.get("audioPlaylistId"),
        thumbnailUrl=request.form.get("thumbnailUrl"),
        artist=request.form.get("artist"),
        title=request.form.get("title"),
        year=int(request.form.get("year")),
    )
    for i in range(1, 1000):
        if f'enable.{i}' not in request.form:
            break
        track = downloader.Track(
            video_id=request.form.get(f'id.{i}'),
            title=request.form.get(f'title.{i}'),
            track_number=int(request.form.get(f'track-number.{i}')),
            enabled=bool(request.form.get(f'enable.{i}')),
        )
        album.tracks.append(track)
    t = Thread(target=downloader.download_album, args=[album])
    t.start()
    return 'Downloading...'


@sock.route('/downloads')
def downloads(web_socket: simple_websocket.ws.Server):
    last_updated = 0
    while web_socket.connected:
        updated_albums = downloader.get_updates_since(last_updated)
        web_socket.send(render_template(
            "partials/downloading_album.html",
            albums=updated_albums
        ))
        time.sleep(1)


if __name__ == '__main__':
    Tk().withdraw()
    downloader.MusicDirectory = askdirectory(mustexist=True, title="Choose music directory")
    url = 'http://127.0.0.1:5000'
    webbrowser.open(url)
    app.run()
