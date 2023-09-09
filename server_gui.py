from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import QTimer
import sys
import time
import socket
from threading import Thread

from RSA_GUI import Ui_SercurityMessage
from RSA_optimized import RSA_NHOM6

new_messages = []

class SercurityMessageApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Tạo một thể hiện của lớp Ui_SercurityMessage
        self.ui = Ui_SercurityMessage()
        self.setWindowTitle('Server')
        self.ui.setupUi(self)

        self.rsa = RSA_NHOM6()

        # Default
        self.ui.e_input.setText('65537')
        self.ui.Public_key_input.setText(open('keys/client_public_key.txt', mode='r').read())
        self.ui.Private_key_input.setText(open('keys/server_private_key.txt', mode='r').read())

        # next create a socket object
        self.s = socket.socket()
        print ("Socket successfully created")

        # reserve a port on your computer in our
        # case it is 12345 but it can be anything
        port = 12345			

        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        self.s.bind(('', port))		
        print ("socket binded to %s" %(port))

        # put the socket into listening mode
        self.s.listen(5)	
        print ("socket is listening")	

        # Establish connection with client.
        self.c, addr = self.s.accept()
        print('Got connection from', addr )

        # Key generation section
        # self.ui.Generate_key_button.clicked.connect(self.generate_key)
        # self.ui.Export_public_key_button.clicked.connect(self.export_button)
        # self.ui.Import_public_key_button.clicked.connect(self.import_button)

        # Sender section
        self.ui.Send_button.clicked.connect(self.send_message)
        self.ui.Clear_1_button.clicked.connect(self.clear_sender_input)

        # Reciever section
        # self.ui.Send_button.clicked.connect(self.send_message)
        self.ui.Clear_2_button.clicked.connect(self.clear_receiver_input)

    def listen(self):
        global new_messages

        while True:
            response = self.c.recv(1024).decode()
            if response:
                new_messages.append(response)
            time.sleep(.5)
    
    def display_new_message(self):
        while new_messages:
            receiver_messages = self.ui.Receiver_input

            if self.rsa.private_key == None:
                # Check condition
                private_key_text = self.ui.Private_key_input.toPlainText()
                if private_key_text == '':
                    print('Private key input is empty')
                    return None

                self.rsa.private_key = tuple(map(int, private_key_text.split(',')))

                if self.rsa.private_key == None:
                    print('Can not load public key')
                    return None
            new_message = new_messages.pop(0)
            receiver_messages.setText(receiver_messages.toPlainText() + '\n-----NEW MESSAGE-----\n')
            receiver_messages.setText(receiver_messages.toPlainText() + 'Plaintext:\n' + self.rsa.decode(new_message) + '\n')
            receiver_messages.setText(receiver_messages.toPlainText() + 'Ciphertext:\n' + new_message + '\n')

    def clear_sender_input(self):
        self.ui.Sender_text_input.setText('')
    
    def clear_receiver_input(self):
        self.ui.Receiver_input.setText('')

    def send_message(self):
        # Check condition
        public_key_text = self.ui.Public_key_input.toPlainText()
        if public_key_text == '':
            print('Public key input is empty')
            return None

        self.rsa.public_key = tuple(map(int, public_key_text.split(',')))

        if self.rsa.public_key == '':
            print('Can not load public key')
            return None
            
        # Encode message
        message = self.ui.Sender_text_input.toPlainText()
        encoded_message = self.rsa.encode(message)

        # Send message to client
        self.c.send(encoded_message.encode())

    def generate_key(self):
        try:
            self.rsa.generate_key(e_default=int(self.ui.e_input.toPlainText()))

            # Show keys
            if self.rsa.public_key != None and self.rsa.private_key != None:
                e, n = self.rsa.public_key
                d, n = self.rsa.private_key
                self.ui.Public_key_input.setText(f'({e}, {n})')
                self.ui.Private_key_input.setText(f'({d}, {n})')
        except:
            print('Can not generate key')

    # def export_button(self):
    #     try:
    #         if self.check_key():
    #             e, n = self.rsa.public_key
    #             d, n = self.rsa.private_key

    #             options = QFileDialog.Options()
    #             options |= QFileDialog.DontUseNativeDialog
    #             file, _ = QFileDialog.getSaveFileName(self, "Export File", "", "Text Files (*.txt)", options=options)
    #             if file:
    #                 with open(file, mode='w') as f:
    #                     f.write(f'{e},{n}\n')
    #                     f.write(f'{d},{n}\n')

    #             print('Saved keys')
    #     except:
    #         print('Can not export')

    # def import_button(self):
    #     try:
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.ReadOnly
    #         file, _ = QFileDialog.getOpenFileName(self, "Import File", "", "Text Files (*.txt)", options=options)
    #         if file:
    #             with open(file, 'r') as f:
    #                 content = f.readlines()
    #                 if len(content) == 2:
    #                     public_key = content[0].strip().split(',')
    #                     private_key = content[1].strip().split(',')
    #                     if len(public_key) == 2 and len(private_key) == 2:
    #                         e, n = int(public_key[0]), int(public_key[1])
    #                         d, n = int(private_key[0]), int(private_key[1])
    #                         self.rsa.public_key = (e, n)
    #                         self.rsa.private_key = (d, n)
    #                         self.ui.Pubilic_key_output.setText(f'({e}, {n})')
    #                         self.ui.Private_key_output.setText(f'({d}, {n})')
    #                         print('Imported keys')
    #                     else:
    #                         print('Invalid key format')
    #                 else:
    #                     print('Invalid file format')
    #     except:
    #         print('Can not import')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SercurityMessageApp()
    window.setWindowTitle('Server');

    window.show()

    timer = QTimer()
    timer.timeout.connect(window.display_new_message)
    timer.start(1000)

    thread = Thread(target=window.listen, daemon=True)
    thread.start()

    sys.exit(app.exec_())
