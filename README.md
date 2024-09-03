# AC5-Z_radio_lines_organizer
With dubbing and whatnot in mind, this script seeks to facilitate the process of organizing radio files from Ace Combat Zero/5

## CONCEPT
After importing tracks extracted from the game with the "bgm_pac_ace" tool, the script will go through the tracks, reproduce them using MFAudio, and prompt the user to fill out information about them, according to some indexing criteria. They are as follow:

### INDEXING_CRITERIA 
    'CHARACTER' - Who speaks the line
    'MISSION_NUMBER' - In what mission it appears
    'ACE_STYLE' - In what ace style it appears
    'TEXT' - What is said in the track


## SETUP:
When obtaining the scripts, make sure to source them from the "Releases' tab. It will contain the "MFAudio.exe" executable, which is necessary for audio playback. It will also contain project files for ACZs radio lines, besides the table already present in the repo, so you can use the indexed lines for your own projects.

## USAGE:
### PROJECTS: - CREATING YOUR FIRST PROJECT
The program separates its files into projects. Since indexing projects are expected to take longer than a simple unpacking, you can work on many indexing projects in paralel without worries.
When running the script, you will be prompted to choose which project to open, or to create one. When running the script for the first time, creating a new project will be the only option.

    0 - Create new project

    Enter index:

Input the index for the desired option. In this case, "0". Afterwards, Input the name of your new project:

    Enter index: 0
    Input your answer: MY_PROJECT

The tool will prompt you to choose if you are dealing with radio lines or BGM files. This matters, as this info determines which parameters to pass to MFAudio when playing the tracks.

    Opening "MY_PROJECT".
    Are you working with BGM or RADIO?
    0 - BGM
    1 - RADIO

    Enter index:

In this case, this project will be for radio lines.

    Enter index: 1

### IMPORTING TRACKS
When creating a project for the first time, you must import the track files to the **PROJECTS/PROJECT_NAME/lines** folder.

    There are no tracks to be indexed!
    Copy tracks to the "lines" folder
    PRESS ENTER TO EXIT

Exit the tool and transfer the files. Once done, start the tool and open the project again:

### NORMAL USAGE
With the project ready, we can start working. The main menu will open automatically, presenting a few options. These will help you navigate and visualize the tracks.

    Opening "MY_PROJECT".
    0 - CHOOSE_TRACK
    1 - DISPLAY_TRACKS
    2 - SET_DISPLAY_INTERVAL
    3 - HELP
    4 - SAVE_AND_EXIT

    Enter index:

#### HELP PROMPT
A full list of the commands and their usage can be summoned by choosing the "HELP" command:

    COMMANDS:
    HELP - Displays the help prompt
    SAVE_AND_EXIT - Saves progress and exits tool
    CHOOSE_TRACK - Choose a track by index
    DISPLAY_TRACKS - Displays tracks in the desired interval. Shows all tracks by default
    SET_DISPLAY_INTERVAL - Set interval of tracks that shall be shown when using DISPLAY_TRACKS
    PLAYBACK - Invokes MFAudio to play the current track
    SHOW_DATA - Shows metadata for current track
    ENTER_DATA - Input metadata for current line
    BACK - Return to previous menu



#### NAVIGATING THE MAIN MENU - TRACK DISPLAYING
First of all, to see the current state of the indexing, **DISPLAY_TRACKS**.

    DISPLAY_TRACKS
    ['CHARACTER', 'MISSION_NUMBER', 'ACE_STYLE', 'TEXT']
    ['0', '0000_ACZ_VoiceDummy02FX.npsf', '', '', '', '']
    ['1', '0001_ACZ_VoiceDummy02FX.npsf', '', '', '', '']
    ['2', '0002_ACZ_VoiceDummy02FX.npsf', '', '', '', '']
    ['3', '0003_ACZ_VoiceDummy02FX.npsf', '', '', '', '']
    ...
    ['5111', '5111_C268_003.npsf', '', '', '', '']
    ['5112', '5112_C026_523.npsf', '', '', '', '']
    ['5113', '5113_C264_010.npsf', '', '', '', '']
    ['5114', '5114_C264_011.npsf', '', '', '', '']

Doing so right away wil display all tracks present in the project. In the case of ACZ's radio lines, 5115. Quite a lot, and you don't always want to display 5000+ lines every time.
By using **SET_DISPLAY_INTERVAL**, you can limit what tracks are shown when using **DISPLAY_TRACKS**:

    0 - CHOOSE_TRACK
    1 - DISPLAY_TRACKS
    2 - SET_DISPLAY_INTERVAL
    3 - HELP
    4 - SAVE_AND_EXIT

    Enter index: 2
    SET_DISPLAY_INTERVAL
    Choose the interval of tracks you wish to see displayed when using DISPLAY_TRACKS
    Range: 0-5115
    First index (first track is 0):
    Enter index: 14
    Last index (last track is 5115): 
    Enter index: 20
    Chosen interval: 14-20
    0 - CHOOSE_TRACK
    1 - DISPLAY_TRACKS
    2 - SET_DISPLAY_INTERVAL
    3 - HELP
    4 - SAVE_AND_EXIT

    Enter index: 1
    DISPLAY_TRACKS
    ['CHARACTER', 'MISSION_NUMBER', 'ACE_STYLE', 'TEXT']
    ['14', '0014_C001_015.npsf', 'Pixy', '1', '?', "Galm 2 to Galm 1. I'll leave the orders to you. Give us a good show."]
    ['15', '0015_C001_016.npsf', 'Pixy', '1', 'NONE', 'Cipher. I have a feeling you and me are gonna get along just fine.']
    ['16', '0016_C001_017.npsf', 'Pixy', '1', 'NONE', 'Buddy.']
    ['17', '0017_ACZ_VoiceDummy02FX.npsf', '', '', '', '']
    ['18', '0018_ACZ_VoiceDummy02FX.npsf', '', '', '', '']
    ['19', '0019_C001_020.npsf', '', '', '', '']
    ['20', '0020_C001_021.npsf', '', '', '', '']

In this case, I chose the interval 14-20 and only those lines will be displayed. The line we will alter now is line 14.

#### INPUTTING DATA
With the desired tracks set, let's now alter them by using the **CHOOSE_TRACK** command:

    0 - CHOOSE_TRACK
    1 - DISPLAY_TRACKS
    2 - SET_DISPLAY_INTERVAL
    3 - HELP
    4 - SAVE_AND_EXIT

    Enter index: 0

Choose option 0, for **CHOOSE_TRACK**, and input the desired line index

    CHOOSE_TRACK
    Enter index: 14
    Chosen track: 14

    ID: 14 - TRACK: 0014_C001_015.npsf
    ['CHARACTER', 'MISSION_NUMBER', 'ACE_STYLE', 'TEXT']
    ['Pixy', '1', '?', "Galm 2 to Galm 1. I'll leave the orders to you. Give us a good show."] - CURRENTLY SAVED

    0 - PLAYBACK
    1 - SHOW_DATA
    2 - ENTER_DATA
    3 - BACK
    4 - HELP
    5 - SAVE_AND_EXIT

    Enter index:

DOCUMENTATION IN PROGRESS

## CSV DATA
This tool uses a custom .csv separator and quotechar.

SEPARATOR: \\

QUOTECHAR: `


## ROADMAP

    ! - Completed
    @ - In progress
    # - Soon to be started

This tool is a WIP. Some of the features implement and objectives to reach are the following:

- Organize files: When prompted, make a copy of the tracks and separate them in folders based on the indexing criteria

- Enforce preset values - Use preset values to spare the typing and avoid typos

- Detect dummy files automatically - Dummy files have the word "Dummy" in their filenames. Detect it and mark line accordingly

- Move the indexing criterion field from hard-coded to a list in the project.ACL file. This will ensure the tool is more customizeable and can be suited to more situations

- Add hooks for easier autocomplete.
    - This will allow for less typing for many repeated data, like character names.
    - Add newly input values to autocomplete
- Integrate with the text decoding utilities
    - As the radio text data extracted with other tools already has text, character name and mission attached, they might help a lot with the process! It may make sense to integrate both tools into a single package.
    - It also will help with fighting text discrepancies with the in-game text that would naturally happen when typing by ear
- Implement the second part of the tool, where it guides the dubbing and organizing process, not only the indexing process.

- Consider restructuring the code. The current structure was created for the old, linear workflow. With the new changes to the UI, the old structure showed itself limiting. This might hinder the next developments of the project, which include tools for better organizing a dubbing job.
    - Considering this code is almost a year old (I could swear this was older!)