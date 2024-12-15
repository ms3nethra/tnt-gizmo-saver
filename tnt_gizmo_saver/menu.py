import nuke
from tnt_gizmo_saver.modules.gizmo_saver_ui import GizmoSaverUI

ui_window = None

def launch_gizmo_saver():
    """Launch the Gizmo Saver UI."""
    global ui_window 
    try:
        # Check if the UI already exists and is visible
        if not ui_window or not ui_window.isVisible():
            ui_window = GizmoSaverUI()
            ui_window.show()
        else:
            # If it's already open, bring it to the front
            ui_window.raise_()
            ui_window.activateWindow()
    except Exception as e:
        nuke.message(f"Error loading Gizmo Saver: {e}")


menu = nuke.menu("Nuke")
custom_menu = menu.addMenu("TNT Tools")
custom_menu.addCommand("TNT Gizmo Saver", launch_gizmo_saver)

print("TNT Gizmo Saver added to the Nuke menu.")
