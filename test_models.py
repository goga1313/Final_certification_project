import unittest
from models import Operation
from utils import validate_date
from datetime import datetime

class TestOperation(unittest.TestCase):

    def test_to_dict(self):
        """Проверяет, равны ли два значения (фактическое и ожидаемое)"""
        op = Operation(1500, "АИ-95", "2025-12-20", "expense", "Test comment")
        d = op.to_dict()
        self.assertEqual(d["volume"], 1500)
        self.assertEqual(d["category"], "АИ-95")
        self.assertEqual(d["date"], "2025-12-20")
        self.assertEqual(d["op_type"], "expense")
        self.assertEqual(d["comment"], "Test comment")

    def test_date_conversion(self):
        """Проверяет является ли строка датой, в соответствующем формате"""
        op = Operation(3500, "АИ-92", "2025-12-12", "income", "Test comment")
        self.assertIsInstance(op.date, datetime)
        self.assertEqual(op.date.strftime("%Y-%m-%d"), "2025-12-12")

    def test_create_operation(self):
        """Тест создания операции"""
        op = Operation(1500, "АИ-95", "2025-12-20", "income", "Test")
        self.assertEqual(op.volume, 1500)
        self.assertEqual(op.category, "АИ-95")
        self.assertEqual(op.op_type, "income")
        self.assertEqual(op.comment, "Test")

    def test_operation_date_parsing(self):
        """Тест парсинга даты"""
        op = Operation(100, "ДТ", "2025-01-15", "income", "")
        self.assertEqual(op.date.year, 2025)
        self.assertEqual(op.date.month, 1)
        self.assertEqual(op.date.day, 15)
    
class TestValidateDate(unittest.TestCase):
    """Тесты для валидации даты"""

    def test_valid_date(self):
        """Тест валидации корректной даты"""
        result = validate_date("2025-12-20")
        self.assertEqual(result, "2025-12-20")

    def test_invalid_format(self):
        """Тест для проверки неверного формата"""
        with self.assertRaises(ValueError):
            validate_date("20-12-2025")

    def test_invalid_date(self):
        """Тест проверки несуществующей даты"""
        with self.assertRaises(ValueError):
            validate_date("2025-02-31")

    def test_empty_date(self):
        """Тест проверки пустой даты"""
        with self.assertRaises(ValueError):
            validate_date("")

    def test_date_with_spaces(self):
        """Тест для проверки даты с пробелами"""
        result = validate_date("  2025-12-20  ")
        self.assertEqual(result, "2025-12-20")

if __name__ == "__main__":
    unittest.main()
