import struct
import numpy as np
import matplotlib.pyplot as plt

def read_etl1_single_file(file_path):
    """Lee un solo archivo de datos ETL1 y maneja errores de lectura."""
    data = []
    failed_samples = 0  # Contador de muestras que no se pueden leer correctamente

    with open(file_path, 'rb') as f:
        # Leer el encabezado para obtener el número de muestras
        header = f.read(8)
        num_samples = struct.unpack('>I', header[4:8])[0]  # Número de muestras
        print(f"Reading {file_path}: {num_samples} samples")

        # Leer las muestras una por una
        for _ in range(num_samples):
            sample = f.read(5464)  # Leer 5464 bytes (tamaño de cada muestra)
            
            if len(sample) != 5464:
                raise ValueError(f"Expected 5464 bytes, but got {len(sample)} bytes for a sample.")
            
            # Intentar convertir en un array de 72x76
            try:
                image_data = np.frombuffer(sample, dtype=np.uint8).reshape((72, 76))
                # Recortar a 64x63 (centrar la imagen)
                image_data = image_data[4:68, 6:69]  # Recorte para obtener 64x63
                data.append(image_data)
            except ValueError:
                # Si ocurre un error de reshape, contar y continuar con el siguiente
                failed_samples += 1
                print(f"Error reshaping sample, skipping this one. Total failed: {failed_samples}")

    print(f"Total failed samples: {failed_samples}")
    return np.array(data)

def plot_sample_image(data, index):
    """Muestra una imagen de ejemplo del dataset."""
    plt.imshow(data[index], cmap='gray')
    plt.title(f"Sample {index}")
    plt.show()

# Ruta al archivo ETL1C_01
etl1_file_path = './datasets/ETL1/ETL1C_01'  # Ruta al archivo específico

# Leer los datos del archivo
data = read_etl1_single_file(etl1_file_path)

# Mostrar una imagen de ejemplo
plot_sample_image(data, 0)

# Asegurarse de que los datos estén en formato correcto
print(f"Data shape: {data.shape}")
