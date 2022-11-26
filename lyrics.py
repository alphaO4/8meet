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
        print("Lyrics found in database")
        if (len(x['title']) > 0):
            return(x['data'])
        
    print("Lyrics not found in Database")
    lyrics = get_lyrics(song)
    mydict = { "title": song.lower(), "data": lyrics['lyrics'] }
    mycol.insert_one(mydict)
    return lyrics

# Get the lyrics from the API
def get_lyrics(song):
    songid = get_song_id(song)
    playlist = ytmusic.get_watch_playlist(songid)
    #print("Song ID: " + songid)
    #add song to playlist
    lyrics = ytmusic.get_lyrics(browseId = playlist["lyrics"])
    #print(lyrics)
    return lyrics

def main(song):
    song_lower = song.lower()
    lyrics = check_if_lyrics_exist(song_lower)
    #lyrics = lyrics['lyrics'].replace("*\r*", "")
    #print(lyrics)
    lyrics = lyrics.split('\n')
    return lyrics

main("Yesterday")