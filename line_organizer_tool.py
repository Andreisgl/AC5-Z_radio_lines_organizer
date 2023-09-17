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

def get_rows_line_data_csv():
    # Opens csv and returns all rows
    with open(LINE_INFO_FILE_PATH, mode='r', encoding='UTF8', newline='') as line_file: # Open file
        csv_reader = csv.reader(line_file, delimiter='\\', quotechar='`')
        return [x for x in csv_reader]

def write_row_line_data_csv(data, is_list, append):
    # Write to the csv file.
    #
    # If append == True, append to file.
    # Else, overwrite it.
    #
    # If is_list, write all items of iterables as rows
    # Else, write a single row only

    mode = ''
    if append:
        mode = 'a'
    else:
        mode = 'w'

    with open(LINE_INFO_FILE_PATH, mode=mode, encoding='UTF8', newline='') as line_file: # Create file
            line_writer = csv.writer(line_file, delimiter='\\', quotechar='`')
            if is_list:
                line_writer.writerows(data)
            else:
                line_writer.writerow(data)

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
        # Define data to be written to new file
        # Assemble header with criteria as columns
        for criteria in INDEXING_CRITERIA:
            if type(criteria) == str:
                file_header.append(criteria)
            else: # If criteria has preset answers:
                file_header.append(criteria[0])
        # Constant columns. "constant_columns" = 2, since there are 2
        file_header.insert(0, 'ID') # Insert ID column. It autoincrements.
        file_header.insert(1, 'FILENAME') # Insert FILENAME column.

        # Assemble all files
        all_rows = []
        for field_index, track in enumerate(track_list):
            row = [field_index, track]
            # Write empty data to criteria to have
            # all columns appear as items in the list when reading later.
            padding = ['' for x in INDEXING_CRITERIA]
            row += padding
            all_rows.append(row)
        
        # Write data to file
        write_row_line_data_csv(file_header, False, True) # Write header
        for entry in all_rows: # Write entries
            write_row_line_data_csv(entry, True, True)



    line_file_dump = []
    line_pure_info = []
    line_file_dump = get_rows_line_data_csv()

    # From here, pass "line_pure_info" as a parameter
    # to an indexing prompt function,
    # which will return an updated list.
    # The current function will take it and save it to the .csv file.
    edited_file_data = surf_lines(line_file_dump, True)


    # Rewrite file
    write_row_line_data_csv(edited_file_data, True, False)

def surf_lines(line_info, ignore_unknowns):
    # This will surf the lines and see what data needs completion.
    # Receives the "line_info" of read file, and value for "ignore_unknowns".
    #
    # "ignore_unknowns": During field completion,
    # skip values marked with '?', that couldn't be determined by the user.
    
    # Types of special data that can be found in a field
    empty_data = '' # Empty. Must be filled out.
    unknown_data = '?' # Seen, but not known yet. Must be skipped.
    dummy_data = 'dummy' # Marks dummy files. Skip & mark whole line as dummy.
    
    # Types of special data that can be input in a field
    entry_dummy = dummy_data # Same as before
    entry_terminate = '\\' # Char that terminates a prompt when entered

    num_static_columns = 2 # Ammount of static columns (ID, file name)


    # Split data into parts
    header = line_info[0] # Get header
    line_info = line_info[1:] # Remove header from list.
    data_set = line_info # Pass info to 'data_set'.
    static_columns = data_set

    # Remove ID and track name from editable data
    data_set = [x[num_static_columns:] for x in data_set]
    # Reference header with only columns names for editable data
    editable_header = [x for x in header[num_static_columns:]]
    # Remove editable data from the 'static_columns'
    static_columns = [x[:num_static_columns] for x in static_columns]


    quit = False
    for line_index, line in enumerate(data_set):
        if quit: # If user chose to quit in previous line
            break
        print(static_columns[line_index][1]) # Print file name
        for field_index, field in enumerate(line):
            current_field = editable_header[field_index]
            print(current_field)
            # Decide what to do based on data
            if dummy_data in line: # Mark whole line and skip.
                data_set[line_index] = [dummy_data for x in line]
                break
            elif field == unknown_data: # Determine what to do
                if ignore_unknowns:
                    continue # Skip field
                else:
                    pass # Go ahead to prompt
            elif field == empty_data: # Must be filled up
                pass # Go ahead to prompt
            else: # Is user-input data. Skip.
                continue # Skip field
        
            # Data entry
            answer = input('Enter your data for {}: '.format(current_field))
            if answer == entry_terminate:
                # Quit prompt
                quit = True
                break
            elif answer == entry_dummy:
                # Mark whole line as dummy and skip
                data_set[line_index] = [dummy_data for x in line]
                break
            else: # Pass answer to field
                data_set[line_index][field_index] = answer
                pass
    
    # Reassemble file for outputting
    output_data = []
    for index, entry in enumerate(data_set):
        output_data.append(static_columns[index] + data_set[index])
    output_data.insert(0, header) # Insert header back
    
    return output_data


if __name__ == "__main__":
    main()