import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pytube import YouTube, Playlist
import re
import json
from threading import Thread
import atexit
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from moviepy.editor import VideoFileClip, AudioFileClip

with open("config.json", "r") as f:
    config = json.load(f)

DisableNormalFinishMsg = True
    
def download_highest_resolution(url,output_path):
    global hires_video_thread
    hires_video_thread = Thread(target=download_highest_resolution_thread, args=(url,output_path,))
    hires_video_thread.start()
    

# Function to download the highest quality video from YouTube
def download_highres_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(adaptive=True).filter(mime_type='video/webm').first()
    yt.register_on_progress_callback(update_progress)
    stream.download(filename='video.webm')

# Function to download the highest quality audio from YouTube
def download_highres_audio(url):
    yt = YouTube(url)
    stream = yt.streams.get_audio_only()
    yt.register_on_progress_callback(update_progress)
    stream.download(filename='audio.mp4')

# Function to merge the downloaded video and audio
def merge_video_audio(video_file, audio_file, output_file):
    video = VideoFileClip(video_file)
    
    audio = AudioFileClip(audio_file)
    
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_file)

# Example usage
def download_highest_resolution_thread(video_url, output_path):
    

    download_highres_video(video_url)
    download_highres_audio(video_url)

    video_file = "video.webm"  # Make sure the filename matches the one used in download_highres_video()
    audio_file = "audio.mp4"  # Make sure the filename matches the one used in download_highres_audio()
    output_file = os.path.join(output_path,"merged_video.mp4")

    merge_video_audio(video_file, audio_file, output_file)
    os.remove("audio.mp4")
    os.remove("video.webm")
    messagebox.showinfo("Download Complete", "Downloaded successfully!")






def download_video(url,output_path):
    global video_thread
    video_thread = Thread(target=download_video_thread, args=(url,output_path,))
    video_thread.start()
    
    

    
def download_audio(url,output_path):
    global audio_thread
    audio_thread = Thread(target=download_audio_thread, args=(url,output_path,))
    audio_thread.start()
    


def download_video_thread(url, output_path):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        yt.register_on_progress_callback(update_progress)
        video_stream.download(output_path)
        return True
        
            
    except Exception as e:
        messagebox.showerror("Error", str(e))
        print(e)
        return False


def download_audio_thread(url, output_path):
    try:
        yt = YouTube(url)        
        audio_stream = yt.streams.filter(only_audio=True).first()
        yt.register_on_progress_callback(update_progress)
        audio_file = audio_stream.download(output_path)
        audio_file_path = os.path.splitext(audio_file)[0] + ".mp3"
        os.rename(audio_file, audio_file_path)
        return True
            
    except Exception as e:
        messagebox.showerror("Error", str(e))
        print(e)
        return False

hires_video_thread = Thread(target=download_highest_resolution_thread)
video_thread = Thread(target=download_video_thread)
audio_thread = Thread(target=download_audio_thread)
def kill_threads():
    if video_thread.is_alive():
        video_thread.join()
    if audio_thread.is_alive():
        audio_thread.join()
    if hires_video_thread.is_alive():
        hires_video_thread.join()

atexit.register(kill_threads)


def on_download():
    global DisableNormalFinishMsg
    DisableNormalFinishMsg = format_var.get()== 3 # or is_playlist.get() == 1
        
    reset_progress()
    url = url_entry.get()
    output_path = path_entry.get()
    if not(os.path.isdir(output_path)):
        messagebox.showwarning("Error","Such directory does not exist.")
        return False
    config["path"] = output_path
    if is_playlist.get() == 1:
        if format_var.get() == 2:
            playlist = Playlist(url)
            for video in playlist.videos:
                try:
                    download_video(video.watch_url, output_path)
                except Exception as e:
                    print(e)
                    messagebox.showwarning("Error","Error while downloading")
                    return False
                
            # messagebox.showinfo("Download Complete", "Video downloaded successfully!")
        elif format_var.get() == 1:
            playlist = Playlist(url)
            for video in playlist.videos:
                try:
                    download_audio(video.watch_url, output_path)
                except Exception as e:
                    print(e)
                    messagebox.showwarning("Error","Error while downloading")
                    return False
            # messagebox.showinfo("Download Complete", "Video downloaded successfully!")
        elif format_var.get() == 3:
            playlist = Playlist(url)
            for video in playlist.videos:
                try:
                    download_highest_resolution(video.watch_url, output_path)
                except Exception as e:
                    print(e)
                    messagebox.showwarning("Error","Error while downloading")
                    return False
        
            # messagebox.showinfo("Download Complete", "Audio downloaded successfully!")
        
    else:
        if "," in url:
            vidlist = re.split(r",\s",url)
            for video in vidlist:
                if format_var.get() == 2:
                    try:
                        download_video(video, output_path)
                    except Exception as e:
                        print(e)
                        messagebox.showwarning("Error","Error while downloading")
                        return False
                    
                elif format_var.get() == 1:
                    try:
                        download_audio(video, output_path)
                    except Exception as e:
                        print(e)
                        messagebox.showwarning("Error","Error while downloading")
                        return False
                elif format_var.get() == 3:
                    try:
                        download_highest_resolution(video, output_path)
                    except Exception as e:
                        print(e)
                        messagebox.showwarning("Error","Error while downloading")
                        return False
                
                
                
                # if format_var.get() == 2:
                #     messagebox.showinfo("Download Complete", "Video downloaded successfully!")
                # else:
                #     messagebox.showinfo("Download Complete", "Audio downloaded successfully!")
        else:
            if format_var.get() == 2:
                try:
                    download_video(url, output_path)
                except Exception as e:
                    print(e)
                    return False
                # messagebox.showinfo("Download Complete", "Video downloaded successfully!")
            elif format_var.get() ==1:
                try:
                    download_audio(url, output_path)
                except Exception as e:
                    print(e)
                    return False
            elif format_var.get() == 3:
                try:
                    download_highest_resolution(url, output_path)
                except Exception as e:
                    print(e)
                    return False
                # messagebox.showinfo("Download Complete", "Audio downloaded successfully!")
    with open("config.json", "r+") as f:
        json.dump(config,f)

def reset_progress():
    progress_bar["value"] = 0
    window.update_idletasks()

def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = int((bytes_downloaded / total_size) * 100)
    if progress >= 100 and not(DisableNormalFinishMsg):
        messagebox.showinfo("Download Complete", "Downloaded successfully!")
    progress_bar["value"] = progress
    window.update_idletasks()                
    


def select_path():
    path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)


def update_radio_buttons():
    if format_var.get() == 1:
        mp4_radio.set(None)
    elif format_var.get() == 2:
        mp3_radio.set(None)

    if is_playlist.get() == 1:
        single_radio.set(None)
    elif is_playlist.get() == 0:
        playlist_radio.set(None)


# Create the main window
window = ThemedTk(theme="arc")
window.title("YouTube Downloader")
# ttk.Style().theme_use('clam')

# Set the window size
window_width = int(window.winfo_screenwidth() / 2)  # Window width is a quarter of the screen width
window_height = int(window.winfo_screenheight() / 2)  # Window height is a quarter of the screen height
window.geometry(f"{window_width}x{window_height}")

# URL Entry
url_label = ttk.Label(window, text="URL:")
url_label.pack()
url_entry = ttk.Entry(window, textvariable=10, width=80)
url_entry.pack(ipady=10)

# Playlist or Single Song Selection

is_playlist_radio_frame = ttk.Frame(window)
is_playlist_radio_frame.pack()
is_playlist = tk.IntVar(value=0)  # Initialize with value 0
playlist_radio = ttk.Radiobutton(is_playlist_radio_frame, text="Playlist", variable=is_playlist, value=1)
playlist_radio.grid(row=0, column=0)
single_radio = ttk.Radiobutton(is_playlist_radio_frame, text="Single Song (Use , to split between multiple links)", variable=is_playlist, value=0)
single_radio.grid(row=0, column=1)

# Format Selection


format_radio_frame = ttk.Frame(window)
format_radio_frame.pack()
format_var = tk.IntVar(value=1)
mp3_radio = ttk.Radiobutton(format_radio_frame, text="MP3", variable=format_var, value=1)
mp3_radio.grid(row=0, column=0)
mp4_radio = ttk.Radiobutton(format_radio_frame, text="MP4(Maximum 720p)", variable=format_var, value=2)
mp4_radio.grid(row=0, column=1)
mp4_highres_radio = ttk.Radiobutton(format_radio_frame, text="Highest Resolution MP4 (Requires local processing)", variable=format_var, value=3)
mp4_highres_radio.grid(row=0, column=2)

# Output Path Entry
path_label = ttk.Label(window, text="Output Path:")
path_label.pack()
path_entry = ttk.Entry(window, width=50)
path_entry.insert(0, config["path"]) 
path_entry.pack()
path_button = ttk.Button(window, text="Select Directory", command=select_path)
path_button.pack()

# Download Button
download_button = ttk.Button(window, text="Download", command=on_download)
download_button.pack()

progress_bar = Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack()

disclaimer_label = ttk.Label(window, text="Created by Javin :D\n\n\n\n\nDisclaimer: \nThis YouTube downloader is provided for educational purposes only. \nThe usage of this tool is at your own risk. \nI do not endorse or promote any unauthorized downloading or distribution of copyrighted content. \nPlease ensure that you comply with the applicable laws and the terms of service of YouTube and other content platforms when using this downloader. \nI am not responsible for any misuse or illegal activity performed with this tool. \nUse it responsibly and respect the rights of content creators.")
disclaimer_label.pack()



# Start the GUI
window.mainloop()