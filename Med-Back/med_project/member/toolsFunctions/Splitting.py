import os
import random
import shutil


def is_folder_path_valid(path):
    return os.path.isdir(path)

def is_directory_empty(directory_path):
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return False  # Not a valid directory path
    return len(os.listdir(directory_path)) == 0

def split_directories(input_folder, output_folder):

    if not is_folder_path_valid(input_folder):
        return 0
    
    if not is_directory_empty(output_folder):
        return 0
    
    # Create output folders if they don't exist
    train_folder = os.path.join(output_folder, "train")
    test_folder = os.path.join(output_folder, "test")
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    
    # Get list of directories in the input folder
    directories = [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]
    
    # Calculate the number of directories for the train and test folders
    total_directories = len(directories)
    train_count = int(0.8 * total_directories)
    test_count = total_directories - train_count
    
    # Randomly select directories for the train folder
    train_directories = random.sample(directories, train_count)
    
    # Move directories to the train folder
    for directory in train_directories:
        src = os.path.join(input_folder, directory)
        dst = os.path.join(train_folder, directory)
        shutil.move(src, dst)
    
    # Move remaining directories to the test folder
    directories = [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]  # Update the directories list
    for directory in directories:
        src = os.path.join(input_folder, directory)
        dst = os.path.join(test_folder, directory)
        shutil.move(src, dst)

    return 100
# Usage example
#input_folder_path = "D:/StageETE/RANIA_DATA_AUGMENTATION/SplitTest/train"
#output_folder_path = "D:/StageETE/RANIA_DATA_AUGMENTATION/SplitTest/output"
