import os
import shutil
import argparse

# Supported RAW file extensions
RAW_EXTENSIONS = ['.cr2', '.nef', '.arw', '.dng', '.raf', '.raw', '.rw2', '.orf', '.pef', '.srw']
# JPEG file extensions
JPEG_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.JPEG']

def separate_raw_jpeg(source_dir):
    """
    Separate RAW and JPEG files into corresponding folders
    """
    # Ensure source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Directory {source_dir} does not exist")
        return
    
    # Create target folders
    raw_dir = os.path.join(source_dir, 'RAW')
    jpeg_dir = os.path.join(source_dir, 'JPEG')
    
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
        print(f"Created directory: {raw_dir}")
    
    if not os.path.exists(jpeg_dir):
        os.makedirs(jpeg_dir)
        print(f"Created directory: {jpeg_dir}")
    
    # Traverse source directory and all subdirectories
    raw_count = 0
    jpeg_count = 0
    
    for dirpath, dirnames, filenames in os.walk(source_dir):
        # Skip target folders to avoid duplicate processing
        dirnames[:] = [d for d in dirnames if d not in ['RAW', 'JPEG', 'jpeg', 'rm_raw']]
        
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)
            
            # Get file extension
            ext = os.path.splitext(file_name)[1].lower()
            
            # Process RAW files
            if ext in RAW_EXTENSIONS:
                dest_path = os.path.join(raw_dir, file_name)
                # Ensure target file does not exist to avoid overwriting
                if os.path.exists(dest_path):
                    # Generate unique filename
                    base_name, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(os.path.join(raw_dir, f"{base_name}_{counter}{ext}")):
                        counter += 1
                    dest_path = os.path.join(raw_dir, f"{base_name}_{counter}{ext}")
                shutil.move(file_path, dest_path)
                # print(f"Moved RAW file: {file_path} -> {dest_path}")
                raw_count += 1
            
            # Process JPEG files
            elif ext in JPEG_EXTENSIONS:
                dest_path = os.path.join(jpeg_dir, file_name)
                # Ensure target file does not exist to avoid overwriting
                if os.path.exists(dest_path):
                    # Generate unique filename
                    base_name, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(os.path.join(jpeg_dir, f"{base_name}_{counter}{ext}")):
                        counter += 1
                    dest_path = os.path.join(jpeg_dir, f"{base_name}_{counter}{ext}")
                shutil.move(file_path, dest_path)
                # print(f"Moved JPEG file: {file_path} -> {dest_path}")
                jpeg_count += 1
    
    print(f"\nProcessing completed:")
    print(f"Moved {raw_count} RAW files to {raw_dir}")
    print(f"Moved {jpeg_count} JPEG files to {jpeg_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Separate RAW and JPEG files into corresponding folders")
    parser.add_argument("source_dir", nargs="?", default=".", help="Source directory path (default: current directory)")
    args = parser.parse_args()
    
    separate_raw_jpeg(args.source_dir)
