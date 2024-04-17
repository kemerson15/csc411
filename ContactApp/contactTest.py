import unittest
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from contact import ContactWidget, DatabaseHandler

class TestContactWidget(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize PyQt application instance
        cls.app = QApplication(sys.argv)

    def setUp(self):
        # Create a ContactWidget instance
        self.widget = ContactWidget()
        
        # Create a DatabaseHandler instance
        self.database = DatabaseHandler()

        # Clear the contacts table before each test
        self.database.conn.execute("DELETE FROM contacts")
        self.database.conn.commit()

    def tearDown(self):
        # Close the ContactWidget instance after each test
        self.widget.close()

    def test_add_contact(self):
        dialog = QDialog()
        # Add a contact
        self.widget.add_contact(dialog, "John", "Doe", "1234567890", "January", "1", "2000")
        # Retrieve contacts from the database
        contacts = self.database.retrieve_all_contacts()
        # Check if contact was added
        self.assertEqual(len(contacts), 1)

    def test_remove_contact(self):
        dialog = QDialog()
        # Add a contact
        self.widget.add_contact(dialog, "John", "Doe", "1234567890", "January", "1", "2000")
        # Remove the contact
        self.widget.remove_contact("John", "Doe", "1234567890")
        # Retrieve contacts from the database
        contacts = self.database.retrieve_all_contacts()
        # Check if contact was removed
        self.assertEqual(len(contacts), 0)

    def test_invalid_phone(self):
        dialog = QDialog()
        # Attempt to add a contact with an invalid phone number
        self.widget.add_contact(dialog, "John", "Doe", "abc", "January", "1", "2000")
        # Retrieve contacts from the database
        contacts = self.database.retrieve_all_contacts()
        # Check if contact was not added
        self.assertEqual(len(contacts), 0)

    def test_duplicate_contact(self):
        dialog = QDialog()
        # Add a contact
        self.widget.add_contact(dialog, "John", "Doe", "1234567890", "January", "1", "2000")
        # Attempt to add the same contact again
        self.widget.add_contact("John", "Doe", "1234567890", "January", "1", "2000")
        # Retrieve contacts from the database
        contacts = self.database.retrieve_all_contacts()
        # Check if only one contact was added
        self.assertEqual(len(contacts), 1)

if __name__ == '__main__':
    unittest.main()