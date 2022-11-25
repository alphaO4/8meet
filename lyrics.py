#! /bin/python3
import requests
import json
from ytmusicapi import YTMusic

#Setup 
ytmusic = YTMusic()

# Get the lyrics from the API
def get_lyrics(song):


def main():
    song = input("Enter the song: ")
    lyrics = get_lyrics(song)
    verses = lyrics.split("\n\n")
    for verse in verses:
        print(verse)
        print("")
        # get the image from dall-e 2 

main()