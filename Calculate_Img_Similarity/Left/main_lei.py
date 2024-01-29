from PIL import Image
import os
import numpy as np
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def dhash(image, hash_size=8):
    # Resize the input image, adding a single column (width) so we can compute the gradient.
    resized = image.resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    # Convert the image to grayscale.
    grayscale = resized.convert("L")
    # Compute the (relative) horizontal gradient between adjacent column pixels.
    pixels = np.array(grayscale.getdata()).reshape((hash_size, hash_size + 1))
    diff = pixels[:, 1:] > pixels[:, :-1]
    # Convert the binary array to a hexadecimal string.
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hamming_distance(hash1, hash2):
    return bin(hash1 ^ hash2).count("1")

def are_images_similar(img1, img2, threshold=0.95):
    hash1 = dhash(img1)
    hash2 = dhash(img2)
    max_diff = 64 # 64 bits for D-Hash of size 8x8
    similarity = 1 - hamming_distance(hash1, hash2) / max_diff
    return similarity > threshold

source_directory = r'C:\Users\ASUS\Desktop\111\input'
destination_directory = r'C:\Users\ASUS\Desktop\111\output'

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)
    logging.info(f"Created destination directory: {destination_directory}")

processed_hashes = set()
for filename in os.listdir(source_directory):
    if filename.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
        image_path = os.path.join(source_directory, filename)
        try:
            with Image.open(image_path) as img:
                image_hash = dhash(img)
                # Check if the image is similar to any already processed image
                if not any(are_images_similar(img, Image.open(os.path.join(source_directory, f))) for f in processed_hashes):
                    # If not, copy it to the destination directory
                    processed_hashes.add(filename)
                    img.save(os.path.join(destination_directory, filename))
                    logging.info(f"Copied {filename} to destination directory.")
        except IOError:
            logging.warning(f"Failed to process image: {filename}")

logging.info("Similarity check complete. Images have been copied.")
