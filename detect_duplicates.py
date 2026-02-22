import os
import csv
import hashlib
import argparse
from collections import defaultdict

# Supported file extensions
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.JPEG', '.cr2', '.nef', '.arw', '.dng', '.raf', '.raw', '.rw2', '.orf', '.pef', '.srw']

def get_file_info(file_path, use_hash=True):
    """
    Get file information, including file name, size, modification time, and hash value
    """
    try:
        stat = os.stat(file_path)
        file_size = stat.st_size
        mod_time = stat.st_mtime
        file_name = os.path.basename(file_path)
        file_hash = "N/A"
        
        # Calculate file hash value for more accurate duplicate detection
        if use_hash:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as f:
                # Only read the first 100KB and last 100KB of the file to speed up hash calculation
                # For small files, read the entire file
                if file_size <= 204800:  # 200KB
                    md5_hash.update(f.read())
                else:
                    # Read first 100KB
                    md5_hash.update(f.read(102400))
                    # Jump to 100KB before the end of the file
                    f.seek(max(0, file_size - 102400))
                    # Read last 100KB
                    md5_hash.update(f.read())
            file_hash = md5_hash.hexdigest()
        
        return {
            'file_name': file_name,
            'file_size': file_size,
            'mod_time': mod_time,
            'file_hash': file_hash,
            'file_path': file_path
        }
    except Exception as e:
        print(f"Error getting file information: {file_path} - {e}")
        return None

def detect_duplicates(directory, use_hash=True):
    """
    Detect duplicate files in the directory
    """
    # Store file information, use different keys based on whether hash is used
    if use_hash:
        # Use file name, size, and hash as keys
        file_dict = defaultdict(list)
    else:
        # Only use file name, size, and modification time as keys
        file_dict = defaultdict(list)
    
    # Recursively scan directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check file extension
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                file_info = get_file_info(file_path, use_hash)
                if file_info:
                    if use_hash:
                        # Use file name, size, and hash as keys
                        key = (file_info['file_name'], file_info['file_size'], file_info['file_hash'])
                    else:
                        # Only use file name, size, and modification time as keys
                        key = (file_info['file_name'], file_info['file_size'], file_info['mod_time'])
                    file_dict[key].append(file_info)
    
    # Find duplicate files
    duplicates = []
    for key, files in file_dict.items():
        if len(files) > 1:
            duplicates.append(files)
    
    return duplicates

def write_to_csv(duplicates, csv_file):
    """
    Write duplicate file information to CSV file
    """
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['File Name', 'File Size (bytes)', 'Modification Time', 'File Hash', 'File Path'])
        
        # Write duplicate file information
        for duplicate_group in duplicates:
            for file_info in duplicate_group:
                writer.writerow([
                    file_info['file_name'],
                    file_info['file_size'],
                    file_info['mod_time'],
                    file_info['file_hash'],
                    file_info['file_path']
                ])
            # Add empty line between duplicate groups
            writer.writerow([])

def print_duplicates(duplicates, use_hash=True):
    """
    Print duplicate file information in terminal
    """
    if not duplicates:
        print("No duplicate files found")
        return
    
    print(f"Found {len(duplicates)} groups of duplicate files:\n")
    
    for i, duplicate_group in enumerate(duplicates, 1):
        print(f"Group {i}:")
        print(f"File Name: {duplicate_group[0]['file_name']}")
        print(f"File Size: {duplicate_group[0]['file_size']} bytes")
        if use_hash:
            print(f"File Hash: {duplicate_group[0]['file_hash']}")
        print("File Paths:")
        for file_info in duplicate_group:
            print(f"  - {file_info['file_path']}")
        print()

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description="Detect duplicate jpg or raw files in directory")
    parser.add_argument("directory", help="Directory path to scan")
    parser.add_argument("--output", default="duplicates.csv", help="Output CSV file path (default: duplicates.csv)")
    parser.add_argument("--no-hash", action="store_true", help="Do not use hash for file comparison, speed up scanning")
    args = parser.parse_args()
    
    directory = args.directory
    csv_file = args.output
    use_hash = not args.no_hash
    
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist")
        return
    
    print(f"Scanning directory: {directory}")
    if use_hash:
        print("Using hash for file comparison, this may take some time, please be patient...")
    else:
        print("Not using hash for file comparison, only using file name, size and modification time, scanning will be faster...")
    
    # Detect duplicate files
    duplicates = detect_duplicates(directory, use_hash)
    
    # Output results
    print_duplicates(duplicates, use_hash)
    write_to_csv(duplicates, csv_file)
    
    print(f"Duplicate file information saved to: {csv_file}")

if __name__ == "__main__":
    main()
