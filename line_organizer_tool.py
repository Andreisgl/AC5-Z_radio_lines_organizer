'''This script is used for the indexing of audio lines for the game Ace Combat Zero. Its goal is to aid translation efforts.
This tool allows you to go through the audio lines and fill out data on each track, mainly:CHARACTER - Character that speaks the line
MISSION - Mission where the line is found
ACE STYLE - Ace Style if the line has variants that change with the style
TEXT - what is said in the line

It can playback the track on the go using MFAudio without the need for conversions or leaving the tool, allowing for a more efficient workflow
'''
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

def prompt_user_list(input_option_list, custom_answer=False, display_options=True, custom_answer_text='Other'):
    # This function creates a prompt to choose from a list.
    # Handles invalid answers. Answer must be an index.
    #
    # custom_answer: If true, allows for a custom answer
    # display_options:
        # If true, displays available options. 
        # Otherwise, this func can be used to validate a number inside a range

    # Returns index. If custom, return custom answer.

    # Copies of input list to avoid changing the original one
    #option_list = input_option_list[:]
    option_list = input_option_list

    if custom_answer: # TODO: May accidentally append to original list
        option_list.append(custom_answer_text)

    if display_options: # Display options if desired
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
    
    project_index = prompt_user_list(projects_list, custom_answer=True, custom_answer_text='Create new project')

    chosen_project = projects_list[project_index]


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


def handle__tracks_info_file():
    # Go through the lines in the index
    global PROJECT_PATH
    global LINES_FOLDER_PATH
    global LINE_INFO_FILE_PATH

    global INDEXING_CRITERIA

    global INPUT_EXIT_MESSAGE
    global INPUT_CONTINUE_MESSAGE

    track_list = os.listdir(LINES_FOLDER_PATH)

    # What info will be requested to index each line.
    # In the sublists, default values for each criteria, if they are a closed set.
    INDEXING_CRITERIA = ('CHARACTER',
                        'MISSION_NUMBER',
                        ('ACE_STYLE', ('MERCENARY', 'SOLDIER', 'KNIGHT', '?', 'NONE')),
                        'TEXT')

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
    

    
    # "ignore_unknowns": During field completion,
    # skip values marked with '?', that couldn't be determined by the user.
    global INDEXING_CRITERIA

    global INPUT_CONTINUE_MESSAGE

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
    
    # Display routine

    #region Commands list
    # Types of commands:
    
    # UNIVERSAL COMMANDS: Can be executed anywhere
    cmd_display_help = ('HELP', 'Displays the help prompt') # Display commands
    cmd_exit_loop = ('SAVE_AND_EXIT', 'Saves progress and exits tool') # Saves progress and exits the main program
    #
    universal_cmd_list = (
        cmd_display_help,
        cmd_exit_loop
    )

    # MENU COMMANDS: Can only be executed when no track is selected
    cmd_display_tracks = ('DISPLAY_TRACKS', 'Displays tracks in the desired interval. Shows all tracks by default') # Displays tracks
    cmd_choose_track = ('CHOOSE_TRACK', 'Choose a track by index')
    cmd_set_display_interval = ('SET_DISPLAY_INTERVAL', 'Set interval of tracks that shall be shown when using DISPLAY_TRACKS') # Sets the interval of tracks that are displayed
    #
    menu_cmd_list = (
        cmd_choose_track,
        cmd_display_tracks,
        cmd_set_display_interval
    )

    # TRACK COMMANDS: Can only be executed when a line is selected
    cmd_playback = ('PLAYBACK', 'Invokes MFAudio to play the current track') # Invokes MFAudio to play file
    cmd_show_data = ('SHOW_DATA', 'Shows metadata for current track') # Shows current data for the selected line
    cmd_enter_data = ('ENTER_DATA', 'Input metadata for current line') # Fill out a field in the chosen line
    cmd_back = ('BACK', 'Return to previous menu') # Exit line and return to main menu loop
    #
    track_cmd_list = (
        cmd_playback,
        cmd_show_data,
        cmd_enter_data,
        cmd_back
    )

    all_cmds = universal_cmd_list + menu_cmd_list + track_cmd_list
    #endregion # Commands list
    #region # Command inner functions
    
    #region Main Menu Commands:
    def display_help():
        print()
        print('COMMANDS:')
        for cmd in all_cmds:
            print(f'{cmd[0]} - {cmd[1]}')
        print()
    #
    def exit_loop():
        print('Exiting application')

    # Menu Commands:
    display_set = line_info[:] # Standard value for this set # TODO: Maybe this line is redundant
    display_interval = [0,-1]
    def display_tracks(start=0, end=-1):
        # Copy data from file to display set
        # TODO: Ok, since 'line_info' which is supposed to reflect the saved data, only get updated when this function is calld (once every program execution),
        # I need to use 'data_set' to reflect the most current changes and save every time I update a field. Messy, gotta fix this later!
        if end == -1:
            display_set = line_info[start:]
            display_data_set = data_set[start:]
        else:
            display_set = line_info[start:end+1] 
            display_data_set = data_set[start:end+1] 
        
        headers = [x[:2] for x in display_set]

        print(editable_header) # Print fields
        # TODO: Add logic to filter out dummy tracks and other conditions
        for index in range(len(display_set)):
            print(headers[index] + display_data_set[index])
    #
    def set_display_interval():
        print(f'Choose the interval of tracks you wish to see displayed when using {cmd_display_tracks[0]}')
        
        print(f'Range: {0}-{len(line_info)}')

        print('First index (first track is 0): ')
        start_answer = prompt_user_list(line_info, False, False)

        print(f'Last index (last track is {len(line_info)}): ')
        end_answer = prompt_user_list(line_info, False, False)

        print(f'Chosen interval: {start_answer}-{end_answer}')

        return start_answer, end_answer
    #
    current_track = -1 # Indicates what track was chosen. If none, value = -1
    def choose_track():
        answer = prompt_user_list(line_info, False, False)
        print(f'Chosen track: {answer}')
        return answer
    #endregion
    
    #region Track Commands
    def playback(track_index):
        track_list = os.listdir(LINES_FOLDER_PATH)
        track_path = os.path.join(LINES_FOLDER_PATH, track_list[track_index])
        play_track(track_path)
    #
    def show_data(index):
        original_data = line_info[index]
        saved_data = original_data[2:]
        current_data = data_set[index]

        id = original_data[0]
        track_name = original_data[1]

        print()
        print(f'ID: {id} - TRACK: {track_name}')
        print(editable_header)
        print(f'{saved_data} - CURRENTLY SAVED')
        if saved_data != current_data:
            print(f'{current_data} - CURRENT CHANGES')
        print()
    #
    def enter_data():
        print()
        print('What field do you want to change?')
        options = editable_header + [cmd_back[0]]

        index = prompt_user_list(options)
        
        if options[index] == cmd_back[0]: # If user chose to return, cancel
            return -1, ''

        field_choice = INDEXING_CRITERIA[index]
        field_type = type(field_choice)

        field_name = ''
        data = ''

        # If field is a tuple, it has a fixed set of answers
        if field_type == tuple:
            print()
            print(f'Choose a value for this field')
            field_name = field_choice[0]
            field_options = field_choice[1]
            data = field_options[prompt_user_list(field_options)]
        
        # If field is a type, it allows for custom answers
        elif field_type == str:
            field_name = field_choice
            data = input(f'Input new value for {field_name}: ')

        print()
        return index, data

    def save_data():
        # Reassemble file for outputting
        print('SAVING DATA...')
        output_data = []
        for index, entry in enumerate(data_set):
            output_data.append(static_columns[index] + data_set[index])
        output_data.insert(0, header) # Insert header back
    
        return output_data

    #endregion

    
    while True: # Option loop for commands
        #print('Options:')
        options_list = [] # List containing all available commands
        
        # MAIN MENU
        if current_track == -1:
            options_list = menu_cmd_list + universal_cmd_list
            options_list = [x[0] for x in options_list]

            choice_index = prompt_user_list(options_list, False)
            answer = options_list[choice_index]
            print(answer)

            #region Main Menu option routes
            if answer == cmd_display_tracks[0]:
                display_tracks(display_interval[0], display_interval[1])
            #
            elif answer == cmd_set_display_interval[0]:
                display_interval[0], display_interval[1] = set_display_interval()
            #
            elif answer == cmd_choose_track[0]:
                current_track = choose_track()
            #
            elif answer == cmd_display_help[0]:
                display_help()
            #
            elif answer == cmd_exit_loop[0]:
                quit = True
            #
            else:
                print('Unknown command!')
                break
            #endregion
        
        # TRACK MENU
        elif current_track >= 0 and current_track < len(line_info) : # A track was selected
            while True:
                show_data(current_track)
                options_list = track_cmd_list + universal_cmd_list
                options_list = [x[0] for x in options_list]

                choice_index = prompt_user_list(options_list, False)
                answer = options_list[choice_index]
                print(answer)

                #region Track Menu option routes
                if answer == cmd_playback[0]:
                    playback(current_track)
                #
                elif answer == cmd_show_data[0]:
                    show_data(current_track)
                    break
                #
                elif answer == cmd_enter_data[0]:
                    while True:
                        show_data(current_track)
                        field_index, data = enter_data()
                        if field_index == -1: # User wants to cancel
                            break
                        else:
                            data_set[current_track][field_index] = data
                #
                elif answer == cmd_display_help[0]:
                    display_help()
                #
                elif answer == cmd_back[0]:
                    current_track = -1
                    save_data()
                    print('Back to Main Menu')
                    break
                #
                elif answer == cmd_exit_loop[0]:
                    quit = True
                    break
                #
                else:
                    print('Unknown command!')
                    break
                #endregion
        if quit:
            exit_loop()
            break
    
    
    
    return save_data()


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