import sys
from ytmusicapi import YTMusic
from downloader import download_album

if __name__ == '__main__':
    query = ' '.join(sys.argv[1:])
    ytmusic = YTMusic()
    search = ytmusic.search(query, 'albums')
    download_album(search[0]['browseId'], ytmusic=ytmusic)
