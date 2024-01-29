import os 
import shutil

def copy_files(src_folders,dst_folder,duplicate_folder):
    for i ,src_folder in enumerate(src_folders):
        print(f'copying files from folder {i+1} of 25')
        for root,dirs,files in os.walk(src_folder):
            print(src_folder)
            for file in files:
                if file.endswith('.rar'):
                    continue
                src_path = os.path.join(root,file)
                base_name,ext = os.path.splitext(file)
                duplicate_path = os.path.join(duplicate_folder,file)
                if os.path.exists(duplicate_path):
                    print(f'skipping {file} as it already exists in the duplicate folder!!!')
                    continue
                dst_path = os.path.join(dst_folder,file)
                shutil.copy(src_path,dst_path)
                print(f'copy {file} from {src_path} to {dst_path}')
            if not files and not dirs:
                print('{os.path.basename(root)} not has file')

src_folders = [
    # r"H:\潘秉宏\重新标注样本\7-3-ok-2398",
    # r"H:\潘秉宏\重新标注样本\7-4_ok_2492",
    # r'H:\潘秉宏\重新标注样本\7-5-ok-1793',
    r'H:\潘秉宏\重新标注样本\7-6-ok-3623',
    r'H:\潘秉宏\重新标注样本\7-7-ok-2632',
    r'H:\潘秉宏\重新标注样本\7-10-ok-1551',
    r'H:\潘秉宏\重新标注样本\7-11-ok-866',
    r'H:\潘秉宏\重新标注样本\7-12-ok-743',
    r'H:\潘秉宏\重新标注样本\7-13-ok-1148',
    r'H:\潘秉宏\重新标注样本\7-14-ok-1198',
    r'H:\潘秉宏\重新标注样本\7-17-ok-837',
    r'H:\潘秉宏\重新标注样本\7-18-ok-2242',
    r'H:\潘秉宏\重新标注样本\7-19-ok-722',
    r'H:\潘秉宏\重新标注样本\7-20-0k-1414',
    r'H:\潘秉宏\重新标注样本\7-21-ok-709',
    r'H:\潘秉宏\重新标注样本\7-24-ok-562',
    r'H:\潘秉宏\重新标注样本\7-25-ok-555',
    r'H:\潘秉宏\重新标注样本\7-26-ok-123',
    r'H:\潘秉宏\重新标注样本\7-27-ok-166',
    r'H:\潘秉宏\重新标注样本\7-28-ok-238',
    r'H:\潘秉宏\重新标注样本\7-31-ok-1515',
    r'H:\潘秉宏\重新标注样本\8-1-ok-256',
    r'H:\潘秉宏\重新标注样本\8-2-ok-352',
    r'H:\潘秉宏\重新标注样本\8-3-ok-271',
    r'H:\潘秉宏\重新标注样本\8-4-ok-95'
]  
dst_folders = r"H:\潘秉宏\重新标注样本\待上传样本库样本_12-18_(7-3至7-20)"
duplicate_folder = r'H:\潘秉宏\重新标注样本\duplicate'
copy_files(src_folders,dst_folders,duplicate_folder)