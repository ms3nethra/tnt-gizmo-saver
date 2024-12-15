import os
import sys
import nuke

current_dir = os.path.dirname(os.path.abspath(__file__))

modules_path = os.path.join(current_dir, "modules")
icons_path = os.path.join(current_dir, "icons")

nuke.pluginAddPath(modules_path)
nuke.pluginAddPath(icons_path)

print("Modules Path:", modules_path)
print("Icons Path:", icons_path)

# parent_dir = os.path.dirname(current_dir)

# if parent_dir not in sys.path:
#     sys.path.append(parent_dir)