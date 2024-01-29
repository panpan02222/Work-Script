import os  
import shutil  
import logging  
from PIL import Image  
import imagehash  
import time  
  
# 设置日志  
logging.basicConfig(filename='image_processing.log', level=logging.INFO)  
  
def calculate_hash(file_path):  
    image = Image.open(file_path)  
    hash = imagehash.dhash(image)  
    return hash  
  
def hamming_distance(hash1, hash2):  
    return hash1 - hash2  
  
def process_images(src_folder, dst_folder_res, dst_folder,  threshold=85, batch_size=1000): 
    dhash_dict = {}  
    counter = 0  
    batch_counter = 0  
    processed_files = set()  # 用于存储已经处理过的文件路径  
    try :
        for root, dirs, files in os.walk(src_folder):  
            for file in files:  
                if file.endswith(('.png', '.jpg', '.jpeg')):  
                    file_path = os.path.join(root, file)  
                    batch_counter += 1  
                    if batch_counter == batch_size:  # 达到批次大小，进行一次完整的处理  
                        for path1 in dhash_dict.keys():  
                            for path2 in dhash_dict.keys():  
                                if path1 != path2 and 1 - hamming_distance(dhash_dict[path1], dhash_dict[path2]) / (len(str(dhash_dict[path1])) * 4) < threshold / 100:  
                                    logging.info(f"文件名称为{path1}与文件名称为{path2}相似度小于{threshold}%")
                                    if file.split('_')[-1].split('.')[0] == 'res':  
                                        shutil.copy2(path2, dst_folder_res)  # 注意这里复制的是path2，因为我们希望保留每个相似对中唯一的文件（即dhash值较小的那个）  
                                        logging.info(f"已将{path2}复制到{dst_folder_res}")  
                                    else:
                                        shutil.copy2(path2, dst_folder)  # 注意这里复制的是path2，因为我们希望保留每个相似对中唯一的文件（即dhash值较小的那个）  
                                        logging.info(f"已将{path2}复制到{dst_folder}")  
                        dhash_dict = {}  # 重置字典，为下一个批次做准备  
                        batch_counter = 0  # 重置批次计数器  
                        processed_files.clear()  # 重置已处理文件集合  
                    dhash = calculate_hash(file_path)  
                    dhash_dict[file_path] = dhash  
                    logging.info(f"计算了{file_path}的dhash值")  
                    processed_files.add(file_path)  # 将当前文件路径添加到已处理集合中  
                    counter += 1  
        # 处理最后一批次的文件，如果总数不是批次大小，也需要处理剩余的文件  
        for path1 in dhash_dict.keys():  
            for path2 in dhash_dict.keys():  
                if path1 != path2 and path2 not in processed_files and 1 - hamming_distance(dhash_dict[path1], dhash_dict[path2]) / (len(str(dhash_dict[path1])) * 4) < threshold / 100:  
                    logging.info(f"文件名称为{path1}与文件名称为{path2}相似度小于{threshold}%")  
                    if file.split('_')[-1].split('.')[0] == 'res':  
                        shutil.copy2(path2, dst_folder_res)  # 注意这里复制的是path2，因为我们希望保留每个相似对中唯一的文件（即dhash值较小的那个）  
                        logging.info(f"已将{path2}复制到{dst_folder_res}")  
                    else:
                        shutil.copy2(path2, dst_folder)  # 注意这里复制的是path2，因为我们希望保留每个相似对中唯一的文件（即dhash值较小的那个）  
                        logging.info(f"已将{path2}复制到{dst_folder}")    
    except Exception as error:
        print(error)
    



t0 = time.time()
src_directory = r'C:\Users\ASUS\Desktop\111\input'
dst_folder_res = r'C:\Users\ASUS\Desktop\111\output_res'
dst_folder = r'C:\Users\ASUS\Desktop\111\output'
process_images(src_directory, dst_folder_res, dst_folder, threshold=90, batch_size=1000)  # 注意这里增加了batch_size参数，设置为1000，与您的需求一致。
t1 = time.time()
print('运行完毕\n')
print(f'共耗时: {((t1-t0)/60)/60} hours')
