import os
import csv
import hashlib
import argparse
from collections import defaultdict

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.JPEG', '.cr2', '.nef', '.arw', '.dng', '.raf', '.raw', '.rw2', '.orf', '.pef', '.srw']

def get_file_info(file_path, use_hash=True):
    """
    获取文件信息，包括文件名、大小、修改时间和哈希值
    """
    try:
        stat = os.stat(file_path)
        file_size = stat.st_size
        mod_time = stat.st_mtime
        file_name = os.path.basename(file_path)
        file_hash = "N/A"
        
        # 计算文件的哈希值，用于更准确地判断重复文件
        if use_hash:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as f:
                # 只读取文件的前100KB和后100KB，加速哈希计算
                # 对于小文件，读取整个文件
                if file_size <= 204800:  # 200KB
                    md5_hash.update(f.read())
                else:
                    # 读取前100KB
                    md5_hash.update(f.read(102400))
                    # 跳转到文件末尾前100KB
                    f.seek(max(0, file_size - 102400))
                    # 读取后100KB
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
        print(f"获取文件信息时出错：{file_path} - {e}")
        return None

def detect_duplicates(directory, use_hash=True):
    """
    检测目录下的重复文件
    """
    # 存储文件信息，根据是否使用哈希值选择不同的键
    if use_hash:
        # 使用文件名、大小和哈希值作为键
        file_dict = defaultdict(list)
    else:
        # 只使用文件名、大小和修改时间作为键
        file_dict = defaultdict(list)
    
    # 递归扫描目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                file_info = get_file_info(file_path, use_hash)
                if file_info:
                    if use_hash:
                        # 使用文件名、大小和哈希值作为键
                        key = (file_info['file_name'], file_info['file_size'], file_info['file_hash'])
                    else:
                        # 只使用文件名、大小和修改时间作为键
                        key = (file_info['file_name'], file_info['file_size'], file_info['mod_time'])
                    file_dict[key].append(file_info)
    
    # 找出重复的文件
    duplicates = []
    for key, files in file_dict.items():
        if len(files) > 1:
            duplicates.append(files)
    
    return duplicates

def write_to_csv(duplicates, csv_file):
    """
    将重复文件信息写入CSV文件
    """
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['文件名', '文件大小(字节)', '修改时间', '文件哈希', '文件路径'])
        
        # 写入重复文件信息
        for duplicate_group in duplicates:
            for file_info in duplicate_group:
                writer.writerow([
                    file_info['file_name'],
                    file_info['file_size'],
                    file_info['mod_time'],
                    file_info['file_hash'],
                    file_info['file_path']
                ])
            # 在每组重复文件之间添加空行
            writer.writerow([])

def print_duplicates(duplicates, use_hash=True):
    """
    在终端中打印重复文件信息
    """
    if not duplicates:
        print("未发现重复文件")
        return
    
    print(f"发现 {len(duplicates)} 组重复文件：\n")
    
    for i, duplicate_group in enumerate(duplicates, 1):
        print(f"第 {i} 组重复文件：")
        print(f"文件名: {duplicate_group[0]['file_name']}")
        print(f"文件大小: {duplicate_group[0]['file_size']} 字节")
        if use_hash:
            print(f"文件哈希: {duplicate_group[0]['file_hash']}")
        print("文件路径:")
        for file_info in duplicate_group:
            print(f"  - {file_info['file_path']}")
        print()

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="检测目录下的重复jpg或raw文件")
    parser.add_argument("directory", help="要扫描的目录路径")
    parser.add_argument("--output", default="duplicates.csv", help="输出CSV文件路径（默认为duplicates.csv）")
    parser.add_argument("--no-hash", action="store_true", help="不使用哈希值进行文件对比，加速扫描")
    args = parser.parse_args()
    
    directory = args.directory
    csv_file = args.output
    use_hash = not args.no_hash
    
    if not os.path.exists(directory):
        print(f"错误：目录 {directory} 不存在")
        return
    
    print(f"正在扫描目录：{directory}")
    if use_hash:
        print("使用哈希值进行文件对比，这可能需要一些时间，请耐心等待...")
    else:
        print("不使用哈希值进行文件对比，仅使用文件名、大小和修改时间，扫描速度会更快...")
    
    # 检测重复文件
    duplicates = detect_duplicates(directory, use_hash)
    
    # 输出结果
    print_duplicates(duplicates, use_hash)
    write_to_csv(duplicates, csv_file)
    
    print(f"重复文件信息已保存到：{csv_file}")

if __name__ == "__main__":
    main()
