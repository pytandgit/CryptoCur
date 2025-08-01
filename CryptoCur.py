from tkinter import ttk
import requests
from tkinter import *
from tkinter import messagebox as mb


def update_cc_label(event):
    code = cc_combobox.get()
    name = crp[code]
    cc_label.config(text=name)


def update_c_label(event):
    code = c_combobox.get()
    name = cur[code]
    c_label.config(text=name)


def exchange():
    cc_code = cc_combobox.get().lower()
    c_code = c_combobox.get().lower()
    if cc_code and c_code:
        try:
            response = requests.get(
                f'https://api.coingecko.com/api/v3/simple/price?ids={cc_code}&vs_currencies={c_code}')
            response.raise_for_status()
            data = response.json()
            if c_code in data[cc_code]:
                exchange_rate = data[cc_code][c_code]
                cc_name = crp[cc_code.capitalize()]
                c_name = cur[c_code.upper()]
                mb.showinfo('Курс обмена криптовалюты', f'Курс: {exchange_rate:.2f} {c_name} за 1 {cc_name}')
            else:
                mb.showerror('Ошибка', f'Курс для валюты {c_code.upper()} не найден!')
        except Exception as e:
            mb.showerror('Ошибка', f'Произошла ошибка: {e}.')
    else:
        mb.showwarning('Внимание!', 'Выберите коды для криптовалюты и валюты!')


crp = {'Bitcoin': 'Биткоин',
       'Ethereum': 'Эфириум',
       'Litecoin': 'Лайткоин',
       'Solana': 'Солана',
       'Tether': 'Тизер'
       }

cur = {'RUB': 'Российский рубль',
       'USD': 'Американский доллар'}

window = Tk()
window.title('Курс обмена криптовалют')
window.geometry('360x300')

Label(text='Криптовалюта').pack(padx=10, pady=10)
cc_combobox = ttk.Combobox(values=list(crp.keys()))
cc_combobox.pack(padx=10, pady=10)
cc_combobox['state'] = 'readonly'  # Блокировка ввода (только выбор из списка)
cc_combobox.bind('<<ComboboxSelected>>', update_cc_label)

cc_label = ttk.Label()
cc_label.pack(padx=10, pady=10)

Label(text='Целевая валюта').pack(padx=10, pady=10)
c_combobox = ttk.Combobox(values=list(cur.keys()))
c_combobox.pack(padx=10, pady=10)
c_combobox['state'] = 'readonly'  # Блокировка ввода (только выбор из списка)
c_combobox.bind('<<ComboboxSelected>>', update_c_label)

c_label = ttk.Label()
c_label.pack(padx=10, pady=10)

Button(text='Получить курс обмена криптовалюты', command=exchange).pack(padx=10, pady=10)

window.mainloop()
