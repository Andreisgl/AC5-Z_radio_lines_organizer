#region

# TODO: Change criteria in function of the chosen game
CURRENT_GAME = 'ACZ' # 'AC5'
INDEXING_CRITERIA = ('CHARACTER',
                     'TEXT',
                     'MISSION',
                     'ACE_STYLE', 
                     )


character_values = ['Pixy', 'AWACS', 'PJ']
text_values = ["Galm 2 to Galm 1. I'll leave the orders to you. give us a good show",
                                "Yo buddy, still alive?",
                                "Galm 1 was shot down!"]
# Mission values for both games
mission_values_acz = ('01', '02', '03', '04', '05',
                      '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27')
mission_values_ac5 = ('01','02', '03', '04', '05',
                      '06', '07', '08', '09', '10', '11A', '11B', '12A', '12B', '13', '14', '15', '16A', '16B', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27')
mission_values = mission_values_acz # Choose wich game's values to use
acestyle_values = ['MERCENARY', 'SOLDIER', 'KNIGHT']

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

    
 
class TrackField():
    '''This class sets the baseline characteristics 
    for the widgets, including font, font size, and colors
    '''

    # Attributes
    varFont = "Calibri"
    fontSize = 14
    varFG = "#000000"
    varBG = "grey"
    
    # Constructor
    def __init__(self, parent, name, label_text, width, std_values):
        self.parent  = parent
        self.name = name
        self.label_text = label_text
        
        self.frame1 = LabelFrame(
            parent,
            text=label_text,
            fg = self.varFG, 
            bg = self.varBG,

        )
        #self.label = tk.Label(
        #    self.frame1, 
        #    text = label_text,
        #    fg = self.varFG, 
        #    bg = self.varBG, 
        #    font = (self.varFont, self.fontSize),
        #    width=15
        #    )
        #self.label.grid(row=0, column=0)
        
        self.entry = AutocompleteCombobox(
            self.frame1,
            width=width, 
            font=('Times', 14),
            completevalues=std_values
            )
        self.entry.grid(row=0, column=0)

    # Allows you to grid as you would normally
    # Can subsitute pack() here or have both class methods
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
        #self.label.grid(kwargs)
        #self.entry.grid(kwargs)



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
    
    #entry2 = AutocompleteCombobox(
    #    frame,
    #    text = 'aaaaa',
    #    width=30, 
    #    font=('Times', 18),
    #    completevalues=INDEXING_CRITERIA[3][1]
    #    )
    #entry.pack()
    #entry2.pack()

def main():
    setup_root_window()
    #lines_input_prompt()

    # Create an instance of your class
    sectionHeader = TrackField(root, "character_field","Character", 20, character_values)
    sectionHeader.grid(row=0, column=0)

    sectionHeader3 = TrackField(root, "mission_field","Mission", 20, mission_values)
    sectionHeader3.grid(row=1, column=0)

    sectionHeader4 = TrackField(root, "acestyle_field","Ace Style", 20, acestyle_values)
    sectionHeader4.grid(row=2, column=0)

    sectionHeader2 = TrackField(root, "text_field","Text", 60, text_values)
    sectionHeader2.grid(row=0, column=1)


    root.mainloop()


if __name__ == '__main__':
    main()










