import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models import Operation, IncomeOperation, ExpenseOperation
from storage import load_operations, save_operations, create_excel_file
from utils import validate_date, validate_volume, validate_category
from analysis import operations_to_df, histplot_income_expense_by_category, plot_income_expense_over_time


class ProductsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Журнал движения нефтепродуктов на АЗС")

        # Загружаем существующие операции
        self.operations = load_operations()

        # Ввод операций 
        ttk.Label(root, text="Литры").grid(row=0, column=0, padx=5, pady=5)
        self.volume_entry = tk.Entry(root)
        self.volume_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Марка топлива").grid(row=1, column=0, padx=5, pady=5)
        brand = ["АИ-95", "АИ-92", "ДТ"]  
        self.category_entry = ttk.Combobox(values=brand)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(root, text="Комментарий").grid(row=3, column=0, padx=5, pady=5)
        self.comment_entry = tk.Entry(root)
        self.comment_entry.grid(row=3, column=1, padx=5, pady=5)

        self.type_var = tk.StringVar(value="income")
        ttk.Checkbutton(root, text="Отпущено", variable=self.type_var, onvalue="expense").grid(row=4, column=0)
        ttk.Checkbutton(root, text="Принято", variable=self.type_var, onvalue="income").grid(row=4, column=1)
        # Кнопки
        tk.Button(root, text="Добавить операцию", command=self.add_operation, bg="lightgreen").grid(row=5, column=0, padx=10)
        tk.Button(root, text="Редактировать операцию", command=self.edit_data, bg="lightyellow").grid(row=5, column=1, padx=4)
        tk.Button(root, text="Удалить операцию", command=self.add_operation, bg="lightcoral").grid(row=6, column=0, columnspan=2)
        ttk.Button(root, text="Анализ", command=self.analyze).grid(row=7, column=0)
        ttk.Button(root, text="Сохранить в excel", command=self.add_excel).grid(row=7, column=1)
        # Основное окно
        # Создаём таблицу с окном данных справа
        columns = ("id", "volume", "category", "date", "type", "comment")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        self.tree.grid(row=0, column=2, rowspan=8, sticky="s", padx=10, pady=[25,10])

        # Подпись окна данных
        ttk.Label(root, text=" История операций ").grid(row=0, column=2, sticky="n", padx=5, pady=3)

        # Заголовки таблицы
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("category", text="Марка")
        self.tree.heading("volume", text="Литры")
        self.tree.heading("comment", text="Комментарий")

        # Размер колонок
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("date", width=90, anchor="center")
        self.tree.column("type", width=90, anchor="center")
        self.tree.column("category", width=80, anchor="center")
        self.tree.column("volume", width=80, anchor="w")
        self.tree.column("comment", width=150)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.set(0.2, 0.5)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=3, rowspan=8, sticky="ns", pady=[25,10])

        self.update_tree()  

    def add_excel(self):
        """Записывает данные в excel файл."""
        if create_excel_file() == False:
            messagebox.showinfo("Ошибка", "Нет данных для записи")      
        else: 
            messagebox.showinfo("Успех", "Данные экспортированы в папку FILE_EXCEL")
            
    def add_operation(self):
        """Добавляет новую операцию после валидации введённых данных."""
        try:
            volume = validate_volume(self.volume_entry.get())
            category = validate_category(self.category_entry.get())
            date = validate_date(self.date_entry.get())
            comment = self.comment_entry.get().strip()
            op_type = self.type_var.get()

            # Полиморфное создание объекта
            if op_type == "income":
                op = IncomeOperation(float(volume), category, date, comment)
            else:
                op = ExpenseOperation(float(volume), category, date, comment)

            # Сохраняем данные
            save_operations([op])            
            self.operations.append(op)            

            # Обновляем интерфейс
            self.update_tree()
            self.clear_input_windows()

            messagebox.showinfo("Готово", "Операция добавлена")

        except Exception as e:
            messagebox.showerror("Ошибка ввода", f"Не удалось добавить операцию:\n{e}")
 
    def edit_data(self):
        """Редактируем операцию после валидации введённых данных."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите строку для изменения")
            return
        try:
            # Получаем ID из выбранной строки
            selected_id = self.tree.item(selected, "values")[0] # ID выбранной строки

            # Находим операцию по ID
            operation_index = None
            for i, op in enumerate(self.operations):
                if op.id == selected_id:
                    operation_index = i
                break
        
            if operation_index is None:
                messagebox.showerror("Ошибка", "Операция не найдена")
                return
            # Получаем и валидируем данные
            volume = validate_volume(self.volume_entry.get())
            category = validate_category(self.category_entry.get())
            date = validate_date(self.date_entry.get())
            comment = self.comment_entry.get().strip()
            op_type = self.type_var.get()

            # Создаём новую операцию с ТЕМ ЖЕ ID
            if op_type == "income":
                new_op = IncomeOperation(volume, category, date, comment, selected_id)
            else:
                new_op = ExpenseOperation(volume, category, date, comment, selected_id)
            # Заменяем операцию
            self.operations[operation_index] = new_op    

            # Сохраняем данные
            save_operations(self.operations)

            # Обновляем интерфейс
            self.update_tree()
            self.clear_input_windows()
            messagebox.showinfo("Готово", "Операция добавлена")

        except Exception as e:
            print(e)
            messagebox.showerror("Ошибка ввода", f"Не удалось добавить операцию:\n{e}")
    
    def clear_input_windows(self):
        """Очищает поля ввода (кроме даты)."""
        self.comment_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.volume_entry.delete(0, tk.END)

    def update_tree(self):
        """Очищаем текущие строки"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        """Добавляем значения на следующую стоку"""
        for op in self.operations:
            row_type = "Принято" if op.op_type == "income" else "Отпущено"
            self.tree.insert("", "end", values=(
                op.id,  # Добавляем ID как первую колонку
                f"{op.volume:.1f}",
                op.category, 
                op.date.strftime("%Y-%m-%d"), 
                row_type, 
                op.comment
                ))
        # Прокрутка к новой операции
        self.tree.yview_moveto(1.0)

    def analyze(self):
        """Анализ и визуализация данных, полученных за период"""
        df = operations_to_df(self.operations)
        if df.empty:
            messagebox.showinfo("Ошибка", "Нет данных для графика")
            return
    #   Столбчатая диаграмма приёма и отпуска топлива
        histplot_income_expense_by_category(df)             
    #   Динамика приёма и отпуска топлива по времени
        plot_income_expense_over_time(df)




