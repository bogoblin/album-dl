from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
import pathlib
import requests
import shutil
import sys
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def download_album(ytmusic, query):
    search = ytmusic.search(query, 'albums')
    first_result = search[0]
    browse_id = first_result['browseId']
    album = ytmusic.get_album(browse_id)
    playlist_id = album['audioPlaylistId']
    artist = ', '.join([artist['name'] for artist in album['artists']])
    album_name = album['title']

    # Create output directory:
    music_dir = pathlib.Path('D:\\Music')
    artist_dir = music_dir / artist
    if not artist_dir.exists():
        os.mkdir(artist_dir)
    album_dir = artist_dir / album_name
    if not album_dir.exists():
        os.mkdir(album_dir)

    # Download album cover:
    # Thumbnails are sorted, with highest resolution last, so pick that one:
    thumbnail_url = album['thumbnails'][-1]['url']
    thumbnail_response = requests.get(thumbnail_url, stream=True)
    if thumbnail_response.status_code == 200:
        thumbnail_path = pathlib.Path(album_dir, 'cover.jpg')
        with open(thumbnail_path, 'wb') as f:
            shutil.copyfileobj(thumbnail_response.raw, f)

    with YoutubeDL({
        'paths': {
            'home': str(album_dir)
        },
        'postprocessors': [
            { 'key': 'FFmpegMetadata', },
            { 'key': 'FFmpegThumbnailsConvertor', },
            {  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }
        ],
        # 'keepvideo': True
    }) as ydl:
        info = ydl.extract_info(playlist_id)
        total_tracks = len(info['entries'])
        for track_number, entry in enumerate(info['entries']):
            for download in entry['requested_downloads']:
                file_path = download['filepath']
                try:
                    mp3 = MP3(file_path, ID3=EasyID3)
                    mp3['tracknumber'] = f'{track_number+1}/{total_tracks}'
                    mp3.save()
                    break
                except:
                    pass



    # zip_path = pathlib.Path(shutil.make_archive(album_directory, 'zip', album_directory))
    # shutil.move(zip_path, pathlib.Path("D:\\Music", zip_path.name))
    # shutil.rmtree(album_directory)


if __name__ == '__main__':
    yt_music = YTMusic()
    download_album(yt_music, ' '.join(sys.argv[1:]))
