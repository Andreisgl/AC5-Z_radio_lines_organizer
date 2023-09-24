# This script runs through the extracted audio lines in a folder
# and reproduces them one by one. Upon hearing it, you can enter
# the information you know about it as prompted. This metadata 
# will be saved to a .csv file for indexing.

import os
import csv
import subprocess

def main():
    check_paths()
    

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
    TRACK_TYPE_OPTIONS = ('BGM', 'RADIO')

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

def prompt_user_list(option_list, custom_answer):
    # This function creates a prompt to choose from a list.
    # Handles invalid answers. Answer must be an index.
    #
    # custom_answer: If true, allows for a custom answer
    # Returns index. If custom, return custom answer.

    if custom_answer:
        option_list.append('Other')

    for index, entry in enumerate(option_list):
        print('{} - {}'.format(index, entry))
    print()

    max_index = len(option_list)-1
    valid_index = True
    while True:
        answer = ''
        if not valid_index: # Display error message accordig to flag
            print('Input a valid index!')

        try:
            answer = int(input('Enter index: ')) # Receive answer
        except ValueError:
            valid_index = False # Set flag to false on invalidity
            continue

        if answer < 0 or answer > max_index: # Answer is outisde index range
            valid_index = False # Set flag to false on invalidity
            continue
        
        valid_index = True
        if custom_answer and answer == max_index:
            user_input = input('Input your answer: ')
            # Changing the list here changes the list passed as parameter.
            option_list.pop() # Remove old item
            option_list.append(user_input) # Insert custom answer
        break

    return answer

def choose_project():
    # Prompt user to choose which project to open/create
    # For now, name is hard-coded.
    global PROJECTS_DB_PATH

    projects_list = os.listdir(PROJECTS_DB_PATH)

    print('Choose which project to open/create:')
    
    chosen_project = projects_list[prompt_user_list(projects_list, True)]


    print('Opening "{}".'.format(chosen_project))

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
        answer = prompt_user_list(TYPE_OPTIONS, False)
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