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
acestyle_values = ['MERCENARY', 'SOLDIER', 'KNIGHT', 'NONE']

#endregion



import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from ttkwidgets.autocomplete import *
from tkinter.messagebox import showinfo


def setup_root_window():
    global root
    root = tk.Tk()
    root.title('AC5-Z_RADIO_LINES_ORGANIZER')

    window_width = 800
    window_heigth = 400

    root.geometry(f'{window_width}x{window_heigth}')

    root.config(bg='#ffffff')

    
 
class FieldInput():
    '''This class sets the baseline characteristics 
    for the widgets, including font, font size, and colors
    '''
    # Output vars
    #acestyle_value = ''
    
    # Attributes
    varFont = "Calibri"
    fontSize = 14
    varFG = "#000000"
    varBG = "grey"
    
    # Constructor
    def __init__(self, parent, name, frame_text, std_values, isradio, width):
        self.parent  = parent
        self.name = name
        self.frame_text = frame_text
        
        self.sisradio = isradio # Just so I can access "isradio"
        self.acestyle_value = tk.StringVar()

        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
            width=width,
            fg = self.varFG, 
            bg = self.varBG,

        )
        
        if isradio: # If radio button option was chosen
            
            for index, value in enumerate(std_values):
                self.entry = ttk.Radiobutton(
                self.frame1,
                text=value,
                variable=self.acestyle_value,
                value=value
                )
                self.entry.grid(row=index, column=0) # Put them side by side.
            pass
        else: # Display options as autocomplete combo box
            pass
            self.entry = AutocompleteCombobox(
                self.frame1,
                #width=width, 
                font=('Times', 14),
                completevalues=std_values
                )
            self.entry.grid(row=0, column=0)
    
         # Create a button to get the selected value
        self.get_value_button = ttk.Button(self.frame1, text="Get Value", command=self.get_combobox_value)
        self.get_value_button.grid(row=6, column=0)
        #self.get_value_button.pack()

    # Allows you to grid as you would normally
    # Can subsitute pack() here or have both class methods
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
        #self.label.grid(kwargs)
        #self.entry.grid(kwargs)

    def get_combobox_value(self):
        selected_value = ''
        if self.sisradio:
            selected_value = self.acestyle_value.get()
        else:
            selected_value = self.entry.get()
        
        print(f"Selected value: {selected_value}")
        return selected_value
        
class LineInputMenu():
    def __init__(self, parent, name, frame_text, isACZ, isRadio, width):
        self.parent  = parent
        self.name = name
        self.frame_text = frame_text
        
        self.sisACZ = isACZ # If True, use values for ACZ. Else, use AC5
        self.sisRadio = isRadio # If True, tracks are RADIO lines.


        # Create an instance of your class
        char_field = FieldInput(root, "character_field","Character", character_values, False, 20)
        char_field.grid(row=0, column=0)

        miss_field = FieldInput(root, "mission_field","Mission", mission_values, False, 20)
        miss_field.grid(row=1, column=0)

        acestyle_values.append('?')
        acesty_field = FieldInput(root, "acestyle_field","Ace Style", acestyle_values, True, 60)
        acesty_field.grid(row=1, column=1)

        txt_field = FieldInput(root, "text_field","Text", text_values, False, 200)
        txt_field.grid(row=0, column=1)
        
        


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

    while False:

        # Create an instance of your class
        sectionHeader = FieldInput(root, "character_field","Character", character_values, False, 20)
        sectionHeader.grid(row=0, column=0)

        sectionHeader3 = FieldInput(root, "mission_field","Mission", mission_values, False, 20)
        sectionHeader3.grid(row=1, column=0)

        acestyle_values.append('?')
        sectionHeader4 = FieldInput(root, "acestyle_field","Ace Style", acestyle_values, True, 60)
        sectionHeader4.grid(row=1, column=1)

        sectionHeader2 = FieldInput(root, "text_field","Text", text_values, False, 60)
        sectionHeader2.grid(row=0, column=1)

        ####

        # Create a Tkinter variable to store the selected option
        var = tk.StringVar()

        # Create Radiobuttons
        option1 = tk.Radiobutton(root, text="Option 1", variable=var, value="Option 1")
        option2 = tk.Radiobutton(root, text="Option 2", variable=var, value="Option 2")
        option3 = tk.Radiobutton(root, text="Option 3", variable=var, value="Option 3")
    
    linemenu = LineInputMenu(root, 'line_menu', 'Fields Input Menu', True, True, 100)


    root.mainloop()


if __name__ == '__main__':
    main()










