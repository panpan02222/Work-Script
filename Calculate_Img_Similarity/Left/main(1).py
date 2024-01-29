from PIL import Image
import os
import numpy as np
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def dhash(image, hash_size=8):
    resized = image.resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    grayscale = resized.convert("L")
    pixels = np.array(grayscale.getdata()).reshape((hash_size, hash_size + 1))
    diff = pixels[:, 1:] > pixels[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hamming_distance(hash1, hash2):
    return bin(hash1 ^ hash2).count("1")

def are_images_similar(hash1, hash2, threshold=0.95):
    max_diff = 64
    similarity = 1 - hamming_distance(hash1, hash2) / max_diff
    return similarity > threshold

source_directory = r'E:\pic'
destination_directory = r'E:\已清洗_正样本'

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)
    logging.info(f"Created destination directory: {destination_directory}")

def process_batch(filenames):
    image_hashes = {}
    to_remove = set()

    for filename in filenames:
        image_path = os.path.join(source_directory, filename)
        try:
            with Image.open(image_path) as img:
                image_hash = dhash(img)
                image_hashes[filename] = image_hash
        except IOError:
            logging.warning(f"Failed to process image: {filename}")

    for filename, image_hash in image_hashes.items():
        if filename in to_remove:
            continue
        for other_filename, other_hash in image_hashes.items():
            if filename != other_filename and are_images_similar(image_hash, other_hash):
                to_remove.add(other_filename)

    for filename in filenames:
        if filename not in to_remove:
            img_path = os.path.join(source_directory, filename)
            with Image.open(img_path) as img:
                img.save(os.path.join(destination_directory, filename))
                logging.info(f"Copied {filename} to destination directory.")

def get_image_files(directory, batch_size=1000):
    count = 0
    batch = []
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
            batch.append(entry.name)
            count += 1
            if count % batch_size == 0:
                yield batch
                batch = []
    if batch:
        yield batch

for batch in get_image_files(source_directory, batch_size=1000):
    process_batch(batch)
    logging.info(f"Processed a batch of {len(batch)} images.")

logging.info("All batches processed. Similarity check complete.")
