import base64
import json
import socket
import ssl
from hashlib import sha512
from decouple import config
import sqlite3
import argparse
from connector import Connector


def base64_to_file(encoded_data, output_file_path):
    try:
        decoded_data = base64.b64decode(encoded_data.encode('utf-8'))
        with open(output_file_path, 'wb') as file:
            file.write(decoded_data)
    except Exception as e:
        print(f"Error decoding Base64 to file: {e}")


class CAKEClient(Connector):
    """A client to communicate with the CAKE SKM server

    A class to manage the communication with the CAKE SKM server

    Attributes:
        message_id (str): message id
        reader_address (str): reader address
        slice_id (str): slice id
    """

    def __init__(self, process_instance_id=config('PROCESS_INSTANCE_ID'), message_id="", reader_address="",
                 slice_id=""):
        """Initialize the CAKEClient class
        
        Args:
            process_instance_id (int, optional): process instance id. Defaults to config('PROCESS_INSTANCE_ID').
            message_id (str, optional): message id. Defaults to "".
            reader_address (str, optional): reader address. Defaults to "".
            slice_id (str, optional): slice id. Defaults to "".
            
        """
        super().__init__(path_to_db='files/reader/reader.db', port=int(config('SKM_PORT')),
                         process_instance_id=process_instance_id)
        self.__setArgs__(message_id, reader_address, slice_id)
        return

    def __setArgs__(self, message_id, reader_address, slice_id=""):
        """Set the arguments of the class

        Set the message id, the reader address and the slice id of the class

        Args:
            message_id (str): message id
            reader_address (str): reader address
            slice_id (str, optional): slice id. Defaults to "".
        """
        self.message_id = message_id
        self.reader_address = reader_address
        self.slice_id = slice_id
        return

    def __receive_message__(self):
        message = ""
        while True:
            data = self.conn.recv(1024).decode(self.FORMAT)  # Receive data in chunks of 1024 bytes
            if not data:  # No data received
                break
            message += data

            # Check if the end of the message is reached
            if message.endswith("Msg received!"):
                return message
            elif message.endswith("Number to be signed:"):
                return message
            elif message.endswith("Here are the IPFS link and key:"):
                return message
            elif message.endswith("Here are the plaintext and salt:"):
                return message
            elif message.endswith("Here is the file and salt:"):
                return message

    def send(self, msg):
        """Send a message to the CAKE SKM server

        Send a message to the CAKE SKM server and receive a response

        Args:
            msg (str): message to send
        """
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
        receive = self.__receive_message__()

        if receive.startswith('Number to be signed: '):
            len_initial_message = len('Number to be signed: ')
            self.x.execute("INSERT OR IGNORE INTO handshake_number VALUES (?,?,?,?)",
                           (self.process_instance_id, self.message_id, self.reader_address,
                            receive[len_initial_message:]))
            self.connection.commit()

        if receive.startswith('Here are the IPFS link and key'):
            key = receive.split('\n\n')[0].split("b'")[1].rstrip("'")
            ipfs_link = receive.split('\n\n')[1]

            self.x.execute("INSERT OR IGNORE INTO decription_keys VALUES (?,?,?,?,?)",
                           (self.process_instance_id, self.message_id, self.reader_address, ipfs_link, key))
            self.connection.commit()

        if receive.startswith('Here are the plaintext and salt'):
            plaintext = receive.split('\n\n')[0].split('Here are the plaintext and salt: ')[1]
            salt = receive.split('\n\n')[1]

            self.x.execute("INSERT OR IGNORE INTO plaintext VALUES (?,?,?,?,?,?)",
                           (self.process_instance_id, self.message_id, self.slice_id, self.reader_address, plaintext,
                            salt))
            self.connection.commit()
            print(plaintext)

        if receive.startswith('Here is the file and salt'):
            plaintext = receive.split('\n\n')[0].split('Here is the file and salt: ')[1]
            plaintext_value = json.loads(plaintext)
            plaintext_file = list(plaintext_value.items())[0][1]

            salt = receive.split('\n\n')[1]
            salt = salt[:-13]

            output_folder = "files/prova/"
            filename = list(plaintext_value.items())[0][0]
            base64_to_file(plaintext_file, output_folder + filename)

            self.x.execute("INSERT OR IGNORE INTO plaintext VALUES (?,?,?,?,?,?)",
                           (self.process_instance_id, self.message_id, self.slice_id, self.reader_address,
                            plaintext_file, salt))
            self.connection.commit()
        return receive

    def handshake(self):
        """Start the handshake with the CAKE SKM server"""
        self.send("Start handshake§" + str(self.message_id) + '§' + self.reader_address)
        self.disconnect()
        return

    def generate_key(self):
        """Generate the key for the reader"""
        signature_sending = self.sign_number()
        self.send("Generate my key§" + self.message_id + '§' + self.reader_address + '§' + str(signature_sending))
        self.disconnect()
        return

    def access_data(self):
        """Access the data of the reader"""
        signature_sending = self.sign_number()
        self.send("Access my data§" + self.message_id + '§' + self.slice_id + '§' + self.reader_address + '§' + str(
            signature_sending))
        self.disconnect()
        return

    def access_file(self):
        """Access the files of the reader"""
        signature_sending = self.sign_number()
        self.send("Access my files§" + self.message_id + '§' + self.slice_id + '§' + self.reader_address + '§' + str(
            signature_sending))
        self.disconnect()
        return

    '''
    def full_request(self):
        self.handshake()
        self.generate_key()
        self.access_data()
        return
    '''

    def sign_number(self):
        """Sign a number 

        Sign a number with the private key of the reader

        Returns:
            str: signature of the number
        """

        self.x.execute("SELECT * FROM handshake_number WHERE process_instance=? AND message_id=? AND reader_address=?",
                       (self.process_instance_id, self.message_id, self.reader_address))
        result = self.x.fetchall()
        number_to_sign = result[0][3]
        return super().sign_number(number_to_sign, self.reader_address)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client request details",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--message_id', type=str, help='Message ID')
    parser.add_argument('-s', '--slice_id', type=str, help='Slice ID')
    parser.add_argument('-rd', '--reader_address', type=str, help='Reader address')

    parser.add_argument('-hs', '--handshake', action='store_true', help='Handshake')
    parser.add_argument('-gs', '--generate_key', action='store_true', help='Generate key')
    parser.add_argument('-ad', '--access_data', action='store_true', help='Access data')
    parser.add_argument('-af', '--access_files', action='store_true', help='Access files')
    args = parser.parse_args()

    message_id = args.message_id
    slice_id = args.slice_id
    reader_address = args.reader_address

    client = CAKEClient(message_id=message_id, reader_address=reader_address, slice_id=slice_id)
    if args.handshake:
        client.handshake()
    if args.generate_key or args.access_data or args.access_files:
        if args.generate_key:
            client.generate_key()
        if args.access_data:
            client.access_data()
        if args.access_files:
            client.access_file()
