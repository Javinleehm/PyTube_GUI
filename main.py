import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pytube import YouTube, Playlist
import re
import json
from threading import Thread
import atexit

with open("config.json", "r") as f:
    config = json.load(f)


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


video_thread = Thread(target=download_video_thread)
audio_thread = Thread(target=download_audio_thread)
def kill_threads():
    if video_thread.is_alive():
        video_thread.join()
    if audio_thread.is_alive():
        audio_thread.join()

atexit.register(kill_threads)


def on_download():
    reset_progress()
    url = url_entry.get("1.0",'end-1c')
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
        else:
            playlist = Playlist(url)
            for video in playlist.videos:
                try:
                    download_audio(video.watch_url, output_path)
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
                    
                else:
                    try:
                        download_audio(video, output_path)
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
            else:
                try:
                    download_audio(url, output_path)
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
    if progress >= 100:
        messagebox.showinfo("Download Complete", "Downloaded successfully!")
    progress_bar["value"] = progress
    window.update_idletasks()                
    


def select_path():
    path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)


def update_radio_buttons():
    if format_var.get() == 1:
        mp4_radio.deselect()
    elif format_var.get() == 2:
        mp3_radio.deselect()

    if is_playlist.get() == 1:
        single_radio.deselect()
    elif is_playlist.get() == 0:
        playlist_radio.deselect()


# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")

# Set the window size
window_width = int(window.winfo_screenwidth() / 2)  # Window width is a quarter of the screen width
window_height = int(window.winfo_screenheight() / 2)  # Window height is a quarter of the screen height
window.geometry(f"{window_width}x{window_height}")

# URL Entry
url_label = tk.Label(window, text="URL:")
url_label.pack()
url_entry = tk.Text(window, height = 5, width=80)
url_entry.pack()

# Playlist or Single Song Selection
is_playlist = tk.IntVar(value=0)  # Initialize with value 0
playlist_radio = tk.Radiobutton(window, text="Playlist", variable=is_playlist, value=1, command=update_radio_buttons)
playlist_radio.pack()
single_radio = tk.Radiobutton(window, text="Single Song (Use , to split between multiple links)", variable=is_playlist, value=0, command=update_radio_buttons)
single_radio.pack()

# Format Selection
format_var = tk.IntVar(value=1)
mp3_radio = tk.Radiobutton(window, text="MP3", variable=format_var, value=1, command=update_radio_buttons)
mp3_radio.pack()
mp4_radio = tk.Radiobutton(window, text="MP4", variable=format_var, value=2, command=update_radio_buttons)
mp4_radio.pack()

# Output Path Entry
path_label = tk.Label(window, text="Output Path:")
path_label.pack()
path_entry = tk.Entry(window, width=50)
path_entry.insert(0, config["path"]) 
path_entry.pack()
path_button = tk.Button(window, text="Select Directory", command=select_path)
path_button.pack()

# Download Button
download_button = tk.Button(window, text="Download", command=on_download)
download_button.pack()

progress_bar = Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack()

disclaimer_label = tk.Label(window, text="Created by Javin :D\n\n\n\n\nDisclaimer: \nThis YouTube downloader is provided for educational purposes only. \nThe usage of this tool is at your own risk. \nI do not endorse or promote any unauthorized downloading or distribution of copyrighted content. \nPlease ensure that you comply with the applicable laws and the terms of service of YouTube and other content platforms when using this downloader. \nI am not responsible for any misuse or illegal activity performed with this tool. \nUse it responsibly and respect the rights of content creators.")
disclaimer_label.pack()



# Start the GUI
window.mainloop()