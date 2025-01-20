import os
import requests
from threading import Thread
from tqdm import tqdm

# Function to download a specific part of the file
def download_part(url, start, end, part_num, output_dir, pbar, chunk_size=1024 * 16):  # 16 KB chunks
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True, timeout=10)

    part_filename = os.path.join(output_dir, f"part_{part_num}")
    with open(part_filename, "wb") as part_file:
        # Stream and write content in chunks to monitor progress
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:  # Filter out keep-alive chunks
                part_file.write(chunk)
                pbar.update(len(chunk))  # Update the progress bar

# Function to combine all parts into a single file
def combine_parts(output_dir, output_filename, total_parts):
    with open(output_filename, "wb") as output_file:
        for part_num in range(total_parts):
            part_filename = os.path.join(output_dir, f"part_{part_num}")
            with open(part_filename, "rb") as part_file:
                output_file.write(part_file.read())
            os.remove(part_filename)  # Remove part after combining

# Main function to download the file using multiple threads
def download_file_multithreaded(url, output_filename, num_threads=16):  # Increase to 16 threads
    response = requests.head(url)
    file_size = int(response.headers.get("content-length", 0))

    # Create directory to store the parts
    output_dir = "downloaded_parts"
    os.makedirs(output_dir, exist_ok=True)

    # Calculate the size of each part
    part_size = file_size // num_threads
    parts = []

    # Setup tqdm progress bar
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=output_filename) as pbar:
        # Start downloading parts
        for part_num in range(num_threads):
            start = part_num * part_size
            # Ensure the last part downloads the remaining bytes
            end = file_size - 1 if part_num == num_threads - 1 else (start + part_size - 1)
            part_thread = Thread(target=download_part, args=(url, start, end, part_num, output_dir, pbar))
            parts.append(part_thread)
            part_thread.start()

        # Wait for all threads to finish
        for part in parts:
            part.join()

    # Combine parts into a single file
    combine_parts(output_dir, output_filename, num_threads)

    print(f"Download completed: {output_filename}")

# User input for the download URL
url = input("Enter the download link: ")
output_filename = input("Enter the output filename (with extension): ")

# Download file using multiple threads
download_file_multithreaded(url, output_filename, num_threads=16)  # Using 16 threads for faster download
