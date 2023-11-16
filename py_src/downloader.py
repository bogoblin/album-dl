import re
import tempfile
import time
from dataclasses import dataclass, field
from yt_dlp import YoutubeDL
import pathlib
import requests
import shutil
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

MusicDirectory = ''


@dataclass
class Track:
    video_id: str
    enabled: bool
    track_number: int
    title: str
    latest_download_event: dict | None = None


@dataclass
class Album:
    audioPlaylistId: str
    thumbnailUrl: str
    title: str
    artist: str
    year: int
    tracks: list = field(default_factory=list)
    last_updated: float = 0

    def process_event(self, download_event):
        video_id = download_event["info_dict"]["id"]
        for track in self.tracks:
            if track.video_id == video_id:
                track.latest_download_event = download_event
                self.last_updated = time.time()
                return

        for track in self.tracks:
            if track.latest_download_event is None:
                track.latest_download_event = download_event
                track.video_id = video_id
                self.last_updated = time.time()
                return


albums = []


def add_album(album):
    albums.append(album)


def get_updates_since(time_seconds):
    return [album for album in albums if album.last_updated > time_seconds]


def download_album(album: Album):
    # We create a temporary directory to work in, otherwise
    # foobar2000 can start reading the files:
    temp_dir = tempfile.mkdtemp()

    # Create output directory:
    music_dir = pathlib.Path(MusicDirectory)
    album_dir = (music_dir
                 / sanitize_path_segment(album.artist)
                 / sanitize_path_segment(album.title)
                 )
    os.makedirs(album_dir, 0o777, True)

    thumbnail_response = requests.get(album.thumbnailUrl, stream=True)
    if thumbnail_response.status_code == 200:
        with open(album_dir / 'cover.jpg', 'wb') as f:
            shutil.copyfileobj(thumbnail_response.raw, f)

    add_album(album)

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
        'progress_hooks': [lambda event: album.process_event(event)]
    }) as ydl:
        info = ydl.extract_info(album.audioPlaylistId)
        total_tracks = len(info['entries'])
        for track, entry in zip(album.tracks, info['entries']):
            track_number = int(track.track_number)
            for download in entry['requested_downloads']:
                if not track.enabled:
                    continue
                file_path = download['filepath']
                mp3 = MP3(file_path, ID3=EasyID3)
                mp3['tracknumber'] = f'{track_number}/{total_tracks}'
                mp3['albumartist'] = album.artist
                mp3['album'] = album.title
                mp3['artist'] = album.artist
                mp3['date'] = f'{album.year}'
                mp3['title'] = track.title
                mp3.save()
                shutil.move(file_path, album_dir)
                break

        print(f'Downloaded album to {album_dir}')
        return info


def sanitize_path_segment(path_segment: str):
    not_allowed_in_path = re.compile(r"[:\\/<>\"|?*]")
    return not_allowed_in_path.sub(' ', path_segment)
