import os
import pydicom
import numpy as np
from PIL import Image



def is_folder_path_valid(path):
    return os.path.isdir(path)

def is_directory_empty(directory_path):
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return False  # Not a valid directory path
    return len(os.listdir(directory_path)) == 0


def Conversion(input_directory, output_directory):

    if not is_folder_path_valid(input_directory):
        return 0,0,0
    
    if not is_directory_empty(output_directory):
        return 0,0,0
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    subfolder_counter = 0

    num_total_images = 0
    num_valid_images = 0
    num_invalid_images = 0
    examinated_parts = {}

    for root, dirs, files in os.walk(input_directory):
        # Get the relative path from the input directory to the current directory
        relative_path = os.path.relpath(root, input_directory)

        # Create the corresponding subfolder in the output directory
        output_subfolder = os.path.join(output_directory, f"Patient_{subfolder_counter}")
        os.makedirs(output_subfolder, exist_ok=True)

        # Iterate through the files in the current directory
        for file_name in files:
            file_path = os.path.join(root, file_name)

            try:
                # Read the DICOM file with force=True
                dcm = pydicom.dcmread(file_path, force=True)

                # Check if the attribute (0x0018, 0x0015) exists
                if (0x0018, 0x0015) in dcm:
                    examinated_part = dcm[(0x0018, 0x0015)].value
                    if examinated_part not in examinated_parts:
                        examinated_parts[examinated_part] = 1
                    else:
                        examinated_parts[examinated_part] += 1
                else:
                    print(f"Missing attribute (0x0018, 0x0015) in DICOM file: {file_path}")

                # Modify DICOM attributes
                if hasattr(dcm, "PixelData"):
                    image_data = dcm.pixel_array

                    # Conversion des valeurs de l'image en niveaux de gris
                    image_data = image_data - np.min(image_data)
                    image_data = image_data / np.max(image_data)
                    image_data = (image_data * 255).astype(np.uint8)

                    if np.all(image_data == 0):
                        print(f"Skipping entirely black image: {file_path}")
                        num_invalid_images += 1
                        continue

                    if image_data is None or len(image_data.shape) != 2:
                        print(f"Skipping invalid image: {file_path}")
                        num_invalid_images += 1
                        continue

                    # Convert to grayscale if image has three dimensions
                    if image_data.ndim == 3:
                        image_data = np.squeeze(image_data[:, :, 0])

                    # Create a PIL Image from the array and save as PNG
                    output_file_path_im = os.path.join(output_subfolder, file_name + ".png")
                    image = Image.fromarray(image_data)
                    image.save(output_file_path_im)

                    num_valid_images += 1
                else:
                    print(f"Missing pixel data attribute in DICOM file: {file_path}")
                    num_invalid_images += 1

            except pydicom.errors.InvalidDicomError:
                print(f"Invalid DICOM file: {file_path}")
                num_invalid_images += 1
                

            num_total_images += 1

        subfolder_counter += 1

    # Calculate statistics for total images, valid images, and invalid images
    print("Statistics:")
    print(f"Number of total images: {num_total_images}")
    print(f"Number of valid images: {num_valid_images}")
    print(f"Number of invalid images: {num_invalid_images}")

    return num_total_images,num_valid_images,num_invalid_images