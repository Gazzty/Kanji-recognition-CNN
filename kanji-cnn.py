import os
import struct
import numpy as np
from PIL import Image

def read_etl1c_record(f):
    header = f.read(5)
    if len(header) < 5:
        return None
    jis_code, quality = struct.unpack('>2H1x', header)
    image_data = f.read(4032)
    if len(image_data) < 4032:
        print("Registro incompleto, tamaño inesperado.")
        return None
    bitmap = np.frombuffer(image_data, dtype=np.uint8).reshape((63, 64))
    return jis_code, quality, bitmap

def extract_images_from_etl_file(file_path, output_folder, max_images=10):
    images = []
    with open(file_path, 'rb') as f:
        i = 0
        while i < max_images:
            record = read_etl1c_record(f)
            if record is None:
                break
            jis_code, quality, bitmap = record
            kanji_images = []
            for row in range(2):
                for col in range(2):
                    kanji = bitmap[row*32:(row+1)*32, col*32:(col+1)*32]
                    kanji_images.append(kanji)
                    kanji_image = Image.fromarray(kanji)
                    kanji_image.save(os.path.join(output_folder, f"{jis_code}_{i}_kanji_{row*2+col}.png"))
                    print(f"Guardado {jis_code}_{i}_kanji_{row*2+col}.png")
            i += 1
            images.extend(kanji_images)
    return images

def process_dataset(dataset_folder, output_folder, max_images=10):
    for subfolder in os.listdir(dataset_folder):
        subfolder_path = os.path.join(dataset_folder, subfolder)
        if os.path.isdir(subfolder_path):
            for file_name in os.listdir(subfolder_path):
                if file_name.endswith('.bin') or file_name.startswith(subfolder + 'C'):
                    file_path = os.path.join(subfolder_path, file_name)
                    print(f"Procesando {file_path}...")
                    output_subfolder = os.path.join(output_folder, subfolder)
                    os.makedirs(output_subfolder, exist_ok=True)
                    extract_images_from_etl_file(file_path, output_subfolder, max_images)

# Ruta de la carpeta del dataset y de salida
dataset_folder = './datasets'
output_folder = './kanji_images'
os.makedirs(output_folder, exist_ok=True)

# Procesar todo el dataset, tomando solo 10 imágenes por archivo
process_dataset(dataset_folder, output_folder, max_images=10)
