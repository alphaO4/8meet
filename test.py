import whisper

model = whisper.load_model("base.en")
result = model.transcribe("audio.opus")
for segment in result['segments']:
    text = segment['text']
    start = round(segment['start']/60, 2)
    end = round(segment['end']/60, 2)
    print('text:',text,'Start:', start, 'End:', end)

