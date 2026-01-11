from datetime import datetime

class Operation:
    def __init__(self, volume, category, date, op_type="expense", comment=""):
        self.volume = volume
        self.category = category
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.op_type = op_type  # расход или доход            
        self.comment = comment      

    def to_dict(self):
        return {
            "volume": self.volume,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d"),
            "op_type": self.op_type,
            "comment": self.comment            
        }
    
class ExpenseOperation(Operation):
    def __init__(self, volume, category, date, op_type="expense", comment=""):

class IncomeOperation(Operation):
    def __init__(self, volume, category, date, op_type="expense", comment=""):