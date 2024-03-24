import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog

class ContactWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.name_birthday_map = {}  # Dictionary to store name-birthday pairs

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)

        add_name_button = QPushButton("Add Name")
        add_name_button.clicked.connect(self.add_name)
        layout.addWidget(add_name_button)

        # Display area for selected contact information
        self.contact_info_label = QLabel("")
        layout.addWidget(self.contact_info_label)

    def add_name(self):
        name = self.name_edit.text()
        if name:
            if name not in self.name_birthday_map:
                name_label = QLabel(name)
                layout = self.layout()
                layout.addWidget(name_label)

                # Add edit button for the name
                edit_button = QPushButton("Edit Name")
                edit_button.clicked.connect(lambda state, name=name: self.edit_name(name))
                layout.addWidget(edit_button)

                # Add "Add Birthday" button for the name
                add_birthday_button = QPushButton("Add Birthday")
                add_birthday_button.clicked.connect(lambda state, name=name: self.add_birthday(name))
                layout.addWidget(add_birthday_button)

                self.name_birthday_map[name] = (name_label, None, None)  # Placeholder for birthday labels and edits

    def edit_name(self, name):
        new_name, ok = QInputDialog.getText(self, "Edit Name", "Enter new name:")
        if ok and new_name:
            if new_name != name:
                name_label, _, _ = self.name_birthday_map[name]
                name_label.setText(new_name)
                self.name_birthday_map[new_name] = self.name_birthday_map.pop(name)
                self.update_contact_info()

    def add_birthday(self, name):
        if name in self.name_birthday_map:
            birthday, ok = QInputDialog.getText(self, "Add Birthday", "Enter birthday:")
            if ok and birthday:
                _, birthday_label, _ = self.name_birthday_map[name]
                if birthday_label is None:
                    birthday_label = QLabel(f"Birthday: {birthday}")
                    layout = self.layout()
                    layout.addWidget(birthday_label)
                    self.name_birthday_map[name] = (self.name_birthday_map[name][0], birthday_label, birthday)

                    # Replace "Add Birthday" button with "Edit Birthday" button
                    for child in layout.children():
                        if isinstance(child, QPushButton) and child.text() == "Add Birthday":
                            child.deleteLater()
                            edit_birthday_button = QPushButton("Edit Birthday")
                            edit_birthday_button.clicked.connect(lambda state, name=name: self.edit_birthday(name))
                            layout.addWidget(edit_birthday_button)
                            break

    def edit_birthday(self, name):
        if name in self.name_birthday_map:
            birthday, ok = QInputDialog.getText(self, "Edit Birthday", "Enter new birthday:")
            if ok and birthday:
                _, birthday_label, _ = self.name_birthday_map[name]
                birthday_label.setText(f"Birthday: {birthday}")
                self.name_birthday_map[name] = (self.name_birthday_map[name][0], birthday_label, birthday)

    def update_contact_info(self):
        name = self.name_edit.text()
        if name in self.name_birthday_map:
            _, birthday_label, birthday_edit = self.name_birthday_map[name]
            if birthday_label is not None:
                self.contact_info_label.setText(f"Name: {name}, {birthday_label.text()}")
            else:
                self.contact_info_label.setText(f"Name: {name}")

def main():
    app = QApplication(sys.argv)
    window = ContactWidget()
    window.setWindowTitle("Contact Widget Example")
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()