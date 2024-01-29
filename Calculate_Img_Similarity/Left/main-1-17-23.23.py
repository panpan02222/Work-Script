

from PIL import Image
import os
import shutil
import imagehash


def hamming_distance(hash1, hash2):
    return hash1 - hash2

def calculate_similarity(device_code_mapping):
    for device_code, files in device_code_mapping.items():
        for i in range(len(files)):
            for j in range(i+1, len(files)):
                file1 = list(files[i].keys())[0]
                file2 = list(files[j].keys())[0]
                similarity = 1 - hamming_distance(file1, file2) / len(file1)
                print(f"文件 {files[i][file1]} 和文件 {files[j][file2]} 的相似度为 {similarity}")


def calculate_hash(file_path):
    image = Image.open(file_path)
    hash = imagehash.dhash(image)
    # print(f'hash: ', hash)
    return hash
def copy_images(src_directory, dest_directory, threshold=0.90):
    device_code_mapping = {}

    for filename in os.listdir(src_directory):
        file_path = os.path.join(src_directory, filename)

        if os.path.isfile(file_path):
            # 提取设备编码
            device_code = filename.split('_')[0]

            # 计算哈希值
            file_hash = calculate_hash(file_path)

            # 如果设备编码已经存在于字典中，我们将文件名添加到该设备编码的列表中
            if device_code in device_code_mapping:
                device_code_mapping[device_code].append({file_hash: filename})
            else:
                # 否则，我们为设备编码创建一个新的列表
                device_code_mapping[device_code] = [{file_hash: filename}]

    for device_code, files in device_code_mapping.items():
        for i in range(len(files)):
            for j in range(i+1, len(files)):
                file1 = list(files[i].keys())[0]
                file2 = list(files[j].keys())[0]
                similarity = 1 - hamming_distance(file1, file2) / len(file1)
                print(f"文件 {files[i][file1]} 和文件 {files[j][file2]} 的相似度为 {similarity}")

                # 如果相似度小于阈值，我们将文件复制到目标文件夹
                if similarity < threshold:
                    dest_path = os.path.join(dest_directory, device_code)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    shutil.copy2(os.path.join(src_directory, files[i][file1]), dest_path)
                    shutil.copy2(os.path.join(src_directory, files[j][file2]), dest_path)

    return device_code_mapping




src_directory = r'C:\Users\ASUS\Desktop\111\input'
dest_directory = r'C:\Users\ASUS\Desktop\111\output'
copy_images(src_directory, dest_directory)