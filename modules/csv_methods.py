# This module contains custom csv functions necessary for the main script to work
import csv



def get_rows_line_data_csv(file_path):
    # Opens csv and returns all rows
    with open(file_path, mode='r', encoding='UTF8', newline='') as line_file: # Open file
        csv_reader = csv.reader(line_file, delimiter='\\', quotechar='`')
        return (x for x in csv_reader)

def write_row_line_data_csv(data, is_list, file_path):
    # Write to the csv file.
    #
    # If append == True, append to file.
    # Else, overwrite it.
    #
    # If is_list, write all items of iterables as rows
    # Else, write a single row only

    #mode = ''
    #if append:
    #    mode = 'a'
    #else:
    #    mode = 'w'
#
    with open(file_path, 'w', encoding='UTF8', newline='') as line_file: # Create file
            line_writer = csv.writer(line_file, delimiter='\\', quotechar='`')
            if is_list:
                line_writer.writerows(data)
            else:
                line_writer.writerow(data)