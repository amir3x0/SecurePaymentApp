import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from idea import idea_encrypt, idea_decrypt
from ecdh import generate_ecdh_key_pair, compute_shared_secret
from schnorr import generate_schnorr_signature, verify_schnorr_signature

class SecurePaymentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Secure Payment Application')
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel('Enter payment data:')
        self.payment_data_input = QLineEdit()
        self.encrypt_button = QPushButton('Encrypt Data')
        self.decrypt_button = QPushButton('Decrypt Data')

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.payment_data_input)
        vbox.addWidget(self.encrypt_button)
        vbox.addWidget(self.decrypt_button)

        self.setLayout(vbox)

        self.encrypt_button.clicked.connect(self.encrypt_data)
        self.decrypt_button.clicked.connect(self.decrypt_data)

    def encrypt_data(self):
        plaintext = self.payment_data_input.text()
        key = b'MySecretKey'  # Replace with actual key generation logic
        encrypted_data = idea_encrypt(plaintext, key)
        print(f'Encrypted Data: {encrypted_data}')

    def decrypt_data(self):
        ciphertext = self.payment_data_input.text()
        key = b'MySecretKey'  # Replace with actual key generation logic
        decrypted_data = idea_decrypt(ciphertext, key)
        print(f'Decrypted Data: {decrypted_data}')

def main():
    app = QApplication(sys.argv)
    window = SecurePaymentApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
