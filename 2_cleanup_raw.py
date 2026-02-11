import os
import shutil
import argparse

# 支持的RAW文件扩展名
RAW_EXTENSIONS = ['.cr2', '.nef', '.arw', '.dng', '.raf', '.raw', '.rw2', '.orf', '.pef', '.srw']
# JPEG文件扩展名
JPEG_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.JPEG']

def get_base_name(file_name):
    """
    获取文件名的基础部分（不含扩展名）
    """
    return os.path.splitext(file_name)[0]

def cleanup_raw(source_dir, action='move'):
    """
    根据jpeg文件夹中的文件，清理RAW文件夹中对应的文件
    将未被选中的RAW文件移动到rm_raw文件夹或直接删除
    
    参数：
    source_dir: 源目录路径
    action: 操作类型，'move' 或 'delete'，默认为 'move'
    """
    # 确保源目录存在
    if not os.path.exists(source_dir):
        print(f"错误：目录 {source_dir} 不存在")
        return
    
    # 定义目录路径
    raw_dir = os.path.join(source_dir, 'RAW')
    jpeg_dir = os.path.join(source_dir, 'jpeg')
    rm_raw_dir = os.path.join(source_dir, 'rm_raw')
    
    # 确保必要的目录存在
    if not os.path.exists(raw_dir):
        print(f"错误：RAW目录 {raw_dir} 不存在")
        return
    
    if not os.path.exists(jpeg_dir):
        print(f"错误：jpeg目录 {jpeg_dir} 不存在")
        return
    
    if action == 'move' and not os.path.exists(rm_raw_dir):
        os.makedirs(rm_raw_dir)
        print(f"创建目录：{rm_raw_dir}")
    
    # 获取jpeg文件的基础名称集合
    jpeg_basenames = set()
    for file_name in os.listdir(jpeg_dir):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in JPEG_EXTENSIONS:
            jpeg_basenames.add(get_base_name(file_name))
    
    print(f"找到 {len(jpeg_basenames)} 个JPEG文件")
    
    # 遍历RAW文件
    processed_count = 0
    for file_name in os.listdir(raw_dir):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in RAW_EXTENSIONS:
            base_name = get_base_name(file_name)
            # 检查对应的JPEG文件是否存在
            if base_name not in jpeg_basenames:
                src_path = os.path.join(raw_dir, file_name)
                if action == 'move':
                    # 移动到rm_raw文件夹
                    dest_path = os.path.join(rm_raw_dir, file_name)
                    shutil.move(src_path, dest_path)
                    # print(f"移动未选中的RAW文件：{file_name} -> {rm_raw_dir}")
                elif action == 'delete':
                    # 直接删除文件
                    os.remove(src_path)
                    # print(f"删除未选中的RAW文件：{file_name}")
                processed_count += 1
    
    print(f"\n处理完成：")
    if action == 'move':
        print(f"移动了 {processed_count} 个未选中的RAW文件到 {rm_raw_dir}")
    elif action == 'delete':
        print(f"删除了 {processed_count} 个未选中的RAW文件")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据JPEG文件清理未选中的RAW文件")
    parser.add_argument("source_dir", nargs="?", default=".", help="源目录路径（默认为当前目录）")
    args = parser.parse_args()
    
    # 配置操作类型：'move' 或 'delete'
    # 只在程序中设置，不需要外部用户输入
    # action = 'move'  # 默认为移动到rm_raw文件夹
    action = 'delete'  # 直接删除未选中的RAW文件
    
    cleanup_raw(args.source_dir, action)
