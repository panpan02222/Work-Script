import os
#
#
# def copy_files_to_directory(source_dir, destination_dir):
#     """
#     复制指定路径下的所有文件到另一个指定文件夹下。
#
#     参数:
#         source_dir (str): 源文件夹路径。
#         destination_dir (str): 目标文件夹路径。
#     """
#     # 确保目标文件夹存在，如果不存在则创建
#     if not os.path.exists(destination_dir):
#         os.makedirs(destination_dir)
#
#         # 遍历源文件夹中的文件
#     for filename in os.listdir(source_dir):
#         # 构建源文件路径和目标文件路径
#         source_file = os.path.join(source_dir, filename)
#         destination_file = os.path.join(destination_dir, filename)
#
#         # 复制文件到目标文件夹
#         if os.path.isfile(source_file):
#             os.copy2(source_file, destination_file)
#             print(f"已将文件 {filename} 复制到 {destination_dir}")
#
#         # 示例用法：将目录 /path/to/source 下的所有文件复制到 /path/to/destination 目录下



import shutil


def copy_files_to_directory(source_dir, destination_dir):
    """
    复制指定路径下的所有文件到另一个指定文件夹下。

    参数:
        source_dir (str): 源文件夹路径。
        destination_dir (str): 目标文件夹路径。
    """
    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

        # 遍历源文件夹中的文件
    for filename in os.listdir(source_dir):
        # 构建源文件路径和目标文件路径
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)

        # 复制文件到目标文件夹并保持元数据
        if os.path.isfile(source_file):
            shutil.copy2(source_file, destination_file)
            print(f"已将文件 {filename} 复制到 {destination_dir}")
src = r'E:\下图工具3\保定2024年1月'
dst = r'H:\智洋输电通道\下载工具3\保定2024年1月'
copy_files_to_directory(src,dst)