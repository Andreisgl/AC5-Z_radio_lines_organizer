#region
words = ['apple', 'banana', 'cherry', 'grape', 'kiwi', 'orange', 'pear', 'strawberry']

# Each entry is a tuple. First item in the tuple is the criterion name,
# second is a list with autocomplete values
INDEXING_CRITERIA = (('CHARACTER', []),
                     ('TEXT', []),
                     ('MISSION', []),
                     ('ACE_STYLE', ['MERCENARY', 'SOLDIER', 'KNIGHT'])
                     )

#endregion



import tkinter as tk
from tkinter import *
from ttkwidgets.autocomplete import *


def setup_root_window():
    global root
    root = tk.Tk()
    root.title('AC5-Z_RADIO_LINES_ORGANIZER')

    window_width = 400
    window_heigth = 300

    root.geometry(f'{window_width}x{window_heigth}')

    root.config(bg='#ffffff')

    
 



def lines_input_prompt():
    global root
    frame = Frame(root, bg='#f25252')
    frame.pack(expand=True)

    Label(
        frame, 
        bg='#f25252',
        font = ('Times',21),
        text='Field data'
        ).pack()

    entry = AutocompleteCombobox(
        frame,
        text = 'aaaaa',
        width=30, 
        font=('Times', 18),
        completevalues=INDEXING_CRITERIA[3][1]
        )
    entry.pack()

def main():
    setup_root_window()
    lines_input_prompt()

    root.mainloop()


if __name__ == '__main__':
    main()










