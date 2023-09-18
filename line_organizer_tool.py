# This script runs through the extracted audio lines in a folder
# and reproduces them one by one. Upon hearing it, you can enter
# the information you know about it as prompted. This metadata 
# will be saved to a .csv file for indexing.

import os
import csv
import subprocess

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

    if not os.path.exists(PROJECT_FLAG_FILE_PATH): # If project is new:
        TRACKS_ARE_BGM = get_track_playback_info(True) # Ask user track type
        with open(PROJECT_FLAG_FILE_PATH, 'w', encoding="utf-8") as file:
            # Write track type info:
            if TRACKS_ARE_BGM: # Tracks are BGM
                file.write(TRACK_TYPE_HEADER + TRACK_TYPE_OPTIONS[0])
            else: # Tracks are RADIO
                file.write(TRACK_TYPE_HEADER + TRACK_TYPE_OPTIONS[1])
    else: # If file already exists
        with open(PROJECT_FLAG_FILE_PATH, 'r', encoding="utf-8") as file:
            data = (file.read()).splitlines()
            # Find track type info
            track_type_entry = [x for x in data if TRACK_TYPE_HEADER in x][0]
            if TRACK_TYPE_OPTIONS[0] in track_type_entry:
                get_track_playback_info(False, True)
            else:
                get_track_playback_info(False, False)
        pass
    #endregion

def prompt_user_list(option_list):
    # This function creates a prompt to choose from a list.
    # Handles invalid answers. Answer must be an index.
    # Returns index

    for index, entry in enumerate(option_list):
        print('{} - {}'.format(index, entry))
    print()

    index_range = len(option_list)-1
    valid_index = True
    while True:
        answer = ''
        if not valid_index: # Cisplay error message accordig to flag
            print('Input a valid index!')

        try:
            answer = int(input('Enter index: ')) # Receive answer
        except ValueError:
            valid_index = False # Set flag to false on invalidity
            continue

        if answer < 0 or answer > index_range:
            valid_index = False # Set flag to false on invalidity
            continue

        break
        
    return answer

def choose_project():
    # Prompt user to choose which project to open/create
    # For now, name is hard-coded.
    global PROJECTS_DB_PATH

    projects_list = os.listdir(PROJECTS_DB_PATH)
    create_new_flag = 'CREATE NEW'
    projects_list.append(create_new_flag)

    print('Choose which project to open/create:')
    
    chosen_project = projects_list[prompt_user_list(projects_list)]
    if chosen_project == create_new_flag:
        answer = input('Input the new project\'s name: ')
        chosen_project = answer

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

    global INPUT_EXIT_MESSAGE
    global INPUT_CONTINUE_MESSAGE

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
    # If csv does not exist and there are tracks to be indexed:
    if (not os.path.exists(LINE_INFO_FILE_PATH)) and len(track_list) != 0:
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
        write_row_line_data_csv(all_rows, True, True)
    elif len(track_list) == 0: # If there are no tracks to be indexed:
        print('There are no tracks to be indexed!')
        print('Copy tracks to the "{}" folder'
              .format(os.path.basename(LINES_FOLDER_PATH)))
        input(INPUT_EXIT_MESSAGE)
        return False


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
    skip_line = '||' # Skip whole line
    unknown_line = '?:' # Mark whole line as unknown
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
        playback = True
        track_name = static_columns[line_index][1]
        print('\n' + track_name) # Print file name
        
        for field_index, field in enumerate(line): # Check field
            current_field = editable_header[field_index]
            #print(current_field)
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
            
            # Play track for user
            if playback:
                track_path = os.path.join(LINES_FOLDER_PATH, track_name)
                play_track(track_path)
            playback = False

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
            elif answer == skip_line: # Skip line without inputting
                break
            elif answer == unknown_line: # Mark whole line as unknown and skip
                data_set[line_index] = [unknown_data for x in line]
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


def get_track_playback_info(new_file, is_bgm = True):
    # This function prompts the use
    # If tracks are BGM, choose BGM parameters.
    # Else, use RADIO parameters.
    #
    # If new_file == true, prompt user to input type data
    # Else, receive if tracks are BGM or not

    # Argument list for MFAudio, with indexes for the lists used in this code
        # 0 -  /IFnnnnn	Input frequency
        # 1 -  /ICn	Input channels
        # 2 -  /IIxxxx	Input interleave (hex)
        # 3 -  /IHxxxx	Input headerskip (hex)
        # 4 -  /OTtttt	Output type (WAVU, VAGC,
        # 	            SS2U, SS2C, RAWU, RAWC)
        # 5 -  /OFnnnnn	Output frequency
        # 6 -  /OCn	Output channels
        # 7 -  /OIxxxx	Output interleave (hex)
        # 8 -  "InputFile"	Input file to play/convert
        # 9 -  "OutputFile"	Output file to convert to

    global TRACKS_ARE_BGM
    global MFAUDIO_ARG_SET
    global MFAUDIO_PATH
    MFAUDIO_PATH = os.path.join(os.path.dirname(SCRIPT_PATH), 'MFAudio', 'MFAudio.exe')

    # Argument set for BGM and RADIO tracks.
    # AFAIK, there is no reason for them to differ between AC5 and ACZ.
    MFAUDIO_BGM_ARGS = [44100, 2, 320, 0, 'WAVU', 44100, 2, 320]
    MFAUDIO_RADIO_ARGS = [22050, 1, 320, 0, 'WAVU', 22050, 1, 320]

    TYPE_OPTIONS = ['BGM', 'RADIO']

    if new_file: # If file is new, prompt user.
        print('Are you working with BGM or RADIO?')
        answer = prompt_user_list(TYPE_OPTIONS)
        if answer == 0:
            TRACKS_ARE_BGM = True
            MFAUDIO_ARG_SET = MFAUDIO_BGM_ARGS
        else:
            TRACKS_ARE_BGM = False
            MFAUDIO_ARG_SET = MFAUDIO_RADIO_ARGS
    else: # If file already exists, get type data from parameter
        if not is_bgm:
            TRACKS_ARE_BGM = False
            MFAUDIO_ARG_SET = MFAUDIO_RADIO_ARGS
        else:
            TRACKS_ARE_BGM = True
            MFAUDIO_ARG_SET = MFAUDIO_BGM_ARGS

def play_track(track_path):
    # This method plays the chosen track through MFAudio,
    # with the predefined arguments chosen on project creation
    global MFAUDIO_ARG_SET
    global SCRIPT_PATH
    global MFAUDIO_PATH

    input_filename = os.path.basename(track_path)
    
    args = ['/IF', '/IC', '/II', '/IH', '/OT', '/OF', '/OC', '/OI'] #Contains the core arguments.
    
    # Concatenate args and values
    args = [args[index] + str(MFAUDIO_ARG_SET[index]) for index, x in enumerate(args)]
    args.append('"{}"'.format(track_path)) # Append track path to args
    args.insert(0, MFAUDIO_PATH)

    ## Adds a input filename to 'argumentBuffer' string and...
    #argument_buffer = exe_filename + ' ' + argument_buffer + '"' + DESTINATION_PATH + '\\'+ input_filename + '"'
    #
    #if mode == 0:  # ... if the mode is "Convert (0)", add output filename as well.
    #    argument_buffer = argument_buffer + ' ' + '"' + output_filename + '"'
    #
    args_string = ''
    for index, arg in enumerate(args):
        args_string += arg
        if index < 9:
            args_string += ' '
    

    subprocess.Popen(args_string)
    
    pass

INPUT_EXIT_MESSAGE = 'PRESS ENTER TO EXIT'
INPUT_CONTINUE_MESSAGE = 'PRESS ENTER TO CONTINUE'

if __name__ == "__main__":
    main()