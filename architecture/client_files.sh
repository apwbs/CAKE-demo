message_id='9927996960327668857'
reader_address='0xf78F10d7CeC746B85CECb44e66875618d15F9e43'
slice_id='3877031780826419281'
output_folder='files/prova/'

python3 client.py --handshake --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -af --message_id $message_id --reader_address $reader_address --slice_id $slice_id --output_folder $output_folder