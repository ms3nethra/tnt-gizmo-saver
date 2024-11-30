import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox, QComboBox, QFormLayout, QPushButton, QSizePolicy, QSpacerItem

class GizmoSaverUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TNT Gizmo Saver")
        self.setMinimumSize(600, 400)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.create_input_groupbox())

    def create_input_groupbox(self):
        input_groupbox = QGroupBox("Gizmo Input Details")
        input_layout = QVBoxLayout(input_groupbox)
        input_layout.addLayout(self.create_input_section())

        return input_groupbox

    def create_input_section(self):
        # author input
        author_label = QLabel("Author:")
        self.author_input = QLineEdit()
        
        # Department input
        dept_label = QLabel("Department:")
        self.dept_input = QComboBox()
        self.dept_input.addItems(["comp", "lighting", "fx", "animation"])

        self.add_dept_button = QPushButton("+")
        self.add_dept_button.setFixedSize(24, 24)

        dept_layout = QHBoxLayout()
        dept_layout.addWidget(self.dept_input, 9)
        dept_layout.addWidget(self.add_dept_button, 1)

        # Gizmo name
        gizmo_label = QLabel("Gizmo Name:")
        self.gizmo_name_input = QLineEdit()

        # Form Layouts 1 (Author, Department, Gizmo Name)
        form_layout1 = QFormLayout()
        form_layout1.addRow(author_label, self.author_input)
        form_layout1.addRow(dept_label, dept_layout)
        form_layout1.addRow(gizmo_label, self.gizmo_name_input)

        # Version Section (Major and Minor)
        major_label = QLabel("Major:")
        self.major_version_input = QSpinBox()
        minor_label = QLabel("Minor:")
        self.minor_version_input = QSpinBox()

        major_form_layout = QFormLayout()
        major_form_layout.addRow(major_label, self.major_version_input)
        minor_form_layout = QFormLayout()
        minor_form_layout.addRow(minor_label, self.minor_version_input)

        version_layout = QHBoxLayout()
        version_layout.addLayout(major_form_layout)
        version_layout.addSpacing(20)
        version_layout.addLayout(minor_form_layout)

        # Description 
        disciption_label = QLabel("Description:")
        self.disciption_input = QLineEdit()

        # Form Layout 2 (Version and Description)
        form_layout2 = QFormLayout()
        form_layout2.addRow(QLabel(""))
        form_layout2.addRow(version_layout)
        form_layout2.addRow(disciption_label, self.disciption_input)

        # Combine Input Layouts
        create_input_layout = QHBoxLayout()
        create_input_layout.addLayout(form_layout1)
        create_input_layout.addSpacing(20)
        create_input_layout.addLayout(form_layout2)

        return create_input_layout

    """
    def filepath_format_widgets(self):

    def gizmo_nameformat_display_widgets(self):

    def save_cancel_widgets(self)
    """



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GizmoSaverUI()
    window.show()
    sys.exit(app.exec_())


