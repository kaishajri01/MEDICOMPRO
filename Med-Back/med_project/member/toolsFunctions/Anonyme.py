import os
import csv
import pydicom
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
anonymized_fields=[(0x0008,0x0020),(0x0008,0x0021),(0x0008,0x0022),(0x0008,0x0023),
                   (0x0008,0x0030),(0x0008,0x0031),(0x0008,0x0032),(0x0008,0x0033),

                   (0x0008,0x0050),(0x0008,0x0080),(0x0008,0x0081),(0x0008,0x0090),
                   (0x0008,0x1010),

                   (0x0008,0x1030),(0x0008,0x1040),(0x0008,0x1050),(0x0008,0x1070),
                   (0x0008,0x0012),(0x0008,0x0013),(0x0008,0x0014),(0x0008,0x1150),
                   (0x0020,0x0013),(0x2005,0x0014),

                   (0x0010,0x0010),(0x0010,0x0020),(0x0010,0x0030),(0x0010,0x2180),
                   (0x0010,0x21b0),

                   (0x0020,0x000d),(0x0020,0x000e),(0x0020,0x0010),(0x0020,0x0011),
                   (0x0040,0x0244),(0x0040,0x0245),(0x0040,0x0250),(0x0040,0x0251),
                   (0x0040,0x0253),(0x0040,0x0006),

                   (0x0008,0x0050),(0x0040,0x0009),(0x0040,0x1001),(0x2001,0x0010),
                   (0x2001,0x0011),(0x2001,0x0012),(0x2001,0x0013),(0x2001,0x0014),
                   (0x2001,0x0015),(0x0008,0x002a),(0x0008,0x9123)
]

field_needed=[(0x0008,0x1030),(0x0010,0x0040),(0x0010,0x1010),(0x0010,0x1030),(0x0010,0x2100),(0x0018,0x0015)]

def is_folder_path_valid(path):
    return os.path.isdir(path)

def is_directory_empty(directory_path):
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return False  # Not a valid directory path
    return len(os.listdir(directory_path)) == 0

def Anonymizing(input_directory, output_directory):   
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if not is_folder_path_valid(input_directory):
        return 0,0,0
    
    if not is_directory_empty(output_directory):
        return 0,0,0

        
    csv_file_path=output_directory+'/informations.csv'
    num_total_files = 0
    num_valid_files = 0
    num_invalid_files = 0
    examinated_parts = {}


    csv_file = open(csv_file_path, 'w', newline='')
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')

            # Counter for renaming the files
            
        subfolder_counter = 0
            # Iterate through the directory tree
        for root, dirs, files in os.walk(input_directory):
                
            # Get the relative path from the input directory to the current directory
            relative_path = os.path.relpath(root, input_directory)

            # Create the corresponding subfolder in the output directory
            output_subfolder = os.path.join(output_directory, f"Patient_{subfolder_counter}")
            os.makedirs(output_subfolder, exist_ok=True)
            
            x=0
            # Iterate through the files in the current directory
            for file_name in files:
                file_path = os.path.join(root, file_name)
                num_total_files += 1

                try:
                    # Read the DICOM file with force=True
                    dcm = pydicom.dcmread(file_path, force=True)

                    if (0x0018, 0x0015) in dcm:
                        examinated_part = dcm[(0x0018, 0x0015)].value
                        if examinated_part not in examinated_parts:
                            examinated_parts[examinated_part] = 1
                        else:
                            examinated_parts[examinated_part] += 1
                    else:
                        print(f"Missing attribute (0x0018, 0x0015) in DICOM file: {file_path}")

                    # Modify DICOM attributes 
                    new_value = ''
                    for i in anonymized_fields:  
                        if i in dcm:
                            dcm[i].value = new_value

                    # Save the modified DICOM file to the output subfolder with numeric filename
                    output_file_path = os.path.join(output_subfolder, file_name)
                    dcm.save_as(output_file_path)

                    # Send progress message through WebSocket
                    

                    num_valid_files += 1

                    if  x==0:
                        csv_writer = csv.writer(csv_file, delimiter=';')
                        csv_writer.writerow(['Patient Number'] + [dcm[tag_code].description() if tag_code in dcm else '' for tag_code in field_needed])
                        # Write attribute values for each tag code
                        csv_writer.writerow([str(subfolder_counter)] + [str(dcm[tag_code].value) if tag_code in dcm else '' for tag_code in field_needed])
                        x=1
                except pydicom.errors.InvalidDicomError:
                    print(f"Invalid DICOM file: {file_path}")
                    num_invalid_files += 1

            # Increment the file counter
            subfolder_counter += 1

    

    # Calculate statistics for total images, valid images, and invalid images
    print("Statistics:")
    print(f"Number of total files: {num_total_files}")
    print(f"Number of valid files: {num_valid_files}")
    print(f"Number of invalid files: {num_invalid_files}")
    return num_total_files,num_valid_files,num_invalid_files

    


