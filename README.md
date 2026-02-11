# 照片批量处理工具

本项目提供了两个Python脚本，用于批量处理相机拍摄的照片，主要功能是将RAW和JPEG文件分开，并根据用户选择的JPEG文件清理对应的RAW文件。

## 功能介绍

### 1. 分离RAW和JPEG文件 (`separate_raw_jpeg.py`)
- 遍历指定目录下的所有文件
- 识别RAW格式和JPEG格式的文件
- 在指定目录下创建`RAW`和`jpeg`文件夹
- 将对应的文件移动到相应的文件夹中

### 2. 清理未选中的RAW文件 (`cleanup_raw.py`)
- 扫描`RAW`和`jpeg`文件夹
- 根据`jpeg`文件夹中的文件，识别未被选中的RAW文件
- 创建`rm_raw`文件夹（如果不存在）
- 将未被选中的RAW文件移动到`rm_raw`文件夹中

## 支持的文件格式

### RAW格式
- `.cr2` (Canon)
- `.nef` (Nikon)
- `.arw` (Sony)
- `.dng` (Adobe Digital Negative)
- `.raf` (Fujifilm)
- `.raw` (通用)
- `.rw2` (Panasonic)
- `.orf` (Olympus)
- `.pef` (Pentax)
- `.srw` (Samsung)

### JPEG格式
- `.jpg`
- `.jpeg`
- `.JPG`
- `.JPEG`

## 使用方法

### 前提条件
- 安装Python 3.x
- 将脚本复制到照片所在的目录

### 步骤1：分离RAW和JPEG文件

```bash
# 在当前目录运行
python separate_raw_jpeg.py

# 或指定目录运行
python separate_raw_jpeg.py /path/to/photos
```

### 步骤2：选择JPEG文件

在`jpeg`文件夹中删除不需要的照片，只保留您想要的照片。

### 步骤3：清理未选中的RAW文件

```bash
# 在当前目录运行
python cleanup_raw.py

# 或指定目录运行
python cleanup_raw.py /path/to/photos
```

### 步骤4：确认并删除

检查`rm_raw`文件夹中的文件，确认都是不需要的RAW文件后，可以删除该文件夹。

## 示例

假设您有以下照片文件：
- `DSC0001.jpg`
- `DSC0001.arw`
- `DSC0002.jpg`
- `DSC0002.arw`
- `DSC0003.jpg`
- `DSC0003.arw`

1. 运行`separate_raw_jpeg.py`后，文件会被分离到：
   - `jpeg/DSC0001.jpg`
   - `jpeg/DSC0002.jpg`
   - `jpeg/DSC0003.jpg`
   - `RAW/DSC0001.arw`
   - `RAW/DSC0002.arw`
   - `RAW/DSC0003.arw`

2. 如果您只想要`DSC0001.jpg`和`DSC0002.jpg`，可以删除`jpeg/DSC0003.jpg`。

3. 运行`cleanup_raw.py`后，`RAW/DSC0003.arw`会被移动到`rm_raw/DSC0003.arw`。

## 注意事项

1. 脚本会直接移动文件，请确保在运行前备份重要文件。
2. 脚本根据文件名的基础部分（不含扩展名）来匹配RAW和JPEG文件，请确保同一张照片的RAW和JPEG文件具有相同的基础文件名。
3. 脚本支持Windows、Linux和macOS系统。

## 故障排除

如果遇到问题，请检查以下几点：

1. 确保Python已正确安装并添加到系统路径中。
2. 确保指定的目录存在并且有读写权限。
3. 确保RAW和JPEG文件的文件名匹配（除了扩展名）。

## 许可证

本项目采用MIT许可证，详见LICENSE文件。
