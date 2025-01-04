import sys
import os
import re
import getpass

"""'''''''''''''''''''''''''''''''getting_default_nuke_directory'''''''''''''''''''''''''''''''"""
def get_default_nuke_directory():
    """ Returns the default .nuke directory. """
    user_home_directory = os.path.expanduser("~")
    nuke_directory = os.path.join(user_home_directory, ".nuke")
    return nuke_directory

"""'''''''''''''''''''''''''''''''getting_system_user'''''''''''''''''''''''''''''''"""
def get_system_user():
    """Fetch the current system user as the author."""
    return getpass.getuser()

"""'''''''''''''''''''''''''''''''extracting_group_node_name_details'''''''''''''''''''''''''''''''"""
def extract_group_node_details(group_name):
    """
    Extract author, department, gizmo name, major, and minor versions from a group node name.
    """
    pattern = re.compile(
        r"^(?P<author>[a-zA-Z0-9]+)[_\-.]"
        r"(?P<department>[a-zA-Z0-9]+)[_\-.]"
        r"(?P<gizmo_name>[a-zA-Z0-9]+)[_\-.]"
        r"(?P<major>\d+)[_\-.]"
        r"(?P<minor>\d+)_group\d+$"
    )

    match = pattern.match(group_name)
    if match:
        return match.groupdict()
    return None

"""'''''''''''''''''''''''''''''''finding_latest_gizmo_file'''''''''''''''''''''''''''''''"""
def find_latest_gizmo_file(directory, department, gizmo_name):
    """
    Find the latest gizmo file matching the department and gizmo name in the directory.
    """
    latest_file = None
    latest_major = 1
    latest_minor = 0

    for file in os.listdir(directory):
        if file.endswith(".gizmo"):
            details = extract_gizmo_details(file)
            if details and details["department"] == department and details["gizmo_name"] == gizmo_name:
                major = int(details["major"])
                minor = int(details["minor"])

                if (major > latest_major) or (major == latest_minor and minor > latest_minor):
                    latest_file = file
                    latest_major = major
                    latest_minor = minor
    
    return latest_file, latest_major, latest_minor

"""'''''''''''''''''''''''''''''''extracting name details from gizmo'''''''''''''''''''''''''''''''"""
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

if __name__ == "__main__":
    nuke_dir = get_default_nuke_directory()
    # print(f"[DEBUG] Checking for gizmo files in directory: {nuke_dir}")

    #Debugging extract_gizmo_details function
    test_file = "thrinethra_comp_motionblur_1_0.gizmo"
    details = extract_gizmo_details(test_file)
    print(f"[DEBUG] Extracted details: {details}")
    department = details["department"]
    
    print(department)
    # latest_versions = find_latest_gizmo_file()





