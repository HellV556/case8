import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QMessageBox, QComboBox, QTextEdit)

class RestaurantApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("АС Ресторана")
        self.setGeometry(100, 100, 600, 450)

        # Виджеты
        self.menu_label = QLabel("Выберите блюдо из меню:")
        self.menu_combo = QComboBox()
        self.menu_combo.addItems(["Пицца", "Паста", "Салат", "Суп", "Десерт"])

        self.quantity_label = QLabel("Количество (макс. 10):")
        self.quantity_textbox = QLineEdit()
        self.quantity_textbox.setText("1")

        self.order_button = QPushButton("Добавить в заказ")
        self.order_button.clicked.connect(self.add_to_order)

        self.order_label = QLabel("Заказ:")
        self.order_text = QTextEdit()
        self.order_text.setReadOnly(True)

        self.total_label = QLabel("Итого: 0.00")

        self.complete_button = QPushButton("Завершить заказ")
        self.complete_button.clicked.connect(self.complete_order)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.menu_label)
        layout.addWidget(self.menu_combo)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_textbox)
        layout.addWidget(self.order_button)
        layout.addWidget(self.order_label)
        layout.addWidget(self.order_text)
        layout.addWidget(self.total_label)
        layout.addWidget(self.complete_button)  # Добавляем кнопку "Завершить заказ"

        self.setLayout(layout)

        # Данные
        self.order_items = []
        self.menu_prices = {
            "Пицца": 500.00,
            "Паста": 400.00,
            "Салат": 300.00,
            "Суп": 250.00,
            "Десерт": 350.00
        }

    def add_to_order(self):
        item = self.menu_combo.currentText()
        try:
            quantity = int(self.quantity_textbox.text())
            if quantity <= 0:
                QMessageBox.warning(self, "Ошибка", "Количество должно быть больше нуля.")
                return
            if quantity > 10:  # Ограничение количества
                QMessageBox.warning(self, "Ошибка", "Максимальное количество - 10.")
                return
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректное количество.")
            return

        price = self.menu_prices[item]
        total_price = price * quantity

        self.order_items.append({"item": item, "quantity": quantity, "price": price})

        self.update_order_text()
        self.update_total()

    def update_order_text(self):
        order_text = ""
        for item in self.order_items:
            order_text += f"{item['item']} x {item['quantity']} - {item['price'] * item['quantity']:.2f}\n"
        self.order_text.setText(order_text)

    def update_total(self):
        total = 0.00
        for item in self.order_items:
            total += item['price'] * item['quantity']
        self.total_label.setText(f"Итого: {total:.2f}")

    def complete_order(self):
        if not self.order_items:
            QMessageBox.information(self, "Информация", "Заказ пуст.")
            return

        total = 0.00
        for item in self.order_items:
            total += item['price'] * item['quantity']

        message = f"Заказ принят!\nИтого: {total:.2f}\nСпасибо за заказ!"
        QMessageBox.information(self, "Заказ завершен", message)

        # Очищаем заказ после завершения
        self.order_items = []
        self.update_order_text()
        self.update_total()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantApp()
    window.show()
    sys.exit(app.exec_())