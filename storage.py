import os
import csv
import pandas as pd
from datetime import datetime
from models import Operation

# Папка и файл для хранения данных в csv
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "operations.csv")

def create_excel_file():
    """Выгрузка данных в Excel"""
    # Начало, операций не было
    if not os.path.exists(CSV_FILE):
        return False
    # Создаёт папку 'FILE_EXCEL', если папки нет.
    if not os.path.exists("FILE_EXCEL"):
        os.makedirs("FILE_EXCEL")
    
    try:
        # Замена названия колонок
        columns = ["Количество, литры", "Марка топлива", "Дата операции", "Тип операции", "Комментарий"]
        df = pd.read_csv(CSV_FILE, header=None, names=columns)
        df = df[df["Количество, литры"] != "volume"]

        # Сохранение в excel  
        filename = datetime.now().strftime("file_%Y-%m-%d_%H-%M-%S.xlsx")
        file_path = os.path.join("FILE_EXCEL", filename)
        excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        df.to_excel(excel_writer, sheet_name='Журнал операций', index=False)
        excel_writer.sheets['Журнал операций'].set_column(0, 4, 20)
        excel_writer.close()       
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def ensure_data_dir():
    """Создаёт папку 'data', если папки нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_operations(operations):
    """
    Сохраняет список Operation в CSV.
    Добавляет новые данные в конец файла, создаёт заголовок при первом сохранении.
    """
    # Если операций не было
    if not operations:
        return

    ensure_data_dir()
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            fieldnames = ["volume", "category", "date", "op_type", "comment"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Записываем заголовок только при создании файла
            if not file_exists:
                writer.writeheader()

            # Записываем каждую операцию
            for op in operations:
                writer.writerow(op.to_dict())

    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_operations():
    """
    Загружает все операции из CSV и возвращает список Operation.
    При ошибках возвращает пустой список.
    """
    operations = []
    # Начало, файла ещё нет
    if not os.path.exists(CSV_FILE):
        return operations 

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader_file = csv.DictReader(f)
            # Преобразуем строку CSV в объект Operation с проверкой данных
            for row in reader_file:           
                try:
                    op = Operation(
                        volume=float(row["volume"]),
                        category=row["category"],
                        date=row["date"],
                        op_type=row["op_type"],
                        comment=row.get("comment", "")                        
                    )
                    operations.append(op)
                except ValueError as ve:
                    print(f"Пропущена некорректная запись: {ve}")

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []
    
    return operations
