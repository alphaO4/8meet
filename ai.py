import openai
from lyrics import main
import urllib.request
import os
import json
import moviepy.video.io.ImageSequenceClip as movieclip
import random

openai.api_key = open("./dalle-key.txt").read()
images = []
imagetimes = []

def generateImage(i):
    response = openai.Image.create(
        prompt=i,
        n=1,
        size="256x256",
    )
    image_url = response['data'][0]['url']
    print("Generated Image for", i + ":", image_url)
    urllib.request.urlretrieve(image_url, "images/" + str(len(images)) + ".png")
    images.append(i)
    imagetimes.append(random.random() * 15)

try:
    os.mkdir("./images")
except Exception:
    None

for i in main(input("Enter Song: ")):
    if(len(i)):
        generateImage(i)

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
movieclip.ImageSequenceClip(imagefiles, 1).write_videofile("video.mp4")
print("done")