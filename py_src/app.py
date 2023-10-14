from flask import Flask, request, send_file
from ytmusicapi import YTMusic

import downloader

app = Flask(__name__,
            static_url_path='',
            static_folder="static")


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
    ytmusic = YTMusic()
    return ytmusic.get_album(browse_id)


@app.route("/download", methods=['POST'])
def download():
    album = request.get_json()
    browse_id = album['browseId']
    album = downloader.download_album(browse_id)
    return album
