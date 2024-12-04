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
# import json
from tkinter import font

class MainFrame(tk.Frame):
  """Main Frame holds application widgets"""
  def __init__(self, parent, vars, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    # Define fonts styles 
    title_font = font.Font( family='Anta', size=30,
    weight='bold', slant='roman', underline=False, overstrike=False
    )
    value_font = font.Font( family='Anta', size=80,
    weight='bold', slant='roman', underline=False, overstrike=False
    )
    unit_font = font.Font( family='Anta', size=30,
    weight='normal', slant='italic', underline=False, overstrike=False
    )
    
    # Root geometry
    parent.title("Display Application")
    parent.geometry('800x600+50+10')  # 800x600 ->1280x720 (16:9) -> 1920x1080
    parent.resizable(False, False) # comment out for testing.

    self.title_var = tk.StringVar()
    # self.speed_var = tk.DoubleVar() # tk.StringVar()
    self.speed_units = 'mt/min'
    self.total_var = tk.StringVar()
    self.total_units = 'mt'
    
    self.title_var.set('Line 1 Production Status')
    
    # Expand the 2 columns
    self.columnconfigure(0, weight=4)
    self.columnconfigure(1, weight=1)

    tk.Label(self, textvariable=self.title_var, font= title_font).grid(columnspan=2,sticky=tk.EW) #kwargs['title'].grid(sticky=tk.EW)
    i = 0
    for key,var in vars.items() :
      var['txt_var'].set(var['value'])
      tk.Label(self, textvariable = var['txt_var'], 
             font= value_font).grid(row=i+1, column=0,sticky=tk.EW)
      tk.Label(self, text=var['units'], font=unit_font).grid(row=i+1, column=1, sticky=tk.W)
      i += 1
  

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

    self.status_var = tk.StringVar()

    self.vars = {
      'speed': { 'value': 0.0, 'txt_var': tk.StringVar(), 'units': 'mt/min' },
      'total': { 'value': 0.0, 'txt_var': tk.StringVar(), 'units': 'mt' },
    }

    # Main Frame is at row 0 and expand it in row and column 
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0,weight=1)
    main_frame_args = { 'relief': 'groove' ,'borderwidth': 5 } 
    self.mf = MainFrame(self, self.vars, **main_frame_args ).grid(padx=10, pady=10, sticky=tk.NSEW)
    
    self.status_var = tk.StringVar()
    StatusFrame(self, self.status_var ).grid(padx=10, pady=10, sticky=tk.NSEW)
    
    # Init some display data
    self.ticks = 0
    self.vars['speed']['value'] = 100.0
    
    # Trigger first periodic task
    self.after(2500, self.periodic_task)
    
  def periodic_task(self) :
    speed = self.vars['speed']  # reference alias
    if speed['value'] < 105 :
      speed['value'] += 0.01
      status = "Accelerating to 105"
    else :
      status = "Speed reached"
    speed['txt_var'].set(f'{speed['value']:.2f}')

    total = self.vars['total']  # reference alias
    total['value'] += speed['value']/100 
    total['txt_var'].set( f'{total['value']:.1f}')
    if total['value'] > 600:
      status = "Length above 600"

    self.status_var.set(status)
    self.after(250, self.periodic_task)
    
if __name__ == "__main__":
  app = Application()
  app.mainloop()