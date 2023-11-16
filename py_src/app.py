from flask import Flask, request, send_file, render_template
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
    track_options = []
    for i in range(1, 1000):
        if f'enable.{i}' not in request.form:
            break
        track_options.append({
            'enable': request.form.get(f'enable.{i}'),
            'track-number': request.form.get(f'track-number.{i}'),
            'title': request.form.get(f'title.{i}'),
        })

    t = Thread(target=downloader.download_album, args=(request.form, track_options))
    t.start()
    return 'Downloading...'


if __name__ == '__main__':
    Tk().withdraw()
    downloader.MusicDirectory = askdirectory(mustexist=True, title="Choose music directory")
    url = 'http://127.0.0.1:5000'
    webbrowser.open(url)
    app.run()
