import json
import base64
import os
from decouple import config
import argparse
from connector import Connector


class CAKEDataOwner(Connector):
    def __init__(self, sender_address, process_instance_id=config('PROCESS_INSTANCE_ID')):
        super().__init__("../databases/data_owner/data_owner.db", int(config('SDM_PORT')),
                         process_instance_id=process_instance_id, sender_address=sender_address)
        return

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
        receive = self.conn.recv(6000).decode(self.FORMAT)
        # print(receive)
        if receive.startswith('Number to be signed: '):
            len_initial_message = len('Number to be signed: ')
            print(receive[len_initial_message:])
            self.x.execute("INSERT OR IGNORE INTO handshake_number VALUES (?,?,?)",
                           (self.process_instance_id, self.sender_address, receive[len_initial_message:]))
            self.connection.commit()
        if receive.startswith('Here is the message_id:'):
            self.x.execute("INSERT OR IGNORE INTO messages VALUES (?,?,?)",
                           (self.process_instance_id, receive[24:], self.sender_address))
            self.connection.commit()

    def handshake(self):
        """Handshake with the CAKE SDM server"""

        self.x.execute("SELECT * FROM handshake_number WHERE process_instance=? AND sender_address=?",
                  (str(self.process_instance_id), self.sender_address))
        result = self.x.fetchall()
        if result:
            print("the number is already present")
            self.disconnect()
        else:
            print("Start handshake")
            self.send("Start handshake§" + self.sender_address)
            self.disconnect()
        return

    def cipher_files(self, message_to_send, policy_string):
        """Cipher a message and set the policy

        Args:
            message_to_send (str): message to send
            policy_string (str): policy converted to string"""
        signature_sending = self.sign_number()
        self.send(
            "Cipher these files§" + message_to_send + '§' + policy_string + '§' + self.sender_address + '§' + str(signature_sending))
        self.disconnect()
        return

    def sign_number(self):
        """Sign a number

        Sign a number and return the signature

        Returns:
            str: signature
        """
        self.x.execute("SELECT * FROM handshake_number WHERE process_instance=?", (self.process_instance_id,))
        result = self.x.fetchall()
        number_to_sign = result[0][2]
        return super().sign_number(number_to_sign, self.sender_address)


def file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            encoded = base64.b64encode(file.read()).decode('utf-8')
        return encoded
    except Exception as e:
        print(f"Error encoding file to Base64: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', '--handshake', action='store_true')
    parser.add_argument('-s', '--sender_address', type=str, help='Sender address of the requester')
    parser.add_argument('-c', '--cipher', action='store_true')
    parser.add_argument('-i', '--input', type=str, help='Path to the input-file to load.')
    parser.add_argument('-p', '--policies', type=str, help='Path to the policies-file to load.')

    args = parser.parse_args()
    sender_address = args.sender_address
    dataOwner = CAKEDataOwner(sender_address=sender_address)
    process_instance_id = config('PROCESS_INSTANCE_ID')

    if args.handshake:
        dataOwner.handshake()

    if args.input:
        input_path = args.input
        encoded_files = {}

        if args.policies:
            policies_path = args.policies
            with open(policies_path, "r") as json_file:
                data = json.load(json_file)
                policy_keys = data.keys()

                for filename in policy_keys:
                    file_path = os.path.join(input_path, filename)
                    if os.path.isfile(file_path):
                        encoded_data = file_to_base64(file_path)
                        if encoded_data is not None:
                            encoded_files[filename] = encoded_data

            message_to_send = json.dumps(encoded_files)

            policies_strings = data.values()
            policy = [f"{process_instance_id} and {policy}" for policy in policies_strings]
            policy_string = '###'.join(policy)

            if args.cipher:
                dataOwner.cipher_files(message_to_send, policy_string)

