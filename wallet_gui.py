import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import DateEntry  # календарь для гуи

from func import add_transaction, show_transaction, del_transaction, get_total_amount


# Создаем класс кошелька
class Wallet:
    def __init__(self, root):
        self.root = root
        self.root.title("Убывающий кошелек")
        self.root.geometry('550x350')
        self.root.resizable(False, False)

        self.create_widgets()
        self.update_transaction_list()

    def create_widgets(self):
        self.date_label = ttk.Label(self.root, text="Дата транзакции")
        self.date_label.grid(row=0, column=0)
        self.date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=0, column=1)

        self.description = ttk.Label(self.root, text="Описание траты")
        self.description.grid(row=1, column=0)
        self.description_entry = ttk.Entry(self.root)
        self.description_entry.grid(row=1, column=1)

        self.amount = ttk.Label(self.root, text="Сумма")
        self.amount.grid(row=2, column=0)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1)

        # пара кнопок
        self.add_btn = ttk.Button(self.root, text="Добавить", command=self.add_transaction)
        self.add_btn.grid(row=3, column=1)

        self.del_btn = ttk.Button(self.root, text="Удалить", command=self.del_transaction)
        self.del_btn.grid(row=3, column=2)

        self.sum_btn = ttk.Button(self.root, text="Общая сумма", command=self.summa_transaction)
        self.sum_btn.grid(row=5, column=2)

        # таблица Treeview
        self.transaction_list = ttk.Treeview(self.root, columns=("id", "Сумма", "Описание", "Дата"), show='headings')
        self.transaction_list.heading("id", text="ID")
        self.transaction_list.heading("Сумма", text="Сумма")
        self.transaction_list.heading("Описание", text="Описание")
        self.transaction_list.heading("Дата", text="Дата")

        self.transaction_list.column("id", width=30)
        self.transaction_list.column("Сумма", width=100)
        self.transaction_list.column("Описание", width=280, stretch=True, anchor='w')
        self.transaction_list.column("Дата", width=100)

        # Создание вертикального скроллбара
        y_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.transaction_list.yview)
        y_scrollbar.grid(row=4, column=3, sticky="ns")


        # Привязка скроллбаров к Treeview
        self.transaction_list.configure(yscrollcommand=y_scrollbar.set)

        self.transaction_list.grid(row=4, column=0, padx=10, columnspan=3)

    # функция добавления транзакции
    def add_transaction(self):
        date = self.date_entry.get_date()
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        if amount and description:
            try:
                amount = float(amount)
                add_transaction(date, description, amount)
                self.update_transaction_list()

                # очистка полей Описание и Сумма
                self.description_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                messagebox.showinfo("Удача", f"Транзакция '{description}' добавлена")
            except ValueError:
                messagebox.showerror("error", "Поле 'Сумма' должно быть числом")
        else:
            messagebox.showwarning("error", "Введите значения в поля")

    # функция удаления транзакции
    def del_transaction(self):
        selected_item = self.transaction_list.selection()
        if selected_item:
            transaction_id = self.transaction_list.item(selected_item, "values")[0]
            del_transaction(transaction_id)
            self.update_transaction_list()
        else:
            messagebox.showwarning("Предупреждение", "Выберите транзакцию для удаления")

    def summa_transaction(self):
        all_summa = get_total_amount()
        messagebox.showinfo("Общая сумма за все траты", f'Общая сумма трат = {all_summa} руб')

    # обновление информации в бд
    def update_transaction_list(self):
        for i in self.transaction_list.get_children():
            self.transaction_list.delete(i)

        for transaction in show_transaction():
            self.transaction_list.insert('', 'end', values=transaction)

if __name__ == '__main__':
    root = tk.Tk()
    app = Wallet(root)
    root.mainloop()