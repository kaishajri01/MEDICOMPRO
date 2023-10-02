import os
import cv2
import numpy as np
from scipy.ndimage import map_coordinates
from scipy.ndimage.filters import gaussian_filter
from skimage import util
import matplotlib.pyplot as plt

def rotate_image(image, angle):
    rows, cols = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    return rotated_image

def flip_image(image, flip_code):
    flipped_image = cv2.flip(image, flip_code)
    return flipped_image

def scale_image(image, scale_factor):
    scaled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    return scaled_image

def shear_image(image, shear_factor):
    rows, cols = image.shape[:2]
    shear_matrix = np.float32([[1, shear_factor, 0], [0, 1, 0]])
    sheared_image = cv2.warpAffine(image, shear_matrix, (cols, rows))
    return sheared_image

def elastic_deformation(image, alpha, sigma):
    random_state = np.random.RandomState(None)
    shape = image.shape

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha

    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    indices = np.reshape(y+dy, (-1, 1)), np.reshape(x+dx, (-1, 1))

    deformed_image = map_coordinates(image, indices, order=1, mode='reflect')
    deformed_image = np.reshape(deformed_image, shape)

    return deformed_image

def add_noise(image, mean, std_dev):
    noisy_image = util.random_noise(image, mode='gaussian', mean=mean, var=std_dev**2)
    noisy_image = np.array(255 * noisy_image, dtype=np.uint8)
    return noisy_image

def adjust_contrast_brightness(image, alpha, beta):
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

def apply_histogram_equalization(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized_image = clahe.apply(image)
    return equalized_image

def apply_affine_transform(image, rotation_angle, scale_factor, translation):
    rows, cols = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, scale_factor)
    affine_matrix = np.vstack([rotation_matrix, [0, 0, 1]])
    affine_matrix = affine_matrix.astype(np.float64)  # Ensure matrix data type is float64
    transformed_image = cv2.warpAffine(image, affine_matrix[:2, :], (cols, rows))
    return transformed_image


def is_folder_path_valid(path):
    return os.path.isdir(path)

def is_directory_empty(directory_path):
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return False  # Not a valid directory path
    return len(os.listdir(directory_path)) == 0

def apply_data_augmentation(root_directory_path,output_path):

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not is_folder_path_valid(root_directory_path):
        return 0,0,0
    
    if not is_directory_empty(output_path):
        return 0,0,0

    total_original_images = 0
    total_black_images = 0
    total_augmented_images = 0

    for patient_directory in os.listdir(root_directory_path):
        patient_directory_path = os.path.join(root_directory_path, patient_directory)

        image_directory = os.path.join(patient_directory_path, "images")
        corresponding_image_directory = os.path.join(patient_directory_path, "masks")

        if not os.path.exists(image_directory) or not os.path.exists(corresponding_image_directory):
            continue

        augmented_image_directory = os.path.join(output_path, patient_directory)
        os.makedirs(augmented_image_directory, exist_ok=True)

        augmented_image_original_directory = os.path.join(augmented_image_directory, "images")
        os.makedirs(augmented_image_original_directory, exist_ok=True)

        augmented_image_corresponding_directory = os.path.join(augmented_image_directory, "masks")
        os.makedirs(augmented_image_corresponding_directory, exist_ok=True)

        original_images_count = 0
        black_images_count = 0
        augmented_images_count = 0

        for image_filename in os.listdir(image_directory):
            image_path = os.path.join(image_directory, image_filename)
            corresponding_image_path = os.path.join(corresponding_image_directory, image_filename)

            # Check if the corresponding image is fully black
            corresponding_image = cv2.imread(corresponding_image_path, cv2.IMREAD_GRAYSCALE)
            if np.all(corresponding_image == 0):
                # Delete both the image and its corresponding image
                #os.remove(image_path)
                #os.remove(corresponding_image_path)
                black_images_count += 1
                #continue

            # Read the image
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            corresponding_image = cv2.imread(corresponding_image_path, cv2.IMREAD_GRAYSCALE)

            # Apply data augmentation functions
            augmented_images = []  # Placeholder for the list of augmented images
            corresponding_augmented_images=[]

            # Data augmentation function 1
            augmented_image1 = rotate_image(image, angle=45)
            augmented_images.append(augmented_image1)

            # Apply the same data augmentation to the corresponding image
            corresponding_augmented_image1 = rotate_image(corresponding_image, angle=45)
            corresponding_augmented_images.append(corresponding_augmented_image1)

            # Data augmentation function 2
            augmented_image2 = flip_image(image, flip_code=1)
            augmented_images.append(augmented_image2)

            # Apply the same data augmentation to the corresponding image
            corresponding_augmented_image2 = flip_image(corresponding_image, flip_code=1)
            corresponding_augmented_images.append(corresponding_augmented_image2)

            # ... Add more data augmentation functions as needed
            scaled_image = scale_image(image, scale_factor=0.8)
            augmented_images.append(scaled_image)

            corresponding_augmented_image3 = scale_image(corresponding_image, scale_factor=0.8)
            corresponding_augmented_images.append(corresponding_augmented_image3)

            # 4. Shear image
            sheared_image = shear_image(image, shear_factor=0.2)
            augmented_images.append(sheared_image)

            corresponding_augmented_image4 = shear_image(corresponding_image,shear_factor=0.2)
            corresponding_augmented_images.append(corresponding_augmented_image4)

            # 5. Elastic deformation
            deformed_image = elastic_deformation(image, alpha=50, sigma=5)
            augmented_images.append(deformed_image)

            corresponding_augmented_image5 = elastic_deformation(corresponding_image, alpha=50, sigma=5)
            corresponding_augmented_images.append(corresponding_augmented_image5)

            # 6. Add noise
            noisy_image = add_noise(image, mean=0, std_dev=0.1)
            augmented_images.append(noisy_image)

            corresponding_augmented_image6 = add_noise(corresponding_image, mean=0, std_dev=0.1)
            corresponding_augmented_images.append(corresponding_augmented_image6)

            # 7. Adjust contrast and brightness
            adjusted_image = adjust_contrast_brightness(image, alpha=1.5, beta=0)
            augmented_images.append(adjusted_image)

            corresponding_augmented_image7 = adjust_contrast_brightness(corresponding_image, alpha=1.5, beta=0)
            corresponding_augmented_images.append(corresponding_augmented_image7)


            # 8. Apply histogram equalization
            equalized_image = apply_histogram_equalization(image)
            augmented_images.append(equalized_image)

            corresponding_augmented_image8 = apply_histogram_equalization(corresponding_image)
            corresponding_augmented_images.append(corresponding_augmented_image8)

            # 9. Apply affine transform
            transformed_image = apply_affine_transform(image, rotation_angle=30, scale_factor=1.2, translation=(50, 50))
            augmented_images.append(transformed_image)

            corresponding_augmented_image9 = apply_affine_transform(corresponding_image, rotation_angle=30, scale_factor=1.2, translation=(50, 50))
            corresponding_augmented_images.append(corresponding_augmented_image9)

            # Save augmented images with indexed filenames
            for i, augmented_image in enumerate(augmented_images):
                augmented_image_path = os.path.join(augmented_image_original_directory, f"{image_filename[:-4]}_{i}.png")
                cv2.imwrite(augmented_image_path, augmented_image)
                augmented_images_count += 1

            # Save corresponding augmented images with indexed filenames
            for i, corresponding_augmented_image in enumerate(corresponding_augmented_images):
                corresponding_augmented_image_path = os.path.join(augmented_image_corresponding_directory, f"{image_filename[:-4]}_{i}.png")
                cv2.imwrite(corresponding_augmented_image_path, corresponding_augmented_image)

            original_images_count += 1

        total_original_images += original_images_count
        total_black_images += black_images_count
        total_augmented_images += augmented_images_count 


    # Print total statistics
    print("Total Statistics:")
    print(f"Total Original Images: {total_original_images}")
    print(f"Total Black Images: {total_black_images}")
    print(f"Total Augmented Images: {total_augmented_images}")

    return total_original_images,total_black_images,total_augmented_images
    




