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
  # def __init__(self, parent, title_arg, vars, *args, **kwargs):
  def __init__(self, parent, vars, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    
    # Root geometry
    parent.title("Display Application")
    parent.geometry('800x600+50+10')  # 800x600 ->1280x720 (16:9) -> 1920x1080
    parent.resizable(False, False) # comment out for testing.

    # Expand the 2 columns
    self.columnconfigure(0, weight=4)
    self.columnconfigure(1, weight=1)

    i = 0
    for key,var in vars.items() :
      if key == 'title':
        var['txt_var'].set(var['text'])
        tk.Label(self, textvariable=var['txt_var'], font= var['font']
        ).grid(columnspan=2,sticky=tk.EW)
      else :
        if key != 'status' : # Variables value and their units
          var['txt_var'].set(var['value'])
          tk.Label(self, textvariable = var['txt_var'],font= var['font'][0]
          ).grid(row=i+1, column=0,sticky=tk.EW)
          tk.Label(self, text=var['units'], font=var['font'][1]
          ).grid(row=i+1, column=1, sticky=tk.W)
          i += 1

class StatusFrame(tk.Frame):
  """Status Frame holds status and notifications """
  def __init__(self, parent, var, event, font_arg, *args, **kwargs):
    kwargs['relief'] = 'groove'
    kwargs['borderwidth'] = 5
    super().__init__(parent, *args, **kwargs)
    pad = {'padx': 10, 'pady': 5}
    ttk.Label( self, text="1",font=font_arg).grid(row=0, column=0, **pad)
    ttk.Label( self, textvariable=var, font=font_arg).grid(sticky=tk.W, row=0, column=1, **pad)
    ttk.Label( self, text="3",font=font_arg).grid(row=0, column=2, **pad)
    b1 = tk.Button( self, text='ACK',repeatdelay=100, repeatinterval= 250, font=font_arg) # ttk no font
    b1.grid(row=0, column=3, sticky=tk.E ) # padx='10', pady=5)
    self.columnconfigure(1, weight=1)
    b1.configure(command=event)

class Application(tk.Tk):
  """Line Display root window"""
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) # self = tk.Tk

    fonts = {
      'title': font.Font( family='Anta', size=30, weight='bold', slant='roman', underline=False, overstrike=False ),
      'value': font.Font( family='Anta', size=80, weight='bold', slant='roman', underline=False, overstrike=False ),
      'unit' : font.Font( family='Anta', size=30, weight='normal', slant='italic', underline=False, overstrike=False ),
      'status': font.Font( family='Arial', size=18, weight='bold', slant='roman', underline=False, overstrike=False )
    }
    self.ack = False
    self.vars = {
      'title': { 'text': 'Line 1 Production Status 2', 'txt_var': tk.StringVar(), 'font': fonts['title'] },
      'speed': { 'value': 0.0, 'txt_var': tk.StringVar(), 'units': 'mt/min', 'font': (fonts['value'], fonts['unit']) },
      'total': { 'value': 0.0, 'txt_var': tk.StringVar(), 'units': 'mt', 'font': (fonts['value'], fonts['unit']) },
      'status': tk.StringVar() 
    }

    # Main Frame is at row 0 and expand it in row and column 
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0,weight=1)
    main_frame_args = { 'relief': 'groove' ,'borderwidth': 5 } 
    MainFrame(self, self.vars, **main_frame_args ).grid(padx=10, pady=10, sticky=tk.NSEW)
    StatusFrame(self, self.vars['status'], self.on_ack, fonts['status'] ).grid(padx=10, pady=10, sticky=tk.NSEW)
    
    # Init some display data
    self.ticks = 0
    self.vars['speed']['value'] = 100.0
    self.vars['status'].set('Start Application')

    # Trigger first periodic task
    self.after(2500, self.periodic_task)
  
  def on_ack(self) :
    """User ACK status"""
    self.ack = True
    
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

    if self.ack :
      self.vars['status'].set('Acknowledged!')
      self.ack = False
    else :
      self.vars['status'].set(status)

    self.after(250, self.periodic_task)
    
if __name__ == "__main__":
  app = Application()
  app.mainloop()