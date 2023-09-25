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

    
 
class ui_Labels():
    '''This class sets the baseline characteristics 
    for the widgets, including font, font size, and colors
    '''

    # Attributes
    varFont = "Calibri"
    fontSize = 14
    varFG = "#F2F2F2"
    varBG = "#3b3b3b"
    
    # Constructor
    def __init__(self, parent, name, varText):
        self.parent  = parent
        self.name = name
        self.varText = varText

        self.label = tk.Label(
            parent, 
            text = varText, 
            fg = self.varFG, 
            bg = self.varBG, 
            font = (self.varFont, self.fontSize)
            )

    # Allows you to grid as you would normally
    # Can subsitute pack() here or have both class methods
    def grid(self, **kwargs):
        self.label.grid(kwargs)



def lines_input_prompt():
    global root
    global INDEXING_CRITERIA
    frame = Frame(root, bg='#f25252')
    frame.pack(expand=True)

    Label(
        frame, 
        bg='#f25252',
        font = ('Times',21),
        text='Field data'
        ).pack()
    
    frame.grid(row=0, column=0)

    entry = AutocompleteCombobox(
        frame,
        text = 'aaaaa',
        width=30, 
        font=('Times', 18),
        completevalues=INDEXING_CRITERIA[3][1]
        )
    
    entry2 = AutocompleteCombobox(
        frame,
        text = 'aaaaa',
        width=30, 
        font=('Times', 18),
        completevalues=INDEXING_CRITERIA[3][1]
        )
    entry.pack()
    entry2.pack()

def main():
    setup_root_window()
    #lines_input_prompt()

    # Create an instance of your class
    sectionHeader = ui_Labels(root, "Section Header","Magic XML Iterator")
    sectionHeader.grid(row=0, column=0)

    sectionHeader2 = ui_Labels(root, "Section aaaa","Magic HU3 Iterator")
    sectionHeader2.grid(row=0, column=1)

    sectionHeader3 = ui_Labels(root, "Section uuuuu","Magic LULZ Iterator")
    sectionHeader3.grid(row=0, column=3)


    root.mainloop()


if __name__ == '__main__':
    main()










