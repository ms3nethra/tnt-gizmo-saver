import os
import nuke

current_dir = os.path.dirname(os.path.abspath(__file__))

modules_path = os.path.join(current_dir, "modules")
icons_path = os.path.join(current_dir, "icons")

nuke.pluginAddPath(modules_path)
nuke.pluginAddPath(icons_path)
