import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox, QComboBox, QFormLayout, QPushButton

class GizmoSaverUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TNT Gizmo Saver")
        self.init_ui()

    def init_ui(self):
        self.main_gizmo_layout = QVBoxLayout(self)
        self.main_gizmo_layout.addWidget(self.input_widgets(self))

    def create_input_section(self):
        # author, department, gizmo widgets and layouts
        author_label = QLabel("Author:")
        self.author_input = QLineEdit()
        
        dept_label = QLabel("Department:")
        self.dept_input = QComboBox()
        self.dept_input.addItem(["comp", "lighting", "fx", "animation"])
        self_add_dept_button = QPushButton("+")

        dept_layout = QHBoxLayout()
        dept_layout.addWidget(self.dept_input)
        dept_layout.addWidget(self_add_dept_button)

        # Gizmo name
        gizmo_label = QLabel("Gizmo Name:")
        self.gizmo_name_input = QLineEdit()

        # Major and Mionr versions 
        major_label = QLabel("Major:")
        self.major_version_input = QSpinBox()

        minor_label = QLabel("Minor:")
        self.minor_version_input = QSpinBox()

        version_layout = QHBoxLayout()
        version_layout.addWidget(major_label)
        version_layout.addWidget(self.major_version_input)
        version_layout.addWidget(minor_label)
        version_layout.addWidget(self.minor_version_input)

        self.input_farmlayout1 = QFormLayout()
        self.input_farmlayout1.addRow(self.author_label, self.author_input)
        self.input_farmlayout1.addRow(self.dept_label, self.dept_input)
        self.input_farmlayout1.addRow(self.gizmo_label, self.gizmo_name)



        self.major_farmlayout = QFormLayout()
        self.major_farmlayout.addRow(self.major_label, self.major_name)
        self.minor_farmlayout = QFormLayout()
        self.minor_farmlayout.addRow(self.minor_label, self.minor_name)

        self.version_layout = QHBoxLayout()
        self.version_layout.addWidget(self.major_farmlayout)
        self.version_layout.addWidget(self.minor_farmlayout)

        # Description widgets and layouts,
        self.disciption_label = QLabel("Minor:")
        self.disciption_name = QLineEdit()

        self.Disc_farmlayout = QFormLayout()
        self.Disc_farmlayout.addRow(self.major_label, self.major_name)

        # input_layout2 - Versions and Discription layout
        self.input_layout2 = QVBoxLayout()
        self.input_layout2.addWidget(self.version_layout, self.Disc_farmlayout)

        # Gizmo Inputs main layout
        self.input_main_layout = QHBoxLayout()
        self.input_main_layout.addWidget(self.input_farmlayout1, self.input_layout2)

    def filepath_format_widgets(self):

    def gizmo_nameformat_display_widgets(self):

    def save_cancel_widgets(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GizmoSaverUI()
    window.show()
    sys.exit(app.exec_())


