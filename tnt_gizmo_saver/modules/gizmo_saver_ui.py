import sys
import os
import nuke
import re
import getpass
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QGroupBox, QLabel, QLineEdit, QSpinBox, QComboBox, QFormLayout, 
    QPushButton, QSizePolicy, QDialog, QListWidget, QListWidgetItem
)
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QFont, QIcon, QPixmap
import json

# -----------------------------------------------------------------------
# Major and Minor Qdialog ui
# -----------------------------------------------------------------------
class MajorMinorDialog(QDialog):
    def __init__(self, major_filename, minor_filename, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Major or Minor Versions")
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "icons", "tnt_icon_dark.svg",)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon file not found at: {icon_path}")

        self.setMinimumSize(460, 120)

        self.major_filename = major_filename
        self.minor_filename = minor_filename

        main_layout = QVBoxLayout(self)

        major_minor_groupbox = QGroupBox("")

        major_minor_main_layout = QVBoxLayout(major_minor_groupbox)

        # Major widgets
        major_hlayout = QHBoxLayout()
        self.major_version_label = QLabel(self.major_filename)
        self.major_version_save_button = QPushButton("Save Major")
        self.major_version_save_button.setMaximumWidth(80)
        major_hlayout.addWidget(self.major_version_label)
        major_hlayout.addWidget(self.major_version_save_button)

        major_minor_main_layout.addLayout(major_hlayout)

        # Minor widgets
        minor_hlayout = QHBoxLayout()
        self.minor_version_label = QLabel(self.minor_filename)
        self.minor_version_save_button = QPushButton("Save minor")
        self.minor_version_save_button.setMaximumWidth(80)
        minor_hlayout.addWidget(self.minor_version_label)
        minor_hlayout.addWidget(self.minor_version_save_button)

        major_minor_main_layout.addLayout(minor_hlayout)

        main_layout.addWidget(major_minor_groupbox)

        self.major_version_save_button.clicked.connect(self.on_save_major)
        self.minor_version_save_button.clicked.connect(self.on_save_minor)

    def on_save_major(self):
        self.save_group_as_gizmo_dialog(self.major_filename)

    def on_save_minor(self):
        self.save_group_as_gizmo_dialog(self.minor_filename)

    def save_group_as_gizmo_dialog(self, gizmo_filename):
        try:
            parent_ui = self.parent()
            if not parent_ui:
                nuke.message("Error: missing parent UI.")
                return

            directory = parent_ui.filepath_input.text().strip()
            if not os.path.isdir(directory):
                directory = parent_ui.get_default_nuke_directory()

            full_path = os.path.join(directory, gizmo_filename)

            selected_node = nuke.selectedNode()
            if not isinstance(selected_node, nuke.Group):
                nuke.message("Please select a Group node to save.")
                return

            parent_ui.export_group_as_gizmo(selected_node, full_path)

        except Exception as e:
            nuke.message(f"Error saving major/minor:\n{e}")

        self.accept()

# -----------------------------------------------------------------------
# Add Departments to department combo box
# -----------------------------------------------------------------------
class add_department_ui(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Departments")
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "icons", "tnt_icon_dark.svg",)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon file not found at: {icon_path}")

        # Adjust these paths as needed
        self.json_file_path = os.path.join(os.path.dirname(__file__), "departments.json")

        self.default_departments = ["comp", "roto", "key"]

        self.departments = [] 

        self.load_departments()
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        departments_label = QLabel("Departments:")

        self.departments_list = QListWidget()
        self.populate_departments()

        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")

        self.move_up_button = QPushButton("˄")
        self.move_down_button = QPushButton("˅")

        self.accept_button = QPushButton("Accept")
        self.cancel_button = QPushButton("Cancel")

        main_layout.addWidget(departments_label)
        main_layout.addWidget(self.departments_list)

        add_remove_button_layout = QHBoxLayout()
        add_remove_button_layout.addWidget(self.add_button)
        add_remove_button_layout.addWidget(self.remove_button)

        move_button_layout = QHBoxLayout()
        move_button_layout.addWidget(self.move_up_button)
        move_button_layout.addWidget(self.move_down_button)

        add_remove_move_layout = QHBoxLayout()
        add_remove_move_layout.addLayout(add_remove_button_layout)
        add_remove_move_layout.addLayout(move_button_layout)

        main_layout.addLayout(add_remove_move_layout)

        accept_cancel_layout = QHBoxLayout()
        accept_cancel_layout.addWidget(self.accept_button)
        accept_cancel_layout.addWidget(self.cancel_button)

        main_layout.addLayout(accept_cancel_layout)

    def connect_signals(self):
        self.add_button.clicked.connect(self.add_department)
        self.remove_button.clicked.connect(self.remove_department)

        self.move_up_button.clicked.connect(self.move_up_department)
        self.move_down_button.clicked.connect(self.move_down_department)

        self.accept_button.clicked.connect(self.accept_changes)
        self.cancel_button.clicked.connect(self.close_window)

    def load_departments(self):
        loaded = []
        try:
            with open(self.json_file_path, "r") as f:
                loaded = json.load(f)

        except FileNotFoundError:
            pass

        combined = list(self.default_departments)
        for dept in loaded:
            if dept not in combined:
                combined.append(dept)

        self.departments = combined

    def save_departments(self):
        with open(self.json_file_path, "w") as f:
            json.dump(self.departments, f, indent=4)

    def populate_departments(self):
        self.departments_list.clear()

        for dept in self.departments:
            item = QListWidgetItem(dept)

            if dept in self.default_departments:
                # Make it non-editable
                # Remove the editable flag from the item
                flags = item.flags()
                flags &= ~Qt.ItemIsEditable
                item.setFlags(flags)
            else:
                # Make user items editable
                item.setFlags(item.flags() | Qt.ItemIsEditable)

            self.departments_list.addItem(item)

    def add_department(self):
        new_item = QListWidgetItem("department")
        new_item.setFlags(new_item.flags() | Qt.ItemIsEditable)
        self.departments_list.addItem(new_item)

        row_count = self.departments_list.count()
        self.departments_list.setCurrentRow(row_count - 1)

    def remove_department(self):
        selected_items = self.departments_list.selectedItems()
        for item in selected_items:
            if item.text() in self.default_departments:
                nuke.message(f"Cannot remove default department: {item.text()}")
                continue
            self.departments_list.takeItem(self.departments_list.row(item))

    def move_up_department(self):
        current_row = self.departments_list.currentRow()
        if current_row > 0:
            current_item = self.departments_list.takeItem(current_row)
            self.departments_list.insertItem(current_row - 1, current_item)
            self.departments_list.setCurrentRow(current_row - 1)

    def move_down_department(self):
        current_row = self.departments_list.currentRow()
        if current_row < self.departments_list.count() - 1:
            current_item = self.departments_list.takeItem(current_row)
            self.departments_list.insertItem(current_row + 1, current_item)
            self.departments_list.setCurrentRow(current_row + 1)

    def accept_changes(self):
        self.departments.clear()
        for i in range(self.departments_list.count()):
            self.departments.append(self.departments_list.item(i).text())

        self.save_departments()
        self.close()

    def close_window(self):
        self.close()

# -----------------------------------------------------------------------
# Gizmo Saver Main UI
# -----------------------------------------------------------------------
class GizmoSaverUI(QWidget):
    def __init__(self, parent=None):
        super(GizmoSaverUI, self).__init__(parent)
        self.setWindowTitle("TNT Gizmo Saver")
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "icons", "tnt_icon_dark.svg",)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon file not found at: {icon_path}")

        self.set_style_sheet()
        self.init_ui()
        self.signals_and_connections()
        self.load_departments_into_combo()
        self.refresh_input_details_if_group_selected()
        self.refresh_file_format_display()

    """'''''''''''''''''''''''''''''''setting style sheet foe widgets'''''''''''''''''''''''''''''''"""
    def set_style_sheet(self):
        self.groupbox_small_tittle = """QGroupBox
        {
        font-size: 10px;
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

        self.display_label_big_text = """QLabel {
            font-size: 18px; 
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

        self.add_dept_button = QPushButton()
        self.add_dept_button.setIcon(QIcon(":/qrc/images/Add.png"))
        self.add_dept_button.setIconSize(QSize(16, 16))
        self.add_dept_button.setMaximumSize(20, 20)

        dept_layout = QHBoxLayout()
        dept_layout.addWidget(self.dept_input, stretch=1)
        dept_layout.addWidget(self.add_dept_button, stretch=0)

        dept_layout.setAlignment(Qt.AlignRight)

        # Gizmo name
        gizmo_label = QLabel("Gizmo Name:")
        self.gizmo_name_input = QLineEdit()
        self.gizmo_name_input.setPlaceholderText("gizmoname")

        # Form Layouts 1 (Author, Department, Gizmo Name)
        form_layout1 = QFormLayout()
        form_layout1.addRow(author_label, self.author_input)
        form_layout1.addRow(dept_label, dept_layout)
        form_layout1.addRow(gizmo_label, self.gizmo_name_input)

        
        self.refresh_button = QPushButton("Refresh")

        # Version Section (Major and Minor)
        major_label = QLabel("Major:")
        self.major_version_input = QSpinBox()
        self.major_version_input.setMaximumHeight(24)
        self.major_version_input.setMinimum(1)
        self.major_version_input.setValue(1)
        minor_label = QLabel("Minor:")
        self.minor_version_input = QSpinBox()
        self.minor_version_input.setMaximumHeight(24)
        self.minor_version_input.setMinimum(0)
        self.minor_version_input.setValue(0)

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

        self.Directory_path_button = QPushButton()
        self.Directory_path_button.setIcon(QIcon(":/qrc/images/FolderIcon.png"))
        self.Directory_path_button.setIconSize(QSize(16, 16))
        self.Directory_path_button.setMaximumSize(20, 20)

        self.path_reset_button = QPushButton()
        self.path_reset_button.setIcon(QIcon(":/qrc/images/revert.png"))
        self.path_reset_button.setIconSize(QSize(16, 16))
        self.path_reset_button.setMaximumSize(20, 20)

        file_format_label = QLabel("File Format:")
        self.file_format_input = QComboBox()
        self.file_format_input.addItems([
            "author_dept_asset_major_minor_description",
            "author-dept-asset-major-minor-description",
            "author.dept.asset.major.minor.description"
        ])
        self.file_format_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        filepath_format_layout = QFormLayout()
        filepath_format_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
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
        self.file_format_output.setStyleSheet(self.display_label_big_text)

        self.file_exists_warning = QLabel()
        self.file_exists_warning.setStyleSheet(self.label_small_red_text)

        self.save_button = QPushButton("Save")
        self.save_button.setMaximumWidth(80)

        file_exists_and_save_hlayout = QHBoxLayout()
        file_exists_and_save_hlayout.addWidget(self.file_exists_warning)
        file_exists_and_save_hlayout.addWidget(self.save_button)
        # file_exists_and_save_hlayout.setAlignment(Qt.AlignRight)

        display_main_layout.addWidget(self.file_format_output)
        display_main_layout.addLayout(file_exists_and_save_hlayout)

        # -------------------------------Add sub layouts to main layouts-------------------------------
        self.main_layout = QVBoxLayout(self)
        
        self.main_layout.addWidget(cvrt_groupbox)
        self.main_layout.addWidget(input_groupbox)
        self.main_layout.addWidget(location_groupbox)
        self.main_layout.addWidget(display_groupbox)

    """'''''''''''''''''''''''''''''''signals_and_connections'''''''''''''''''''''''''''''''"""
    def signals_and_connections(self):
        """signals and connections for ui"""
        self.add_dept_button.clicked.connect(self.on_add_dept_button_clicked)
        self.filepath_input.textChanged.connect(self.refresh_file_format_display)
        self.filepath_input.textChanged.connect(self.refresh_input_details)

        # Whenever the user edits these widgets, re‐compute the filename:
        self.author_input.textChanged.connect(self.refresh_file_format_display)
        self.dept_input.currentIndexChanged.connect(self.refresh_file_format_display)
        self.gizmo_name_input.textChanged.connect(self.refresh_file_format_display)
        self.major_version_input.valueChanged.connect(self.refresh_file_format_display)
        self.minor_version_input.valueChanged.connect(self.refresh_file_format_display)
        self.disciption_input.textChanged.connect(self.refresh_file_format_display)
        self.file_format_input.currentIndexChanged.connect(self.refresh_file_format_display)

        self.cvrt_group_button.clicked.connect(self.convert_to_group)
        self.refresh_button.clicked.connect(self.refresh_input_details)
        self.Directory_path_button.clicked.connect(self.browse_folder)
        self.path_reset_button.clicked.connect(self.reset_folder_path)
        self.save_button.clicked.connect(self.on_save_clicked)

        # Set defaults
        self.author_input.setText(self.get_system_user())
        self.filepath_input.setText(self.get_default_nuke_directory())

    """'''''''''''''''''''''''''''''''convert_to_group'''''''''''''''''''''''''''''''"""
    def convert_to_group(self):
        """Converts the selected gizmo node to a Group node."""

        selected_nodes = nuke.selectedNodes()

        if len(selected_nodes) != 1:
            nuke.message("Please select exactly one Gizmo node.")
            return

        selected_node = selected_nodes[0]
        if not isinstance(selected_node, nuke.Gizmo):
            nuke.message("The selected node is not a Gizmo.")
            return

        try:
            gizmo_class_name = selected_node.Class()
            standardized_name = self.standardize_name_format(gizmo_class_name)
            gizmo_unique_name = self.generate_unique_name(standardized_name)

            group_node = selected_node.makeGroup()
            group_node.setSelected(True)
            group_node.knob("name").setValue(gizmo_unique_name)
            group_name = group_node.knob("name").value()

            #Assign UI details from the group name
            self.get_details_from_group_node(group_name)

            nuke.message(f"Gizmo successfully converted to Group: {group_name}")

        except Exception as e:
            nuke.message(f"Error converting Gizmo to Group: {e}")

    """'''''''''''''''''''''''''''''''generate_unique_name for convert group'''''''''''''''''''''''''''''''"""
    def generate_unique_name(self, base_name):
        """Generates a unique name by appending _groupX, X is a numbe"""
        index = 1
        unique_name = f"{base_name}_group{index}"
        while nuke.toNode(unique_name):
            index += 1
            unique_name = f"{base_name}_group{index}"

        return unique_name
    
    """'''''''''''''''''''''''''''''''Standardize name format for creating group'''''''''''''''''''''''''''''''"""
    def standardize_name_format(self, name):
        """Standardize the name by removing any text after major.minor version."""
        pattern = r"(.+?)[_\-\.](\d+)[_\-\.](\d+)"
        match = re.match(pattern, name)
        if match:
            base_name = f"{match.group(1)}_{match.group(2)}_{match.group(3)}"
            return base_name
        return name
    
    """'''''''''''''''''''''''''''''''load_departments_into_combo box'''''''''''''''''''''''''''''''"""
    def load_departments_into_combo(self):
        json_path = os.path.join(os.path.dirname(__file__), "departments.json")
        default_departments = ["comp", "roto", "key"]

        final_depts = list(default_departments)

        try:
            with open(json_path, "r") as f:
                user_depts = json.load(f)
                for dep in user_depts:
                    if dep not in final_depts:
                        final_depts.append(dep)
        except FileNotFoundError:
            pass

        self.dept_input.clear()
        self.dept_input.addItems(final_depts)

    """'''''''''''''''''''''''''''''''on_add_dept_button_clicked'''''''''''''''''''''''''''''''"""
    def on_add_dept_button_clicked(self):
        dialog = add_department_ui(parent=self)
        dialog.exec_()

        self.load_departments_into_combo()

    """'''''''''''''''''''''''''''''''extracting_group_node_name_details'''''''''''''''''''''''''''''''"""
    def extract_group_node_details(self, group_name):
        """
        Extract author, department, gizmo name, major, and minor versions from a group node name.
        """
        try:
            pattern = re.compile(
                r"^(?P<author>[a-zA-Z0-9]+)[_\-.]"
                r"(?P<department>[a-zA-Z0-9]+)[_\-.]"
                r"(?P<gizmo_name>[a-zA-Z0-9]+)[_\-.]"
                r"(?P<major>\d+)[_\-.]"
                r"(?P<minor>\d+)_group\d+$"
            )

            match = re.match(pattern, group_name)
            if match:
                return match.groupdict()
            
        except Exception:
            pass
        return None

    """'''''''''''''''''''''''''''''''finding_latest_gizmo_file'''''''''''''''''''''''''''''''"""
    def find_latest_gizmo_file(self, directory, department, gizmo_name):
        """
        Find the latest gizmo file matching the department and gizmo name in the directory.
        """
        latest_file = None
        latest_major = 1
        latest_minor = 0
        try:
            for file in os.listdir(directory):
                if file.endswith(".gizmo"):
                    details = self.extract_gizmo_details(file)
                    if details and details["department"] == department and details["gizmo_name"] == gizmo_name:
                        major = int(details["major"])
                        minor = int(details["minor"])

                        if (major > latest_major) or (major == latest_major and minor > latest_minor):
                            latest_file = file
                            latest_major = major
                            latest_minor = minor
        
        except Exception as e:
            nuke.message(f"Error finding latest gizmo file: {e}")

        return latest_file, latest_major, latest_minor

    """'''''''''''''''''''''''''''''''extracting name details from gizmo'''''''''''''''''''''''''''''''"""
    def extract_gizmo_details(self, file_name):
        """
        Extract details from gizmo file name, such as author, departmernt,
        gizmo name, major and minor virsion.
        """
        pattern = re.compile(
            r"^(?P<author>[a-zA-Z0-9]+)[_\-\.]"
            r"(?P<department>[a-zA-Z0-9]+)[_\-\.]"
            r"(?P<gizmo_name>[a-zA-Z0-9]+)[_\-\.]"
            r"(?P<major>\d+)[_\-\.]"
            r"(?P<minor>\d+)\.gizmo$"
        )

        file_match = pattern.match(file_name)
        if file_match:
            return file_match.groupdict()
        return None


    """'''''''''''''''''''''''''''''''get_details_from_group_node'''''''''''''''''''''''''''''''"""
    def get_details_from_group_node(self, group_name):
        """Get and assign the UI fields from the selected Group node."""
        try:
            #Extarct details from the group name
            details = self.extract_group_node_details(group_name)
            if not details:
                nuke.message("Invalid group name format.")
                return

            self.author_input.setText(details["author"])
            self.dept_input.setCurrentText(details["department"])
            self.gizmo_name_input.setText(details["gizmo_name"])

            self.major_version_input.setValue(int(details["major"]))
            self.minor_version_input.setValue(int(details["minor"]))

            # Find latest gizmo version
            direcory = self.get_default_nuke_directory()
            department = details["department"]
            gizmo_name = details["gizmo_name"]
            latest_file, latest_major, latest_minor = self.find_latest_gizmo_file(direcory, department, gizmo_name)

            self.file_format_output.setText(latest_file or "No existing file.")
            self.major_version_input.setValue(latest_major)
            self.minor_version_input.setValue(latest_minor)

        except Exception as e:
            nuke.message(f"Error getting details from group node: {e}")

    """'''''''''''''''''''''''''''''''format_gizmo_name'''''''''''''''''''''''''''''''"""
    def format_gizmo_name(self, details, ignore_description=False):
        """Format gizmo name for display and saving."""
        selected_format = self.file_format_input.currentText()

        author = details.get("author", "")
        dept   = details.get("department", "")
        asset  = details.get("gizmo_name", "")
        major  = details.get("major", "")
        minor  = details.get("minor", "")

        desc = ""
        if not ignore_description:
            desc = self.disciption_input.text().strip()

        def add_description(base_name, separator):
            if desc:
                return f"{base_name}{separator}{desc}"  
            else:
                return base_name

        if selected_format == "author_dept_asset_major_minor_description":
            name = f"{author}_{dept}_{asset}_{major}_{minor}"
            name = add_description(name, "_")
            return name + ".gizmo"

        elif selected_format == "author-dept-asset-major-minor-description":
            name = f"{author}-{dept}-{asset}-{major}-{minor}"
            name = add_description(name, "-")
            return name + ".gizmo"

        elif selected_format == "author.dept.asset.major.minor.description":
            name = f"{author}.{dept}.{asset}.{major}.{minor}"
            name = add_description(name, ".")
            return name + ".gizmo"

        name = f"{author}_{dept}_{asset}_{major}_{minor}"
        name = add_description(name, "_")
        return name + ".gizmo"

    """'''''''''''''''''''''''''''''''refresh_file_format_display'''''''''''''''''''''''''''''''"""
    def refresh_file_format_display(self):
        """
        Gather the needed details and call 'format_gizmo_name' to
        get the final filename, then update the label.
        """
        try:
            details = {
                "author":       self.author_input.text().strip(),
                "department":   self.dept_input.currentText().strip(),
                "gizmo_name":   self.gizmo_name_input.text().strip(),
                "major":        str(self.major_version_input.value()),
                "minor":        str(self.minor_version_input.value())
            }
            
            final_name = self.format_gizmo_name(details, ignore_description=False)
            self.file_format_output.setText(final_name)

            directory = self.filepath_input.text().strip()
            if not os.path.isdir(directory):
                directory = self.get_default_nuke_directory()

            full_path = os.path.join(directory, final_name)

            if os.path.isfile(full_path):
                self.file_exists_warning.setText("Gizmo already Exists in .nuke folder")
            else:
                self.file_exists_warning.setText("")

        except Exception as e:
            nuke.message(f"Error refreshing display: {e}")

    """'''''''''''''''''''''''''''''''refresh_input_details'''''''''''''''''''''''''''''''"""
    def refresh_input_details(self):
        """Refresh the input details based on the currently selected Group node."""
        try:
            selected_nodes = nuke.selectedNodes()
            is_group_selected = (
                len(selected_nodes) == 1 and
                selected_nodes[0].Class() == "Group"
            )

            if is_group_selected:
                group_node = selected_nodes[0]
                group_name = group_node.knob("name").value()
                self.get_details_from_group_node(group_name)
            else:
                if not self.author_input.text().strip():
                    self.author_input.setText(self.get_system_user())

                self.dept_input.setCurrentIndex(0)
                self.gizmo_name_input.clear()
                self.major_version_input.setValue(1)
                self.minor_version_input.setValue(0)
                self.file_exists_warning.setText("")

            directory = self.filepath_input.text().strip()
            if not os.path.isdir(directory):
                directory = self.get_default_nuke_directory()

            department = self.dept_input.currentText().strip()
            gizmo_name = self.gizmo_name_input.text().strip()

            latest_file, latest_major, latest_minor = self.find_latest_gizmo_file(
                directory, department, gizmo_name
            )

            if latest_file is None:
                self.major_version_input.setValue(1)
                self.minor_version_input.setValue(0)
            else:
                self.major_version_input.setValue(latest_major)
                self.minor_version_input.setValue(latest_minor)

            self.refresh_file_format_display()

        except Exception as e:
            nuke.message(f"Error refreshing input details: {e}")

    """'''''''''''''''''''''''''''''''refresh_input_details_if_group_selected'''''''''''''''''''''''''''''''"""
    def refresh_input_details_if_group_selected(self):
        try:
            selected_nodes = nuke.selectedNodes()

            if len(selected_nodes) == 1 and selected_nodes[0].Class() == "Group":
                group_node = selected_nodes[0]
                group_name = group_node.knob("name").value()
                self.get_details_from_group_node(group_name)

        except Exception as e:
            nuke.message(f"Error checking selected Group node: {e}")

    """''''''''''''''''''''''''''''''' on_save_clicked logic '''''''''''''''''''''''''''''"""
    def on_save_clicked(self):
        """
        If file already exists in the folder, pop up MajorMinorDialog.
        """
        try:
            selected_nodes = nuke.selectedNodes()
            if len(selected_nodes) != 1 or selected_nodes[0].Class() != "Group":
                nuke.message("Please select exactly one Group node.")
                return

            selected_node = selected_nodes[0]

            details = {
                "author":       self.author_input.text().strip(),
                "department":   self.dept_input.currentText().strip(),
                "gizmo_name":   self.gizmo_name_input.text().strip(),
                "major":        str(self.major_version_input.value()),
                "minor":        str(self.minor_version_input.value())
            }

            final_name = self.format_gizmo_name(details, ignore_description=False)

            directory = self.filepath_input.text().strip()
            if not os.path.isdir(directory):
                directory = self.get_default_nuke_directory()

            full_path = os.path.join(directory, final_name)

            if os.path.isfile(full_path):
                self.show_major_minor_dialog(details)
            else:
                self.export_group_as_gizmo(selected_node, full_path)

        except Exception as e:
            nuke.message(f"Error saving gizmo:\n{e}")

    """''''''''''''''''''''''''''''''' save_group_as_gizmo '''''''''''''''''''''''''''''"""
    def export_group_as_gizmo(self, group_node, full_path):
        """
        Exports the given group_node to 'full_path' as a .gizmo 
        by using nuke.nodeCopy under the hood. 
        """
        selected_nodes = nuke.selectedNodes()

        if len(selected_nodes) != 1:
            nuke.message("Please select exactly one Group node.")
            return

        group_node = selected_nodes[0]
        if group_node.Class() != "Group":
            nuke.message("Please select a valid Group node.")
            return

        try:
            for node in selected_nodes:
                node.setSelected(False)
            group_node.setSelected(True)

            nuke.nodeCopy(full_path)

            base, extention = os.path.splitext(full_path)
            if extention.lower() != ".gizmo":
                new_path = base + ".gizmo"
                os.rename(full_path, new_path)
                full_path = new_path

            nuke.message(f"Group node exported to:\n{full_path}")

        except Exception as e:
            nuke.message(f"Error exporting as gizmo:\n{e}")

        finally:
            group_node.setSelected(True)

    """''''''''''''''''''''''''''''''' show_major_minor_dialog '''''''''''''''''''''''''''''"""
    def show_major_minor_dialog(self, details):
        """
        Builds the next major/minor filenames,
        """
        current_major = self.major_version_input.value()
        current_minor = self.minor_version_input.value()

        major_details = details.copy()
        major_details["major"] = str(current_major + 1)
        major_details["minor"] = "0"
        major_file_name = self.format_gizmo_name(major_details, ignore_description=True)

        minor_details = details.copy()
        minor_details["major"] = str(current_major)
        minor_details["minor"] = str(current_minor + 1)
        minor_file_name = self.format_gizmo_name(minor_details, ignore_description=True)

        dialog = MajorMinorDialog(major_file_name, minor_file_name, parent=self)
        dialog.exec_()

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

        try:
            current_path = self.filepath_input.text()

            if not os.path.isdir(current_path):
                current_path = self.get_default_nuke_directory()

            folder_path = QFileDialog.getExistingDirectory(self, "Select Save Directory", current_path)

            if folder_path:
                self.filepath_input.setText(folder_path)
                self.refresh_input_details()
                self.refresh_file_format_display() 

        except Exception as e:
            nuke.message(f"Error selecting directory: {e}")

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


