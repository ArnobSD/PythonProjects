import psutil
import speedtest
import GPUtil
import time
import os

# Function to check internet speed
def check_internet_speed():
    print("Checking internet speed...")
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    results = st.results.dict()
    download_speed = results['download'] / 1_000_000  # Convert to Mbps
    upload_speed = results['upload'] / 1_000_000  # Convert to Mbps
    ping = results['ping']
    
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms")

# Function to check CPU speed
def check_cpu_speed():
    print("Checking CPU speed...")
    cpu_freq = psutil.cpu_freq()
    print(f"Current CPU Frequency: {cpu_freq.current:.2f} MHz")
    print(f"Max CPU Frequency: {cpu_freq.max:.2f} MHz")
    print(f"Min CPU Frequency: {cpu_freq.min:.2f} MHz")
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")

# Function to check RAM speed and usage
def check_ram_speed():
    print("Checking RAM speed and usage...")
    virtual_memory = psutil.virtual_memory()
    print(f"Total RAM: {virtual_memory.total / 1_073_741_824:.2f} GB")
    print(f"Available RAM: {virtual_memory.available / 1_073_741_824:.2f} GB")
    print(f"Used RAM: {virtual_memory.used / 1_073_741_824:.2f} GB")
    print(f"RAM Usage: {virtual_memory.percent}%")

# Function to check GPU stats
def check_gpu_speed():
    print("Checking GPU stats...")
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"GPU: {gpu.name}")
        print(f"Load: {gpu.load * 100}%")
        print(f"Memory Used: {gpu.memoryUsed} MB")
        print(f"Memory Total: {gpu.memoryTotal} MB")
        print(f"Temperature: {gpu.temperature} °C")

# Function to test SSD/HDD read/write speed
def test_disk_speed(disk_path='/'):
    print("Testing disk read/write speed...")
    file_size = 100_000_000  # 100 MB for test
    filename = os.path.join(disk_path, "test_file.bin")
    
    # Write speed test
    start_time = time.time()
    with open(filename, 'wb') as f:
        f.write(os.urandom(file_size))  # Write 100 MB of random bytes
    write_time = time.time() - start_time
    write_speed = file_size / (write_time * 1_000_000)  # Convert to MB/s
    print(f"Write Speed: {write_speed:.2f} MB/s")
    
    # Read speed test
    start_time = time.time()
    with open(filename, 'rb') as f:
        f.read()  # Read the file back
    read_time = time.time() - start_time
    read_speed = file_size / (read_time * 1_000_000)  # Convert to MB/s
    print(f"Read Speed: {read_speed:.2f} MB/s")
    
    os.remove(filename)  # Clean up test file

# Main function to run all checks
def main():
    print("PC Performance and Speed Test")
    print("============================\n")
    
    # Check internet speed
    check_internet_speed()
    print("\n")

    # Check CPU speed
    check_cpu_speed()
    print("\n")

    # Check RAM speed
    check_ram_speed()
    print("\n")

    # Check GPU speed
    check_gpu_speed()
    print("\n")

    # Test disk speed (both SSD and HDD, specify the path)
    print("Testing SSD (or primary drive) speed...")
    test_disk_speed('/')  # Assuming root (/) for primary disk
    print("\n")

    # If you have an HDD mounted separately, specify the path to test HDD
    hdd_path = input("Enter path for HDD speed test (leave blank to skip): ")
    if hdd_path:
        print(f"Testing HDD speed at {hdd_path}...")
        test_disk_speed(hdd_path)

if __name__ == "__main__":
    main()
