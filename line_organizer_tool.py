# This script runs through the extracted audio lines in a folder
# and reproduces them one by one. Upon hearing it, you can enter
# the information you know about it as prompted. This metadata 
# will be saved to a .csv file for indexing.

import os
import csv

def main():
    check_paths()
    surf_lines()

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
    global META_FILE_PATH
    # The existence of this file indicates a dir is a project
    global PROJECT_FLAG_FILE_PATH 
    
    PROJECT_NAME = chosen_project
    PROJECT_PATH = os.path.join(PROJECTS_DB_PATH, PROJECT_NAME)
    PROJECT_FLAG_FILE_PATH = os.path.join(PROJECT_PATH, 'project.ACL')
    LINES_FOLDER_PATH = os.path.join(PROJECT_PATH, 'lines')
    META_FILE_PATH = os.path.join(PROJECT_PATH, 'line_data.csv')

    if not os.path.exists(PROJECT_PATH):
        os.mkdir(PROJECT_PATH)

    if not os.path.exists(LINES_FOLDER_PATH):
        os.mkdir(LINES_FOLDER_PATH)

    if not os.path.exists(PROJECT_FLAG_FILE_PATH):
        with open(PROJECT_FLAG_FILE_PATH, 'w'):
            # File can be empty. Maybe I could add stuff here later...
            pass
    #endregion


def choose_project():
    # Prompt user to choose which project to open/create
    # For now, name is hard-coded.
    print('Choose which project to open/create:')
    print('Oops! Chose it for you!')

    chosen_project = 'test_project'

    print('Opening {}.'.format(chosen_project))
    return chosen_project


def surf_lines():
    # Go through the lines in the index
    global PROJECT_PATH
    global LINES_FOLDER_PATH
    global META_FILE_PATH

    files = os.listdir(LINES_FOLDER_PATH)

    # Save lines
    

    pass
# What info will be requested to index each line.
# In the sublists, default values for each criteria, if they are a closed set.
INDEXING_CRITERIA = ['CHARACTER',
                     'MISSION_NUMBER',
                     ['ACE_STYLE', 'MERCENARY', 'SOLDIER', 'KNIGHT'],
                     'PHRASE']


if __name__ == "__main__":
    main()