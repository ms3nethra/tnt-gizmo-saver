import nuke
import os
import platform
import subprocess

def get_current_username():
    username = os.getlogin()
    return username

def get_nuke_directory():
    user_home_directory = os.path.expanduser("~")
    nuke_directory = os.path.join(user_home_directory, ".nuke")
    return nuke_directory

def open_nuke_directory(directory):
    directory = get_nuke_directory()
    
    try:
        if not os.path.exists(directory):
                nuke.message("The .nuke folder does not exist in your home directory.")
                return

        # Open the directory in the system's file explorer
        if platform.system() == "Windows":  # Windows
            os.startfile(directory)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", directory], check=True)
        elif platform.system() == "Linux":  # Linux
            subprocess.run(["xdg-open", directory], check=True)
        else:
            nuke.message("Unsupported operating system.")
            
    except Exception as e:
        nuke.message(f"Failed to open the directory: {str(e)}")


get_current_username()
get_nuke_directory()
