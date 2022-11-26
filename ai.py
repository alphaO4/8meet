import openai
from lyrics import main
import urllib.request
import os
import json

openai.api_key = open("./dalle-key.txt").read()
images = []

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

try:
    os.mkdir("./images")
except Exception:
    None
for i in main(input("Enter Song: ")):
    if(len(i)):
        generateImage(i)

open("./images/images.json", "w").write(json.dumps({"images": images}))
