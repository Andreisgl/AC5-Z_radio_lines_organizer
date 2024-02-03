# This script runs through the extracted audio lines in a folder
# and reproduces them one by one. Upon hearing it, you can enter
# the information you know about it as prompted. This metadata 
# will be saved to a .csv file for indexing.

import os
import csv
#import subprocess

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.ttk import *

from modules import tkinter_classes as GUItems
from modules import csv_methods as csv_m


# TKINTER SETUP
def setup_root_window():
    global root
    root = tk.Tk()
    root.title('AC5-Z_RADIO_LINES_ORGANIZER')

    GUItems.center_window(root)


# BASIC PATH AND PROJECT PREPARING
def check_paths():
    # Make sure important paths and dirs are created

    #region # General paths
    global SCRIPT_PATH # Where this script is
    global SCRIPT_DIR_PATH # This script's dir
    global PROJECTS_DB_PATH # Where all projects will be contained

    SCRIPT_PATH = __file__
    SCRIPT_DIR_PATH = os.path.dirname(SCRIPT_PATH)
    PROJECTS_DB_PATH = os.path.join(SCRIPT_DIR_PATH, 'PROJECTS')
    
    if not os.path.exists(PROJECTS_DB_PATH):
        os.mkdir(PROJECTS_DB_PATH)
    #endregion

def choose_project():
    # Prompt user to choose which project to open/create
    # For now, name is hard-coded.
    global root
    global PROJECTS_DB_PATH

    global SCREEN_WIDTH 
    global SCREEN_HEIGHT

    chosen_project = ''
    projects_list = os.listdir(PROJECTS_DB_PATH)

    print('Choose which project to open/create:')


    project_popup = Toplevel()
    project_popup.attributes("-topmost", True)
    

    project_menu = GUItems.ChooseProjectFrame(project_popup, 'choose_project', 'Choose Project', projects_list, '')
    project_combobox = project_menu.project_prompt
    project_menu.pack()

    # Create a button to get the selected project
    def get_project():
        chosen_project = project_menu.get_value()
        if not chosen_project:
            get_project_button['text'] = 'Input a valid name!'
            return
        print('Project selected: "{}"'.format(chosen_project))
        project_popup.destroy()
        open_project(chosen_project)
    
    get_project_button = ttk.Button(project_popup, text="Choose Project", command=get_project)
    get_project_button.pack()




    GUItems.center_window(project_popup)


    

def open_project(chosen_project):
    # Assemble important paths and folders for the project.
    # Receives project name and opens it.
    # If project does not exist, create it

    #region # Intra-project paths
    # Project specific folder
    # lines folder
    # csv file
    global PROJECT_NAME
    global PROJECT_PATH
    global LINES_FOLDER_PATH
    global LINE_INFO_FILE_PATH
    # The existence of this file indicates a dir is a project
    global PROJECT_META_FILE_PATH 
    
    # Print
    print('Opening "{}"'.format(chosen_project))

    # Names and paths
    PROJECT_NAME = chosen_project
    PROJECT_PATH = os.path.join(PROJECTS_DB_PATH, PROJECT_NAME)
    PROJECT_META_FILE_PATH = os.path.join(PROJECT_PATH, 'project.csv')
    LINES_FOLDER_PATH = os.path.join(PROJECT_PATH, 'lines')
    LINE_INFO_FILE_PATH = os.path.join(PROJECT_PATH, 'line_data.csv')

    # Flag stuff
    project_is_new = False

    # Create folders and files if they don't exist
    if not os.path.exists(PROJECT_PATH): # Project's root folder
        os.mkdir(PROJECT_PATH)
    if not os.path.exists(LINES_FOLDER_PATH): # Lines container folder
        os.mkdir(LINES_FOLDER_PATH)
    if not os.path.exists(PROJECT_META_FILE_PATH): # Project metadata folder
        project_is_new = True
        
    
    prepare_meta_file(project_is_new)
    #endregion

def prepare_meta_file(project_is_new):
    # Track info stuff

    # If file is not new, read it. 
    # If it is, create and get data

    # What data do I need to store?
    # If tracks are BGM or RADIO
    # What game they belong to
    #

    global PROJECT_META_FILE_PATH

    global CURRENT_TRACK_TYPE
    TRACK_TYPE_HEADER = 'TRACK_TYPE'
    TRACK_TYPE_OPTIONS = ('BGM', 'RADIO')

    global CURRENT_GAME
    GAME_TYPE_HEADER = 'GAME'
    GAME_TYPE_OPTIONS = ('ACZ',)


    meta_prompt_fields = ((GAME_TYPE_HEADER, GAME_TYPE_OPTIONS),
                          (TRACK_TYPE_HEADER, TRACK_TYPE_OPTIONS)
                          )
    
    # Create a button to get the selected project
    def get_metadata_input():
        '''
        Method to return user-inputted metadata
        and proceed to write metadata file
        '''

        successful = False
        chosen_meta = meta_menu.get_value()
        print('User input: {}'.format(chosen_meta))

        for field in chosen_meta: # Check for any invalid values
            for data in field:
                if data == '':
                    successful = False
                    print('Invalid Metadata!')
                else:
                    successful = True
        
        if successful:
            meta_popup.destroy()
            print('Metadata chosen:', chosen_meta)
            write_metadata_file(chosen_meta)
        #else:
        #    get_metadata_input() # Redo steps
    
    def write_metadata_file(meta_input):
        '''
        Writes data to metadata file in the format:
        FIELD_NAME\VALUE
        '''
        #print(meta_input)
        csv_m.write_row_line_data_csv(meta_input, True, PROJECT_META_FILE_PATH)

        get_existing_metadata() # Open recently-written metadata

    def get_existing_metadata():
        # If already existing or just created, read metadata file
        fetched_metadata = csv_m.get_rows_line_data_csv(PROJECT_META_FILE_PATH)
        
        # Assign fetched data to final variables
        CURRENT_GAME = fetched_metadata[0][1]
        CURRENT_TRACK_TYPE = fetched_metadata[1][1]
    
        #region # Metadata printing
        game_meta = '{}: {}'.format(fetched_metadata[0][0], fetched_metadata[0][1])
        type_meta = '{}: {}'.format(fetched_metadata[1][0], fetched_metadata[1][1])
        print('Project metadata:\n{}\n{}'.format(game_meta, type_meta))
        #endregion

        # Proceed to next section
        manipulate_tracks()

    if project_is_new: # If project is new, prompt user to choose the metadata
        # Initiate metadata GUI
        print('meta file is new!')
        meta_popup = Toplevel()
        meta_popup.attributes("-topmost", True)

        # Create prompt for user to input new metadata
        meta_menu = GUItems.ProjectMetaPromptFrame(meta_popup,
                                                   'choose_meta',
                                                   'Project metadata',
                                                   meta_prompt_fields)

        get_metadata_button = ttk.Button(meta_popup, text="Get Value",
                                         command=get_metadata_input)
        get_metadata_button.pack()
        GUItems.center_window(meta_popup)
    else:
        get_existing_metadata() # Get already-existing metadata
    

def manipulate_tracks():
    # In this function, I need to:
    # Browse all lines,
    # Display their metadata and replay them

    # Create GUI

    global root
    global LINES_FOLDER_PATH

    lines_frame = GUItems.LineManipulationFrame(root, 'lines_frame_thing', ('',))

    

  
    GUItems.center_window(root)
    root.lift()
    pass

def main(): 
    check_paths()
    setup_root_window()
    choose_project()
    
    print('END!')
    root.mainloop()



if __name__ == "__main__":
    main()