# This script runs through the extracted audio lines in a folder
# and reproduces them one by one. Upon hearing it, you can enter
# the information you know about it as prompted. This metadata 
# will be saved to a .csv file for indexing.

import os
import csv
import subprocess

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
    global PROJECT_FLAG_FILE_PATH 
    
    # Names and paths
    PROJECT_NAME = chosen_project
    PROJECT_PATH = os.path.join(PROJECTS_DB_PATH, PROJECT_NAME)
    PROJECT_FLAG_FILE_PATH = os.path.join(PROJECT_PATH, 'project.ACL')
    LINES_FOLDER_PATH = os.path.join(PROJECT_PATH, 'lines')
    LINE_INFO_FILE_PATH = os.path.join(PROJECT_PATH, 'line_data.csv')

    # Track info stuff
    global TRACKS_ARE_BGM
    TRACK_TYPE_HEADER = 'TRACK_TYPE:'
    TRACK_TYPE_OPTIONS = ['BGM', 'RADIO']

    # Check if paths exist
    if not os.path.exists(PROJECT_PATH):
        os.mkdir(PROJECT_PATH)

    if not os.path.exists(LINES_FOLDER_PATH):
        os.mkdir(LINES_FOLDER_PATH)

    #endregion
def choose_project():
    # Prompt user to choose which project to open/create
    # For now, name is hard-coded.
    global PROJECTS_DB_PATH

    projects_list = os.listdir(PROJECTS_DB_PATH)

    print('Choose which project to open/create:')
    
    print('By the Power of hardcoding, I choose the project for you!')
    #chosen_project = projects_list[prompt_user_list(projects_list, True)]
    chosen_project = 'test_project'

    print('Opening "{}".'.format(chosen_project))

    return chosen_project


def main():
    check_paths()

INPUT_EXIT_MESSAGE = 'PRESS ENTER TO EXIT'
INPUT_CONTINUE_MESSAGE = 'PRESS ENTER TO CONTINUE'

if __name__ == "__main__":
    main()