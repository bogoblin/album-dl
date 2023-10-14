import tempfile
from yt_dlp import YoutubeDL
import pathlib
import requests
import shutil
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def download_album(album_options, track_options):
    album_artist = album_options['artist']
    album_name = album_options['title']

    # We create a temporary directory to work in, otherwise
    # foobar2000 can start reading the files:
    temp_dir = tempfile.mkdtemp()

    # Create output directory:
    music_dir = pathlib.Path('D:\\Music')
    album_dir = music_dir / album_artist / album_name
    os.makedirs(album_dir, 0o777, True)

    thumbnail_response = requests.get(album_options['thumbnailUrl'], stream=True)
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
        info = ydl.extract_info(album_options['audioPlaylistId'])
        total_tracks = len(info['entries'])
        for options_for_track, entry in zip(track_options, info['entries']):
            track_number = int(options_for_track['track-number'])
            for download in entry['requested_downloads']:
                if not options_for_track['enable']:
                    continue
                file_path = download['filepath']
                mp3 = MP3(file_path, ID3=EasyID3)
                mp3['tracknumber'] = f'{track_number}/{total_tracks}'
                mp3['albumartist'] = album_artist
                mp3['artist'] = album_artist
                mp3['date'] = f'{album_options["year"]}'
                mp3['title'] = options_for_track['title']
                mp3.save()
                shutil.move(file_path, album_dir)
                break

        print(f'Downloaded album to {album_dir}')
        return info
