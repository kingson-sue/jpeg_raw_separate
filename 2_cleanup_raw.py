import os
import shutil
import argparse

# Supported RAW file extensions
RAW_EXTENSIONS = ['.cr2', '.nef', '.arw', '.dng', '.raf', '.raw', '.rw2', '.orf', '.pef', '.srw']
# Supported JPEG file extensions
JPEG_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.JPEG']

def get_base_name(file_name):
    """
    Get the base name of the file (without extension)
    """
    return os.path.splitext(file_name)[0]

def cleanup_raw(source_dir, action='move'):
    """
    Clean up RAW files based on JPEG files
    Move unselected RAW files to rm_raw folder or delete them directly
    
    Parameters:
    source_dir: Source directory path
    action: Action type, 'move' or 'delete', default is 'move'
    """
    # Ensure source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Directory {source_dir} does not exist")
        return
    
    # Define directory paths
    raw_dir = os.path.join(source_dir, 'RAW')
    jpeg_dir = os.path.join(source_dir, 'jpeg')
    rm_raw_dir = os.path.join(source_dir, 'rm_raw')
    
    # Ensure necessary directories exist
    if not os.path.exists(raw_dir):
        print(f"Error: RAW directory {raw_dir} does not exist")
        return
    
    if not os.path.exists(jpeg_dir):
        print(f"Error: jpeg directory {jpeg_dir} does not exist")
        return
    
    if action == 'move' and not os.path.exists(rm_raw_dir):
        os.makedirs(rm_raw_dir)
        print(f"Created directory: {rm_raw_dir}")
    
    # Get base names of JPEG files
    jpeg_basenames = set()
    for file_name in os.listdir(jpeg_dir):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in JPEG_EXTENSIONS:
            jpeg_basenames.add(get_base_name(file_name))
    
    print(f"Found {len(jpeg_basenames)} JPEG files")
    
    # Traverse RAW files
    processed_count = 0
    for file_name in os.listdir(raw_dir):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in RAW_EXTENSIONS:
            base_name = get_base_name(file_name)
            # Check if corresponding JPEG file exists
            if base_name not in jpeg_basenames:
                src_path = os.path.join(raw_dir, file_name)
                if action == 'move':
                    # Move to rm_raw folder
                    dest_path = os.path.join(rm_raw_dir, file_name)
                    shutil.move(src_path, dest_path)
                    # print(f"Moved unselected RAW file: {file_name} -> {rm_raw_dir}")
                elif action == 'delete':
                    # Delete file directly
                    os.remove(src_path)
                    # print(f"Deleted unselected RAW file: {file_name}")
                processed_count += 1
    
    print(f"\nProcessing completed:")
    if action == 'move':
        print(f"Moved {processed_count} unselected RAW files to {rm_raw_dir}")
    elif action == 'delete':
        print(f"Deleted {processed_count} unselected RAW files")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up unselected RAW files based on JPEG files")
    parser.add_argument("source_dir", nargs="?", default=".", help="Source directory path (default: current directory)")
    args = parser.parse_args()
    
    # Configure action type: 'move' or 'delete'
    # Set only in the program, no external user input needed
    action = 'move'  # Default: move to rm_raw folder
    # action = 'delete'  # Directly delete unselected RAW files
    
    cleanup_raw(args.source_dir, action)
