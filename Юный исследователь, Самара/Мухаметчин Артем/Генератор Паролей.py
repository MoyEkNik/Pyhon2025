import random
import string
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os


#Генерация ключа шифрования
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Загрузка ключа шифрования
def load_key():
    if not os.path.exists("secret.key"):
        generate_key()
    with open("secret.key", "rb") as key_file:
        return key_file.read()


# Шифрование данных
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

# Расшифровка данных
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

# Сохранение паролей в файл
def save_passwords_to_file(passwords, key):
    encrypted_passwords = encrypt_data("\n".join(passwords), key)
    with open("passwords.txt", "wb") as file:
        file.write(encrypted_passwords)


# Загрузка паролей из файла
def load_passwords_from_file(key):
    if not os.path.exists("passwords.txt"):
        return []
    with open("passwords.txt", "rb") as file:
        encrypted_passwords = file.read()
    try:
        decrypted_passwords = decrypt_data(encrypted_passwords, key)
        return decrypted_passwords.split("\n")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить пароли: {e}")
        return []


saved_passwords = []
encryption_key = load_key()

# Загрузка паролей при запуске программы
saved_passwords = load_passwords_from_file(encryption_key)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def on_generate():
    try:
        length = int(entry_length.get())
        password = generate_password(length)
        text_password.delete(1.0, tk.END)
        text_password.insert(tk.END, password)
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число!")

def save_password():
    password = text_password.get(1.0, tk.END).strip()
    if password:
        saved_passwords.append(password)
        messagebox.showinfo("Успех", "Пароль сохранен!")
    else:
        messagebox.showerror("Ошибка", "Нет пароля для сохранения!")

def show_saved_passwords():
    saved_window = tk.Toplevel(root)
    saved_window.title("Сохраненные пароли")
    saved_window.geometry("400x300")

    if saved_passwords:
        text_saved_passwords = tk.Text(saved_window, height=15, width=50)
        text_saved_passwords.pack(pady=10, padx=10)
        for pwd in saved_passwords:
            text_saved_passwords.insert(tk.END, pwd + "\n")
        text_saved_passwords.config(state=tk.DISABLED)
    else:
        label_no_passwords = tk.Label(saved_window, text="Нет сохраненных паролей.")
        label_no_passwords.pack(pady=10)


def on_closing():
    # Сохранение паролей перед закрытием программы
    save_passwords_to_file(saved_passwords, encryption_key)
    root.destroy()

root = tk.Tk()
root.title("Генератор паролей")
root.geometry("400x300")

label_length = tk.Label(root, text="Введите длину пароля:")
label_length.pack(pady=10)

entry_length = tk.Entry(root)
entry_length.pack(pady=5)

button_generate = tk.Button(root, text="Сгенерировать пароль", command=on_generate)
button_generate.pack(pady=10)

text_password = tk.Text(root, height=5, width=50)
text_password.pack(pady=10)

button_save = tk.Button(root, text="Сохранить пароль", command=save_password)
button_save.pack(pady=5)

button_show_saved = tk.Button(root, text="Показать сохраненные пароли", command=show_saved_passwords)
button_show_saved.pack(pady=5)

# Обработка события закрытия окна
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()