import nuke
import os
from PySide2.QtCore import Qt
from PySide2 import QtWidgets
from tnt_gizmo_saver.modules.gizmo_saver_ui import GizmoSaverUI

ui_window = None

def get_nuke_main_window():
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.metaObject().className() == "Foundry::UI::DockMainWindow":
            return widget
    return None

def launch_gizmo_saver():
    """Launch the Gizmo Saver UI."""
    global ui_window 
    try:
        # Check if the UI already exists and is visible
        if not ui_window or not ui_window.isVisible():
            main_window = get_nuke_main_window()

            ui_window = GizmoSaverUI(parent=main_window)
            # ui_window.setWindowFlags(Qt.Window | Qt.Tool)
            ui_window.show()
            ui_window.raise_()
            ui_window.activateWindow()
        else:
            # If it's already open, bring it to the front
            ui_window.raise_()
            ui_window.activateWindow()
    except Exception as e:
        nuke.message(f"Error loading Gizmo Saver: {e}")


menu = nuke.menu("Nuke")
custom_menu = menu.addMenu("TNT Tools")

current_dir = os.path.dirname(__file__)
icon_path = os.path.join(current_dir, "icons", "tnt_icon_bright.svg")
icon_path = os.path.normpath(icon_path).replace("\\", "/")

custom_menu.addCommand("TNT Gizmo Saver", launch_gizmo_saver, icon=icon_path)

print("TNT Gizmo Saver added to the Nuke menu with an icon.")
