#!/usr/bin/python3
"""Line Speed and Status Indicator"""
import tkinter as tk
from tkinter import font

from pathlib import Path


# First line
root = tk.Tk()

# configure root
root.title('Line Indicator')
root.geometry('800x600')
root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=1)

# Title (subject)
title_font = font.Font(family='Helvetica', name='TitleFont', size=18, weight='bold')
title_frame = tk.Frame(root)
title_frame.columnconfigure(0, weight=1)
title_var = tk.StringVar()
tk.Label(title_frame, text='Line 1 Indicator',font=title_font).grid(sticky='we', padx=5, pady=5)
title_frame.grid(sticky=tk.EW)

# Measurements (message)
measurement_font = font.Font(family='Helvetica', name='MeasurementFont', size=24, weight='bold')
measurement_frm = tk.Frame(root)
measurement_frm.columnconfigure(0, weight=1)
measurement_frm.columnconfigure(1, weight=4)
speed_var = tk.StringVar()
total_var = tk.StringVar()

speed_var.set('1234.5')
total_var.set('123456')

speed_label = tk.Label(measurement_frm,textvariable=speed_var)
speed_units_label = tk.Label(measurement_frm,text='m/s')
speed_label.grid(row=0,column=0,sticky=tk.EW,ipadx=5, ipady=5)
speed_units_label.grid(row=0,column=1,sticky=tk.EW,ipadx=5, ipady=5)

total_label = tk.Label(measurement_frm,textvariable=total_var)
total_units_label = tk.Label(measurement_frm,text='mt')
total_label.grid(row=1,column=0,sticky=tk.EW,ipadx=5, ipady=5)
total_units_label.grid(row=1,column=1,sticky=tk.EW,ipadx=5, ipady=5)

measurement_frm.grid(sticky=tk.NSEW)

# Last line
root.mainloop()