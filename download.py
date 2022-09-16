import youtube_dl
import os


audio_folder="raw_audio"
if not os.path.exists(audio_folder):
    os.mkdir(audio_folder)

with open("youtubeLinks.txt", 'r') as f:
    for line in f:
        song_idx,link = line.strip().split(' ')

        print(link)

        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'raw_audio/'+song_idx+'.webm',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
