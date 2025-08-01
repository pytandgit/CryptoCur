from tkinter import ttk
import requests
from tkinter import *
from tkinter import messagebox as mb

from requests import RequestException


def update(event):
    '''Обновляем метки и состояние кнопки при выборе значений'''
    cc_code = cc_combobox.get()
    c_code = c_combobox.get()
    if cc_code and c_code:
        cc_label.config(text=crp[cc_code])
        c_label.config(text=cur[c_code])
        # Разблокировка кнопки
        button['state'] = 'normal'
        # Даем фокус кнопке для удобства нажатия Enter
        button.focus_set()
    else:
        button['state'] = 'disabled'


def exchange():
    cc_code = cc_combobox.get().lower()
    c_code = c_combobox.get().lower()
    if cc_code and c_code:
        try:
            # Добавлен таймаут для запроса (10 секунд)
            response = requests.get(
                f'https://api.coingecko.com/api/v3/simple/price?ids={cc_code}&vs_currencies={c_code}', timeout=10)
            response.raise_for_status()  # проверка успешности HTTP-статуса ответа сервера
            data = response.json()  # преобразование JSON в словарь
            if cc_code not in data:
                mb.showerror('Ошибка', 'Данные по криптовалюте не найдены!')
                return

            if c_code not in data[cc_code]:
                mb.showerror('Ошибка', f'Курс для валюты {c_code.upper()} не найден!')
                return

            exchange_rate = data[cc_code][c_code]
            cc_name = crp[cc_code.capitalize()]
            c_name = cur[c_code.upper()]

            mb.showinfo('Курс обмена криптовалюты', f'Курс: {exchange_rate:,.2f} {c_name}\n'
                                                    f'за 1 {cc_name}')

        except RequestException as e:
            mb.showerror('Ошибка запроса', f'Не удалось получить данные: {e}.')
        except Exception as e:
            mb.showerror('Ошибка', f'Произошла непредвиденная ошибка: {e}.')


def center_window(window, width, height):
    # Получаем размеры экрана
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Вычисляем координаты для центрирования окна
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Устанавливаем положение и размер
    window.geometry(f'{width}x{height}+{x}+{y}')


# Словари данных
crp = {
    'Bitcoin': 'Биткоин (BTC)',
    'Ethereum': 'Эфириум (ETH)',
    'Litecoin': 'Лайткоин (LTC)',
    'Solana': 'Солана (SOL)',
    'Tether': 'Тезер (USDT)'
}

cur = {
    'RUB': 'Российский рубль',
    'USD': 'Доллар США',
    'EUR': 'Евро'
}

# Создание графического интерфейса
window = Tk()
window.title('Курс обмена криптовалют')
center_window(window, 400, 300)  # Центрируем окно
window.resizable(False, False)

# Криптовалюта
Label(text='Выберите криптовалюту', font=('Arial', 10, 'bold')).pack(padx=10, pady=5)
cc_combobox = ttk.Combobox(values=list(crp.keys()), state='readonly')
cc_combobox.pack(pady=5)
cc_combobox.bind('<<ComboboxSelected>>', update)

cc_label = ttk.Label()
cc_label.pack(pady=5)

# Валюта
Label(text='Выберите валюту', font=('Arial', 10, 'bold')).pack(padx=10, pady=5)
c_combobox = ttk.Combobox(values=list(cur.keys()), state='readonly')
c_combobox.pack(pady=5)
c_combobox.bind('<<ComboboxSelected>>', update)

c_label = ttk.Label()
c_label.pack(pady=5)

# Кнопка
button = Button(text='Получить курс обмена', state='disabled', command=exchange)
button.pack(padx=20, pady=20)

# Обработка Enter
window.bind('<Return>', lambda event: button.invoke())  # Привязываем нажатие Enter к кнопке

# Запуск приложения
window.mainloop()
