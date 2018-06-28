# PaletteFile
A Sublime Text plugin to provide file/folder creating functionality from the Command Palette with a hierarchical or flattened view of the project directories.

*Currently tested only on Windows, but will be testing on Linux very soon.*

*If you would be interested in testing it on OSX, that would be much appreciated, so feel free to get in touch.*

![Sublime Text 3 PaletteFile demo - Creating files and folders from the Command Palette](https://user-images.githubusercontent.com/10420664/41960346-6cd7a250-79e7-11e8-8882-ba335bdd63b5.gif)

## Installation
As it is still early days for this plugin, it is not yet added to the Package Control repo, but it will be very soon.

In the meantime, you can get it by navigating to your [packages directory](http://docs.sublimetext.info/en/sublime-text-3/basic_concepts.html#the-data-directory) and cloning the repo

```git clone https://github.com/vshotarov/PaletteFile.git```

## Usage
Fire up your command palette (**Ctrl + Shift + P**) and type *Palette File* to see all available actions.

The following four commands are provided, which can also be assigned to hotkeys in your key bindings file.

| Command                      | Title in command palette                  |
| ---------------------------- |:-----------------------------------------:|
| `new_file_in_project_tree`   | PaletteFile: New file in project (tree)   |
| `new_folder_in_project_tree` | PaletteFile: New folder in project (tree) |
| `new_file_in_project_flat`   | PaletteFile: New file in project (flat)   |
| `new_folder_in_project_flat` | PaletteFile: New folder in project (flat) |
