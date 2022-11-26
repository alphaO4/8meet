from __future__ import unicode_literals
from ytmusicapi import YTMusic
import youtube_dl

ytmusic = YTMusic("headers_auth.json")


def get_song_id(song):
    songid = ytmusic.search(query=song, filter="songs", limit=1)
    songid = songid[0]["videoId"]
    return songid


ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
            "name": "song.mp3",
        }
    ],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(
        ["http://www.youtube.com/watch?v=" + get_song_id(input("Enter a song: "))]
    )
