import sys
import os
import re

def get_default_nuke_directory():
    """ Returns the default .nuke directory. """
    user_home_directory = os.path.expanduser("~")
    nuke_directory = os.path.join(user_home_directory, ".nuke")
    return nuke_directory

def extract_gizmo_details(file_name):
    """
    Extract details from gizmo file name, such as author, departmernt,
    gizmo name, major and minor virsion.
    """
    pattern = re.compile(
        r"^(?P<author>[a-zA-Z0-9]+)[_\-\.]"
        r"(?P<department>[a-zA-Z0-9]+)[_\-\.]"
        r"(?P<gizmo_name>[a-zA-Z0-9]+)[_\-\.]"
        r"(?P<major>\d+)[_\-\.]"
        r"(?P<minor>\d+)\.gizmo$"
    )

    file_match = pattern.match(file_name)
    if file_match:
        return file_match.groupdict()
    return None

def determine_file_format(file_name):
    """
    Determine the file format used in the gizmo file name.
    """
    for format in ["_", "-", "."]:
        if format in file_name:
            return format
    return None

def find_gizmo_files(directory):
    """
    
    """
    gizmo_files = []
    for file in os.listdir(directory):
        if file.endswith(".gizmo"):
            extracted_details = extract_gizmo_details(file)
            if extracted_details:
                extracted_details["file_format"] = determine_file_format(file)
                gizmo_files.append(extracted_details)

    return gizmo_files

if __name__ == "__main__":
    nuke_dir = get_default_nuke_directory()
    print(f"[DEBUG] Checking for gizmo files in directory: {nuke_dir}")

    #Debugging extract_gizmo_details function
    test_file = "thri_comp_renderTool_1.0.gizmo"
    details = extract_gizmo_details(test_file)
    print(f"[DEBUG] Extracted details: {details}")

    # Debugging determine_file_format function
    file_format = determine_file_format(test_file)
    print(f"[DEBUG] Detected file format: {format}")
    print(type(format))

    # Debugging find_gizmo_files function
    test_directory = nuke_dir  # Change to an appropriate test directory
    gizmo_files = find_gizmo_files(test_directory)

    print(f"[DEBUG] Total gizmo files found: {len(gizmo_files)}")

    # if os.path.exists(nuke_dir):
    #     gizmo_files = find_gizmo_files(nuke_dir)

    #     if gizmo_files:
    #         print("\nFound Gizmo Files:")
    #         for gizmo in gizmo_files:
    #             print(f"\nGizmo Details:")
    #             print(f"  Author: {gizmo['author']}")
    #             print(f"  Department: {gizmo['department']}")
    #             print(f"  Gizmo Name: {gizmo['gizmo_name']}")
    #             print(f"  Major Version: {gizmo['major']}")
    #             print(f"  Minor Version: {gizmo['minor']}")
    #             print(f"  File Format: {gizmo['file_format']}")
    #     else:
    #         print("No valid gizmo files found in the directory.")

    # else:
    #     print(f"Directory does not exist: {nuke_dir}")