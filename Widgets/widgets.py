from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QListWidget

class ContactListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add functionality for managing the contact list (e.g., add, remove contacts)

class ContactDetailsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add functionality for displaying and editing contact details

class ContactApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phone Contact Application")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.contact_list_widget = ContactListWidget()
        self.layout.addWidget(self.contact_list_widget)

        self.contact_details_widget = ContactDetailsWidget()
        self.layout.addWidget(self.contact_details_widget)