import os
import shutil
import argparse

# 支持的RAW文件扩展名
RAW_EXTENSIONS = ['.cr2', '.nef', '.arw', '.dng', '.raf', '.raw', '.rw2', '.orf', '.pef', '.srw']
# JPEG文件扩展名
JPEG_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.JPEG']

def separate_raw_jpeg(source_dir):
    """
    将指定目录下的RAW和JPEG文件分别移动到RAW和jpeg文件夹
    """
    # 确保源目录存在
    if not os.path.exists(source_dir):
        print(f"错误：目录 {source_dir} 不存在")
        return
    
    # 创建目标文件夹
    raw_dir = os.path.join(source_dir, 'RAW')
    jpeg_dir = os.path.join(source_dir, 'JPEG')
    
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
        print(f"创建目录：{raw_dir}")
    
    if not os.path.exists(jpeg_dir):
        os.makedirs(jpeg_dir)
        print(f"创建目录：{jpeg_dir}")
    
    # 遍历源目录
    raw_count = 0
    jpeg_count = 0
    
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        
        # 跳过目录
        if os.path.isdir(file_path):
            continue
        
        # 获取文件扩展名
        ext = os.path.splitext(file_name)[1].lower()
        
        # 处理RAW文件
        if ext in RAW_EXTENSIONS:
            dest_path = os.path.join(raw_dir, file_name)
            shutil.move(file_path, dest_path)
            # print(f"移动RAW文件：{file_name} -> {raw_dir}")
            raw_count += 1
        
        # 处理JPEG文件
        elif ext in JPEG_EXTENSIONS:
            dest_path = os.path.join(jpeg_dir, file_name)
            shutil.move(file_path, dest_path)
            # print(f"移动JPEG文件：{file_name} -> {jpeg_dir}")
            jpeg_count += 1
    
    print(f"\n处理完成：")
    print(f"移动了 {raw_count} 个RAW文件到 {raw_dir}")
    print(f"移动了 {jpeg_count} 个JPEG文件到 {jpeg_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将RAW和JPEG文件分别移动到对应文件夹")
    parser.add_argument("source_dir", nargs="?", default=".", help="源目录路径（默认为当前目录）")
    args = parser.parse_args()
    
    separate_raw_jpeg(args.source_dir)
