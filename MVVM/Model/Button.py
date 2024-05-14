from MVVM.View import Inretface, Compare_Window
from tkinter import *
import Compare

from MVVM.View.Compare_Window import CompareWindow


class Button:
    def Button_clicked(event):
        Compare_Window.CompareWindow().Compare_Window()


        Compare.Main_Compare()

Inretface.App_Interface().button.bind("<Button-1>", Button.Button_clicked)





Inretface.App_Interface().button(command=Button.Button_clicked)
Inretface.App_Interface().button.pack()
Inretface.App_Interface().main_window.mainloop()