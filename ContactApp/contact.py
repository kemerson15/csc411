from PyQt5.QtWidgets import  QApplication, QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QPushButton, QLineEdit, QScrollArea, QHBoxLayout, QInputDialog, QFormLayout, QComboBox, QDialog, QListWidgetItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMessageBox  # Import QMessageBox for displaying contact information
from datetime import datetime  # Import datetime module
import sqlite3

class ContactWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.database = DatabaseHandler()
        self.added_contacts = set()  # Maintain a set to store added contact names
        self.init_ui()

        self.setWindowTitle("Contact Widget")

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        add_contact_button = QPushButton("Add Contact")
        add_contact_button.clicked.connect(self.show_add_contact_dialog)
        layout.addWidget(add_contact_button)

        # Create a scrollable list widget to display contact names
        self.contact_list_widget = QListWidget()
        self.contact_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contact_list_widget.itemClicked.connect(self.show_contact_info)
        layout.addWidget(self.contact_list_widget)

        # Initialize the contact list
        self.update_contacts_list()

    def show_add_contact_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Add Contact")

        form_layout = QFormLayout()

        first_name_edit = QLineEdit()
        form_layout.addRow("First Name:", first_name_edit)

        last_name_edit = QLineEdit()
        form_layout.addRow("Last Name:", last_name_edit)

        phone_edit = QLineEdit()
        phone_validator = QIntValidator()  # Validator for integer input
        phone_edit.setMaxLength(10)  # Set maximum length to 10 characters
        phone_edit.setValidator(QIntValidator())  # Allow only integers
        form_layout.addRow("Phone:", phone_edit)

        birthday_month_combo = QComboBox()
        birthday_month_combo.addItems(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        birthday_month_combo.currentIndexChanged.connect(self.update_day_combo)
        form_layout.addRow("Birthday Month:", birthday_month_combo)

        birthday_day_combo = QComboBox()
        self.update_day_combo(birthday_month_combo, birthday_day_combo)  # Initialize day combo with days for January
        form_layout.addRow("Birthday Day:", birthday_day_combo)

        # Add year selection as combo box
        current_year = datetime.now().year
        year_combo = QComboBox()
        year_combo.addItems([str(year) for year in range(1930, current_year + 1)])
        form_layout.addRow("Year of Birth:", year_combo)

        
        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_contact(dialog, first_name_edit.text(), last_name_edit.text(), phone_edit.text(), birthday_month_combo.currentText(), birthday_day_combo.currentText(), year_combo.currentText()))
        form_layout.addRow(add_button)

        dialog.setLayout(form_layout)
        dialog.exec_()
        
        
    def show_contact_info(self, item):
        # Retrieve the selected contact name
        selected_contact_name = item.text()

        # Retrieve contact information from the database based on the selected name
        contact_info = self.database.retrieve_contact_by_name(selected_contact_name)

        if contact_info:
            # Extract contact details
            first_name, last_name, phone, birthday = contact_info
            print(birthday)
            # Format the birthday
            formatted_birthday = datetime.strptime(birthday, "%B-%d-%Y").strftime("%B %d, %Y")

            # Display contact information in a message box
            QMessageBox.information(self, "Contact Information", 
                                    f"Name: {first_name} {last_name}\n"
                                    f"Phone Number: {phone}\n"
                                    f"Birthday: {formatted_birthday}")
    
    def update_day_combo(self, month_combo, day_combo):
        # Clear existing items in day combo
        day_combo.clear()

        # Get the number of days in the selected month
        selected_month = month_combo.currentIndex() + 1
        num_days = QDate(QDate.currentDate().year(), selected_month, 1).daysInMonth()

        # Add days to the combo box
        for day in range(1, num_days + 1):
            day_combo.addItem(str(day))

    def add_contact(self, dialog, first_name, last_name, phone, birthday_month, birthday_day, year):
        print("Adding contact...")
        # Format birthday
        birthday = f"{birthday_month}-{birthday_day}-{year}"

        # Check if the contact is already added
        contact_info = (first_name, last_name, phone, birthday)
        if contact_info in self.added_contacts:
            print(f"Contact {contact_info} is already added.")
            return

        # Add contact to the database
        self.database.add_contact(first_name, last_name, phone, birthday)
        
        # Update the contacts list
        self.update_contacts_list()
        
        # Add the contact information tuple to the set of added contacts
        self.added_contacts.add(contact_info)
        
        # Close the dialog
        dialog.accept()

    def update_contacts_list(self):
        # Retrieve all contacts from the database
        contacts = self.database.retrieve_all_contacts()

        # Clear existing items in the contact list widget
        self.contact_list_widget.clear()

        # Display contact names in the list widget
        if contacts:
            for contact in contacts:
                first_name = contact[0]
                last_name = contact[1]
                phone_number = contact[2]
                full_name = f"{first_name} {last_name}"
                self.contact_list_widget.addItem(full_name)
                
                
                # Create a list widget item with the contact name
                item = QListWidgetItem(full_name)
                
                 # Create a remove button
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda _, name=full_name: self.confirm_remove_contact(first_name, last_name, phone_number))

                # Add the remove button to the list widget item
                self.contact_list_widget.addItem(item)
                self.contact_list_widget.setItemWidget(item, remove_button)
                
                
    
    def confirm_remove_contact(self, first_name, last_name, phone_number):
        # Prompt the user with a confirmation dialog
        reply = QMessageBox.question(self, "Confirmation", f"Are you sure you want to remove {first_name + last_name}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # If the user confirms, remove the contact
            self.remove_contact(first_name, last_name, phone_number)
            
    def remove_contact(self, first_name, last_name, phone):
        # Remove the contact from the database
        self.database.delete_contact(first_name, last_name, phone)

        # Update the contacts list in the UI
        self.update_contacts_list()

    def clear_contacts_list(self):
        for i in reversed(range(self.contacts_layout.count())):
            widget = self.contacts_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


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

    def retrieve_all_contacts(self):
        self.c.execute("SELECT * FROM contacts")
        contacts = self.c.fetchall()
        return contacts

    def delete_contact(self, first_name, last_name, phone):
        self.c.execute("DELETE FROM contacts WHERE first_name=? AND last_name=? AND phone=?", (first_name, last_name, phone))
        self.conn.commit()
        
    def retrieve_contact_by_name(self, full_name):
        # Split the full name into first name and last name
        first_name, last_name = full_name.split()

        self.c.execute("SELECT * FROM contacts WHERE first_name=? AND last_name=?", (first_name, last_name))
        contact = self.c.fetchone()
        return contact


if __name__ == "__main__":
    app = QApplication([])
    window = ContactWidget()
    window.setWindowTitle("Contact Widget Example")
    window.setGeometry(100, 100, 400, 600)
    window.show()
    app.exec_()