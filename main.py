import os
import ffmpeg
import pytube
import json

with open("config.json") as f:
    config = json.load(f)

video = pytube.YouTube(f'https://www.youtube.com/watch?v={config["Youtube_id"]}')
Streams = video.streams
highresvid = Streams.filter(res = f"{config['quality']}", file_extension = 'mp4').first()  

highresvid.download(filename=f"{config['video_name']}_video.mp4")
stream = sorted([stream for stream in video.streams if stream.mime_type.startswith("audio")], key=lambda stream: int(stream.abr[:-4]), reverse=True)[0]
stream.download(filename=f"{config['video_name']}_audio.mp3")
video = ffmpeg.input(f"{config['video_name']}_video.mp4").video
audio = ffmpeg.input(f"{config['video_name']}_audio.mp3").audio
ffmpeg.output(
    video,
    audio,
    f"{config['video_name']}.mp4",
    vcodec='copy',
    acodec='copy',
).run()
os.remove(f"{config['video_name']}_video.mp4")
os.remove(f"{config['video_name']}_audio.mp3")
