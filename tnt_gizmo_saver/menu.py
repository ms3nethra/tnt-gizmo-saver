import nuke
from tnt_gizmo_saver.modules.gizmo_saver_ui import GizmoSaverUI

def launch_gizmo_saver():
    """Launch the Gizmo Saver UI."""
    try:
        ui = GizmoSaverUI()
        ui.show()
    except Exception as e:
        nuke.message(f"Error loading Gizmo Saver: {e}")

menu = nuke.menu("Nuke")
custom_menu = menu.addMenu("TNT Tools")
custom_menu.addCommand("TNT Gizmo Saver", "launch_gizmo_saver()")