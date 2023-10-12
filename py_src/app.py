from flask import Flask, request
from ytmusicapi import YTMusic

import downloader

app = Flask(__name__)


@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query', '')
    ytmusic = YTMusic()
    search = ytmusic.search(query, 'albums')
    for album in search:
        album['href'] = "/album?browseId="+album['browseId']
    return search


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
