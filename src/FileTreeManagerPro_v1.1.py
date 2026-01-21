import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import zipfile
import tempfile

# --- File Templates ---
TEMPLATES = {
    ".py": '"""Auto-generated Python file"""\n\nif __name__ == "__main__":\n    pass\n',
    ".json": '{}\n',
    ".md": '# New Document\n',
    ".rst": '# New RST Document\n',
    ".sh": '#!/bin/bash\n\n# Auto-generated shell script\n',
    ".yml": '# Auto-generated YAML file\n',
    ".qss": '/* Auto-generated QSS file */\n',
    ".txt": '# Auto-generated text file\n',
    ".ipynb": '# Auto-generated Jupyter Notebook\n'
}

# --- Preset Templates ---
PRESETS = {
    "Top-Level Structure": """project_name/
├── .gitignore
├── README.md
├── LICENSE.md
├── pyproject.toml
├── setup.cfg
├── setup.py
├── venv/
└── src/""",
    "Internal Package Structure (src/)": """src/
└── project_name/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── utils.py
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   └── product.py
    ├── api/
    │   ├── __init__.py
    │   └── routes.py
    └── cli.py""",
    "Testing Directory (tests/)": """project_name/
└── tests/
    ├── __init__.py
    ├── test_core.py
    ├── test_api.py
    └── conftest.py""",
    "Other Directories (docs/, scripts/, data/)": """project_name/
├── docs/
│   ├── index.rst
│   └── conf.py
├── scripts/
│   ├── install.sh
│   └── deploy.py
└── data/
    ├── raw/
    └── processed/""",
    "pip-installable Package with CLI": """my_package_project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── pyproject.toml
├── README.md
├── LICENSE.md
├── requirements.txt
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── core.py
│       ├── utils.py
│       └── models/
│           ├── __init__.py
│           └── data_models.py
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_core.py
    └── conftest.py""",
    "Project with CLI and GUI": """my_package_project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── pyproject.toml
├── README.md
├── LICENSE.md
├── requirements.txt
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── logic.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── commands.py
│       └── gui/
│           ├── __init__.py
│           ├── main_window.py
│           ├── widgets.py
│           └── assets/
│               ├── icon.png
│               └── style.qss
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_core.py
    ├── test_gui.py
    └── conftest.py""",
    "Standard CLI Project": """my_cli_app_project/
├── .gitignore
├── pyproject.toml
├── README.md
├── LICENSE.md
├── requirements.txt
├── src/
│   └── my_cli_app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── core/
│           ├── __init__.py
│           ├── logic.py
│           └── utils.py
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_core.py
    └── conftest.py""",
    "Minimal Microservice / API-Only Structure": """simple_api_project/
├── .gitignore
├── pyproject.toml
├── README.md
├── LICENSE.md
├── requirements.txt
├── src/
│   └── simple_api/
│       ├── __init__.py
│       └── routes.py
├── run.py
└── tests/
    ├── test_routes.py
    └── conftest.py""",
    "Library with Plugin Architecture": """plugin_library_project/
├── README.md
├── pyproject.toml
├── src/
│   └── pluginlib/
│       ├── __init__.py
│       ├── core.py
│       ├── cli.py
│       └── plugins/
│           ├── __init__.py
│           ├── plugin_foo.py
│           └── plugin_bar.py
└── tests/
    ├── test_core.py
    ├── test_plugins.py
    └── conftest.py""",
    "Data Science / Analysis Workflow": """data_insights_project/
├── README.md
├── pyproject.toml
├── environment.yml
├── notebooks/
│   ├── exploration.ipynb
│   └── modeling.ipynb
├── src/
│   └── analysis/
│       ├── __init__.py
│       ├── preprocessing.py
│       ├── train.py
│       └── visualize.py
├── data/
│   ├── raw/
│   └── cleaned/
└── tests/
    ├── test_train.py
    └── test_preprocessing.py""",
    "Security-Focused or Encryption Library": """securex_project/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── securex/
│       ├── __init__.py
│       ├── crypto/
│       │   ├── __init__.py
│       │   ├── encrypt.py
│       │   └── decrypt.py
│       └── auth/
│           ├── __init__.py
│           └── login.py
└── tests/
    ├── test_encrypt.py
    ├── test_auth.py
    └── conftest.py"""
}

class FileTreeManagerGUI:
    def __init__(self, master):
        self.master = master
        master.title("FileTree Manager")
        master.geometry("900x800")
        master.resizable(True, True)

        # Dark mode state
        self.dark_mode = False
        self.bg_light = "SystemButtonFace"
        self.fg_light = "#000000"
        self.bg_dark = "#2e2e2e"
        self.fg_dark = "#ffffff"

        # Configure grid weights
        master.grid_rowconfigure(0, weight=0)  # Menu bar
        master.grid_rowconfigure(1, weight=0)  # Input frame
        master.grid_rowconfigure(2, weight=0)  # Listbox label
        master.grid_rowconfigure(3, weight=1)  # Listbox
        master.grid_rowconfigure(4, weight=0)  # Tabbed interface
        master.grid_rowconfigure(5, weight=1)  # Output area
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=0)

        # Menu bar
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)
        presets_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Presets", menu=presets_menu)
        for preset_name in PRESETS:
            presets_menu.add_command(
                label=preset_name,
                command=lambda name=preset_name: self._load_preset(name)
            )
        self.menu_bar.add_command(label="Toggle Dark Mode", command=self._toggle_dark_mode)
        self.menu_bar.add_command(label="Save Preset", command=self._save_preset)
        self.menu_bar.add_command(label="Load Preset", command=self._load_preset_file)

        # Input Frame (Directory Selection)
        self.input_frame = tk.LabelFrame(master, text="Select Root Directory", padx=10, pady=10)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)

        self.directory_label = tk.Label(self.input_frame, text="Selected Directory:")
        self.directory_label.grid(row=0, column=0, sticky="w", pady=5)
        self.directory_entry = tk.Entry(self.input_frame, width=70)
        self.directory_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.directory_entry.insert(0, os.path.expanduser("~") if os.name == 'posix' else os.getcwd())
        self.browse_button = tk.Button(self.input_frame, text="Browse", command=self._browse_directory)
        self.browse_button.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        # Items to Include Listbox
        self.include_label = tk.Label(master, text="Items to Include (Select multiple with Ctrl/Shift):")
        self.include_label.grid(row=2, column=0, sticky="nw", padx=10, pady=(0, 5))
        self.file_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, height=10)
        self.file_listbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.listbox_scrollbar = tk.Scrollbar(master, command=self.file_listbox.yview)
        self.listbox_scrollbar.grid(row=3, column=1, sticky="ns", pady=(0, 10))
        self.file_listbox['yscrollcommand'] = self.listbox_scrollbar.set

        # Tabbed Interface
        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Tree Generation Tab
        self.tree_tab = tk.Frame(self.notebook)
        self.notebook.add(self.tree_tab, text="Generate Tree")
        self.generate_button = tk.Button(self.tree_tab, text="Generate Tree Diagram", command=self._generate_tree)
        self.generate_button.pack(pady=10)

        # Tree Editing/Building Tab
        self.build_tab = tk.Frame(self.notebook)
        self.notebook.add(self.build_tab, text="Edit & Build Tree")
        self.build_tab.grid_rowconfigure(0, weight=0)
        self.build_tab.grid_rowconfigure(1, weight=1)
        self.build_tab.grid_rowconfigure(2, weight=0)
        self.build_tab.grid_rowconfigure(3, weight=1)
        self.build_tab.grid_columnconfigure(0, weight=1)

        tk.Label(self.build_tab, text="Edit Directory Tree:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.text_input = scrolledtext.ScrolledText(self.build_tab, width=80, height=15)
        self.text_input.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.text_input.bind("<KeyRelease>", self._update_preview)

        tk.Label(self.build_tab, text="Live Preview:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.preview = scrolledtext.ScrolledText(self.build_tab, width=80, height=10, state="normal")
        self.preview.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        self.btn_frame = tk.Frame(self.build_tab)
        self.btn_frame.grid(row=4, column=0, pady=10)
        tk.Button(self.btn_frame, text="Build Structure", command=self._build_structure).grid(row=0, column=0, padx=5)
        tk.Button(self.btn_frame, text="Export Tree as Zip", command=self._export_zip).grid(row=0, column=1, padx=5)

        # Output Area
        self.output_label = tk.Label(master, text="Output Log:")
        self.output_label.grid(row=5, column=0, sticky="nw", padx=10, pady=(10, 0))
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15, width=100)
        self.output_text.grid(row=6, column=0, sticky="nsew", padx=10, pady=(5, 10), columnspan=2)
        self.output_scrollbar = tk.Scrollbar(master, command=self.output_text.yview)
        self.output_scrollbar.grid(row=6, column=2, sticky="ns", pady=(5, 10))
        self.output_text['yscrollcommand'] = self.output_scrollbar.set

        # Configure output text tags
        self.output_text.tag_config("dir", foreground="blue", font=("TkDefaultFont", 9, "bold"))
        self.output_text.tag_config("file", foreground="green")
        self.output_text.tag_config("error", foreground="red", font=("TkDefaultFont", 9, "bold"))
        self.output_text.tag_config("info", foreground="gray")

        self._log_message("Welcome to FileTree Manager. Select a directory to load its contents.\n", "info")

    def _log_message(self, message, tag="normal"):
        self.output_text.insert(tk.END, message, tag)
        self.output_text.see(tk.END)

    def _toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = self.bg_dark if self.dark_mode else self.bg_light
        fg = self.fg_dark if self.dark_mode else self.fg_light
        self.master.configure(bg=bg)
        for widget in [self.input_frame, self.directory_label, self.directory_entry, self.browse_button,
                       self.include_label, self.file_listbox, self.output_label, self.output_text,
                       self.generate_button, self.tree_tab, self.build_tab, self.btn_frame, self.preview]:
            try:
                widget.configure(bg=bg, fg=fg, insertbackground=fg)
            except:
                pass
        self.text_input.configure(bg=bg, fg=fg, insertbackground=fg)
        self.notebook.configure(style="TNotebook")

    def _browse_directory(self):
        initial_dir = self.directory_entry.get() if os.path.isdir(self.directory_entry.get()) else os.getcwd()
        selected_directory = filedialog.askdirectory(parent=self.master, initialdir=initial_dir, title="Select Directory")
        if selected_directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, selected_directory)
            self._log_message(f"Selected root: {selected_directory}\n", "info")
            self._populate_listbox(selected_directory)
        else:
            self._log_message("Directory selection cancelled.\n", "info")

    def _populate_listbox(self, directory_path):
        self.file_listbox.delete(0, tk.END)
        try:
            items = sorted(os.listdir(directory_path))
            for item in items:
                full_path = os.path.join(directory_path, item)
                self.file_listbox.insert(tk.END, f"{item}/" if os.path.isdir(full_path) else item)
            for i in range(self.file_listbox.size()):
                self.file_listbox.selection_set(i)
            self._log_message(f"Loaded {len(items)} items from '{os.path.basename(directory_path)}'.\n", "info")
        except PermissionError:
            self._log_message(f"ERROR: Permission denied to access '{directory_path}'.\n", "error")
            messagebox.showerror("Permission Error", f"Permission denied to access '{directory_path}'.")
        except Exception as e:
            self._log_message(f"ERROR: Failed to load directory contents: {e}\n", "error")
            messagebox.showerror("Error", f"Failed to load directory contents: {e}")

    def _generate_tree(self):
        self.output_text.delete(1.0, tk.END)
        directory_path = self.directory_entry.get().strip()
        if not directory_path or not os.path.isdir(directory_path):
            messagebox.showerror("Error", "Please select a valid root directory.")
            self._log_message(f"ERROR: Invalid root directory: {directory_path}\n", "error")
            return
        selected_indices = self.file_listbox.curselection()
        selected_items = [self.file_listbox.get(i).strip('/') for i in selected_indices] if selected_indices else []
        if not selected_items:
            messagebox.showwarning("Warning", "No items selected. The tree will be empty except for the root.")
            self._log_message("WARNING: No items selected for tree generation.\n", "info")
        self._log_message(f"Generating tree for selected items in: {directory_path}\n", "info")
        tree_string = self._build_filtered_tree_string(directory_path, selected_items)
        self.output_text.insert(tk.END, tree_string)
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(tk.END, tree_string)
        self._update_preview()
        self._log_message("\nTree generation complete.\n", "info")

    def _build_filtered_tree_string(self, root_dir, selected_top_level_items):
        tree_lines = [f"{os.path.basename(root_dir)}/"]
        sorted_selected_items = sorted(selected_top_level_items, 
                                      key=lambda x: (not os.path.isdir(os.path.join(root_dir, x)), x.lower()))
        for i, item_name in enumerate(sorted_selected_items):
            full_item_path = os.path.join(root_dir, item_name)
            is_last_item = (i == len(sorted_selected_items) - 1)
            self._recursive_add_to_tree(tree_lines, full_item_path, 0, [], is_last_item)
        return "\n".join(tree_lines)

    def _recursive_add_to_tree(self, tree_lines, current_path, level, parent_vertical_lines, is_last_sibling):
        indent_parts = ["    " if is_parent_last else "│   " for is_parent_last in parent_vertical_lines]
        current_prefix = '└── ' if is_last_sibling else '├── '
        indent_str = "".join(indent_parts) + current_prefix
        item_name = os.path.basename(current_path)
        if os.path.isdir(current_path):
            tree_lines.append(f"{indent_str}{item_name}/")
            new_parent_vertical_lines = list(parent_vertical_lines)
            new_parent_vertical_lines.append(is_last_sibling)
            try:
                children = sorted(os.listdir(current_path))
                child_dirs = sorted([d for d in children if os.path.isdir(os.path.join(current_path, d))])
                child_files = sorted([f for f in children if os.path.isfile(os.path.join(current_path, f))])
                all_children_sorted = child_dirs + child_files
                for i, child_name in enumerate(all_children_sorted):
                    child_path = os.path.join(current_path, child_name)
                    is_last_child_sibling = (i == len(all_children_sorted) - 1)
                    self._recursive_add_to_tree(tree_lines, child_path, level + 1, new_parent_vertical_lines, is_last_child_sibling)
            except PermissionError:
                tree_lines.append(f"{indent_str}    <Permission Denied>")
            except Exception as e:
                tree_lines.append(f"{indent_str}    <Error: {e}>")
        else:
            tree_lines.append(f"{indent_str}{item_name}")

    def _parse_tree(self, tree_text):
        lines = tree_text.strip().splitlines()
        path_stack = []
        paths = []
        for line in lines:
            clean = line.lstrip("│├└─ ")
            indent = len(line) - len(clean)
            level = indent // 4
            while len(path_stack) > level:
                path_stack.pop()
            is_dir = clean.endswith("/")
            name = clean.rstrip("/") if not is_dir else clean
            path_stack.append(name)
            full_path = os.path.join(*path_stack)
            paths.append((full_path, is_dir))
        return paths

    def _update_preview(self, event=None):
        try:
            paths = self._parse_tree(self.text_input.get("1.0", tk.END))
            self.preview.delete("1.0", tk.END)
            for path, is_dir in paths:
                tag = "[DIR]" if is_dir else "[FILE]"
                self.preview.insert(tk.END, f"{tag} {path}\n")
        except:
            self.preview.delete("1.0", tk.END)
            self.preview.insert(tk.END, "⚠️ Invalid tree format")

    def _build_structure(self):
        tree_text = self.text_input.get("1.0", tk.END)
        if not tree_text.strip():
            messagebox.showwarning("Input Needed", "Please paste or generate a directory tree.")
            return
        dest_dir = filedialog.askdirectory(title="Choose Destination Folder")
        if not dest_dir:
            return
        try:
            paths = self._parse_tree(tree_text)
            for path, is_dir in paths:
                full_path = os.path.join(dest_dir, path)
                if is_dir:
                    os.makedirs(full_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    ext = os.path.splitext(full_path)[1]
                    content = TEMPLATES.get(ext, "")
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
            messagebox.showinfo("🎉 Success", "Structure created successfully!")
            self._log_message("Structure created successfully.\n", "info")
        except Exception as e:
            self._log_message(f"ERROR: Failed to build structure: {e}\n", "error")
            messagebox.showerror("Error", str(e))

    def _export_zip(self):
        tree_text = self.text_input.get("1.0", tk.END)
        if not tree_text.strip():
            messagebox.showwarning("Input Needed", "Please paste or generate a directory tree.")
            return
        zip_path = filedialog.asksaveasfilename(defaultextension=".zip")
        if not zip_path:
            return
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                paths = self._parse_tree(tree_text)
                for path, is_dir in paths:
                    full_path = os.path.join(temp_dir, path)
                    if is_dir:
                        os.makedirs(full_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        ext = os.path.splitext(full_path)[1]
                        content = TEMPLATES.get(ext, "")
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(content)
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root_dir, _, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root_dir, file)
                            arcname = os.path.relpath(file_path, start=temp_dir)
                            zipf.write(file_path, arcname)
            messagebox.showinfo("📦 Exported", f"Tree structure zipped to:\n{zip_path}")
            self._log_message(f"Tree structure zipped to: {zip_path}\n", "info")
        except Exception as e:
            self._log_message(f"ERROR: Failed to export zip: {e}\n", "error")
            messagebox.showerror("Error", str(e))

    def _save_preset(self):
        content = self.text_input.get("1.0", tk.END)
        file = filedialog.asksaveasfilename(defaultextension=".tree")
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)
            self._log_message(f"Preset saved to: {file}\n", "info")

    def _load_preset_file(self):
        file = filedialog.askopenfilename(filetypes=[("Tree Files", "*.tree")])
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, f.read())
            self._update_preview()
            self._log_message(f"Preset loaded from: {file}\n", "info")

    def _load_preset(self, preset_name):
        tree_text = PRESETS.get(preset_name, "")
        if tree_text:
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, tree_text)
            self._update_preview()
            self._log_message(f"Loaded preset: {preset_name}\n", "info")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTreeManagerGUI(root)
    root.mainloop()