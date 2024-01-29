import os


def delete_jpg_files(folder_path, num_files):
    """删除指定文件夹下指定数量的后缀为.jpg的文件"""
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    if len(jpg_files) <= num_files:
        print("文件夹下没有足够数量的.jpg文件")
        return

    for i in range(num_files):
        os.remove(os.path.join(folder_path, jpg_files[i]))
        print(f"已删除文件: {jpg_files[i]}")

    print(f"已删除 {num_files} 个.jpg文件")


# 示例：删除指定文件夹下3个.jpg文件
folder_path = r'G:\pic'
delete_jpg_files(folder_path, 870000)