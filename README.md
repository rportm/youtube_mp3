# YouTube Audio Downloader

This project is a Flask web application that allows users to download audio tracks from YouTube videos. It leverages the `pytube` library to fetch audio streams from YouTube and provide them to users as downloadable files.

## Features

- Download audio from individual YouTube videos
- Download audio from YouTube playlists

## Requirements

- Python 3.9+
- Docker (for running within a Docker container)

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/rportm/youtube_mp3.git
cd youtube-audio-downloader
```

## Running with Docker

```bash
docker build -t youtube-audio-downloader .
docker run -p 4000:80 youtube-audio-downloader
```
