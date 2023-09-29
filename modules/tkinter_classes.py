# This file contains classes for the tkinter menus and custom widgets

import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import *
from ttkwidgets.autocomplete import *
#from tkinter.messagebox import showinfo

class RadioboxFrame():
    # This widget prompts the user to input data from a tuple of fields.
    # Fields must be formatted as such:
    # (option1, option2)

    def __init__(self, parent, name, frame_text, fields):
        self.parent  = parent
        self.name = name
        
        self.fields = fields

        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
            #width=60,
            #fg = '#AAAAAA',
            #bg = '#AAAAAA'
        )

        self.value = tk.StringVar()

        for index, value in enumerate(fields):
            entry = ttk.Radiobutton(
            self.frame1,
            text=value,
            variable=self.value,
            value=value
            )
            #entry.grid(row=index, column=0) # Put them side by side.
            entry.pack(anchor=tk.W)
    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)

class ProjectMetaPromptFrame(Toplevel):
    # Options must be formatted as such:
    # ( (field1, (option1, option2)), (field2, (option1, option2)) )
    def __init__(self, parent, name, frame_text, fields):
        self.parent  = parent
        self.name = name
        
        self.frame1 = LabelFrame(
            parent,
            text=frame_text,
        )

        popup = Toplevel()
        popup.attributes("-topmost", True)

        # Create GUI for project metadata if project is new
        game = RadioboxFrame(popup, 'game_frame', fields[0][0], fields[0][1])
        game.grid(row=0, column=0)

        # Create GUI for project choosing
        track_type = RadioboxFrame(popup, 'track_frame', fields[1][0], fields[1][1])
        track_type.grid(row=0, column=1)
    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)




class ChooseProjectPrompt():
    def __init__(self, parent, name, frame_text, project_list, action):
        self.parent  = parent
        self.name = name
        
        popup = Toplevel()
        popup.attributes("-topmost", True)

        self.frame1 = LabelFrame(
            popup,
            text=frame_text,
        )
        #self.frame1 = frame1        

        # Create GUI for project choosing
        self.project_var = tk.StringVar()
        self.project_prompt = ttk.Menubutton(
            self.frame1,
            textvariable=self.project_var
        )
        menu = tk.Menu(self.project_prompt, tearoff=False)        
        for project in project_list:
            menu.add_radiobutton(
                label=project,
                value=project,
                variable=self.project_var)
        self.project_prompt['menu'] = menu
        self.project_prompt.pack()

        

    
    # Apply grid() functionality to this class
    def grid(self, **kwargs):
        self.frame1.grid(kwargs)
    
    def get_value(self):
        project_choice = self.project_var.get()
        
        print(project_choice)

