# TNT Gizmo Saver Documentation

## Project Description
The **TNT Gizmo Saver** is a Python-based tool developed for Nuke users to streamline the creation, management, and saving of Gizmo nodes. By automating tasks such as naming, version control, and metadata entry, the tool promotes consistency and efficiency while minimizing manual effort. It is designed to ensure professional-grade asset management practices with features like duplicate file handling and incremental version updates.

## Goal of the Project
The primary objective of the TNT Gizmo Saver is to:

- Automate and standardize the process of creating and saving Gizmo nodes.
- Enforce uniform naming conventions and version tracking.
- Simplify metadata management for enhanced collaboration and organization.
- Provide an intuitive interface that reduces repetitive tasks and errors.

## Key Benefits

### 1. Consistency

- Ensures uniform naming formats and metadata standards across all Gizmos.
- Promotes adherence to organizational workflows and guidelines.

### 2. Time-Saving

- Automates repetitive and mundane tasks to boost productivity.
- Allows artists to focus more on creative aspects rather than administrative tasks.

### 3. Version Control

- Provides structured management of major and minor updates.
- Prevents overwriting by offering intuitive handling of duplicate file names.

### 4. Metadata Management

- Enables the inclusion of crucial metadata like author, department, version, and descriptions.
- Enhances collaboration and transparency across teams.

### 5. Error Handling

- Detects duplicate file names and offers options for creating major or minor version updates.
- Provides clear and actionable feedback to users.

## How It Works

### 1. Input Details

Users provide details such as:

- **Author Name:** Automatically fetched or manually entered.
- **Department:** Selected from a pre-defined list or custom-added.
- **Gizmo Name:** Unique identifier for the Gizmo.
- **Version Numbers:** Major and minor versions.
- **Description:** Additional metadata for context.

### 2. Set Save Location

- Specify a folder path where the Gizmo will be saved.
- Default save location is the user's `.nuke` directory.

### 3. Handle Duplicates

- If a file with the same name exists, the tool prompts the user to:
  - Save as a new **major** version.
  - Save as a new **minor** version.

### 4. Save Gizmo

- Save the Gizmo with a structured naming convention based on the provided details.
- Automatically includes metadata for better organization.

### 5. Confirmation

- Displays a success message after saving the Gizmo.
- For duplicates, notifies users about the incremental updates made.

## Step-by-Step Usage

1. **Launch the Tool:** Open the TNT Gizmo Saver interface within Nuke.
2. **Provide Input Details:** Fill in fields such as author, department, Gizmo name, and version numbers. Optionally add a description.
3. **Select Save Location:** Either accept the default path or browse to choose a specific folder.
4. **Preview File Name:** View the generated file name based on the input and formatting settings.
5. **Handle Duplicates:** If a duplicate is detected, decide between creating a major or minor version update.
6. **Save the Gizmo:** Click "Save" to export the Gizmo to the specified location. Confirm success or resolve any issues with clear prompts from the tool.

## Advanced Features

### Convert Gizmos to Groups

- Easily convert selected Gizmo nodes into Group nodes.
- Automatically extracts naming details and updates the interface.

### Department Management

- Add, remove, or reorder departments within the tool.
- Save custom department lists for future use.

### Flexible Naming Conventions

- Choose from multiple naming formats (e.g., underscores, hyphens, or dots).
- Preview the formatted file name in real time.

### Metadata Extraction

- Extract author, department, Gizmo name, and version details from existing nodes for easy editing and reuse.

## Error Handling

- **Invalid Input:** Alerts users to missing or incorrect information.
- **Duplicate Files:** Prompts for creating new versions instead of overwriting.
- **Invalid Node Selection:** Ensures only valid Gizmo or Group nodes are processed.
- **File Save Issues:** Provides detailed error messages for troubleshooting.

