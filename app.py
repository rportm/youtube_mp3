from flask import Flask, request, send_file, render_template
from pytube import YouTube
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    audio_stream = yt.streams.get_audio_only()
    download_path = audio_stream.download()
    # Here, you would convert download_path file to MP3 if it's not already in that format
    # For simplicity, let's assume it's already MP3
    return send_file(download_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)



#
# yt = YouTube("https://www.youtube.com/watch?v=WeZeTiIP_6k&list=PLH92bjCPygQACbmN693INMu0JrZT6GG2R&index=3", use_oauth=True, allow_oauth_cache=True)
# audio_stream = yt.streams.get_audio_only()
# download_path = audio_stream.download()