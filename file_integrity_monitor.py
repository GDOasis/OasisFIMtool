# file_integrity_monitor.py
import os
import hashlib
import json
import time

def get_file_hash(file_path):
    # Calculate the SHA-256 hash of a file
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def monitor_directory(directory, log_file):
    # Create or load the previous hash log
    previous_hashes = {}
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            previous_hashes = json.load(log)

    # Monitor files in the specified directory
    while True:
        current_hashes = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                current_hashes[file_path] = get_file_hash(file_path)

        # Compare current and previous hashes
        changed_files = set(current_hashes.keys()) - set(previous_hashes.keys())
        for file_path in changed_files:
            print(f"File changed: {file_path}")

        # Update the previous hash log
        with open(log_file, 'w') as log:
            json.dump(current_hashes, log, indent=2)

        # Sleep for a specified interval (e.g., 60 seconds)
        time.sleep(60)

if __name__ == "__main__":
    # Replace 'example_directory' with the directory to monitor
    # Replace 'hash_log.json' with the desired log file name
    monitor_directory('example_directory', 'hash_log.json')
