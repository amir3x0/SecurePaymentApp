import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QFormLayout, QHBoxLayout, QLabel
import IDEA_OFB_mode as IDEA
from users import users, find_user_by_name_and_id
from EC_DH import curve, G
from schnorr import SchnorrSignature, generate_schnorr_parameters
import hashlib
import sympy
import random

class SecurePaymentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface for the Secure Payment Application.

        This method sets up the window title, geometry, and the layout for the sender and receiver sections.
        It also creates the necessary input fields and buttons for the user to enter payment information and initiate a transfer.

        Returns:
            None
        """
        self.setWindowTitle('Secure Payment Application')
        self.setGeometry(100, 100, 800, 400)

        # Sender side
        sender_layout = QFormLayout()

        self.sender_card_holder_name = QLineEdit()
        self.sender_card_holder_id = QLineEdit()
        self.sender_card_holder_id.setMaxLength(9)
        self.sender_card_number = QLineEdit()
        self.sender_card_number.setMaxLength(16)
        self.sender_expiry_month = QComboBox()
        self.sender_expiry_month.addItems([str(i).zfill(2) for i in range(1, 13)])
        self.sender_expiry_year = QComboBox()
        self.sender_expiry_year.addItems([str(i) for i in range(2024, 2035)])
        self.sender_ccv = QLineEdit()
        self.sender_ccv.setMaxLength(3)
        self.sender_amount = QLineEdit()

        sender_layout.addRow("Card Holder Name:", self.sender_card_holder_name)
        sender_layout.addRow("Card Holder ID:", self.sender_card_holder_id)
        sender_layout.addRow("Card Number:", self.sender_card_number)
        sender_layout.addRow("Expiry Month:", self.sender_expiry_month)
        sender_layout.addRow("Expiry Year:", self.sender_expiry_year)
        sender_layout.addRow("CCV:", self.sender_ccv)
        sender_layout.addRow("Amount:", self.sender_amount)

        sender_widget = QWidget()
        sender_widget.setLayout(sender_layout)

        # Receiver side
        receiver_layout = QFormLayout()

        self.receiver_name = QLineEdit()
        self.receiver_id = QLineEdit()
        self.receiver_id.setMaxLength(9)

        receiver_layout.addRow("Receiver Name:", self.receiver_name)
        receiver_layout.addRow("Receiver ID:", self.receiver_id)

        receiver_widget = QWidget()
        receiver_widget.setLayout(receiver_layout)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(sender_widget)
        main_layout.addWidget(receiver_widget)

        self.transfer_button = QPushButton('Transfer Payment')
        self.transfer_button.clicked.connect(self.transfer_payment)

        self.result_label = QLabel('')  # Label to show the result of the payment

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addWidget(self.transfer_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def transfer_payment(self):
        """
        Transfers a payment from a sender to a receiver.

        This method performs the following steps:
        1. Retrieves sender and receiver data.
        2. Computes the shared secret key using EC DH.
        3. Encrypts the payment data using IDEA algorithm.
        4. Generates a Schnorr signature for the payment data.
        5. Computes the shared secret key on the receiver side.
        6. Decrypts the encrypted data using IDEA algorithm.
        7. Verifies the Schnorr signature.

        If the sender and receiver are found, the payment is considered successful and a message is printed.
        If the sender or receiver is not found, the payment is not sent.

        Note: This method contains hard-coded data for demonstration purposes. In a real application, the data
        would be retrieved from user input or a database.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        # Sender data
        # sender_name = self.sender_card_holder_name.text()
        # sender_id = self.sender_card_holder_id.text()
        # sender_card_number = self.sender_card_number.text()
        # sender_expiry_month = self.sender_expiry_month.currentText()
        # sender_expiry_year = self.sender_expiry_year.currentText()
        # sender_ccv = self.sender_ccv.text()
        # amount = self.sender_amount.text()

        # # Receiver data
        # receiver_name = self.receiver_name.text()
        # receiver_id = self.receiver_id.text()

        # For testing purposes, hard-coded values can be used as follows:
        sender_name = "Amir Mishayev"
        sender_id = "318212107"
        sender_card_number = "4569871236547890"
        sender_expiry_month = "12"
        sender_expiry_year = "2024"
        sender_ccv = "676"
        amount = "1200"
        receiver_name = "Shimron Ifrah"
        receiver_id = "312423247"

        # Find sender and receiver
        sender = find_user_by_name_and_id(sender_name, sender_id)
        receiver = find_user_by_name_and_id(receiver_name, receiver_id)

        if sender and receiver:
            # ----------------------------- sender side --------------------------------------- #
            # Compute shared secret key using EC DH

            # randomize public key for the schnorr signature
            schnorr_index = random.randint(0, len(sender["schnor_public_key"]) - 1)

            # random two index of the priavte key and the corisponding public key of sender and reciver
            index_sender, index_receiver = random.sample(range(len(sender["private_key"])), 2)
            print(f"--------transfer Payment action-------\n")
            # get private key of sender and public key of reciver
            sender_private_key = sender["private_key"][index_sender]
            receiver_public_key = receiver["public_key"][index_receiver]
            print(f"sender private key: {sender_private_key}\n ")
            print(f"reciver public key: {receiver_public_key}\n")

            # shared secret key
            shared_secret_sender_side = curve.scalar_mult(sender_private_key, receiver_public_key)
            print(f"sender calculated shared key: {shared_secret_sender_side}\n")

            # Encrypt payment data
            plaintext = f"data: {sender_name}|{sender_id}|{sender_card_number}|{sender_expiry_month}/{sender_expiry_year}|{sender_ccv}|{amount}"
            iv = b'\x00' * 8  # Example 64-bit IV
            idea = IDEA.IDEA(shared_secret_sender_side[0])
            print("----Encrypt data----\n")
            encrypted_data = IDEA.idea_ofb_mode(idea, iv, plaintext.encode(), mode='encrypt')
            print(f'Encrypted Data: {encrypted_data.hex()}\n\n')

            # Generate Schnorr signature
            print("----create signature using schnorr----\n")
            sender_shcnorr_public_keys = sender["schnor_public_key"]
            p_schnorr, q_schnorr, g_schnorr = sender_shcnorr_public_keys[schnorr_index]
            print(f"public key p = {p_schnorr} q = {q_schnorr} g= {g_schnorr}\n")
            sender_schnorr = SchnorrSignature(p_schnorr, q_schnorr, g_schnorr)
            sender_schnorr.generate_keys()
            r, s = sender_schnorr.sign(plaintext.encode())
            print(f"Signature: r= {r} s = {s} y ={sender_schnorr.y}\n\n")

            # ----------------------------- receiver side --------------------------------------- #

            # Compute shared secret key using EC DH
            print("---------------receiver side----------\n\n")
            print("receiver side received message\n")

            # get private key of receiver and public key of sender
            receiver_private_key = receiver["private_key"][index_receiver]
            sender_public_key = sender["public_key"][index_sender]
            print(f"receiver private key: {receiver_private_key}\n")
            print(f"sender public key: {sender_public_key}\n")

            shared_secret_receiver_side = curve.scalar_mult(receiver_private_key, sender_public_key)
            print(f"receiver calculated shared key side: {shared_secret_receiver_side}\n")

            # Initialize IDEA for decryption
            idea_receiver = IDEA.IDEA(shared_secret_receiver_side[0])
            print("----decrypt message----\n")
            # decrypt the data using idea
            decrypted_data = IDEA.idea_ofb_mode(idea_receiver, iv, encrypted_data, mode='decrypt')
            decrypted_text = decrypted_data.decode().rstrip("\x00")
            sender_name, sender_id, sender_card_number, sender_expiry_date, sender_ccv, amount = decrypted_text.split('|')
            print(f'decrypted message:  {decrypted_text}')
            
            # Verify Schnorr signature
            print("\n\n----verifying signature----\n")
            schnorr_receiver = SchnorrSignature(p_schnorr, q_schnorr, g_schnorr)
            is_valid = schnorr_receiver.verify(plaintext.encode(), r, s, sender_schnorr.y)
            print(f"\nSignature valid: {is_valid}\n")

            if is_valid:
                message = f"Receiver {receiver_name} (ID: {receiver_id}) received {amount} from data: {sender_name} (ID: {sender_id})."
                self.result_label.setText(message)
                print(f'application message: {message}\n\n')
            else:
                self.result_label.setText('Signature verification failed. Payment not sent.')
                print('Signature verification failed. Payment not sent.')

        else:
            self.result_label.setText('Sender or receiver not found. Payment not sent.')
            print('Sender or receiver not found. Payment not sent.')

def main():
    app = QApplication(sys.argv)
    window = SecurePaymentApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
