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
        self.main_layout.addWidget(self.create_input_section())
        self.main_layout.addWidget(self.filepath_format_section())
        
    def create_input_section(self):
        input_groupbox = QGroupBox("Gizmo Input Details")
        input_main_layout = QVBoxLayout(input_groupbox)

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
        combined_input_layout = QHBoxLayout()
        combined_input_layout.addLayout(form_layout1)
        combined_input_layout.addSpacing(20)
        combined_input_layout.addLayout(form_layout2)

        input_main_layout.addLayout(combined_input_layout)
        return input_groupbox

    
    def filepath_format_section(self):
        location_groupbox = QGroupBox("Location")
        location_main_layout = QVBoxLayout(location_groupbox)

        save_to_label = QLabel("Save To:")
        self.filepath_input = QLineEdit("C:/Users/author1/.nuke")

        Directory_path_button = QPushButton("...")
        Directory_path_button.setFixedSize(30, 24)

        path_reset_button = QPushButton("r")
        path_reset_button.setFixedSize(30, 24)

        file_format_label = QLabel("File Format:")
        self.file_format_input = QComboBox()
        self.file_format_input.addItems(["_", "-", "."])

        filepath_format_layout = QFormLayout()
        filepath_format_layout.addRow(save_to_label, self.filepath_input)
        filepath_format_layout.addRow(file_format_label, self.file_format_input)

        directory_reset_button_layout = QHBoxLayout()
        directory_reset_button_layout.addWidget(Directory_path_button)
        directory_reset_button_layout.addWidget(path_reset_button)

        filepath_format_combine_layout = QHBoxLayout()
        filepath_format_combine_layout.addLayout(filepath_format_layout)
        filepath_format_combine_layout.addLayout(directory_reset_button_layout)

        location_main_layout.addLayout(filepath_format_combine_layout)

        return location_groupbox




    
    #def gizmo_nameformat_display_widgets(self):

    #def save_cancel_widgets(self)
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GizmoSaverUI()
    window.show()
    sys.exit(app.exec_())


