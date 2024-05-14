import psycopg2
from MVVM.View import Inretface, Compare_Window

import MVVM.Model.DNS_Parsing
from MVVM.View import Inretface
from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen
def Main_Compare():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="Log680968amr", host="127.0.0.1")
    cursor = conn.cursor()

    query_DNS = """ SELECT * FROM DNS WHERE name LIKE '%s'""" % "%{}%".format((Inretface.App_Interface().input))
    query_Citilink = """ SELECT * FROM citilink WHERE name LIKE '%s'""" % "%{}%".format((Inretface.App_Interface().input))

    cursor.execute(query_DNS)
    result_DNS = cursor.fetchall(image_names())##############
    print(result_DNS)



    url = result_DNS.get(image_names())

    image = Image.open(urlopen(url))

    # создаем рабочую область
    frame = Frame(Compare_Window.CompareWindow().Compare_Window().compare_window)
    frame.grid()
    # Добавим метку
    label = Label(frame).grid(row=1, column=1)

    # Добавим изображение
    canvas = Canvas(Compare_Window.CompareWindow().Compare_Window().compare_window, height=100, width=50)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.grid(row=2, column=1)
    Compare_Window.CompareWindow().Compare_Window().compare_window.mainloop()






    cursor.execute(query_Citilink)
    result_Citilink = cursor.fetchall()
    print(result_Citilink)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    Main_Compare()