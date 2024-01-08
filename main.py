import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube, Playlist
import re


def download_video(url, output_path):
    try:
        yt = YouTube(url)
        yt.streams.filter(progressive=True).get_highest_resolution().download(output_path)
        
            
    except Exception as e:
        messagebox.showerror("Error", str(e))


def download_audio(url, output_path):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(output_path)
        audio_file_path = os.path.splitext(audio_file)[0] + ".mp3"
        os.rename(audio_file, audio_file_path)
        
            
    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_download():
    url = url_entry.get("1.0",'end-1c')
    output_path = path_entry.get()

    if is_playlist.get() == 1:
        if format_var.get() == 2:
            playlist = Playlist(url)
            for video in playlist.videos:
                download_video(video.watch_url, output_path)
            messagebox.showinfo("Download Complete", "Video downloaded successfully!")
        else:
            playlist = Playlist(url)
            for video in playlist.videos:
                download_audio(video.watch_url, output_path)
            messagebox.showinfo("Download Complete", "Audio downloaded successfully!")
        
    else:
        if "," in url:
            vidlist = re.split(r",\s",url)
            for video in vidlist:
                if format_var.get() == 2:
                    download_video(video, output_path)
                    
                else:
                    download_audio(video, output_path)
                    
                if format_var.get() == 2:
                    messagebox.showinfo("Download Complete", "Video downloaded successfully!")
                else:
                    messagebox.showinfo("Download Complete", "Audio downloaded successfully!")
        else:
            if format_var.get() == 2:
                download_video(url, output_path)
                messagebox.showinfo("Download Complete", "Video downloaded successfully!")
            else:
                download_audio(url, output_path)
                messagebox.showinfo("Download Complete", "Audio downloaded successfully!")
                


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
path_entry.pack()
path_button = tk.Button(window, text="Select Path", command=select_path)
path_button.pack()

# Download Button
download_button = tk.Button(window, text="Download", command=on_download)
download_button.pack()

disclaimer_label = tk.Label(window, text="Created by Javin :D\n\n\n\n\nDisclaimer: \nThis YouTube downloader is provided for educational purposes only. \nThe usage of this tool is at your own risk. \nI do not endorse or promote any unauthorized downloading or distribution of copyrighted content. \nPlease ensure that you comply with the applicable laws and the terms of service of YouTube and other content platforms when using this downloader. \nI am not responsible for any misuse or illegal activity performed with this tool. \nUse it responsibly and respect the rights of content creators.")
disclaimer_label.pack()



# Start the GUI
window.mainloop()