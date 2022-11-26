from __future__ import unicode_literals

import openai
from lyrics import main
import urllib.request
import os
import json
import moviepy.video.io.ImageSequenceClip as movieclip
import moviepy.editor
import random
from mutagen.mp3 import MP3


from ytmusicapi import YTMusic
import youtube_dl

ytmusic = YTMusic("headers_auth.json")


def get_song_id(song):
    songid = ytmusic.search(query=song, filter="songs", limit=1)
    songid = songid[0]["videoId"]
    return songid

def makeMP3(songname):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(
            ["http://www.youtube.com/watch?v=" + get_song_id(songname)]
        )




openai.api_key = open("./dalle-key.txt").read()
images = []
imagetimes = []
chars = 0
videolength = 0
basesong = ""

def generateImage(i):
    #response = openai.Image.create(
    #    prompt=i,
    #    n=1,
    #    size="256x256",
    #)
    #image_url = response['data'][0]['url']
    #print("Generated Image for", i + ":", image_url)
    #urllib.request.urlretrieve(image_url, "images/" + str(len(images)) + ".png")
    images.append(i)
    imagetimes.append(len(i)/chars*videolength)


try:
    os.mkdir("./images")
except Exception:
    None
basesong = input("Enter Song: ")
for i in main(basesong):
    chars += len(i)
#makeMP3(basesong)
audio = MP3("song.mp3")
videolength = audio.info.length

for i in main(basesong):
    if(len(i)):
        generateImage(i)

print(imagetimes)

open("./images/images.json", "w").write(json.dumps({"images": images}))

#open("./images/imagetimes.txt", "w").write(imagetimes)

#os.system("ffmpeg-python -f concat -i ./images/imagetimes.txt -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4")


imagefiles = []
processed = 0
while(len(imagetimes)):
    print("appending frame")
    imagefiles.append("./images/" + str(processed) + ".png")
    imagetimes[0] -= 1
    if(imagetimes[0] <= 0):
        del imagetimes[0]
        del images[0]
        processed += 1
print("got all frames")
movieclip.ImageSequenceClip(imagefiles, 1).write_videofile("videoscreen.mp4")
videoscreen = moviepy.editor.VideoFileClip("videoscreen.mp4")
video = videoscreen.set_audio(moviepy.editor.AudioFileClip("song.mp3"))
video.write_videofile("video.mp4")
print("done")