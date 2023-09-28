# This script runs through the extracted audio lines in a folder
# and reproduces them one by one. Upon hearing it, you can enter
# the information you know about it as prompted. This metadata 
# will be saved to a .csv file for indexing.

import os
#import csv
#import subprocess

import tkinter as tk


from modules import tkinter_classes as GUItems

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

    # PROMPT USER TO CHOOSE PROJECT
    chosen_project = choose_project()

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
    
    # Names and paths
    PROJECT_NAME = chosen_project
    PROJECT_PATH = os.path.join(PROJECTS_DB_PATH, PROJECT_NAME)
    PROJECT_META_FILE_PATH = os.path.join(PROJECT_PATH, 'project.ACL')
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
        
    if project_is_new:
        prepare_meta_file()
    #endregion

def prepare_meta_file():
    # Track info stuff

    # What data do I need to store?
    # If tracks are BGM or RADIO
    # What game they belong to
    # 

    global PROJECT_META_FILE_PATH

    global TRACKS_ARE_BGM
    TRACK_TYPE_HEADER = 'TRACK_TYPE:'
    TRACK_TYPE_OPTIONS = ('BGM', 'RADIO')

    global CURRENT_GAME
    GAME_TYPE_HEADER = 'GAME:'
    GAME_TYPE_OPTIONS = ('ACZ',)


    print('meta file is new!')
    print('PROMPT USER ABOUT FILE METADATA')
    #with open(PROJECT_META_FILE_PATH, 'wb'):
    #        pass


def choose_project():
    # Prompt user to choose which project to open/create
    # For now, name is hard-coded.
    global root
    global PROJECTS_DB_PATH

    projects_list = os.listdir(PROJECTS_DB_PATH)

    # Create GUI for project choosing
    input = GUItems.PopupPromptChoose(root, 'project_prompt', 'Project stuff!', ('foo', 'bar'))
    input.grid(row=0, column=0)    


    print('Choose which project to open/create:')
    
    print('By the Power of hardcoding, I choose the project for you!')
    #chosen_project = projects_list[prompt_user_list(projects_list, True)]
    chosen_project = 'test_project'

    print('Opening "{}".'.format(chosen_project))

    return chosen_project

# TKINTER SETUP
def setup_root_window():
    global root
    root = tk.Tk()
    root.title('AC5-Z_RADIO_LINES_ORGANIZER')

    window_width = 800
    window_heigth = 400

    root.geometry(f'{window_width}x{window_heigth}')

    root.config(bg='#ffffff')

def main():
    setup_root_window()
    check_paths()
    

    root.mainloop()

INPUT_EXIT_MESSAGE = 'PRESS ENTER TO EXIT'
INPUT_CONTINUE_MESSAGE = 'PRESS ENTER TO CONTINUE'

if __name__ == "__main__":
    main()