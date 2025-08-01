from tkinter import ttk
import requests
from tkinter import *
from tkinter import messagebox as mb


def update(event):
    '''Получаем значение криптовалюты и валюты из словаря и обновляем метки.
    Кнопка "Получить курс обмена криптовалюты" разблокируется при выборе значений криптовалюты и валюты.'''
    cc_code = cc_combobox.get()
    c_code = c_combobox.get()
    if cc_code and c_code:
        cc_label.config(text=crp[cc_code])
        c_label.config(text=cur[c_code])
        button['state'] = 'normal'
    else:
        button['state'] = 'disabled'


def exchange():
    cc_code = cc_combobox.get().lower()
    c_code = c_combobox.get().lower()
    if cc_code and c_code:
        try:
            response = requests.get(
                f'https://api.coingecko.com/api/v3/simple/price?ids={cc_code}&vs_currencies={c_code}')
            response.raise_for_status()  # проверка успешности HTTP-статуса ответа сервера
            data = response.json()  # преобразование JSON в словарь
            if c_code in data[cc_code]:
                exchange_rate = data[cc_code][c_code]
                cc_name = crp[cc_code.capitalize()]
                c_name = cur[c_code.upper()]
                mb.showinfo('Курс обмена криптовалюты', f'Курс: {exchange_rate:.2f} {c_name} за 1 {cc_name}')
            else:
                mb.showerror('Ошибка', f'Курс для валюты {c_code.upper()} не найден!')
        except Exception as e:
            mb.showerror('Ошибка', f'Произошла ошибка: {e}.')


# Словарь кодов криптовалют и их полных названий
crp = {'Bitcoin': 'Биткоин',
       'Ethereum': 'Эфириум',
       'Litecoin': 'Лайткоин',
       'Solana': 'Солана',
       'Tether': 'Тизер'
       }
# Словарь кодов валют и их полных названий
cur = {'RUB': 'Российский рубль',
       'USD': 'Американский доллар'}

# Создание графического интерфейса
window = Tk()
window.title('Курс обмена криптовалют')
window.geometry('360x300')

Label(text='Криптовалюта').pack(padx=10, pady=10)
cc_combobox = ttk.Combobox(values=list(crp.keys()))
cc_combobox.pack(padx=10, pady=10)
cc_combobox['state'] = 'readonly'  # Блокировка ввода (только выбор из списка)
cc_combobox.bind('<<ComboboxSelected>>', update)

cc_label = ttk.Label()
cc_label.pack(padx=10, pady=10)

Label(text='Целевая валюта').pack(padx=10, pady=10)
c_combobox = ttk.Combobox(values=list(cur.keys()))
c_combobox.pack(padx=10, pady=10)
c_combobox['state'] = 'readonly'  # Блокировка ввода (только выбор из списка)
c_combobox.bind('<<ComboboxSelected>>', update)

c_label = ttk.Label()
c_label.pack(padx=10, pady=10)

button = Button(text='Получить курс обмена криптовалюты', state='disabled', command=exchange)
button.pack(padx=10, pady=10)
window.bind('<Return>', lambda event: button.invoke())  # Привязываем нажатие Enter к кнопке

window.mainloop()
