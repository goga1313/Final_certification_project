from datetime import datetime

class Operation:
    """Базовый класс для операций"""
    _next_id = 1 
    
    def __init__(self, volume, category, date, op_type="expense", comment="", operation_id=None):
        self.volume = volume
        self.category = category
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.op_type = op_type # расход или доход 
        self.comment = comment
        
        # Сгенерировать ID, ЕСЛИ ЕГО НЕТ
        if operation_id is None:
            self.id = Operation._next_id
            Operation._next_id += 1
        else:
            self.id = operation_id
            # Обновить _next_id если мы создали запись с каким-то ID
            if operation_id >= Operation._next_id:
                Operation._next_id = operation_id + 1

    def to_dict(self):
        return {
            "id": self.id, 
            "volume": self.volume,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d"),
            "op_type": self.op_type,
            "comment": self.comment          
        }
    
class ExpenseOperation(Operation):
    """Операция расхода топлива"""
    def __init__(self, volume, category, date, comment="", operation_id=None):
        super().__init__(volume, category, date, "expense", comment, operation_id)


class IncomeOperation(Operation):
    """Операция прихода топлива"""
    def __init__(self, volume, category, date, comment="", operation_id=None):
        super().__init__(volume, category, date, "income", comment, operation_id)