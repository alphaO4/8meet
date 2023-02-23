import whisper

model = whisper.load_model("small.en")
result = model.transcribe("audio.opus")
print(result["text"])