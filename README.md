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
### PROJECTS:
The program separates its files into projects. Since indexing projects are expected to take longer than a simple unpacking, you can work on many indexing projects in paralel without worries.

When running the script, you will be prompted to choose which project to open, or to create one. When running the script for the first time, creating a new project will be the only option.

### IMPORTING TRACKS
When opening a project for the first time, the program will close, prompting you to copy the radio lines to their final folder. Then, run the script again and use it normally.

    There are no tracks to be indexed!
    Copy tracks to the "lines" folder
    PRESS ENTER TO EXIT

### NORMAL USAGE
With the project ready, we can start working. The process starts automatically.

#### HELP PROMPT
A help prompt explaining the special commands will appear. It reads:

    Time to fill out the data!
    Special commands:
    "COMMAND" - Description
    dummy - Dummy data. The whole line will be marked as such
    || - Skip line. Skip whole line without inputting anything
    ? - Unknown data. When you don't know the answer for a field
    ?: - Unknown line. Mark whole line as unknown
    \ - Terminate. Stop inputting data, save and quit application
    PRESS ENTER TO CONTINUE

Press enter when ready to begin.

#### INPUTTING DATA
The script will print out the track's file name and first field to be filled out. It will also play the track through MFAudio. It can be replayed as much as you wish. Input the fields and you can close MFAudio when done.

As the current track is finished, the next one will come right after. Repeat the process.

Examples:

The first file for ACZ is a dummy file. They are frequent, so they have their own "dummy" command, so we can skip them with a single input.

    0000_ACZ_VoiceDummy02FX.npsf
    Enter your data for CHARACTER: dummy

The first non-dummy file is one of Pixy's lines. Let's see how it will be filled out:

    0014_C001_015.npsf
    Enter your data for CHARACTER: Pixy
    Enter your data for MISSION_NUMBER: 1
    Choose preset data for ACE_STYLE: 
    0 - MERCENARY
    1 - SOLDIER
    2 - KNIGHT
    3 - NONE
    4 - Other

    Enter index: 3
    Enter your data for TEXT: Galm 2 to Galm 1. I'll leave the orders to you. Give us a good show!

As you can see, the "ACE_STYLE" field has preset values to choose from, but it also gives you the option to input a custom value.


## CSV DATA
This tool uses a custom .csv separator and quotechar.
SEPARATOR: \
QUOTECHAR: `


## ROADMAP
This tool is a WIP. Some of the features implement and objectives to reach are the following:

- Organize files: When prompted, make a copy of the tracks and separate them in folders based on the indexing criteria

- Enforce preset values - Use preset values to spare the typing and avoid typos

- Detect dummy files automatically - Dummy files have the word "Dummy" in their filenames. Detect it and mark line accordingly
