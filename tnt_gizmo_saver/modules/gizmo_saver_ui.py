import sys
import os
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox, QComboBox, QFormLayout, QPushButton, QSizePolicy, QSpacerItem
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QFont

class GizmoSaverUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TNT Gizmo Saver")
        self.set_style_sheet()
        self.init_ui()
        self.signals_and_connections()

    """'''''''''''''''''''''''''''''''setting style sheet foe widgets'''''''''''''''''''''''''''''''"""
    def set_style_sheet(self):
        self.groupbox_small_tittle = """QGroupBox::title {
            font-size: 50%;
            }
        """

        self.lineedit_background_none = """QLineEdit {
        background: transparent;
        border: none
        }
        """

        self.label_small_red_text = """QLabel {
            font-size: 30%; 
            color: red; 
            }
        """


    """'''''''''''''''''''''''''''''''create ui elements and layouts'''''''''''''''''''''''''''''''"""
    def init_ui(self):
        # -------------------------------Convert to group section-------------------------------
        cvrt_groupbox = QGroupBox("")
        cvrt_main_layout = QVBoxLayout(cvrt_groupbox)
        self.cvrt_group_button = QPushButton("Convert to Group")
        self.cvrt_group_button.setMaximumWidth(160)

        cvrt_main_layout.addWidget(self.cvrt_group_button, alignment=Qt.AlignCenter)

        # -------------------------------create_input_section-------------------------------
        input_groupbox = QGroupBox("Gizmo Input Details")
        input_groupbox.setStyleSheet(self.groupbox_small_tittle)
        input_main_layout = QVBoxLayout(input_groupbox)

        # author input
        author_label = QLabel("Author:")
        self.author_input = QLineEdit()
        self.author_input.setStyleSheet(self.lineedit_background_none)
        self.author_input.setReadOnly(True)
        
        # Department input
        dept_label = QLabel("Department:")
        self.dept_input = QComboBox()
        self.dept_input.addItems(["comp", "lighting", "fx", "animation"])

        self.add_dept_button = QPushButton("+")
        self.add_dept_button.setMaximumWidth(24)

        dept_layout = QHBoxLayout()
        dept_layout.addWidget(self.dept_input, stretch=1)
        dept_layout.addWidget(self.add_dept_button, stretch=0)

        dept_layout.setAlignment(Qt.AlignRight)

        # Gizmo name
        gizmo_label = QLabel("Gizmo Name:")
        self.gizmo_name_input = QLineEdit()

        # Form Layouts 1 (Author, Department, Gizmo Name)
        form_layout1 = QFormLayout()
        form_layout1.addRow(author_label, self.author_input)
        form_layout1.addRow(dept_label, dept_layout)
        form_layout1.addRow(gizmo_label, self.gizmo_name_input)

        
        self.refresh_button = QPushButton("Refresh")

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
        vertical_layout2 = QVBoxLayout()
        form_layout2 = QFormLayout()
        form_layout2.addRow(version_layout)
        form_layout2.addRow(disciption_label, self.disciption_input)

        vertical_layout2.addWidget(self.refresh_button)
        vertical_layout2.addLayout(form_layout2)

        # Combine Input Layouts
        combined_input_layout = QHBoxLayout()
        combined_input_layout.addLayout(form_layout1)
        combined_input_layout.addSpacing(20)
        combined_input_layout.addLayout(vertical_layout2)

        input_main_layout.addLayout(combined_input_layout)

        # -------------------------------create_filepath_format_section-------------------------------
        location_groupbox = QGroupBox("Location")
        location_groupbox.setStyleSheet(self.groupbox_small_tittle)
        location_groupbox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        location_main_layout = QVBoxLayout(location_groupbox)

        save_to_label = QLabel("Save To:")
        self.filepath_input = QLineEdit()

        self.Directory_path_button = QPushButton("...")
        self.Directory_path_button.setMaximumWidth(24)

        self.path_reset_button = QPushButton("r")
        self.path_reset_button.setMaximumWidth(24)

        file_format_label = QLabel("File Format:")
        self.file_format_input = QComboBox()
        self.file_format_input.addItems(["_", "-", "."])

        filepath_format_layout = QFormLayout()
        filepath_format_layout.addRow(save_to_label, self.filepath_input)
        filepath_format_layout.addRow(file_format_label, self.file_format_input)

        
        directory_reset_button_hlayout = QHBoxLayout()
        directory_reset_button_hlayout.addWidget(self.Directory_path_button)
        directory_reset_button_hlayout.addWidget(self.path_reset_button)

        directory_reset_button_vlayout = QVBoxLayout()
        directory_reset_button_vlayout.addLayout(directory_reset_button_hlayout)
        directory_reset_button_vlayout.setAlignment(Qt.AlignTop)

        # Combine File Path Buttons with File Path Input
        filepath_format_combine_layout = QHBoxLayout()
        filepath_format_combine_layout.addLayout(filepath_format_layout)
        filepath_format_combine_layout.addLayout(directory_reset_button_vlayout)

        location_main_layout.addLayout(filepath_format_combine_layout)

        # -------------------------------create_gizmo_nameformat_display_section-------------------------------
        display_groupbox = QGroupBox("Name Format Display")
        display_groupbox.setStyleSheet(self.groupbox_small_tittle)
        display_groupbox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        display_groupbox.setMinimumHeight(140)

        display_main_layout = QVBoxLayout(display_groupbox)

        self.file_format_output = QLabel("author1_comp_motionblur_1_0_beta.gizmo")
        self.file_format_output.setAlignment(Qt.AlignCenter)

        # setting up font size twice bigger than the acual size
        font = self.file_format_output.font()
        font.setPointSize(font.pointSize() * 2)
        self.file_format_output.setFont(font)

        self.file_exists_warning = QLabel("Gizmo already Exists in .nuke folder")
        self.file_exists_warning.setStyleSheet(self.label_small_red_text)

        self.save_button = QPushButton("Save")
        self.save_button.setMaximumWidth(80)

        file_exists_and_save_hlayout = QHBoxLayout()
        file_exists_and_save_hlayout.addWidget(self.file_exists_warning)
        file_exists_and_save_hlayout.addWidget(self.save_button)
        # file_exists_and_save_hlayout.setAlignment(Qt.AlignRight)

        display_main_layout.addWidget(self.file_format_output)
        display_main_layout.addLayout(file_exists_and_save_hlayout)
        
        # -------------------------------save_major_minor_section-------------------------------
        major_minor_groupbox = QGroupBox("Save Major or Minor Versions")
        major_minor_groupbox.setStyleSheet(self.groupbox_small_tittle)
        major_minor_groupbox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        major_minor_groupbox.setMinimumHeight(100)

        major_minor_main_layout = QVBoxLayout(major_minor_groupbox)

        # Major widgets
        major_hlayout = QHBoxLayout()
        self.major_version_label = QLabel("author1_comp_motionblur_2_0.gizmo")

        self.major_version_save_button = QPushButton("Save Major")
        self.major_version_save_button.setMaximumWidth(80)

        major_hlayout.addWidget(self.major_version_label)
        major_hlayout.addWidget(self.major_version_save_button)

        # Minor widgets
        minor_hlayout = QHBoxLayout()
        self.minor_version_label = QLabel("author1_comp_motionblur_1_1.gizmo")

        self.minor_version_save_button = QPushButton("Save minor")
        self.minor_version_save_button.setMaximumWidth(80)

        minor_hlayout.addWidget(self.minor_version_label)
        minor_hlayout.addWidget(self.minor_version_save_button)

        major_minor_main_layout.addLayout(major_hlayout)
        major_minor_main_layout.addLayout(minor_hlayout)

        # -------------------------------create_cancel_section-------------------------------
        cancel_groupbox = QGroupBox()
        cancel_groupbox.setStyleSheet("QGroupBox { border: none; }")
        cancel_main_layout = QVBoxLayout(cancel_groupbox)

        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMaximumWidth(80)

        cancel_layout = QHBoxLayout()
        cancel_layout.addWidget(self.cancel_button)
        cancel_layout.setAlignment(Qt.AlignRight)

        cancel_main_layout.addLayout(cancel_layout)

        # -------------------------------Add sub layouts to main layouts-------------------------------
        self.main_layout = QVBoxLayout(self)
        
        self.main_layout.addWidget(cvrt_groupbox)
        self.main_layout.addWidget(input_groupbox)
        self.main_layout.addWidget(location_groupbox)
        self.main_layout.addWidget(display_groupbox)
        self.main_layout.addWidget(major_minor_groupbox)
        self.main_layout.addWidget(cancel_groupbox)

    """'''''''''''''''''''''''''''''''signals_and_connections'''''''''''''''''''''''''''''''"""
    def signals_and_connections(self):
        """signals and connections for ui"""
        # author - system user name connection 
        self.author_input.setText(self.get_system_user())

        # save to - nuke default directoty connection
        self.filepath_input.setText(self.get_default_nuke_directory())
        self.Directory_path_button.clicked.connect(self.browse_folder)

        self.path_reset_button.clicked.connect(self.reset_folder_path)


    """'''''''''''''''''''''''''''''''get_system_user'''''''''''''''''''''''''''''''"""
    @staticmethod
    def get_system_user():
        """Retrieve the system's current username"""
        username = os.getenv("USERNAME") or os.getenv("USER") or "Unknown"
        return username
    
    """'''''''''''''''''''''''''''''''get_default_nuke_directory'''''''''''''''''''''''''''''''"""
    @staticmethod
    def get_default_nuke_directory():
        """Returns the default .nuke directory"""
        user_home_directory = os.path.expanduser("~")
        nuke_directory = os.path.join(user_home_directory, ".nuke")
        return nuke_directory
    
    """'''''''''''''''''''''''''''''''browse_folder'''''''''''''''''''''''''''''''"""
    def browse_folder(self):
        """Open a folder browser dialog and update the current folder path"""

        current_path = self.filepath_input.text()

        if not os.path.isdir(current_path):
            current_path = self.get_default_nuke_directory()

        folder_path = QFileDialog.getExistingDirectory(self, "Select Save Directory", current_path)

        if folder_path:
            self.filepath_input.setText(folder_path)

    """'''''''''''''''''''''''''''''''reset_folder_path'''''''''''''''''''''''''''''''"""
    def reset_folder_path(self):
        """Reset the folder path to the default .nuke directory."""
        default_path = self.get_default_nuke_directory()
        self.filepath_input.setText(default_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GizmoSaverUI()
    window.show()
    sys.exit(app.exec_())


