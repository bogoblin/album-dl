import tempfile
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
import pathlib
import requests
import shutil
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def download_album(browse_id, ytmusic=YTMusic()):
    album = ytmusic.get_album(browse_id)
    album_artist = ', '.join([artist['name'] for artist in album['artists']])
    album_name = album['title']

    # We create a temporary directory to work in, otherwise
    # foobar2000 can start reading the files:
    temp_dir = tempfile.mkdtemp()

    # Create output directory:
    music_dir = pathlib.Path('D:\\Music')
    album_dir = music_dir / album_artist / album_name
    os.makedirs(album_dir, 0o777, True)

    # Download album cover:
    # Thumbnails are sorted, with highest resolution last, so pick that one:
    thumbnail_response = requests.get(album['thumbnails'][-1]['url'], stream=True)
    if thumbnail_response.status_code == 200:
        with open(album_dir / 'cover.jpg', 'wb') as f:
            shutil.copyfileobj(thumbnail_response.raw, f)

    with YoutubeDL({
        'paths': {
            'home': str(temp_dir)
        },
        'format': 'm4a/bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegMetadata', },
            {'key': 'FFmpegThumbnailsConvertor', },
            {  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }
        ],
        # 'keepvideo': True
    }) as ydl:
        info = ydl.extract_info(album['audioPlaylistId'])
        total_tracks = len(info['entries'])
        for track_number, entry in enumerate(info['entries']):
            for download in entry['requested_downloads']:
                file_path = download['filepath']
                try:
                    mp3 = MP3(file_path, ID3=EasyID3)
                    mp3['tracknumber'] = f'{track_number + 1}/{total_tracks}'
                    mp3['albumartist'] = album_artist
                    mp3['artist'] = album_artist
                    mp3['date'] = f'{album["year"]}'
                    mp3.save()
                    shutil.move(file_path, album_dir)
                    break
                except:
                    pass

    print(f'Downloaded album to {album_dir}')
    return album
