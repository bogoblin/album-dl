import sys
from ytmusicapi import YTMusic
from downloader import download_album

if __name__ == '__main__':
    ytmusic = YTMusic()
    while True:
        query = input("Enter album name and artist: ")
        if len(query) == 0:
            exit(0)
        search = ytmusic.search(query, 'albums')
        for i, album in enumerate(search):
            album_artist = ', '.join([artist['name'] for artist in album['artists']])
            print(f'{i+1}. {album_artist} - {album["title"]}')
        choice = int(input("Enter choice: "))
        album = search[choice - 1]
        download_album(album['browseId'], ytmusic=ytmusic)
