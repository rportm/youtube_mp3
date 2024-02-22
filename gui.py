from tkinter import *
from tkinter import filedialog  # Import filedialog
from pytube import YouTube, Playlist  # Use pytube for YouTube interaction
from moviepy.editor import *
import os

# Initialize tkinter window
root = Tk()
root.geometry('500x300')  # Set the window size
root.title('YouTube Downloader')

# Add a text field to input the YouTube URL
url_label = Label(root, text='Enter YouTube URL or Playlist:', font=('calibre', 10, 'bold'))
url_label.pack()
url_entry = Entry(root, width=50)
url_entry.pack()

# Function to let user choose the download folder
def choose_download_folder():
    folder_selected = filedialog.askdirectory()  # Open dialog to choose folder
    if not folder_selected:  # If the user cancels the selection, use the current working directory
        return os.getcwd()
    return folder_selected

# Function to decide and download video or playlist
def download():
    url = url_entry.get()  # Get the URL from the entry widget
    if "list=" in url:
        download_playlist(url)
    else:
        download_video(url)

# Function to download single video
def download_video(url):
    folder = choose_download_folder()  # Let the user choose the download folder
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        video = yt.streams.filter(only_audio=True).first()
        output = video.download(output_path=folder)

        # Convert to MP3 using moviepy
        base, ext = os.path.splitext(os.path.basename(output))
        new_file_path = os.path.join(folder, base + '.mp3')
        clip = AudioFileClip(output)
        clip.write_audiofile(new_file_path)
        os.remove(output)

        action_button.config(text="Download Complete")
    except Exception as e:
        print(e)
        action_button.config(text="Error")

# Function to download playlist
def download_playlist(url):
    folder = choose_download_folder()
    try:
        p = Playlist(url)
        for video_url in p.video_urls:
            yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
            video = yt.streams.filter(only_audio=True).first()
            output = video.download(output_path=folder)

            # Convert to MP3
            base, ext = os.path.splitext(os.path.basename(output))
            new_file_path = os.path.join(folder, base + '.mp3')
            clip = AudioFileClip(output)
            clip.write_audiofile(new_file_path)
            os.remove(output)

        action_button.config(text="Playlist Download Complete")
    except Exception as e:
        print(e)
        action_button.config(text="Error")

# Add a single action button
action_button = Button(root, text='Download', command=download)
action_button.pack(pady=20)

root.mainloop()
