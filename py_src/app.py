from flask import Flask, request, send_file, render_template
from ytmusicapi import YTMusic
from threading import Thread

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
    return send_file("static/index.html")


@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query', '')
    ytmusic = YTMusic()
    search = ytmusic.search(query, 'albums')
    output = ''
    for album in search:
        output += f'<li hx-get="/album?browseId={album["browseId"]}" hx-trigger="load"></li>'
    return output


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
    url = 'http://127.0.0.1:5000'
    webbrowser.open(url)
    app.run()
