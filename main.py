import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QFormLayout, QHBoxLayout
import IDEA_OFB_mode as IDEA
from users import users, find_user_by_name_and_id
from EC_DH import scalar_mult, Point, p
from Schnorr import Schnorr
import hashlib

class SecurePaymentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addWidget(self.transfer_button)

        self.setLayout(layout)

    def derive_key(self, shared_secret, key_size=128):
        # Convert the shared secret to bytes
        shared_secret_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, byteorder='big')
        
        # Hash the shared secret using SHA-256
        hashed_secret = hashlib.sha256(shared_secret_bytes).digest()
        
        # Truncate or expand the hashed secret to the desired key size (128 bits)
        key = hashed_secret[:key_size // 8]  # 128 bits / 8 = 16 bytes
        
        # Ensure the key is 128 bits by padding with zeros if necessary
        key = key.ljust(key_size // 8, b'\x00')
        
        return int.from_bytes(key, byteorder='big')

    def transfer_payment(self):
        # Sender data
        sender_name = self.sender_card_holder_name.text()
        sender_id = self.sender_card_holder_id.text()
        sender_card_number = self.sender_card_number.text()
        sender_expiry_month = self.sender_expiry_month.currentText()
        sender_expiry_year = self.sender_expiry_year.currentText()
        sender_ccv = self.sender_ccv.text()
        amount = self.sender_amount.text()

        # Receiver data
        receiver_name = self.receiver_name.text()
        receiver_id = self.receiver_id.text()

        # Find sender and receiver
        sender = find_user_by_name_and_id(sender_name, sender_id)
        receiver = find_user_by_name_and_id(receiver_name, receiver_id)

        if sender and receiver:
            # Compute shared secret key using EC DH
            sender_private_key = sender["private_key"]
            receiver_public_key = receiver["public_key"]

            shared_secret_point = scalar_mult(sender_private_key, receiver_public_key)
            shared_secret = (shared_secret_point.x * shared_secret_point.y) % p

            # Derive a 128-bit key from the shared secret
            key = self.derive_key(shared_secret)

            # Encrypt payment data
            plaintext = f"{sender_name}|{sender_id}|{sender_card_number}|{sender_expiry_month}/{sender_expiry_year}|{sender_ccv}|{amount}"
            iv = b'\x00' * 8  # Example 64-bit IV
            idea = IDEA.IDEA(key)
            encrypted_data = IDEA.idea_ofb_mode(idea, iv, plaintext.encode(), mode='encrypt')
            print(f'Encrypted Data: {encrypted_data.hex()}')

            # Generate Schnorr signature
            schnorr = Schnorr(sender_private_key)
            signature = schnorr.sign(plaintext)
            print(f"Signature: {signature}")

            # Decrypt the data on the receiver side
            receiver_private_key = receiver["private_key"]
            sender_public_key = sender["public_key"]
            shared_secret_point = scalar_mult(receiver_private_key, sender_public_key)
            shared_secret = (shared_secret_point.x * shared_secret_point.y) % p

            # Derive the same 128-bit key from the shared secret
            key = self.derive_key(shared_secret)

            decrypted_data = IDEA.idea_ofb_mode(idea, iv, encrypted_data, mode='decrypt')
            decrypted_text = decrypted_data.decode().rstrip("\x00")
            sender_name, sender_id, sender_card_number, sender_expiry_date, sender_ccv, amount = decrypted_text.split('|')
            print(f'Receiver {receiver_name} (ID: {receiver_id}) received {amount} from {sender_name} (ID: {sender_id}).')

            # Verify Schnorr signature
            schnorr_receiver = Schnorr(receiver_private_key)
            is_valid = schnorr_receiver.verify(plaintext, signature)
            print(f"Signature valid: {is_valid}")

        else:
            print('Sender or receiver not found. Payment not sent.')

def main():
    app = QApplication(sys.argv)
    window = SecurePaymentApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
