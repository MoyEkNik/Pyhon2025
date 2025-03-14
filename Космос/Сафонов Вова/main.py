import tkinter
#import requests
#from io import BytesIO
#from PIL import image, ImegeTk



import requests
import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
def get_planet_data(planet_name):
    # URL API для получения данных о планетах
    url = f"https://api.le-systeme-solaire.net/rest/bodies/{planet_name}"
    response = requests.get(url)

    if response.status_code == 200:
        planet_data = response.json()
        return planet_data
    else:
        messagebox.showerror("Ошибка", f"Ошибка при получении данных: {response.status_code}")
        return None

def show_planet_info():
    print(planets)
    print(planet_var.get())
    res_name = planet_var.get()
    if  res_name != 'выберите планету':

        ind = planets.index(res_name)
    else:
        ind = 0

    planet_var_eng = planets1[ind]
    # planet_name = planet_var.get().lower()
    planet_name = planet_var_eng
    planet_data = get_planet_data(planet_name)

    if planet_data:
        # Формирование информации о планете
        info = f"Название: {res_name}\n"
        if 'meanRadius' in planet_data:
            info += f"Диаметр: {planet_data['meanRadius']} км\n"
        if 'mass' in planet_data:
            info += f"Масса: {planet_data['mass']['massValue']} x 10^{planet_data['mass']['massExponent']} кг\n"
        print(planet_data)
        if planet_data['moons'] != None:
            num_moons = len(planet_data['moons']) if 'moons' in planet_data else 0
        else:
            num_moons = 0
        info += f"Количество спутников: {num_moons}"

        info_label.config(text=info)

# Создание основного окна
root = tk.Tk()
root.title("Информация о планетах")

#win. = tkinter.Tk()
root.geometry("800x800")
# bgimg = tkinter.PhotoImage(file='космос2.ppm')
# l = tkinter.Label(image=bgimg)
# l.pack()

root.config(bg='#00CED1')
root.config(bg='#E6E6FA')
# Переменная для выпадающего списка
planet_var = StringVar(root)
planet_var.set("Выберите планету",)


# Список планет
planets = ["Земля", "Марс", "Юпитер", "Сатурн", "Уран", "Нептун",'Венера']
planets1 = ["earth", "mars", "jupiter", "saturn", "uranus", "neptune",'venus']
# Создание выпадающего списка
planet_menu = OptionMenu(root, planet_var, *planets)
planet_menu.config(bg='#00CED1')
planet_menu.pack(pady=20,)


# Кнопка для получения информации
button = tk.Button(root, text="Получить информацию", command=show_planet_info, bg='#00CED1',font='Arial 18',)
button.pack(pady=100)

# Метка для отображения информации
info_label = tk.Label(root, text="", justify="left", padx=100, pady=100, bg='#E6E6FA', font='Arial 24')
info_label.pack(pady=20)

root.mainloop()