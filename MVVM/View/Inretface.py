from tkinter import *

def App_Interface():
    main_window = Tk()
    main_window.title("Ekelmende")
    main_window.geometry("1050x1050")

    buttton = Button(main_window, width=10,
                 height=2, text="Поиск",
                 bg="Red", fg="white",
                 command=App_Interface)

    input = Entry(main_window, width=50, borderwidth=10).place(x=300, y=200)
    buttton.place(x=623, y=197)
    main_window.mainloop()























if __name__ == "__main__":
    App_Interface()