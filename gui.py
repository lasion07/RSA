from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
import sys

from RSA_GUI import Ui_SercurityMessage
from RSA_optimized import RSA_NHOM6

class SercurityMessageApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Tạo một thể hiện của lớp Ui_SercurityMessage
        self.ui = Ui_SercurityMessage()
        self.ui.setupUi(self)

        self.rsa = RSA_NHOM6()

        # Default
        self.ui.e_input.setText('65537')

        # Key generation panel
        self.ui.Generate_key_button.clicked.connect(self.generate_key)
        self.ui.Export_button.clicked.connect(self.export_button)
        self.ui.Import_button.clicked.connect(self.import_button)

        # Encryption panel
        self.ui.Encrypt_button.clicked.connect(self.encrypt)
        self.ui.Clear_1_button.clicked.connect(self.clear_plaintext_input)

        # Decryption panel
        self.ui.Decrypt_button.clicked.connect(self.decrypt)
        self.ui.Clear_1_button_2.clicked.connect(self.clear_ciphertext_input)
    
    def check_key(self):
        return self.rsa.public_key != None and self.rsa.private_key != None

    def generate_key(self):
        try:
            self.rsa.generate_key(e_default=int(self.ui.e_input.toPlainText()))
            
            # Show keys
            if self.check_key():
                e, n = self.rsa.public_key
                d, n = self.rsa.private_key
                self.ui.Pubilic_key_output.setText(f'({e}, {n})')
                self.ui.Private_key_output.setText(f'({d}, {n})')
        except:
            print('Can not generate key')
    
    def export_button(self):
        try:
            if self.check_key():
                e, n = self.rsa.public_key
                d, n = self.rsa.private_key

                with open(f'keys/public_key.txt', mode='w') as f:
                    f.write(f'{e},{n}')
                    f.close()
                
                with open(f'keys/private_key.txt', mode='w') as f:
                    f.write(f'{d},{n}')
                    f.close()
            
                print('Saved keys in keys/')
        except:
            print('Can not export')
    
    def import_button(self):
        try:
            self.rsa.load_key()

            # Show keys
            if self.check_key():
                e, n = self.rsa.public_key
                d, n = self.rsa.private_key

                self.ui.Pubilic_key_output.setText(f'({e}, {n})')
                self.ui.Private_key_output.setText(f'({d}, {n})')

                print('Imported from keys/')
        except:
            print('Can not import')

    def encrypt(self):
        try:
            plaintext = self.ui.Plain_text_input.toPlainText()
            if plaintext != '' and self.check_key():
                coded = self.rsa.encode(plaintext)
                ciphertext = ''.join(str(p) + ' ' for p in coded)
                self.ui.Cipher_text_input.setText(ciphertext)
        except:
            print('Can not encrypt')

    def clear_plaintext_input(self):
        self.ui.Plain_text_input.setText('')
    
    def decrypt(self):
        try:
            ciphertext = self.ui.Cipher_text_input.toPlainText()
            if ciphertext != '' and self.check_key():
                coded = []
                temp = ciphertext.split()
                for i in temp:
                    coded.append(int(i))
                plaintext = ''.join(str(p) for p in self.rsa.decode(coded))
                self.ui.Plain_text_input.setText(plaintext)
        except:
            print('Can not decrypt')
    
    def clear_ciphertext_input(self):
        self.ui.Cipher_text_input.setText('')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SercurityMessageApp()
    window.show()
    sys.exit(app.exec_())
