# PaletteFile
A Sublime Text plugin to provide file/folder creating functionality from the Command Palette with a hierarchical or flattened view of the project directories.

*Currently tested only on Windows and Linux.*

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

The *tree* options will let you traverse your project's hierarchy up and down until you find the desired location of your new file/folder. Because all this is happening inside of the Command Palette you can take advantage of the excellent fuzzy searching support in Sublime. Once you accept a directory, the input panel pops up asking for you to type the name.

The *flat* options presents you with a flattened version of your project hierarchy, where you can start typing the relative directory you want to create your file/folder in and quickly reach it. Similar to the *tree* option, once a choice has been made, the input panel pops up asking for a name.

## Settings
The following four settings are available:

- `parent_directory_command` - The title of the command for going UP a level when traversing the tree. The default is `..`.
- `this_directory_command` - The title of the command for choosing the current directory when traversing the tree. The default is `<here>`.
- `top_level_message` - The message underneath the title of the command for going UP in the hierarchy, if the parent directory is the project's top level folders. The default is `Current top level folders`.
- `flat_exclude_folders` - Folders to be excluded in the flattened lists of directories. The default is `[".git", "venv"]`.

## Issues and contributing
If you find any issues with the plugin please feel free to open an issue or get in touch with me.

Better yet, if you are keen on fixing problems yourself, feel free to submit a pull request.
