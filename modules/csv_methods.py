# This module contains custom csv functions necessary for the main script to work
import csv

DELIMITER = '\\'
QUOTECHAR = '`'

def get_rows_line_data_csv(file_path):
    '''This method returns a tuple containing every line read from the file specified in 'file path' '''
    global DELIMITER
    global QUOTECHAR
    # Opens csv and returns all rows
    with open(file_path, mode='r', encoding='UTF8', newline='') as line_file: # Open file
        csv_reader = csv.reader(line_file, delimiter=DELIMITER, quotechar=QUOTECHAR)
        return (x for x in csv_reader)

def write_row_line_data_csv(data, many_lines, file_path):
    '''This method writes data to the file specified in 'file path'
    Parameters:
    data: Data to be written
    many_lines: Determines if you are writing a single line or many lines
    file_path: Path to the desired file
    '''
    global DELIMITER
    global QUOTECHAR
    # Write to the csv file.
    #
    # If append == True, append to file.
    # Else, overwrite it.
    #
    # If many_lines, write all items of iterables as rows
    # Else, write a single row only

    #mode = ''
    #if append:
    #    mode = 'a'
    #else:
    #    mode = 'w'
#
    with open(file_path, 'w', encoding='UTF8', newline='') as line_file: # Create file
            line_writer = csv.writer(line_file, delimiter=DELIMITER, quotechar=QUOTECHAR)
            if many_lines:
                line_writer.writerows(data)
            else:
                line_writer.writerow(data)