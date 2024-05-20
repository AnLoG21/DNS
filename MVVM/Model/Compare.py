import psycopg2
from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen

widgets_to_destroy = []

def clear_widgets():
    global widgets_to_destroy
    for widget in widgets_to_destroy:
        widget.destroy()
    widgets_to_destroy = []  # Очищаем список после удаления виджетов

def search_word():
    global scrollable_frame, scrollbar, canvas, left_frame, right_frame, inner_frame
    clear_widgets()  # Очищаем окно перед новым поиском
    word = entry.get()
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="Log680968amr", host="127.0.0.1")
    cursor = conn.cursor()
    cursor.execute(f"SELECT name, price, image FROM DNS WHERE name LIKE '%{word}%'")
    result_DNS = cursor.fetchall()
    cursor.execute(f"SELECT name, price, image FROM citilink WHERE name LIKE '%{word}%'")
    result_Citilink = cursor.fetchall()

    # Создание фрейма с прокруткой
    scrollable_frame = Frame(window)
    scrollable_frame.pack(fill="both", expand=True)

    # Создание scrollbar
    scrollbar = Scrollbar(scrollable_frame)
    scrollbar.pack(side="right", fill="y")

    # Создание canvas для интеграции с scrollbar
    canvas = Canvas(scrollable_frame, yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)

    # Связываем scrollbar с canvas
    scrollbar.config(command=canvas.yview)

    # Создание внутреннего фрейма для размещения элементов
    inner_frame = Frame(canvas)

    # Добавление внутреннего фрейма на canvas
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Обновление прокрутки при изменении размера внутреннего фрейма
    def _configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", _configure_canvas)

    left_frame = Frame(inner_frame)
    left_frame.pack(side="left", fill="both", expand=True)
    right_frame = Frame(inner_frame)
    right_frame.pack(side="right", fill="both", expand=True)
    widgets_to_destroy.extend([scrollable_frame, scrollbar, canvas, left_frame, right_frame, inner_frame])
    for row in result_DNS:
        listbox = Listbox(left_frame, height=3, width=75)
        listbox.pack()
        listbox.insert(END, f"Магазин: DNS")
        listbox.insert(END, f"Название: {row[0]}")
        listbox.insert(END, f"Цена: {row[1]}")

        # Загрузить и отобразить изображение
        image = Image.open(urlopen(row[2])).resize((80, 80))
        photo = ImageTk.PhotoImage(image)
        label = Label(left_frame, image=photo)
        label.config(image=photo)
        label.image = photo
        label.pack()

    for row2 in result_Citilink:
        listbox = Listbox(right_frame, height=3, width=75)
        listbox.pack()
        listbox.insert(END, f"Магазин: Citilink")
        listbox.insert(END, f"Название: {row2[0]}")
        listbox.insert(END, f"Цена: {row2[1]}")

        # Загрузить и отобразить изображение
        image = Image.open(urlopen(row2[2])).resize((80, 80))
        photo = ImageTk.PhotoImage(image)
        label = Label(right_frame, image=photo)
        label.config(image=photo)
        label.image = photo
        label.pack()
    widgets_to_destroy.extend(inner_frame.winfo_children())

    window.mainloop()

    # Закрытие соединения с БД
    cursor.close()
    conn.close()


if __name__ == "__main__":
    # Создаем главное окно GUI
    window = Tk()
    window.geometry("1000x1000")
    window.title("EKELMENDE_228_1337")

    # Метка для ввода слова
    label = Label(window)
    label.pack()

    # Строка для ввода слова
    entry = Entry(window)
    entry.pack()

    # Кнопка поиска
    search_button = Button(window, text="Поиск", command=search_word)

    search_button.pack()

    window.mainloop()

