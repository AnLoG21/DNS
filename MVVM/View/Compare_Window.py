from MVVM.View import Inretface
from tkinter import *


class CompareWindow():
    def Compare_Window(self):
        geometry = Inretface.App_Interface().main_window.geometry().split('+')
        x = geometry[-2]
        y = geometry[-1]
        Inretface.App_Interface().main_window.destroy()
        compare_window = Tk()
        compare_window.title('Compare Window')
        compare_window.geometry("1050x1050")
        compare_window.mainloop()
