#!/usr/bin/python3
"""Line Display

Basic Framework from tkinter_classes_demo
Compound widgets: LabelInput-> LabelOut
MyForm -> DisplayForm
"""
import tkinter as tk
from tkinter import ttk
import json

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

class LabelOut(tk.Frame):
  """A label (variable) and units combined together"""

  def __init__(
    self, parent, var_out, units, *args, **kwargs
   ):
    super().__init__(parent, *args, **kwargs)   # parent
    self.monitor = tk.Label(self, textvariable=var_out, anchor='w')
    self.units = tk.Label(self, text=units, anchor='w')
    
    # side-by-side layout
    self.columnconfigure(0, weight=3)
    self.columnconfigure(1, weight=1)
    self.monitor.grid(sticky=tk.EW)
    self.units.grid(row=0, column=1, sticky=tk.EW)

# class DisplayForm(tk.Frame):
#   """Monitor a Variable with Engineering Units"""

#   def __init__(
#     self, parent, label, units,
#     inp_args, *args, **kwargs
#    ):
#     super().__init__(parent, *args, **kwargs)   # parent
#     self.label = tk.Label(self, text=label, anchor=tk.W)
#     self.units = tk.Label(self, text=units, anchor=tk.CENTER)

#     # side-by-side layout
#     self.columnconfigure(0, weight=1)
#     self.label.grid(sticky=tk.E + tk.W)
#     self.units.grid(row=0, column=1, sticky=tk.E + tk.W)


class DisplayForm(tk.Frame):

  def __init__(self, parent, data_var, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    self.data_var = data_var
    self._vars = {
      'speed': tk.StringVar(),
      'total': tk.StringVar(),
    }
    self.columnconfigure(0, weight=4)
    self.columnconfigure(1, weight=1)
    self._vars['speed'].set('Mil1999')
    tk.Label(self, textvariable=self._vars['speed']).grid(sticky=tk.EW)
    tk.Label(self, text='meters').grid(row=0, column=1, sticky=tk.EW)




    # self._vars['speed'] = '123'
    # LabelOut(
    #   self,
    #   {'textvariable': self._vars['speed']},
    #   'mt/sec'
    # ).grid(sticky=tk.E + tk.W)
    # # LabelOut(
    #   self,
    #   {'textvariable': self._vars['total']},
    #   'meters'
    # ).grid(sticky=tk.E + tk.W)

class Application(tk.Tk):
  """Line Display root window"""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) # self = tk.Tk

    self.jsonvar = JSONVar()
    self.output_var = tk.StringVar()

    self.title("SCIA Line Display") # move to the FRM
    self.geometry('800x600+50+10')
    DisplayForm(self, self.jsonvar).grid(sticky=tk.NSEW)
    self.columnconfigure(0, weight=1)

    # # status bar
    # self.status = tk.StringVar()
    # ttk.Label(
    #   self, textvariable=self.status
    # ).grid(sticky=(tk.W + tk.E), row=2, padx=10)

    # self._records_saved = 0




if __name__ == "__main__":

  app = Application()
  app.mainloop()