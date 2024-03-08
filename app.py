from flask import Flask, request, send_file, render_template, Response
from pytube import YouTube, Playlist
import os
import zipfile
import io
import time


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def download_video(url):
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()
    download_path = audio_stream.download()
    return download_path


def download_video_zip(url):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()
        download_path = audio_stream.download()
        zip_file.write(download_path, os.path.basename(download_path))
        os.remove(download_path)
        time.sleep(1)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='audio.zip')


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    if 'playlist' in url:
        return download_playlist(url)
    else:
        return download_video_zip(url)
        # download_path = download_video(url)
        # return send_file(download_path, as_attachment=True)


def download_playlist(url):
    try:
        pl = Playlist(url)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            for video_url in pl.video_urls:
                yt = YouTube(video_url)
                audio_stream = yt.streams.get_audio_only()
                download_path = audio_stream.download(skip_existing=True)
                zip_file.write(download_path, os.path.basename(download_path))
                os.remove(download_path)
                time.sleep(1)
        zip_buffer.seek(0)
        return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='playlist.zip')
    except Exception as e:
        app.logger.error(f'Error downloading playlist: {e}')
        return Response(f'An error occurred: {e}', status=500)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

