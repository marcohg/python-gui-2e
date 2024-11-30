#!/usr/bin/python3
"""Line Display

Arrange in 2 columns 
- Subclass tk for the application
- Provide a MainFrame to place widgets
  - Title
  - Rows with variable-units
  - Status line 
- Update data to display from file
"""
import tkinter as tk
from tkinter import ttk
import json
from tkinter import font

class JSONVar(tk.StringVar):
  """A Tk variable that can hold dicts and lists"""

  def __init__(self, *args, **kwargs):
    kwargs['value'] = json.dumps(kwargs.get('value'))
    super().__init__(*args, **kwargs)

  def set(self, value, *args, **kwargs):
    string = json.dumps(value)
    super().set(string, *args, **kwargs)

  def get(self, *args, **kwargs):
    """Get the list or dict value"""
    string = super().get(*args, **kwargs)
    return json.loads(string)

class MainFrame(tk.Frame):
  """Main Frame holds application widgets"""
  def __init__(self, parent, data_var, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    # Define fonts styles 
    title_font = font.Font( family='Anta', size=30,
    weight='bold', slant='roman', underline=False, overstrike=False
    )
    value_font = font.Font( family='Anta', size=60,
    weight='bold', slant='roman', underline=False, overstrike=False
    )
    unit_font = font.Font( family='Anta', size=30,
    weight='normal', slant='italic', underline=False, overstrike=False
    )
    
    # Root geometry
    parent.title("Display Application")
    parent.geometry('800x600+50+10')  # 800x600 ->1280x720 (16:9) -> 1920x1080
    # parent.resizable(False, False) slide-in on last versions

    self.data_var = data_var
    self.title_var = tk.StringVar()
    self.speed_var = tk.StringVar()
    self.speed_units = 'mt/min'
    self.total_var = tk.StringVar()
    self.total_units = 'mt'
    
    self.title_var.set('Line 1 Production Status')
    self.speed_var.set('Spd:1234.5')
    self.total_var.set('12345.67')
    
    # Expand the 2 columns
    self.columnconfigure(0, weight=4)
    self.columnconfigure(1, weight=1)

    tk.Label(self, textvariable=self.title_var, font= title_font).grid(columnspan=2,sticky=tk.EW) #kwargs['title'].grid(sticky=tk.EW)
    tk.Label(self, textvariable=self.speed_var, font= value_font).grid(row=1, column=0,sticky=tk.EW)
    tk.Label(self, text=self.speed_units, font=unit_font).grid(row=1, column=1, sticky=tk.W)
    tk.Label(self, textvariable=self.total_var, font= value_font).grid(row=2,column=0,sticky=tk.EW)
    tk.Label(self, text=self.total_units, font=unit_font).grid(row=2,column=1, sticky=tk.W)

class StatusFrame(tk.Frame):
  """Status Frame holds status and notifications """
  def __init__(self, parent, status_var, *args, **kwargs):
    kwargs['relief'] = 'groove'
    kwargs['borderwidth'] = 5
    super().__init__(parent, *args, **kwargs)
    # Define fonts styles 
    self.status_font = font.Font( family='Arial', size=18,
      weight='bold', slant='roman', underline=False, overstrike=False 
      )

    pad = {'padx': 10, 'pady': 5}

    ttk.Label( self, text="1",font=self.status_font).grid(row=0, column=0, **pad)
    ttk.Label( self, textvariable=status_var, font=self.status_font).grid(sticky=tk.W, row=0, column=1, **pad)
    ttk.Label( self, text="3",font=self.status_font).grid(row=0, column=2, **pad)
    b1 = tk.Button( self, text='ACK',font=self.status_font) # ttk no font
    b1.grid(row=0, column=3, sticky=tk.E ) # padx='10', pady=5)
    
    # status_frame.grid(row=1, padx=10, pady=10, sticky=tk.EW)
    self.columnconfigure(1, weight=1)

class Application(tk.Tk):
  """Line Display root window"""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) # self = tk.Tk

    self.jsonvar = dict()# JSONVar()
    
    self.output_var = tk.StringVar()
    self.status_var = tk.StringVar()

    # Main Frame is at row 0 and expand it in row and column 
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0,weight=1)
    main_frame_args = { 'relief': 'groove' ,'borderwidth': 5 } 
    MainFrame(self, self.jsonvar, **main_frame_args ).grid(padx=10, pady=10, sticky=tk.NSEW)
    
    # status_frame_args = { 'relief': 'groove' ,'borderwidth': 5 } 
    self.status_var = tk.StringVar()
    StatusFrame(self, self.status_var ).grid(padx=10, pady=10, sticky=tk.NSEW)

    # status_frame = ttk.Frame(self,relief='groove', borderwidth=5)  # Arrange status widgets
    
    # self.status_font = font.Font( family='Arial', size=18,
    #   weight='bold', slant='roman', underline=False, overstrike=False )
    # status_args = { 'padx': 10, 'pady': 5}    
    # ttk.Label( status_frame, text="1",font=self.status_font).grid(row=0, column=0, **status_args)
    # ttk.Label( status_frame, textvariable=self.status_var, font=self.status_font).grid(row=0, column=1)
    # ttk.Label( status_frame, text="3",font=self.status_font).grid(row=0, column=2)
    # b1 = tk.Button( status_frame, text='ACK',font=self.status_font) # ttk no font
    # b1.grid(row=0, column=3, sticky=tk.E, **status_args) # padx='10', pady=5)
    
    # status_frame.grid(row=1, padx=10, pady=10, sticky=tk.EW)
    # status_frame.columnconfigure(1, weight=1)
    
    self.after(500, self.periodic_task)
    self.ticks = 0

  
  def periodic_task(self) :
    self.after(250, self.periodic_task)
    self.ticks += 1
    self.status_var.set(f'Ticks {self.ticks}')

if __name__ == "__main__":

  app = Application()
  app.mainloop()