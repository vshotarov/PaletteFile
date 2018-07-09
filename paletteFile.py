'''A plugin to provide file/folder creating functionality from the Command 
Palette with hierarchy traversing or flattened view of the hierarchy.
'''
import sublime
import sublime_plugin

import os


def _get_setting(setting):
    '''Returns the queried setting from the collapsed list of settings.

    By using the active view's settings we make sure that the project
    specific settings take priority over the plugin specific settings.

    Args:
        setting: The name of the setting which is being queried.

    Returns:
        The value of the setting or None if it's not found
        string or NoneType
    '''
    plugin_settings = sublime.load_settings("PaletteFile.sublime-settings")
    view_settings = sublime.active_window().active_view().settings()

    return view_settings.get(setting, plugin_settings.get(setting))


def _create_path(name, pathType, chosen_directory, window):
    '''Creates a file or folder {pathType} with the specified {name} in the
    {chosen_directory}.

    Args:
        name: The last portion of the path - the name of the file or folder
        pathType: The type of path being created - file or directory
        chosen_directory: The parent directory of the file or folders
        window: The sublime Window object from the WindowCommand
    '''
    full_path = os.path.join(chosen_directory, name)

    try:
        if pathType == "file":
            with open(full_path, "x"):
                pass
            window.open_file(full_path)
        else:
            os.makedirs(full_path, exist_ok=False)

        window.status_message("Created " + full_path)
    except FileExistsError:
        sublime.error_message("%s %s already exists." % (
            pathType.capitalize(), full_path.capitalize()))
    except PermissionError:
        sublime.error_message("Cannot write to " +
                              full_path + ". Check access permissions.")
    except OSError:
        sublime.error_message("Cannot write to " + full_path + "." +
                              "The path may be invalid.")


class _HierarchyTraverse():
    '''Provides traversal options for a hierarchy of directories,
    so they can be walked as a tree.
    '''

    def __init__(self, window, on_done):
        '''Initializes the traversal object.

        Args:
            window: The sublime window instance
            on_done: The function to be called on accepting a path
        '''
        self.window = window
        self.on_done = on_done

        self.top_folders = self.window.folders()

        self.current_path = ""
        self.chosen_directory = None

        self.set_top_level_directories()

    def run(self):
        '''Creates the panel with the top level folders.'''
        self.show_panel()

    def parent_path(self):
        '''Returns the directory one level up from the current one.

        Returns:
            Parent directory
            string
        '''
        return os.path.split(self.current_path)[0] if self.current_path else ""

    def set_top_level_directories(self):
        '''Sets the current available directories to the top folders of the 
        project.'''
        self.directories = [
            [os.path.split(folder)[1], folder] for folder in self.top_folders]

    def set_directories(self, directories):
        '''Sets the specified directories as options in the command palette.

        The options available are as follows:
        - the parent directory if the current one is not already a top level
        directory
        - this directory
        - all available children directories

        Args:
            directories: The directories in the current level of the hierarchy.
        '''
        if self.current_path not in self.top_folders:
            parent_directory = [
                [_get_setting("parent_directory_command"), self.parent_path()]]
        else:
            parent_directory = [
                [_get_setting("parent_directory_command"),
                 _get_setting("top_level_message")]]

        this_directory = [
            [_get_setting("this_directory_command"), self.current_path]]

        self.directories = parent_directory + this_directory + directories

    def show_panel(self):
        '''A wrapper around Sublime's show_quick_panel to automatically grab
        the correct data from this class.'''
        self.window.show_quick_panel(self.directories, self.on_choice)

    def on_choice(self, choice):
        '''Called once either a choice has been made in the command palette or 
        it has been dismissed.

        If the current directory has been chosen, then we close the panel and 
        move on to specifying the name of the new file/directory using the
        on_accept function.

        Otherwise, we keep traversing the tree, using the specified choice
        for navigating.

        Args:
            choice: The choice that has been made in the quick_panel as an int
            value.
        '''
        if choice < 0:
            return

        chosen_command, chosen_directory = self.directories[choice]

        if chosen_command == _get_setting("this_directory_command"):
            self.on_accept(chosen_directory)
            return

        if not chosen_directory == _get_setting("top_level_message"):
            directories = []
            for each in os.listdir(chosen_directory):
                full_path = os.path.join(chosen_directory, each)
                if os.path.isdir(full_path):
                    directories.append([each, full_path])

            self.current_path = chosen_directory
            self.set_directories(directories)
        else:
            self.current_path = ""
            self.set_top_level_directories()

        self.show_panel()

    def on_accept(self, directory):
        '''Once a directory has been chosen, we call Sublime's show_input_panel
        to type the name of the new file/folder.

        Once the name is specified, the on_done function is ran, which is
        not implemented in the class, but is assigned from outside in order
        to implement the correct functionality for the specific task, meaning
        either creating a folder or a file.

        Args:
            directory: The chosen directory from the quick panel.
        '''
        self.chosen_directory = directory
        self.window.show_input_panel(os.path.join(directory, ""),
                                     "", self.on_done, None, None)


class NewFileInProjectTree(sublime_plugin.WindowCommand):
    '''This class creates the "New file in project (tree)" command.

    Invoking this command the user is presented with a panel in the command
    palette, containing all the top level folders of the project. The user
    can traverse up and down their hierarchies and settle on a location
    for creating the new file in.
    '''

    def run(self, *args):
        '''Initializes the _HierarchyTraverse object and runs it.

        The on_done method is passed as the function that's called once a 
        choice has been made in the panel.

        This function is called when the user invokes the command.
        '''
        traverseObj = self.hierarchy_traverse = _HierarchyTraverse(
            self.window, self.on_done)
        traverseObj.run()

    def on_done(self, fileName):
        '''Creates the file with the path that has been chosen in the
        _HieararchyTraverse object.

        Args:
            fileName: The name of the file to be created.
        '''
        _create_path(fileName, "file",
                     self.hierarchy_traverse.chosen_directory, self.window)


class NewFolderInProjectTree(sublime_plugin.WindowCommand):
    '''This class creates the "New file in project (tree)" command.

    Invoking this command the user is presented with a panel in the command
    palette, containing all the top level folders of the project. The user
    can traverse up and down their hierarchies and settle on a location
    for creating the new folder in.
    '''

    def run(self, *args):
        '''Initializes the _HierarchyTraverse object and runs it.

        The on_done method is passed as the function that's called once a 
        choice has been made in the panel.

        This function is called when the user invokes the command.
        '''
        traverseObj = self.hierarchy_traverse = _HierarchyTraverse(
            self.window, self.on_done)
        traverseObj.run()

    def on_done(self, dirName):
        '''Creates the folder with the path that has been chosen in the
        _HieararchyTraverse object.

        Args:
            dirName: The name of the folder to be created.
        '''
        _create_path(dirName, "directory",
                     self.hierarchy_traverse.chosen_directory, self.window)


class _FlatProject:
    '''Base class for flattening down the project directories to a single list.
    '''

    def populateAndShowPanel(self, window):
        '''Walks down from the top folders of the project and shows a panel 
        with a list of flattened directories.

        Args:
            window: The window object from the sublime_plugin.WindowCommand
        '''
        self.window = window

        self.all_directories = self.window.folders()

        for top_folder in self.window.folders():
            for dp, dn, fn in os.walk(top_folder):
                dn[:] = [d for d in dn if d not in _get_setting(
                    "flat_exclude_folders")]
                self.all_directories += [os.path.join(dp, d) for d in dn]

        self.window.show_quick_panel(self.all_directories, self.on_choice)

    def on_choice(self, choice):
        '''Called once a choice has been made in the panel.

        Grabs the selected directory from the panel and passes it to an
        input_panel for writing down the final section of the path.

        Args:
            choice: The choice as an int value.
        '''
        if choice < 0:
            return

        self.chosen_directory = self.all_directories[choice]
        self.window.show_input_panel(os.path.join(self.chosen_directory, ""),
                                     "", self.on_done, None, None)

    def on_done(self, name):
        '''A virtual function to be called once the full path is chosen.

        It is overwritten by the NewFileInProjectFlat and 
        NewFolderInProjectFlat classes to provide their relative functinalities.

        Args:
            name: The final portion of the path - either the file name or the
            folder name, depending on which functionality is needed.
        '''
        pass


class NewFileInProjectFlat(sublime_plugin.WindowCommand, _FlatProject):
    '''This class creates the "New file in project (flat)" command.

    Invoking this command the user is presented with a panel in the command
    palette, containing all the directories in the project as a flattened list. 

    The user can choose a location from that list for creating the new file in.
    '''

    def run(self, *args):
        '''Creates and shows the flattened list in a quick panel.

        This function is called when the user invokes the command.
        '''
        self.populateAndShowPanel(self.window)

    def on_done(self, fileName):
        '''Creates the file (fileName) in the chosen directory.

        Args:
            fileName: The name of the file to be created.
        '''
        _create_path(fileName, "file", self.chosen_directory, self.window)


class NewFolderInProjectFlat(sublime_plugin.WindowCommand, _FlatProject):
    '''This class creates the "New folder in project (flat)" command.

    Invoking this command the user is presented with a panel in the command
    palette, containing all the directories in the project as a flattened list. 

    The user can choose a location from that list for creating the 
    new folder in.
    '''

    def run(self, *args):
        '''Creates and shows the flattened list in a quick panel.

        This function is called when the user invokes the command.
        '''
        self.populateAndShowPanel(self.window)

    def on_done(self, dirName):
        '''Creates the folder (dirName) in the chosen directory.

        Args:
            dirName: The name of the directory to be created.
        '''
        _create_path(dirName, "directory", self.chosen_directory, self.window)
