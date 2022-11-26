#! /bin/python3
from ytmusicapi import YTMusic
from dotenv import dotenv_values
import pymongo

#Setup 
ytmusic = YTMusic('headers_auth.json')
config = dotenv_values(".env")
mylient = pymongo.MongoClient(config["ATLAS_URI"])
mydb = mylient[config["DB_NAME"]]

def get_song_id(song):
    songid = ytmusic.search(query=song, filter='songs', limit=1)
    songid = songid[0]['videoId']
    return songid

def check_if_lyrics_exist(song):
    #make a Database request and check if the lyrics exist
    #if they do, return the lyrics
    #if they don't, call get_lyrics and return the lyrics
    mycol = mydb["lyrics"]
    query = mycol.find({'title':song.lower()})
    for x in query:
        if (len(x['title']) > 0):
            return(x['data'])
    
    #print("Lyrics not found Song: " + song)
    return get_lyrics(song)

# Get the lyrics from the API
def get_lyrics(song):
    songid = get_song_id(song)
    playlist = ytmusic.get_watch_playlist(songid)
    #print("Song ID: " + songid)
    #add song to playlist
    lyrics = ytmusic.get_lyrics(browseId = playlist["lyrics"])
    #print(lyrics)
    return lyrics

def testing():
    song = input("Enter the song: ")
    lyrics = check_if_lyrics_exist(song)
    verses = lyrics['lyrics'].split('\n')
    print(verses)
def main(song):
    song_lower = song.lower()
    lyrics = check_if_lyrics_exist(song_lower)
    if "*\r*" in lyrics:
        print("removing \\r")
        lyrics = lyrics.replace("*\r*", "")
    lyrics = lyrics['lyrics'].split('\n')
    print(lyrics)

main("Yesterday")