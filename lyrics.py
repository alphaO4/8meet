#! /bin/python3
import requests
import json
from ytmusicapi import YTMusic
import pymongo

#Setup 
ytmusic = YTMusic('headers_auth.json')
client = pymongo.MongoClient("mongodb://localhost:27017/")

def get_song_id(song):
    songid = ytmusic.search(query=song, filter='songs', limit=1)
    songid = songid[0]['videoId']
    return songid

#make a Database request and check if the lyrics exist
#if they do, return the lyrics
#if they don't, call get_lyrics and return the lyrics
#def check_if_lyrics_exist(song):
#    db = client.8meet
#    collection = db.lyrics
    


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
    song = '"' + song + '"'
    lyrics = get_lyrics(song)
    verses = lyrics['lyrics'].split('\n')
    print(verses)

testing()