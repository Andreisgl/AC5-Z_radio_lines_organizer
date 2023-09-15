# This script runs through the extracted audio lines in a folder
# and reproduces them one by one. Upon hearing it, you can enter
# the information you know about it as prompted. This metadata 
# will be saved to a .csv file for indexing.

import os
import csv

def main():
    check_paths()
    handle__tracks_info_file()

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
    
    PROJECT_NAME = chosen_project
    PROJECT_PATH = os.path.join(PROJECTS_DB_PATH, PROJECT_NAME)
    PROJECT_FLAG_FILE_PATH = os.path.join(PROJECT_PATH, 'project.ACL')
    LINES_FOLDER_PATH = os.path.join(PROJECT_PATH, 'lines')
    LINE_INFO_FILE_PATH = os.path.join(PROJECT_PATH, 'line_data.csv')

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


def handle__tracks_info_file():
    # Go through the lines in the index
    global PROJECT_PATH
    global LINES_FOLDER_PATH
    global LINE_INFO_FILE_PATH

    track_list = os.listdir(LINES_FOLDER_PATH)

    # What info will be requested to index each line.
    # In the sublists, default values for each criteria, if they are a closed set.
    INDEXING_CRITERIA = ['CHARACTER',
                        'MISSION_NUMBER',
                        ['ACE_STYLE', ['MERCENARY', 'SOLDIER', 'KNIGHT']],
                        'TEXT']

    file_header = []
    # How many of the first rows shouldn't be editable
    constant_columns = 2
    # Init .csv file
    if not os.path.exists(LINE_INFO_FILE_PATH): # If csv does not exist
        with open(LINE_INFO_FILE_PATH, mode='w', encoding='UTF8', newline='') as line_file: # Create file
            # Define delimiters
            line_writer = csv.writer(line_file, delimiter='\\', quotechar='`')
            # Write file_header with criteria as columns
            for criteria in INDEXING_CRITERIA:
                if type(criteria) == str:
                    file_header.append(criteria)
                else:
                    file_header.append(criteria[0])
            # Constant columns. "constant_columns" = 2, since there are 2
            file_header.insert(0, 'ID') # Insert ID column. It autoincrements.
            file_header.insert(1, 'FILENAME') # Insert FILENAME column.
            # Write file_header
            line_writer.writerow(file_header)

            # Write all files
            for index, track in enumerate(track_list):
                row = [index, track]
                # Write empty data to criteria to have
                # all columns appear as items in the list when reading later.
                padding = ['' for x in INDEXING_CRITERIA]
                row += padding
                line_writer.writerow(row)
            pass

    line_file_dump = []
    line_pure_info = []
    with open(LINE_INFO_FILE_PATH, mode='r', encoding='UTF8', newline='') as line_file: # Open file
        csv_reader = csv.reader(line_file, delimiter='\\', quotechar='`')
        line_file_dump = [x for x in csv_reader]

        # Write/Rewrite header
        file_header = line_file_dump[0]
        # "tracks_pure_info" will be the main list referenced when indexing
        line_pure_info = [x for x in line_file_dump[1:]] # Cut off only ID

    
    # From here, pass "line_pure_info" as a parameter
    # to an indexing prompt function,
    # which will return an updated list.
    # The current function will take it and save it to the .csv file.
    aux = surf_lines(line_pure_info)


    pass

def surf_lines(line_info):

    pass


if __name__ == "__main__":
    main()