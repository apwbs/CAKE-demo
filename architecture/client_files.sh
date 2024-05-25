message_id='8717697024584966088'
reader_address='0xeF4B867984daFD8cbAb41fac185195c18A6ae6Ea'
slice_id='10934594842311023635'

python3 client.py --handshake --message_id $message_id --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -af --message_id $message_id --reader_address $reader_address --slice_id $slice_id