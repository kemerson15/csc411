import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QDateEdit, QLabel, QPushButton, QLineEdit, QScrollArea, QHBoxLayout, QInputDialog, QFormLayout 
import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('phone_directory.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS contacts
                            (first_name text, last_name text, phone text, birthday text)''')
        self.conn.commit()

    def add_contact(self, first_name, last_name, phone, birthday):
        try:
            self.c.execute("INSERT INTO contacts (first_name, last_name, phone, birthday) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, phone, birthday))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error adding contact:", e)

    def add_birthday(self, first_name, birthday):
        self.c.execute("UPDATE contacts SET birthday = ? WHERE first_name = ?", (birthday, first_name))
        self.conn.commit()

    def retrieve_contact(self, first_name):
        self.c.execute("SELECT * FROM contacts WHERE first_name=?", (first_name,))
        contact = self.c.fetchone()
        return contact

    def retrieve_all_contacts(self):
        self.c.execute("SELECT * FROM contacts")
        contacts = self.c.fetchall()
        return contacts

    def delete_contact(self, first_name):
        self.c.execute("DELETE FROM contacts WHERE first_name=?", (first_name,))
        self.conn.commit()

class ContactWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.database = DatabaseHandler()
        self.init_ui()
        
        self.setWindowTitle("Add Contact")

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.first_name_edit = QLineEdit()
        form_layout.addRow("First Name:", self.first_name_edit)

        self.last_name_edit = QLineEdit()
        form_layout.addRow("Last Name:", self.last_name_edit)

        self.phone_edit = QLineEdit()
        form_layout.addRow("Phone:", self.phone_edit)

        self.birthday_edit = QDateEdit()
        form_layout.addRow("Birthday:", self.birthday_edit)

        layout.addLayout(form_layout)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_name)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)

        add_name_button = QPushButton("Add Name")
        add_name_button.clicked.connect(self.add_name)
        layout.addWidget(add_name_button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        contacts_widget = QWidget()
        self.contacts_layout = QVBoxLayout(contacts_widget)
        scroll_area.setWidget(contacts_widget)

        self.update_contacts_list()

    def add_name(self):
        
        # Show the dialog to get contact information
        first_name, ok = QInputDialog.getText(self, "Add Contact", "Enter first name:")
        if ok:
            last_name, ok = QInputDialog.getText(self, "Add Contact", "Enter last name:")
            if ok:
                phone, ok = QInputDialog.getText(self, "Add Contact", "Enter phone number:")
                if ok:
                    birthday, ok = QInputDialog.getText(self, "Add Contact", "Enter birthday (YYYY-MM-DD):")
                    if ok:
                        # Add the contact to the database
                        self.database.add_contact(first_name, last_name, phone, birthday)

                        # Update the contacts list
                        self.update_contacts_list()

            # Update the contacts list
            
       
        if not first_name or not last_name or not phone:
            print("Error: Required fields are empty")
            return

        # Now you have the required information to create a contact
        print("Adding contact...")
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Phone:", phone)
        print("Birthday:", birthday)
        
        self.update_contacts_list()
        
    def update_contacts_list(self):
        self.clear_contacts_list()

        contacts = self.database.retrieve_all_contacts()
        if contacts:
            for contact in contacts:
                first_name = contact[0]
                last_name = contact[1]
                phone = contact[2]
                birthday = contact[3]
                contact_layout = QHBoxLayout()  # Use QHBoxLayout for horizontal arrangement
               

                # Add labels for name, phone, and birthday
                name_label = QLabel(f"{first_name} {last_name}")
                contact_layout.addWidget(name_label)

                phone_label = QLabel(f"Phone: {phone}")
                contact_layout.addWidget(phone_label)

                birthday_label = QLabel(f"Birthday: {birthday}")
                contact_layout.addWidget(birthday_label)

                # Add remove button
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda state, first_name=first_name: self.remove_contact(first_name))
                contact_layout.addWidget(remove_button)

                self.contacts_layout.addLayout(contact_layout)  # Add the horizontal layout to the contacts layout


                
                
                
    def remove_contact_clicked(self):
        sender = self.sender()  # Get the button that triggered the event
        name = sender.property("contact_name")  # Get the contact name associated with the button
        if name:
            self.remove_contact(name)

    def remove_contact(self, name):
        # Remove the contact from the database
        self.database.delete_contact(name)
        
        # Update the contacts list in the UI
        self.update_contacts_list()            

    def clear_contacts_list(self):
        for i in reversed(range(self.contacts_layout.count())):
            widget = self.contacts_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                
    def remove_contact(self, name):
        self.database.delete_contact(name)
        self.update_contacts_list()
        
    def add_birthday_clicked(self):
        sender = self.sender()  # Get the button that triggered the event
        name = sender.property("contact_name")  # Get the contact name associated with the button
        if name:
            birthday, ok = QInputDialog.getText(self, "Add Birthday", f"Enter birthday for {name}:")
            if ok and birthday:
                self.add_birthday(name, birthday)

    def add_birthday(self, name, birthday):
        # Add the birthday to the database
        self.database.add_birthday(name, birthday)
        
        # Update the contacts list in the UI
        self.update_contacts_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactWidget()
    window.setWindowTitle("Contact Widget Example")
    window.setGeometry(100, 100, 400, 600)
    window.show()
    sys.exit(app.exec_())