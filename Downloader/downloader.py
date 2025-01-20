import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import requests
from concurrent.futures import ThreadPoolExecutor
import os
from threading import Thread
import time
import speedtest  # Import speedtest-cli

# Functions remain the same as your original code

def download_audio():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Audio downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    try:
        ydl_opts = {
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def download_part(url, start, end, part_num, output_dir, chunk_size=1024 * 16):
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True, timeout=10)
    part_filename = os.path.join(output_dir, f"part_{part_num}")
    with open(part_filename, "wb") as part_file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                part_file.write(chunk)
                update_progress(len(chunk))

def combine_parts(output_dir, output_filename, total_parts):
    with open(output_filename, "wb") as output_file:
        for part_num in range(total_parts):
            part_filename = os.path.join(output_dir, f"part_{part_num}")
            with open(part_filename, "rb") as part_file:
                output_file.write(part_file.read())
            os.remove(part_filename)

def download_file_multithreaded(url, output_filename, num_threads=16):
    response = requests.head(url)
    file_size = int(response.headers.get("content-length", 0))
    output_dir = "downloaded_parts"
    os.makedirs(output_dir, exist_ok=True)
    part_size = file_size // num_threads

    progress_label.config(text="Downloading...")
    progress_bar['maximum'] = file_size
    progress_bar['value'] = 0
    start_time = time.time()

    def run_download():
        try:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for part_num in range(num_threads):
                    start = part_num * part_size
                    end = file_size - 1 if part_num == num_threads - 1 else (start + part_size - 1)
                    futures.append(executor.submit(download_part, url, start, end, part_num, output_dir))

                for future in futures:
                    future.result()

            combine_parts(output_dir, output_filename, num_threads)
            messagebox.showinfo("Success", f"Download completed: {output_filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            progress_label.config(text="")

    def update_speed():
        while progress_bar['value'] < file_size:
            elapsed_time = time.time() - start_time
            speed = progress_bar['value'] / elapsed_time
            speed_label.config(text=f"Speed: {speed / (1024 * 1024):.2f} MB/s")
            time.sleep(1)

    Thread(target=run_download).start()  # This was missing the run_download logic
    Thread(target=update_speed).start()

def update_progress(value):
    progress_bar['value'] += value
    root.update_idletasks()

def start_file_download():
    url = file_url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return
    dest = url.split('/')[-1]
    Thread(target=download_file_multithreaded, args=(url, dest)).start()

def check_internet_speed():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    download_speed = st.results.download / (1024 * 1024)
    upload_speed = st.results.upload / (1024 * 1024)
    messagebox.showinfo("Internet Speed", f"Download: {download_speed:.2f} Mbps\nUpload: {upload_speed:.2f} Mbps")

# GUI setup with enhanced design
root = tk.Tk()
root.title("YouTube and File Downloader")
root.geometry("500x400")  # Set a bigger window size
root.config(bg="#f2f2f2")  # Set a light gray background for a modern look

# Title Label
title_label = tk.Label(root, text="YouTube & File Downloader", font=("Helvetica", 18, "bold"), bg="#f2f2f2", fg="#333")
title_label.pack(pady=20)

# YouTube URL Input
url_frame = tk.Frame(root, bg="#f2f2f2")
url_frame.pack(pady=10)
tk.Label(url_frame, text="YouTube URL:", font=("Helvetica", 12), bg="#f2f2f2").pack(side=tk.LEFT)
url_entry = tk.Entry(url_frame, width=40, font=("Helvetica", 12))
url_entry.pack(side=tk.LEFT, padx=10)

# Audio and Video Buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=10)
audio_button = tk.Button(button_frame, text="Download Audio", command=download_audio, bg="#4CAF50", fg="white", font=("Helvetica", 12), width=15)
audio_button.pack(side=tk.LEFT, padx=10)
video_button = tk.Button(button_frame, text="Download Video", command=download_video, bg="#2196F3", fg="white", font=("Helvetica", 12), width=15)
video_button.pack(side=tk.LEFT, padx=10)

# File Download URL Input
file_frame = tk.Frame(root, bg="#f2f2f2")
file_frame.pack(pady=20)
tk.Label(file_frame, text="File Download URL:", font=("Helvetica", 12), bg="#f2f2f2").pack(side=tk.LEFT)
file_url_entry = tk.Entry(file_frame, width=40, font=("Helvetica", 12))
file_url_entry.pack(side=tk.LEFT, padx=10)

# File Download Button
file_download_button = tk.Button(root, text="Download File", command=start_file_download, bg="#FF5722", fg="white", font=("Helvetica", 12), width=20)
file_download_button.pack(pady=10)

# Progress Bar and Labels
progress_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f2f2f2")
progress_label.pack()
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=400)
progress_bar.pack(pady=5)

# Speed Label
speed_label = tk.Label(root, text="Speed: 0 MB/s", font=("Helvetica", 12), bg="#f2f2f2", fg="#555")
speed_label.pack(pady=5)

# Speed Test Button
speed_test_button = tk.Button(root, text="Check Speed", command=check_internet_speed, bg="#FF9800", fg="white", font=("Helvetica", 12), width=20)
speed_test_button.pack(pady=10)

root.mainloop()
