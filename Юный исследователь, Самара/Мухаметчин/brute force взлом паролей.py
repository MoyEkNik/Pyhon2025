import itertools
import string

def brute_force_password(password_length, target_password):
    chars = string.ascii_letters + string.digits + string.punctuation  # Все возможные символы
    attempts = 0

    for length in range(1, password_length + 1):
        for guess in itertools.product(chars, repeat=length):
            attempts += 1
            guess = ''.join(guess)  # Преобразуем кортеж в строку
            if guess == target_password:
                return f"Пароль найден: {guess} (попыток: {attempts})"
    return "Пароль не найден."

# Пример использования
target_password = "S;bey"  # Пароль, который нужно подобрать
password_length = 5  # Максимальная длина пароля
print(brute_force_password(password_length, target_password))

































