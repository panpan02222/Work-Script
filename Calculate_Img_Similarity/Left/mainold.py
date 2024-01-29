# import os
# import shutil
# from PIL import Image
#
# def resize_image(image, size=(9, 8)):
#     return image.resize(size).convert('L')
#
# def dhash(image):
#     pixels = list(image.getdata())
#     difference = []
#     for row in range(8):
#         for col in range(8):
#             pixel_left = image.getpixel((col, row))
#             pixel_right = image.getpixel((col + 1, row))
#             difference.append(pixel_left > pixel_right)
#     decimal_value = 0
#     hex_string = []
#     for index, value in enumerate(difference):
#         if value:
#             decimal_value += 2**(index % 8)
#         if (index % 8) == 7:
#             hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
#             decimal_value = 0
#     return ''.join(hex_string)
#
# def calculate_hash(file_path):
#     image = Image.open(file_path)
#     resized_image = resize_image(image)
#     return dhash(resized_image)
#
# def copy_images(src_directory, dest_directory):
#     device_code_mapping = {}
#
#     for filename in os.listdir(src_directory):
#         file_path = os.path.join(src_directory, filename)
#
#         if os.path.isfile(file_path):
#             # 提取设备编码
#             device_code = filename.split('_')[0]
#
#             # 计算哈希值
#             file_hash = calculate_hash(file_path)
#
#             # 如果设备编码不在映射表中，则添加
#             if device_code not in device_code_mapping:
#                 device_code_mapping[device_code] = set()
#
#             # 如果哈希值不在设备编码对应的图片集合中，则复制图片
#             if file_hash not in device_code_mapping[device_code]:
#                 device_code_mapping[device_code].add(file_hash)
#
#                 # 创建设备编码的目录
#                 device_directory = os.path.join(dest_directory, device_code)
#                 os.makedirs(device_directory, exist_ok=True)
#
#                 # 复制图片到设备编码的目录
#                 dest_path = os.path.join(device_directory, filename)
#                 shutil.copy2(file_path, dest_path)
#
# # 示例用法
# src_directory = r"C:\Users\wo\Pictures\input"
# dest_directory = r"C:\Users\wo\Pictures\output"
# copy_images(src_directory, dest_directory)







from PIL import Image
import os
import shutil
import imagehash

def calculate_hash(file_path):
    image = Image.open(file_path)
    hash = imagehash.dhash(image)
    return hash

def copy_images(src_directory, dest_directory, threshold=0.9):
    device_code_mapping = {}

    for filename in os.listdir(src_directory):
        file_path = os.path.join(src_directory, filename)

        if os.path.isfile(file_path):
            # 提取设备编码
            device_code = filename.split('_')[0]

            # 计算哈希值
            file_hash = calculate_hash(file_path)

            # 如果设备编码不在映射表中，则添加
            if device_code not in device_code_mapping:
                device_code_mapping[device_code] = [(file_hash, filename)]
            else:
                # 对比哈希值，如果相似度小于90%，则复制图片
                for existing_hash, _ in device_code_mapping[device_code]:
                    similarity = 1 - (existing_hash - file_hash) / len(existing_hash.hash)**2
                    if similarity < threshold:
                        device_code_mapping[device_code].append((file_hash, filename))

                        # 创建设备编码的目录
                        device_directory = os.path.join(dest_directory, device_code)
                        os.makedirs(device_directory, exist_ok=True)

                        # 复制图片到设备编码的目录
                        dest_path = os.path.join(device_directory, filename)
                        shutil.copy2(file_path, dest_path)
                        break

src_directory = r"C:\Users\wo\Pictures\input"
dest_directory = r"C:\Users\wo\Pictures\output"
copy_images(src_directory, dest_directory)