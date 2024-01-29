# import os
# import shutil
# import logging
#
# def move_large_jpg_files(source_directory, destination_directory, log_file):
#     logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
#
#     with open(log_file, 'a+') as f:
#         f.seek(0)
#         lines = f.read().splitlines()
#         last_line = lines[-1] if lines else None
#
#     started = False if last_line else True
#
#     for foldername, subfolders, filenames in os.walk(source_directory):
#         for filename in filenames:
#             file_path = os.path.join(foldername, filename)
#             if not started:
#                 if file_path == last_line:
#                     started = True
#                 continue
#             if filename.endswith('.jpg'):
#                 file_size = os.path.getsize(file_path)
#                 if file_size > 1024 * 1024:  # file size in bytes
#                     shutil.move(file_path, os.path.join(destination_directory, filename))
#                     logging.info(f'Moved file {file_path} to {destination_directory}')
#                 else:
#                     logging.info(f'Skipped file {file_path} due to size less than 1MB')
#
# source_directory = r'C:\Users\wo\Desktop\src'
# destination_directory = r'C:\Users\wo\Desktop\dst'
# log_file = r'C:\Users\wo\Desktop\log.txt'
# move_large_jpg_files(source_directory, destination_directory, log_file)


import os
import shutil
import logging

def move_large_jpg_files(source_directory, destination_directory, log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    with open(log_file, 'a+') as f:
        f.seek(0)
        lines = f.read().splitlines()
        last_line = lines[-1] if lines else None

    started = False if last_line else True

    for foldername, subfolders, filenames in os.walk(source_directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            if not started:
                if file_path == last_line:
                    started = True
                continue
            if filename.endswith('.jpg'):
                file_size = os.path.getsize(file_path)
                if file_size > 1024 * 1024:  # file size in bytes
                    try:
                        shutil.move(file_path, os.path.join(destination_directory, filename))
                        print('move file ' + filename)
                        logging.info(f'Moved file {file_path} to {destination_directory}')
                    except Exception as e:
                        logging.error(f'Failed to move file {file_path} due to error: {e}')
                else:
                    logging.info(f'Skipped file {file_path} due to size less than 1MB')

source_directory = r'K:\配电无人机\01\01'
destination_directory = r'K:\输电无人机_2'
log_file = r'C:\Users\ASUS\Desktop\log1.txt'
move_large_jpg_files(source_directory, destination_directory, log_file)
