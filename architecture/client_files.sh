message_id='7315059630286805001'
reader_address='0xeF4B867984daFD8cbAb41fac185195c18A6ae6Ea'
slice_id='11808704719922826163'
output_folder='files/prova/'

python3 client.py --handshake --message_id $message_id --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -af --message_id $message_id --reader_address $reader_address --slice_id $slice_id --output_folder $output_folder