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

  def __init__(self, *args_debug, **kwargs_debug):
    kwargs_debug['value'] = json.dumps(kwargs_debug.get('value'))
    super().__init__(*args_debug, **kwargs_debug)

  def set(self, value, *args_debug, **kwargs_debug):
    string = json.dumps(value)
    super().set(string, *args_debug, **kwargs_debug)

  def get(self, *args_debug, **kwargs_debug):
    """Get the list or dict value"""
    string = super().get(*args_debug, **kwargs_debug)
    return json.loads(string)

class MainFrame(tk.Frame):
  """Main Frame holds application widgets"""
  def __init__(self, parent, data_var, *args_debug, **kwargs_debug):
    super().__init__(parent, *args_debug, **kwargs_debug)
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

    tk.Label(self, textvariable=self.title_var, font= title_font).grid(columnspan=2,sticky=tk.EW) #kwargs_debug['title'].grid(sticky=tk.EW)
    tk.Label(self, textvariable=self.speed_var, font= value_font).grid(row=1, column=0,sticky=tk.EW)
    tk.Label(self, text=self.speed_units, font=unit_font).grid(row=1, column=1, sticky=tk.W)
    tk.Label(self, textvariable=self.total_var, font= value_font).grid(row=2,column=0,sticky=tk.EW)
    tk.Label(self, text=self.total_units, font=unit_font).grid(row=2,column=1, sticky=tk.W)

class StatusFrame(tk.Frame):
  """Status Frame holds status and notifications """
  def __init__(self, parent, *args, **kwargs):
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
    



class Application(tk.Tk):
  """Line Display root window"""

  def __init__(self, *args_debug, **kwargs_debug):
    super().__init__(*args_debug, **kwargs_debug) # self = tk.Tk

    self.jsonvar = dict()# JSONVar()
    
    self.output_var = tk.StringVar()
    self.status = tk.StringVar()

    # Main Frame is at row 0 and expand it in row and column 
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0,weight=1)
    args_debug = { 'relief': 'solid' ,'borderwidth': 5 } 
    MainFrame(self, self.jsonvar, **args_debug ).grid(sticky=tk.NSEW)

    # row 0..99 Variables units, row 100 status
    # self.rowconfigure(99,weight=1)  # expand the last row before status (100)
    # self.rowconfigure(0,weight=1)  # MainFrame is r0 
    # status_frame = ttk.LabelFrame(self, text='Status Frame')  # Arrange status widgets
    status_frame = ttk.Frame(self,relief='groove')  # Arrange status widgets
    self.status = tk.StringVar()
    self.status_font = font.Font( family='Arial', size=18,
      weight='bold', slant='roman', underline=False, overstrike=False )
    status_args = { 'padx': 10, 'pady': 5}    
    ttk.Label( status_frame, text="1",font=self.status_font).grid(row=0, column=0, **status_args)
    ttk.Label( status_frame, textvariable=self.status, font=self.status_font).grid(row=0, column=1)
    ttk.Label( status_frame, text="3",font=self.status_font).grid(row=0, column=2)
    b1 = tk.Button( status_frame, text='ACK',font=self.status_font) # ttk no font
    b1.grid(row=0, column=3, sticky=tk.E, **status_args) # padx='10', pady=5)
    
    status_frame.grid(row=1, padx=10, pady=10, sticky=tk.EW)
    status_frame.columnconfigure(1, weight=1)
    
    self.after(500, self.periodic_task)
    self.ticks = 0

  
  def periodic_task(self) :
    self.after(250, self.periodic_task)
    self.ticks += 1
    self.status.set(f'Ticks {self.ticks}')

if __name__ == "__main__":

  app = Application()
  app.mainloop()