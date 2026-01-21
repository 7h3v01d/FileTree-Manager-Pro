# FileTree Manager Pro (v1.1)

️ **LICENSE & USAGE NOTICE — READ FIRST**

This repository is **source-available for private technical evaluation and testing only**.

- ❌ No commercial use  
- ❌ No production use  
- ❌ No academic, institutional, or government use  
- ❌ No research, benchmarking, or publication  
- ❌ No redistribution, sublicensing, or derivative works  
- ❌ No independent development based on this code  

All rights remain exclusively with the author.  
Use of this software constitutes acceptance of the terms defined in **LICENSE.txt**.

---

## Key Features

- Bidirectional Workflow:
- Generate: Scan an existing folder and turn it into a clean, text-based tree diagram.
- Build: Paste or write a tree diagram (e.g., from documentation or AI) and instantly create that entire folder and file structure on your hard drive.
- Smart File Templating: When building a structure, the manager automatically populates files with relevant boilerplate code based on their extension (supporting .py, .json, .md, .sh, .yml, .qss, .ipynb, and more).
- Built-in Project Presets: Includes a library of industry-standard project structures, including:
  - Data Science / Analysis Workflows.
  - Pip-installable Packages with CLI and GUI.
  - Security-focused Encryption Libraries.
  - Microservice / API-only structures.
- Export to Zip: Design your structure in the app and export it directly as a .zip file, perfect for sharing project boilerplates with teammates.
- Live Preview & Editing: A dedicated "Edit & Build" tab with a live preview engine that validates your tree format as you type.
- Custom Preset Management: Save your own custom project architectures as .tree files and reload them whenever you start a new project.
- Dark Mode Support: A fully integrated Dark Mode toggle for a more comfortable developer experience.

---

## Installation

#### Prerequisites ####
- Python 3.x
- Tkinter: Standard with most Python installs.

### Setup
Clone this repository:
```Bash
git clone https://github.com/yourusername/filetree-manager-pro.git
cd filetree-manager-pro
```
Usage
Run the manager using:
```Bash
python FileTreeManagerPro_v1.1.py
```

### Designing and Building a Project

1. Load a Preset: Use the Presets menu to select a starting point (e.g., "Standard CLI Project").
2. Customize: Edit the tree in the Edit & Build Tree tab. The Live Preview will show you exactly what will be created.
3. Build: Click Build Structure to select a destination folder. The app will create all directories and fill files with standard boilerplate code.
4. Export: Alternatively, click Export Tree as Zip to save the entire structure as a compressed archive.

### Boilerplate Templates
The manager includes intelligent templates for common file types:

- Python (.py): Includes a docstring and if __name__ == "__main__": block.
- Shell (.sh): Includes a #!/bin/bash shebang.
- JSON (.json): Pre-populated with an empty object {}.
- Markdown (.md): Includes a placeholder header.

## Project Structure
***FileTreeManagerPro_v1.1.py***: The main application containing the UI, the tree parser, and the file system deployment engine.

## Contribution Policy

Feedback, bug reports, and suggestions are welcome.

You may submit:

- Issues
- Design feedback
- Pull requests for review

However:

- Contributions do not grant any license or ownership rights
- The author retains full discretion over acceptance and future use
- Contributors receive no rights to reuse, redistribute, or derive from this code

---

## License
This project is not open-source.

It is licensed under a private evaluation-only license.
See LICENSE.txt for full terms.
